import sys
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

# 1. Simulate the current buggy implementation
class MockLLMBuggy(BaseModel):
    model: str = "gpt-5.2"
    top_p: float = 1.0
    reasoning_options: Optional[Dict[str, Any]] = None

    def get_model_kwargs(self) -> Dict[str, Any]:
        model_kwargs = {
            "model": self.model,
            "top_p": self.top_p,
        }
        if self.reasoning_options is not None:
            model_kwargs["reasoning"] = self.reasoning_options
        # Missing the fix to pop top_p
        return model_kwargs

# 2. Simulate the fixed implementation
class MockLLMFixed(BaseModel):
    model: str = "gpt-5.2"
    top_p: float = 1.0
    reasoning_options: Optional[Dict[str, Any]] = None

    def get_model_kwargs(self) -> Dict[str, Any]:
        model_kwargs = {
            "model": self.model,
            "top_p": self.top_p,
        }
        if self.reasoning_options is not None:
            model_kwargs["reasoning"] = self.reasoning_options
            # FIX APPLIED HERE
            model_kwargs.pop("top_p", None)
        return model_kwargs

if __name__ == "__main__":
    reasoning = {"effort": "low"}
    
    # Test Buggy
    buggy = MockLLMBuggy(reasoning_options=reasoning)
    buggy_kwargs = buggy.get_model_kwargs()
    print(f"Buggy Kwargs: {buggy_kwargs}")
    
    # Test Fixed
    fixed = MockLLMFixed(reasoning_options=reasoning)
    fixed_kwargs = fixed.get_model_kwargs()
    print(f"Fixed Kwargs: {fixed_kwargs}")

    if "top_p" in buggy_kwargs and "top_p" not in fixed_kwargs:
        print("PASS: top_p removed when reasoning is present.")
    else:
        print("FAIL: top_p behavior incorrect.")
        sys.exit(1)