#!/usr/bin/env python3
"""
Quick test script to verify PocketFlow installation
Run this after setup to ensure everything works
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    
    try:
        from pocketflow import Node, Flow, BatchNode, AsyncNode
        print("✅ PocketFlow imports successful")
    except ImportError as e:
        print(f"❌ PocketFlow import failed: {e}")
        return False
    
    try:
        from anthropic import Anthropic
        print("✅ Anthropic import successful")
    except ImportError as e:
        print(f"❌ Anthropic import failed: {e}")
        print("   Run: pip install anthropic")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv import successful")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        print("   Run: pip install python-dotenv")
        return False
    
    return True

def test_env():
    """Test environment setup"""
    print("\n🔍 Testing environment...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("   Create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        return False
    
    if api_key.startswith("sk-ant-"):
        print("✅ Anthropic API key found")
    else:
        print("⚠️  API key found but doesn't start with 'sk-ant-'")
    
    return True

def test_simple_node():
    """Test a simple node execution"""
    print("\n🔍 Testing simple node...")    
    from pocketflow import Node
    
    class TestNode(Node):
        def exec(self, prep_res):
            return "Hello from PocketFlow!"
    
    try:
        node = TestNode()
        result = node.run({})
        print(f"✅ Node execution successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Node execution failed: {e}")
        return False

def test_simple_flow():
    """Test a simple flow"""
    print("\n🔍 Testing simple flow...")
    
    from pocketflow import Node, Flow
    
    class StartNode(Node):
        def exec(self, prep_res):
            return "Starting"
        
        def post(self, shared, prep_res, exec_res):
            shared["message"] = exec_res
            return None    
    class EndNode(Node):
        def exec(self, prep_res):
            return f"{self.params.get('message', 'No message')} -> Ending"
    
    try:
        start = StartNode()
        end = EndNode()
        start >> end
        
        flow = Flow(start=start)
        shared = {}
        result = flow.run(shared)
        
        print(f"✅ Flow execution successful")
        print(f"   Shared context: {shared}")
        return True
    except Exception as e:
        print(f"❌ Flow execution failed: {e}")
        return False

def test_llm_call():
    """Test LLM API call (optional)"""
    print("\n🔍 Testing LLM call (optional)...")
    
    try:
        from anthropic import Anthropic
        import os
        from dotenv import load_dotenv        
        load_dotenv()
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-opus-4-20250514",
            messages=[{"role": "user", "content": "Say 'PocketFlow works!' in 5 words or less"}],
            max_tokens=20
        )
        
        result = response.content[0].text
        print(f"✅ LLM call successful: {result}")
        return True
    except Exception as e:
        print(f"⚠️  LLM call failed: {e}")
        print("   This is optional - you can still use PocketFlow with mock LLM calls")
        return True  # Don't fail the test for this

def main():
    """Run all tests"""
    print("🚀 PocketFlow Installation Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_env),
        ("Simple Node", test_simple_node),
        ("Simple Flow", test_simple_flow),
        ("LLM Call", test_llm_call)]    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name}: {status}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! PocketFlow is ready to use!")
        print("\n📚 Next steps:")
        print("   1. Try the examples in the examples/ directory")
        print("   2. Start with 01_simple_node.py")
        print("   3. Build something amazing!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("   Check the error messages for guidance.")

if __name__ == "__main__":
    main()