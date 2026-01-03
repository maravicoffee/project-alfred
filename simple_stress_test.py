#!/usr/bin/env python3.11
"""
Project Alfred - Simple Stress Test
Tests system performance using requests library
"""

import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000"

class SimpleStressTest:
    def __init__(self):
        self.results = []
        self.errors = []
    
    def send_request(self, user_id: str, message: str):
        """Send a single chat request"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": message, "user_id": user_id},
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                "success": response.status_code == 200,
                "response_time": response_time,
                "status": response.status_code
            }
        
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            self.errors.append(str(e))
            
            return {
                "success": False,
                "response_time": response_time,
                "error": str(e)
            }
    
    def run_test(self, num_requests: int, num_workers: int = 10):
        """Run stress test with concurrent requests"""
        print(f"\n🔥 Running stress test: {num_requests} requests with {num_workers} workers")
        print("=" * 60)
        
        messages = [
            "Hello Alfred!",
            "What's 42 + 58?",
            "Can you help me?",
            "Test message",
            "Quick question"
        ]
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            
            for i in range(num_requests):
                user_id = f"stress-user-{i % 20}"  # Simulate 20 different users
                message = messages[i % len(messages)]
                future = executor.submit(self.send_request, user_id, message)
                futures.append(future)
            
            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)
                
                if not result["success"]:
                    print(f"❌ Request failed: {result.get('error', result.get('status'))}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return total_time
    
    def print_results(self, total_time: float):
        """Print test results"""
        successful = sum(1 for r in self.results if r["success"])
        failed = len(self.results) - successful
        response_times = [r["response_time"] for r in self.results]
        
        print("\n" + "=" * 60)
        print("STRESS TEST RESULTS")
        print("=" * 60)
        
        print(f"\n📊 Request Statistics:")
        print(f"  Total Requests: {len(self.results)}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Success Rate: {(successful / len(self.results) * 100):.2f}%")
        
        print(f"\n⏱️  Performance Metrics:")
        print(f"  Total Time: {total_time:.2f}s")
        print(f"  Requests/Second: {len(self.results) / total_time:.2f}")
        
        if response_times:
            print(f"\n📈 Response Time Statistics:")
            print(f"  Min: {min(response_times):.3f}s")
            print(f"  Max: {max(response_times):.3f}s")
            print(f"  Mean: {statistics.mean(response_times):.3f}s")
            print(f"  Median: {statistics.median(response_times):.3f}s")
            
            if len(response_times) > 1:
                print(f"  Std Dev: {statistics.stdev(response_times):.3f}s")
        
        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
        
        print("\n" + "=" * 60)
        
        # Verdict
        success_rate = (successful / len(self.results) * 100)
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        print("\n🎯 Test Verdict:")
        if success_rate >= 95 and avg_response_time < 3.0:
            print("  ✅ PASS - System is stable under load")
        elif success_rate >= 80:
            print("  ⚠️  WARNING - System needs optimization")
        else:
            print("  ❌ FAIL - System is not production-ready")
        
        print("=" * 60)


def main():
    """Run stress tests"""
    print("=" * 60)
    print("PROJECT ALFRED - STRESS TESTING")
    print("=" * 60)
    
    # Test 1: Light load
    print("\n🧪 Test 1: Light Load (30 requests, 5 workers)")
    test1 = SimpleStressTest()
    time1 = test1.run_test(30, 5)
    test1.print_results(time1)
    
    time.sleep(2)
    
    # Test 2: Medium load
    print("\n\n🧪 Test 2: Medium Load (50 requests, 10 workers)")
    test2 = SimpleStressTest()
    time2 = test2.run_test(50, 10)
    test2.print_results(time2)
    
    print("\n✅ Stress testing complete!")


if __name__ == "__main__":
    main()
