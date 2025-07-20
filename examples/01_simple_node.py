"""
Example 1: Simple Node
Demonstrates the basic Node concept - a single task execution
"""
from pocketflow import Node
import sys
sys.path.append('..')
from utils.llm_utils import call_llm

class GreetingNode(Node):
    """A simple node that generates a greeting"""
    
    def prep(self, shared):
        """Preparation phase: gather inputs"""
        # Get name from shared context or use default
        name = shared.get("name", "World")
        language = shared.get("language", "English")
        return {"name": name, "language": language}
    
    def exec(self, prep_res):
        """Execution phase: perform the task"""
        messages = [
            {
                "role": "system",
                "content": f"Generate a friendly greeting in {prep_res['language']}."
            },
            {
                "role": "user",
                "content": f"Create a warm greeting for {prep_res['name']}"
            }]        ]
        
        greeting = call_llm(messages, temperature=0.9)
        return greeting
    
    def post(self, shared, prep_res, exec_res):
        """Post-processing phase: handle results"""
        print(f"\n🌟 Greeting in {prep_res['language']}:")
        print(exec_res)
        
        # Store result in shared context
        shared["last_greeting"] = exec_res
        return exec_res

# Example usage
if __name__ == "__main__":
    # Create node instance
    greeting_node = GreetingNode(max_retries=2, wait=1)
    
    # Run with different contexts
    contexts = [
        {"name": "Alice", "language": "English"},
        {"name": "Bob", "language": "Spanish"},
        {"name": "Charlie", "language": "Japanese"}
    ]
    
    for context in contexts:
        greeting_node.run(context)
        print("-" * 50)