# PocketFlow Extended Thinking Example

This example demonstrates how to use Claude's extended thinking capability for complex reasoning tasks that benefit from deeper analysis.

## What is Extended Thinking?

Extended thinking allows Claude to use internal reasoning (thinking tags) to work through complex problems step-by-step before providing a final answer. This is particularly useful for:

- Complex mathematical problems
- Logic puzzles
- Algorithm design
- Physics problems with multiple steps
- Any task requiring careful reasoning

## Features

- **ExtendedThinkingNode**: Uses `call_llm_with_thinking()` for complex reasoning
- **Configurable thinking tokens**: Set max thinking tokens (up to 50,000)
- **Fallback support**: Falls back to standard mode if needed
- **Multiple problem types**: Includes examples for math, logic, coding, and physics

## Usage

### Basic usage with default math problem:
```bash
python main.py
```

### Use a different problem type:
```bash
python main.py --type logic
python main.py --type coding
python main.py --type physics
```

### Use a custom problem:
```bash
python main.py --problem "Explain the halting problem and its implications for computer science"
```

## How it Works

1. **ExtendedThinkingNode** checks if extended thinking is enabled
2. If enabled, it uses `call_llm_with_thinking()` which:
   - Adds a thinking-friendly prompt
   - Enables thinking mode in the API call
   - Allows up to 50,000 tokens for internal reasoning
3. Claude thinks through the problem step-by-step internally
4. Returns only the final, polished answer

## Configuration in llm_utils.py

The extended thinking feature is implemented through:

```python
# Basic usage
response = call_llm(prompt, enable_thinking=True)

# With custom limits
response = call_llm(
    prompt, 
    enable_thinking=True,
    max_thinking_tokens=50000,  # For thinking process
    max_tokens=4096             # For final answer
)

# Convenience function for complex problems
response = call_llm_with_thinking(
    prompt="Complex problem here",
    temperature=0.3,  # Lower for focused reasoning
    max_tokens=4096,
    max_thinking_tokens=50000
)
```

## When to Use Extended Thinking

Use extended thinking for:
- **Mathematical proofs** and complex calculations
- **Multi-step logic problems**
- **Algorithm optimization** challenges
- **Physics problems** with multiple variables
- **Code architecture** decisions
- Any problem where you'd normally say "let me think about this..."

Don't use it for:
- Simple questions with straightforward answers
- Basic information retrieval
- Tasks that don't require reasoning

## Example Output

```
🧠 Using math problem

📝 Problem: Find all positive integer solutions to the equation x^3 + y^3 + z^3 = 33

⏳ Enabling extended thinking mode... This may take a moment.

🤔 Claude is thinking deeply about this problem...
   (Extended thinking mode enabled)

================================================================================
✅ SOLUTION:
================================================================================
After careful analysis, I can confirm that there are positive integer solutions 
to x³ + y³ + z³ = 33.

The smallest known solution is:
x = 88661289752875283
y = -87784054428622393
z = -2736111468807040

However, you asked specifically for positive integer solutions...
[detailed solution continues]

💭 Thinking tokens used: 15,234
```

## Notes

- Extended thinking is only available for Claude Opus 4 and Claude 3.5 Sonnet
- The thinking process happens internally and isn't shown in the output
- Lower temperatures (0.3-0.5) often work better for complex reasoning
- Thinking tokens don't count against your regular token limits