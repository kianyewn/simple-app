#!/usr/bin/env python3
"""
Setup validation script for Simple Groq App.

This script validates that the development environment is properly configured.
"""

import os
import sys
import importlib
from typing import List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """
    Check if Python version is compatible.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)"


def check_required_packages() -> Tuple[bool, List[str]]:
    """
    Check if required packages are installed.
    
    Returns:
        Tuple[bool, List[str]]: (all_success, messages)
    """
    required_packages = [
        "fastapi",
        "uvicorn",
        "streamlit",
        "groq",
        "pydantic",
        "requests",
        "python_dotenv"
    ]
    
    messages = []
    all_success = True
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace("_", "."))
            messages.append(f"✅ {package}")
        except ImportError:
            messages.append(f"❌ {package} (missing)")
            all_success = False
    
    return all_success, messages


def check_environment_variables() -> Tuple[bool, List[str]]:
    """
    Check environment variables configuration.
    
    Returns:
        Tuple[bool, List[str]]: (all_success, messages)
    """
    messages = []
    all_success = True
    
    # Check for .env file
    if os.path.exists('.env'):
        messages.append("✅ .env file exists")
    elif os.path.exists('env.example'):
        messages.append("⚠️ .env file missing (env.example found)")
        messages.append("   Copy env.example to .env and configure it")
        all_success = False
    else:
        messages.append("❌ No .env or env.example file found")
        all_success = False
    
    # Check critical environment variables
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        # Mask the key for security
        masked_key = groq_key[:8] + "*" * (len(groq_key) - 12) + groq_key[-4:] if len(groq_key) > 12 else "***"
        messages.append(f"✅ GROQ_API_KEY configured ({masked_key})")
    else:
        messages.append("❌ GROQ_API_KEY not set")
        all_success = False
    
    return all_success, messages


def check_file_structure() -> Tuple[bool, List[str]]:
    """
    Check if required files and directories exist.
    
    Returns:
        Tuple[bool, List[str]]: (all_success, messages)
    """
    required_paths = [
        "backend/main.py",
        "backend/models/chat_models.py",
        "backend/services/groq_service.py",
        "backend/utils/config.py",
        "frontend/app.py",
        "frontend/components/chat_interface.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "Procfile",
        "runtime.txt",
        "app.json"
    ]
    
    messages = []
    all_success = True
    
    for path in required_paths:
        if os.path.exists(path):
            messages.append(f"✅ {path}")
        else:
            messages.append(f"❌ {path} (missing)")
            all_success = False
    
    return all_success, messages


def check_docker_availability() -> Tuple[bool, str]:
    """
    Check if Docker is available.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, f"✅ Docker available: {version}"
        else:
            return False, "❌ Docker command failed"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "❌ Docker not found or not responding"
    except Exception as e:
        return False, f"❌ Docker check error: {str(e)}"


def main():
    """Main validation function."""
    print("🔍 Simple Groq App - Setup Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check Python version
    python_ok, python_msg = check_python_version()
    print(f"\\n📋 Python Version:")
    print(f"   {python_msg}")
    if not python_ok:
        all_checks_passed = False
    
    # Check required packages
    packages_ok, package_msgs = check_required_packages()
    print(f"\\n📦 Required Packages:")
    for msg in package_msgs:
        print(f"   {msg}")
    if not packages_ok:
        all_checks_passed = False
    
    # Check environment variables
    env_ok, env_msgs = check_environment_variables()
    print(f"\\n🔧 Environment Configuration:")
    for msg in env_msgs:
        print(f"   {msg}")
    if not env_ok:
        all_checks_passed = False
    
    # Check file structure
    files_ok, file_msgs = check_file_structure()
    print(f"\\n📁 File Structure:")
    for msg in file_msgs:
        print(f"   {msg}")
    if not files_ok:
        all_checks_passed = False
    
    # Check Docker availability
    docker_ok, docker_msg = check_docker_availability()
    print(f"\\n🐳 Docker:")
    print(f"   {docker_msg}")
    if not docker_ok:
        print("   ⚠️ Docker is optional for local Python development")
    
    # Final result
    print("\\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 All checks passed! Your setup is ready.")
        print("\\n🚀 Next steps:")
        print("   1. Set your GROQ_API_KEY in .env file")
        print("   2. Run: python3 run_local.py")
        print("   3. Or use Docker: docker-compose up --build")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\\n📖 See README.md for detailed setup instructions.")
    
    print("=" * 50)
    
    return 0 if all_checks_passed else 1


if __name__ == "__main__":
    sys.exit(main())
