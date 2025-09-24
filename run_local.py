#!/usr/bin/env python3
"""
Local development runner for Simple Groq App.

This script helps start the application for local development.
"""

import os
import sys
import subprocess
import time
import signal
from typing import List
from dotenv import load_dotenv

load_dotenv()

class LocalRunner:
    """Runner class for local development."""
    
    def __init__(self):
        """Initialize the local runner."""
        self.processes: List[subprocess.Popen] = []
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\\n🛑 Received signal {signum}, shutting down gracefully...")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up running processes."""
        for process in self.processes:
            if process.poll() is None:  # Process is still running
                print(f"🔄 Stopping process {process.pid}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
    
    def check_requirements(self) -> bool:
        """
        Check if all requirements are met.
        
        Returns:
            bool: True if requirements are met, False otherwise.
        """
        # Check if .env file exists
        if not os.path.exists('.env') and not os.path.exists('env.example'):
            print("❌ No .env file found. Please copy env.example to .env and configure it.")
            return False
        
        # Check if GROQ_API_KEY is set
        if not os.getenv('GROQ_API_KEY'):
            print("❌ GROQ_API_KEY environment variable not set.")
            print("   Please set it in your .env file or environment.")
            return False
        
        # Check if required packages are installed
        try:
            import fastapi
            import streamlit
            import groq
            import uvicorn
        except ImportError as e:
            print(f"❌ Missing required package: {e}")
            print("   Please run: pip install -r requirements.txt")
            return False
        
        return True
    
    def start_backend(self):
        """Start the FastAPI backend."""
        print("🚀 Starting FastAPI backend...")
        
        backend_cmd = [
            "uv", "run", sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        process = subprocess.Popen(
            backend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        self.processes.append(process)
        print("✅ Backend started on http://localhost:8000")
        return process
    
    def start_frontend(self):
        """Start the Streamlit frontend."""
        print("🚀 Starting Streamlit frontend...")
        
        frontend_cmd = [
            "uv", "run", sys.executable, "-m", "streamlit",
            "run", "frontend/app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "false"
        ]
        
        process = subprocess.Popen(
            frontend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        self.processes.append(process)
        print("✅ Frontend started on http://localhost:8501")
        return process
    
    def wait_for_backend(self, timeout: int = 30) -> bool:
        """
        Wait for backend to be ready.
        
        Args:
            timeout (int): Maximum time to wait in seconds.
            
        Returns:
            bool: True if backend is ready, False if timeout.
        """
        import requests
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            time.sleep(1)
        
        return False
    
    def run(self):
        """Run the complete application stack."""
        print("🎯 Simple Groq App - Local Development Runner")
        print("=" * 50)
        
        # Check requirements
        if not self.check_requirements():
            return False
        
        try:
            # Start backend
            backend_process = self.start_backend()
            
            # Wait for backend to be ready
            print("⏳ Waiting for backend to be ready...")
            if not self.wait_for_backend():
                print("❌ Backend failed to start or is not responding")
                self.cleanup()
                return False
            
            # Start frontend
            frontend_process = self.start_frontend()
            
            print("\\n" + "=" * 50)
            print("🎉 Application is running!")
            print("🔗 Backend API: http://localhost:8000")
            print("🔗 API Docs: http://localhost:8000/docs")
            print("🔗 Frontend: http://localhost:8501")
            print("=" * 50)
            print("\\n💡 Press Ctrl+C to stop all services\\n")
            
            # Monitor processes
            while True:
                time.sleep(1)
                
                # Check if any process has died
                for i, process in enumerate(self.processes):
                    if process.poll() is not None:
                        print(f"❌ Process {i} has stopped unexpectedly")
                        self.cleanup()
                        return False
        
        except KeyboardInterrupt:
            print("\\n🛑 Received interrupt signal")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            self.cleanup()
        
        return True


def main():
    """Main function."""
    runner = LocalRunner()
    success = runner.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
