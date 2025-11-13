#!/usr/bin/env python3
"""
Nexa Project Status Checker
Verifies all components are running
"""

import requests
import sys
from datetime import datetime

def check_service(name, url, timeout=5):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: Running at {url}")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code} at {url}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: Not reachable at {url}")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ {name}: Timeout at {url}")
        return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

def main():
    print("🔍 Nexa Project Status Check")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check backend on multiple possible ports
    backend_running = False
    backend_ports = [8001, 8002, 8003, 8000]
    
    for port in backend_ports:
        url = f"http://localhost:{port}/health"
        if check_service(f"Backend (:{port})", url):
            backend_running = True
            
            # Test API endpoint
            api_url = f"http://localhost:{port}/api/test"
            check_service(f"API Test (:{port})", api_url)
            break
    
    if not backend_running:
        print("❌ Backend: Not running on any expected port")
    
    print()
    
    # Check frontend on multiple possible ports
    frontend_running = False
    frontend_ports = [3000, 3001, 3002]
    
    for port in frontend_ports:
        url = f"http://localhost:{port}/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ Frontend: Running at http://localhost:{port}")
                frontend_running = True
                break
        except:
            continue
    
    if not frontend_running:
        print("❌ Frontend: Not running on any expected port")
    
    print()
    print("=" * 40)
    
    if backend_running and frontend_running:
        print("🎉 Nexa Project Status: FULLY OPERATIONAL")
        print("🌐 Visit: http://localhost:3000 (or 3001/3002)")
        return 0
    elif backend_running:
        print("⚠️  Nexa Project Status: BACKEND ONLY")
        print("💡 Start frontend with: python frontend/simple-server.py")
        return 1
    elif frontend_running:
        print("⚠️  Nexa Project Status: FRONTEND ONLY")
        print("💡 Start backend with: python backend/smart_server.py")
        return 1
    else:
        print("❌ Nexa Project Status: NOT RUNNING")
        print("💡 Run: powershell -ExecutionPolicy Bypass -File run-complete-project.ps1")
        return 2

if __name__ == "__main__":
    sys.exit(main())
