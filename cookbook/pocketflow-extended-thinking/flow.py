from pocketflow import Flow
from nodes import ExtendedThinkingNode, StandardSolutionNode

def create_extended_thinking_flow():
    """
    Create a flow that uses extended thinking for complex problems
    """
    # Create nodes
    thinking_node = ExtendedThinkingNode()
    standard_node = StandardSolutionNode()
    
    # Connect nodes - if extended thinking is enabled, use it; otherwise fallback
    thinking_node.next(standard_node, action="fallback")
    
    # Create and return flow
    return Flow(start=thinking_node)