import pytest
import sqlite3
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import todo_app
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    # Store original database path
    original_db = 'todo.db'
    original_db_exists = os.path.exists(original_db)
    
    if original_db_exists:
        # Backup original database
        backup_path = original_db + '.backup'
        os.rename(original_db, backup_path)
    
    # Create a temporary database file
    with open(db_path, 'w') as f:
        pass
    
    yield db_path
    
    # Cleanup
    try:
        os.unlink(db_path)
    except FileNotFoundError:
        pass
    
    if original_db_exists:
        # Restore original database
        try:
            os.rename(backup_path, original_db)
        except FileNotFoundError:
            pass

@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        'topic': 'Test Task',
        'description': 'This is a test task description',
        'due': '2024-12-31',
        'status': 'Pending',
        'impact': 5,
        'tractability': 5,
        'uncertainty': 5
    }

@pytest.fixture
def sample_tasks():
    """Multiple sample tasks for testing"""
    return [
        {
            'topic': 'High Priority Task',
            'description': 'Important and easy task',
            'due': '2024-12-25',
            'status': 'Pending',
            'impact': 9,
            'tractability': 8,
            'uncertainty': 2
        },
        {
            'topic': 'Low Priority Task',
            'description': 'Less important and harder task',
            'due': '2024-12-31',
            'status': 'Pending',
            'impact': 3,
            'tractability': 4,
            'uncertainty': 7
        },
        {
            'topic': 'Completed Task',
            'description': 'Already done task',
            'due': '2024-12-20',
            'status': 'Completed',
            'impact': 6,
            'tractability': 7,
            'uncertainty': 3
        }
    ] 