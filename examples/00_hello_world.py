"""
Hello World Example - Test PocketFlow without LLM
"""
from pocketflow import Node, Flow

class HelloNode(Node):
    """Simple node that says hello"""
    
    def prep(self, shared):
        """Get the name to greet"""
        return shared.get("name", "World")
    
    def exec(self, name):
        """Create greeting"""
        return f"Hello, {name}!"
    
    def post(self, shared, prep_res, exec_res):
        """Display greeting"""
        print(exec_res)
        shared["greeting"] = exec_res
        return "continue"  # Action to take next

class GoodbyeNode(Node):
    """Node that says goodbye"""
    
    def exec(self, prep_res):
        name = self.params.get("name", "Friend")
        return f"Goodbye, {name}! Thanks for using PocketFlow!"
    
    def post(self, shared, prep_res, exec_res):
        print(exec_res)
        return None  # End the flow

# Create and run the flow
if __name__ == "__main__":
    # Create nodes
    hello = HelloNode()
    goodbye = GoodbyeNode()
    
    # Connect nodes: hello -> goodbye when "continue" action
    hello - "continue" >> goodbye
    
    # Create flow starting with hello node
    flow = Flow(start=hello)
    
    # Run with context
    context = {"name": "PocketFlow User"}
    flow.run(context)
    
    print(f"\nFinal context: {context}")