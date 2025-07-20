from pocketflow import Node
import sys
sys.path.append('../..')
from utils.llm_utils import call_llm, call_llm_with_thinking

class ExtendedThinkingNode(Node):
    """
    Node that uses extended thinking for complex reasoning tasks
    """
    def __init__(self):
        super().__init__(max_retries=2, wait=1)
    
    def prep(self, shared):
        return {
            "problem": shared["problem"],
            "enable_thinking": shared.get("enable_thinking", True)
        }
    
    def exec(self, prep_res):
        problem = prep_res["problem"]
        enable_thinking = prep_res["enable_thinking"]
        
        if enable_thinking:
            print("🤔 Claude is thinking deeply about this problem...")
            print("   (Extended thinking mode enabled)")
            
            # Use extended thinking with higher token limits for complex problems
            solution = call_llm_with_thinking(
                prompt=problem,
                temperature=0.3,  # Lower temperature for more focused reasoning
                max_tokens=4096,  # Allow longer answers
                max_thinking_tokens=50000  # Allow extensive thinking
            )
            
            return {
                "solution": solution,
                "used_thinking": True
            }
        else:
            # Fallback to standard mode
            return None
    
    def post(self, shared, prep_res, exec_res):
        if exec_res:
            shared["solution"] = exec_res["solution"]
            shared["used_extended_thinking"] = exec_res["used_thinking"]
            # In a real implementation, we could track thinking tokens
            shared["thinking_tokens_used"] = 0  # Placeholder
            return None  # End flow
        else:
            # Fallback to standard solution
            return "fallback"


class StandardSolutionNode(Node):
    """
    Fallback node for standard problem solving without extended thinking
    """
    def prep(self, shared):
        return shared["problem"]
    
    def exec(self, problem):
        print("📝 Using standard mode (no extended thinking)...")
        
        prompt = f"""Please solve this problem step by step:

{problem}

Provide a clear, detailed solution."""
        
        solution = call_llm(
            prompt,
            temperature=0.7,
            max_tokens=2048
        )
        
        return solution
    
    def post(self, shared, prep_res, exec_res):
        shared["solution"] = exec_res
        shared["used_extended_thinking"] = False