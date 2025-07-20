"""
LLM utility functions for PocketFlow
"""
from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def call_llm(messages, model="claude-opus-4-20250514", temperature=0.7, response_format=None, 
             enable_thinking=False, max_tokens=1024, max_thinking_tokens=50000):
    """
    Call Anthropic Claude LLM with messages
    
    Args:
        messages: List of message dicts with 'role' and 'content' or a string prompt
        model: Model to use (default: claude-opus-4-20250514)
        temperature: Sampling temperature (0-1)
        response_format: Optional format specification (not used for Claude)
        enable_thinking: Enable extended thinking mode for complex reasoning
        max_tokens: Maximum tokens in response (default: 1024)
        max_thinking_tokens: Maximum tokens for thinking process (default: 50000)
        
    Returns:
        String response from LLM (or dict with thinking and answer if enable_thinking=True and return_thinking=True)
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Handle both string prompts and message lists
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    # Convert OpenAI-style messages to Anthropic format
    anthropic_messages = []
    for msg in messages:
        if msg["role"] != "system":  # System messages are handled separately in Anthropic
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    
    # Extract system message if present
    system_message = None
    for msg in messages:
        if msg["role"] == "system":
            system_message = msg["content"]
            break
    
    kwargs = {
        "model": model,
        "messages": anthropic_messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    if system_message:
        kwargs["system"] = system_message
    
    # Add thinking configuration for supported models
    if enable_thinking and model in ["claude-opus-4-20250514", "claude-3-5-sonnet-20241022"]:
        kwargs["metadata"] = {
            "enable_thinking": True,
            "thinking_max_tokens": max_thinking_tokens
        }
    
    response = client.messages.create(**kwargs)
    return response.content[0].text

def call_llm_json(messages, model="claude-opus-4-20250514", temperature=0.7, enable_thinking=False):
    """
    Call LLM expecting JSON response
    
    Args:
        messages: List of message dicts or a string prompt
        model: Model to use
        temperature: Sampling temperature
        enable_thinking: Enable extended thinking for complex JSON generation
    
    Returns:
        Parsed JSON object
    """
    system_prompt = "You are a helpful assistant that always responds in valid JSON format."
    
    # Convert string to messages list if needed
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    # Ensure system message for JSON
    if not any(msg.get("role") == "system" for msg in messages):
        messages.insert(0, {"role": "system", "content": system_prompt})
    else:
        for msg in messages:
            if msg.get("role") == "system":
                msg["content"] = f"{msg['content']}\n{system_prompt}"
                break
    
    response = call_llm(messages, model, temperature, enable_thinking=enable_thinking)
    
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError(f"Invalid JSON response: {response}")


def call_llm_with_thinking(prompt, model="claude-opus-4-20250514", temperature=0.7, 
                          max_tokens=1024, max_thinking_tokens=50000):
    """
    Convenience function for complex reasoning tasks that benefit from extended thinking
    
    Args:
        prompt: The complex problem or question to solve
        model: Model to use (must support thinking)
        temperature: Sampling temperature
        max_tokens: Maximum tokens for the answer
        max_thinking_tokens: Maximum tokens for thinking process
        
    Returns:
        String response with the final answer
    """
    thinking_prompt = f"""You are tasked with solving a complex problem. Use extended thinking to work through it step by step.

Problem: {prompt}

Take your time to think through this carefully before providing your final answer."""
    
    return call_llm(
        thinking_prompt, 
        model=model, 
        temperature=temperature,
        enable_thinking=True,
        max_tokens=max_tokens,
        max_thinking_tokens=max_thinking_tokens
    )