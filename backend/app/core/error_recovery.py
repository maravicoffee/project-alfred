"""
Project Alfred - Advanced Error Recovery System
Handles errors gracefully with retry logic and fallbacks
"""

import asyncio
from typing import Callable, Any, Optional, Dict
from functools import wraps
import time
import traceback


class ErrorRecoverySystem:
    """Advanced error recovery with retry logic and circuit breaker"""
    
    def __init__(self):
        self.error_counts = {}
        self.circuit_breakers = {}
        self.max_retries = 3
        self.retry_delay = 1.0
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_timeout = 60
    
    def with_retry(self, max_retries: int = None, delay: float = None):
        """Decorator for automatic retry on failure"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                retries = max_retries or self.max_retries
                retry_delay = delay or self.retry_delay
                last_exception = None
                
                for attempt in range(retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        
                        if attempt < retries - 1:
                            print(f"[ErrorRecovery] Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay}s...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            print(f"[ErrorRecovery] All {retries} attempts failed")
                
                # All retries failed
                raise last_exception
            
            return wrapper
        return decorator
    
    def with_fallback(self, fallback_func: Callable):
        """Decorator for fallback on failure"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f"[ErrorRecovery] Primary function failed: {e}. Using fallback...")
                    try:
                        return await fallback_func(*args, **kwargs)
                    except Exception as fallback_error:
                        print(f"[ErrorRecovery] Fallback also failed: {fallback_error}")
                        raise e  # Raise original error
            
            return wrapper
        return decorator
    
    def with_circuit_breaker(self, service_name: str):
        """Decorator for circuit breaker pattern"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Check if circuit is open
                if service_name in self.circuit_breakers:
                    breaker = self.circuit_breakers[service_name]
                    if breaker["state"] == "open":
                        if time.time() - breaker["opened_at"] < self.circuit_breaker_timeout:
                            raise Exception(f"Circuit breaker open for {service_name}")
                        else:
                            # Try half-open state
                            breaker["state"] = "half-open"
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # Success - reset or close circuit
                    if service_name in self.circuit_breakers:
                        self.circuit_breakers[service_name]["state"] = "closed"
                        self.circuit_breakers[service_name]["failures"] = 0
                    
                    return result
                
                except Exception as e:
                    # Track failure
                    if service_name not in self.circuit_breakers:
                        self.circuit_breakers[service_name] = {
                            "state": "closed",
                            "failures": 0,
                            "opened_at": None
                        }
                    
                    breaker = self.circuit_breakers[service_name]
                    breaker["failures"] += 1
                    
                    # Open circuit if threshold exceeded
                    if breaker["failures"] >= self.circuit_breaker_threshold:
                        breaker["state"] = "open"
                        breaker["opened_at"] = time.time()
                        print(f"[ErrorRecovery] Circuit breaker opened for {service_name}")
                    
                    raise e
            
            return wrapper
        return decorator
    
    def safe_execute(self, func: Callable, *args, default_value: Any = None, **kwargs) -> Any:
        """Safely execute a function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ErrorRecovery] Safe execution failed: {e}")
            return default_value
    
    async def safe_execute_async(self, func: Callable, *args, default_value: Any = None, **kwargs) -> Any:
        """Safely execute an async function with error handling"""
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"[ErrorRecovery] Safe async execution failed: {e}")
            return default_value
    
    def get_error_context(self, error: Exception) -> Dict[str, Any]:
        """Get detailed error context for logging"""
        return {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": time.time()
        }
    
    def reset_circuit_breaker(self, service_name: str):
        """Manually reset a circuit breaker"""
        if service_name in self.circuit_breakers:
            self.circuit_breakers[service_name] = {
                "state": "closed",
                "failures": 0,
                "opened_at": None
            }
            print(f"[ErrorRecovery] Circuit breaker reset for {service_name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all circuit breakers"""
        return {
            "circuit_breakers": self.circuit_breakers,
            "error_counts": self.error_counts
        }


# Singleton instance
error_recovery = ErrorRecoverySystem()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Test retry
    @error_recovery.with_retry(max_retries=3, delay=0.5)
    async def flaky_function():
        import random
        if random.random() < 0.7:
            raise Exception("Random failure")
        return "Success!"
    
    # Test fallback
    async def fallback_function():
        return "Fallback result"
    
    @error_recovery.with_fallback(fallback_function)
    async def main_function():
        raise Exception("Main function failed")
    
    # Run tests
    async def test():
        try:
            result = await flaky_function()
            print(f"Retry test: {result}")
        except Exception as e:
            print(f"Retry test failed: {e}")
        
        result = await main_function()
        print(f"Fallback test: {result}")
    
    asyncio.run(test())
