#!/usr/bin/env python3
"""
Minimal test server to verify FastAPI is working
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Nexa Test Server")

@app.get("/")
async def root():
    return {"message": "Nexa backend is working!", "status": "success"}

@app.get("/test")
async def test():
    return {"test": "passed", "server": "running"}

if __name__ == "__main__":
    print("🧪 Starting Nexa Test Server...")
    print("URL: http://localhost:8000")
    print("Test: http://localhost:8000/test")
    print("Docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
