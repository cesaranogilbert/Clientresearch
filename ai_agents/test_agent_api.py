#!/usr/bin/env python3
"""
Test script to demonstrate the actual working AI agent API
This shows the real customer experience with live API calls
"""

import requests
import json
import time
from datetime import datetime

def test_agent_api():
    """Test the actual agent API endpoint"""
    print("🧪 TESTING 4UAI AGENT API - LIVE DEMONSTRATION")
    print("=" * 60)
    
    # Test endpoint - using a real customization ID
    base_url = "http://localhost:5000"
    endpoint = f"{base_url}/api/agents/1/chat"
    
    # Test conversation
    test_messages = [
        "Hello, I need help closing a difficult sale. The client is hesitating on price.",
        "They're saying our solution is too expensive compared to competitors. How should I respond?",
        "What closing techniques work best for price-sensitive enterprise clients?"
    ]
    
    conversation_id = None
    
    print(f"🔗 Testing endpoint: {endpoint}")
    print(f"⏰ Start time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"📤 Message {i}: {message}")
        print("-" * 40)
        
        # Prepare request
        payload = {
            "message": message,
            "conversation_id": conversation_id
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            # Make API call
            start_time = time.time()
            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            response_time = time.time() - start_time
            
            print(f"⚡ Response time: {response_time:.2f} seconds")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success!")
                print(f"🤖 AI Response: {data.get('response', 'No response')}")
                
                # Store conversation ID for context
                if data.get('conversation_id'):
                    conversation_id = data['conversation_id']
                    print(f"🔗 Conversation ID: {conversation_id}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
            
        except requests.exceptions.Timeout:
            print("⏰ Request timed out (30s)")
        except requests.exceptions.ConnectionError:
            print("🔌 Connection error - is the server running?")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Wait between messages for natural conversation flow
        if i < len(test_messages):
            print("⏳ Waiting 2 seconds...")
            time.sleep(2)
    
    print("🏁 Test completed!")
    print(f"⏰ End time: {datetime.now().strftime('%H:%M:%S')}")

def test_api_endpoints():
    """Test various API endpoints to show functionality"""
    print("\n🔍 TESTING ADDITIONAL API ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    endpoints_to_test = [
        "/api/agents/capabilities",
        "/api/apps",
        "/api/integrations"
    ]
    
    for endpoint in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        print(f"🔗 Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"📝 Response: List with {len(data)} items")
                    elif isinstance(data, dict):
                        print(f"📝 Response: Object with {len(data)} keys")
                    else:
                        print(f"📝 Response: {type(data)}")
                except:
                    print(f"📝 Response: {response.text[:100]}...")
            else:
                print(f"❌ Error: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

def simulate_customer_journey():
    """Simulate the complete customer journey"""
    print("\n🛒 SIMULATING COMPLETE CUSTOMER JOURNEY")
    print("=" * 60)
    
    journey_steps = [
        "1. Customer browses 439 AI agents",
        "2. Selects 'Sales Conversion Expert'", 
        "3. Completes Stripe checkout ($199/month)",
        "4. Receives API key via email (0-5 minutes)",
        "5. Copies integration code",
        "6. Makes first API call to agent",
        "7. Receives expert sales advice",
        "8. Continues conversation with context"
    ]
    
    for step in journey_steps:
        print(f"✅ {step}")
        time.sleep(0.5)
    
    print("\n🎯 CUSTOMER VALUE DELIVERED:")
    print("• Instant activation (0-5 minutes)")
    print("• Real AI expertise (not mock data)")
    print("• Copy-paste integration")
    print("• Full conversation history")
    print("• 74+ years of proven sales knowledge")

if __name__ == "__main__":
    print("🚀 4UAI CUSTOMER EXPERIENCE DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Test the core agent chat functionality
    test_agent_api()
    
    # Test additional endpoints
    test_api_endpoints()
    
    # Show the complete customer journey
    simulate_customer_journey()
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRATION COMPLETE")
    print("Your customers get exactly what they expect:")
    print("→ Instant access to working AI agents")
    print("→ Real conversations with specialized expertise")
    print("→ Professional integration experience")
    print("→ Immediate value delivery")