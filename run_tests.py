#!/usr/bin/env python3
"""
Test runner for Todo List Manager

This script provides convenient commands to run different types of tests.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Main test runner function"""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <command>")
        print("\nAvailable commands:")
        print("  all          - Run all tests")
        print("  integration  - Run integration tests only")
        print("  database     - Run database tests only")
        print("  calculations - Run calculation tests only")
        print("  coverage     - Run all tests with coverage report")
        print("  install      - Install test dependencies")
        return
    
    command = sys.argv[1].lower()
    
    if command == "install":
        print("Installing test dependencies...")
        run_command("pip install -r requirements.txt", "Installing dependencies")
        
    elif command == "all":
        print("Running all tests...")
        success = run_command("pytest tests/ -v", "All tests")
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
            
    elif command == "integration":
        print("Running integration tests...")
        success = run_command("pytest tests/test_integration.py -v", "Integration tests")
        if success:
            print("\n✅ Integration tests passed!")
        else:
            print("\n❌ Integration tests failed!")
            sys.exit(1)
            
    elif command == "database":
        print("Running database tests...")
        success = run_command("pytest tests/test_database.py -v", "Database tests")
        if success:
            print("\n✅ Database tests passed!")
        else:
            print("\n❌ Database tests failed!")
            sys.exit(1)
            
    elif command == "calculations":
        print("Running calculation tests...")
        success = run_command("pytest tests/test_calculations.py -v", "Calculation tests")
        if success:
            print("\n✅ Calculation tests passed!")
        else:
            print("\n❌ Calculation tests failed!")
            sys.exit(1)
            
    elif command == "coverage":
        print("Running tests with coverage...")
        success = run_command("pytest tests/ --cov=todo_app --cov-report=html --cov-report=term", "Tests with coverage")
        if success:
            print("\n✅ All tests passed with coverage!")
            print("📊 Coverage report generated in htmlcov/")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
            
    else:
        print(f"Unknown command: {command}")
        print("Use 'python run_tests.py' to see available commands")

if __name__ == "__main__":
    main() 