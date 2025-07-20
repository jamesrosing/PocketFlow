#!/usr/bin/env python3
"""
PocketFlow Extended Thinking Example
Demonstrates how to use Claude's extended thinking capability for complex reasoning tasks
"""
import sys
from flow import create_extended_thinking_flow

def main():
    # Default complex problems that benefit from extended thinking
    default_problems = {
        "math": "Find all positive integer solutions to the equation x^3 + y^3 + z^3 = 33",
        "logic": "In a village, there are two types of people: knights who always tell the truth, and knaves who always lie. You meet three villagers A, B, and C. A says 'B is a knave', B says 'A and C are of the same type', and C says 'A is a knight'. What type is each villager?",
        "coding": "Design an algorithm to find the longest palindromic subsequence in a string with O(n) space complexity instead of the typical O(n^2). Explain the approach and provide pseudocode.",
        "physics": "A ball is thrown upward from the top of a 100m tall building with initial velocity 20 m/s. Taking air resistance into account (drag coefficient 0.47, ball radius 0.1m, mass 0.5kg), calculate when and where it will hit the ground."
    }
    
    # Get problem type from command line or use default
    problem_type = "math"
    custom_problem = None
    
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--type" and i + 1 < len(sys.argv) - 1:
            problem_type = sys.argv[i + 2]
        elif arg == "--problem" and i + 1 < len(sys.argv) - 1:
            custom_problem = sys.argv[i + 2]
    
    # Select problem
    if custom_problem:
        problem = custom_problem
        print(f"🧠 Using custom problem")
    else:
        problem = default_problems.get(problem_type, default_problems["math"])
        print(f"🧠 Using {problem_type} problem")
    
    print(f"\n📝 Problem: {problem}\n")
    print("⏳ Enabling extended thinking mode... This may take a moment.\n")
    
    # Create and run the flow
    flow = create_extended_thinking_flow()
    
    shared = {
        "problem": problem,
        "enable_thinking": True,
        "solution": None,
        "thinking_tokens_used": 0
    }
    
    flow.run(shared)
    
    # Display results
    print("\n" + "="*80)
    print("✅ SOLUTION:")
    print("="*80)
    print(shared.get("solution", "No solution found"))
    
    if shared.get("thinking_tokens_used"):
        print(f"\n💭 Thinking tokens used: {shared['thinking_tokens_used']:,}")

if __name__ == "__main__":
    main()