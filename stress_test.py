#!/usr/bin/env python3.11
"""
Project Alfred - Stress Testing & Load Testing
Tests system under heavy load and concurrent users
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict, Any
import json

BASE_URL = "http://localhost:8000"

class StressTest:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "response_times": [],
            "errors": []
        }
    
    async def send_chat_message(self, session: aiohttp.ClientSession, user_id: str, message: str) -> Dict[str, Any]:
        """Send a chat message and measure response time"""
        start_time = time.time()
        
        try:
            async with session.post(
                f"{self.base_url}/chat",
                json={"message": message, "user_id": user_id},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                end_time = time.time()
                response_time = end_time - start_time
                
                self.results["total_requests"] += 1
                self.results["response_times"].append(response_time)
                
                if response.status == 200:
                    self.results["successful_requests"] += 1
                    data = await response.json()
                    return {
                        "success": True,
                        "response_time": response_time,
                        "response": data.get("response", "")
                    }
                else:
                    self.results["failed_requests"] += 1
                    return {
                        "success": False,
                        "response_time": response_time,
                        "error": f"HTTP {response.status}"
                    }
        
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            self.results["total_requests"] += 1
            self.results["failed_requests"] += 1
            self.results["errors"].append(str(e))
            
            return {
                "success": False,
                "response_time": response_time,
                "error": str(e)
            }
    
    async def simulate_user(self, session: aiohttp.ClientSession, user_id: str, num_messages: int):
        """Simulate a single user sending multiple messages"""
        messages = [
            "Hello Alfred!",
            "What's 42 + 58?",
            "Can you search for AI news?",
            "List my files",
            "Execute print('Hello World')",
            "Analyze these numbers: 10, 20, 30, 40, 50"
        ]
        
        for i in range(num_messages):
            message = messages[i % len(messages)]
            result = await self.send_chat_message(session, user_id, message)
            
            if not result["success"]:
                print(f"❌ User {user_id} - Message {i+1} failed: {result.get('error')}")
            
            # Small delay between messages from same user
            await asyncio.sleep(0.5)
    
    async def run_concurrent_users(self, num_users: int, messages_per_user: int):
        """Simulate multiple concurrent users"""
        print(f"\n🔥 Starting stress test: {num_users} users, {messages_per_user} messages each")
        print(f"Total expected requests: {num_users * messages_per_user}")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.simulate_user(session, f"stress-user-{i}", messages_per_user)
                for i in range(num_users)
            ]
            
            start_time = time.time()
            await asyncio.gather(*tasks)
            end_time = time.time()
            
            total_time = end_time - start_time
            
            return total_time
    
    def print_results(self, total_time: float):
        """Print stress test results"""
        print("\n" + "=" * 60)
        print("STRESS TEST RESULTS")
        print("=" * 60)
        
        print(f"\n📊 Request Statistics:")
        print(f"  Total Requests: {self.results['total_requests']}")
        print(f"  Successful: {self.results['successful_requests']}")
        print(f"  Failed: {self.results['failed_requests']}")
        print(f"  Success Rate: {(self.results['successful_requests'] / self.results['total_requests'] * 100):.2f}%")
        
        print(f"\n⏱️  Performance Metrics:")
        print(f"  Total Time: {total_time:.2f}s")
        print(f"  Requests/Second: {self.results['total_requests'] / total_time:.2f}")
        
        if self.results['response_times']:
            print(f"\n📈 Response Time Statistics:")
            print(f"  Min: {min(self.results['response_times']):.3f}s")
            print(f"  Max: {max(self.results['response_times']):.3f}s")
            print(f"  Mean: {statistics.mean(self.results['response_times']):.3f}s")
            print(f"  Median: {statistics.median(self.results['response_times']):.3f}s")
            
            if len(self.results['response_times']) > 1:
                print(f"  Std Dev: {statistics.stdev(self.results['response_times']):.3f}s")
        
        if self.results['errors']:
            print(f"\n❌ Errors ({len(self.results['errors'])}):")
            error_counts = {}
            for error in self.results['errors']:
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in error_counts.items():
                print(f"  - {error}: {count} occurrences")
        
        print("\n" + "=" * 60)
        
        # Determine pass/fail
        success_rate = (self.results['successful_requests'] / self.results['total_requests'] * 100)
        avg_response_time = statistics.mean(self.results['response_times']) if self.results['response_times'] else 0
        
        print("\n🎯 Test Verdict:")
        if success_rate >= 95 and avg_response_time < 3.0:
            print("  ✅ PASS - System is stable under load")
        elif success_rate >= 80:
            print("  ⚠️  WARNING - System is functional but needs optimization")
        else:
            print("  ❌ FAIL - System is not ready for production load")
        
        print("=" * 60)


async def main():
    """Run stress tests"""
    print("=" * 60)
    print("PROJECT ALFRED - STRESS & LOAD TESTING")
    print("=" * 60)
    
    # Test 1: Light load
    print("\n🧪 Test 1: Light Load (10 users, 3 messages each)")
    test1 = StressTest()
    time1 = await test1.run_concurrent_users(10, 3)
    test1.print_results(time1)
    
    await asyncio.sleep(2)
    
    # Test 2: Medium load
    print("\n🧪 Test 2: Medium Load (25 users, 5 messages each)")
    test2 = StressTest()
    time2 = await test2.run_concurrent_users(25, 5)
    test2.print_results(time2)
    
    await asyncio.sleep(2)
    
    # Test 3: Heavy load
    print("\n🧪 Test 3: Heavy Load (50 users, 3 messages each)")
    test3 = StressTest()
    time3 = await test3.run_concurrent_users(50, 3)
    test3.print_results(time3)
    
    print("\n✅ All stress tests complete!")


if __name__ == "__main__":
    asyncio.run(main())
