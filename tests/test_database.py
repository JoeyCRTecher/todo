import pytest
import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# Import the functions from todo_app
from todo_app import (
    init_database, add_task, get_all_tasks, update_task, 
    delete_task, get_task_by_id
)

class TestDatabaseOperations:
    """Database-specific integration tests"""
    
    def test_database_table_structure(self, temp_db):
        """Test that the database table has the correct structure"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Check table structure
            conn = sqlite3.connect(original_db)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("PRAGMA table_info(tasks)")
            columns = cursor.fetchall()
            
            # Expected columns: id, topic, description, due, status, impact, tractability, uncertainty, score, created_at, updated_at
            expected_columns = [
                'id', 'topic', 'description', 'due', 'status', 
                'impact', 'tractability', 'uncertainty', 'score', 
                'created_at', 'updated_at'
            ]
            
            actual_columns = [col[1] for col in columns]
            assert actual_columns == expected_columns
            
            # Check that id is primary key
            id_column = [col for col in columns if col[1] == 'id'][0]
            assert id_column[5] == 1  # Primary key flag
            
            # Check that topic is NOT NULL
            topic_column = [col for col in columns if col[1] == 'topic'][0]
            assert topic_column[3] == 1  # NOT NULL flag
            
            conn.close()
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_database_constraints(self, temp_db):
        """Test database constraints and data validation"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Test that we can't insert a task without topic (should fail)
            conn = sqlite3.connect(original_db)
            cursor = conn.cursor()
            
            # This should raise an exception because topic is NOT NULL
            with pytest.raises(sqlite3.IntegrityError):
                cursor.execute('''
                    INSERT INTO tasks (description, due, status, impact, tractability, uncertainty, score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', ('Test description', '2024-12-31', 'Pending', 5, 5, 5, 25.0))
            
            conn.close()
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_auto_increment_id(self, temp_db, sample_task_data):
        """Test that IDs auto-increment properly"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Add multiple tasks
            task_ids = []
            for i in range(3):
                add_task(
                    f"{sample_task_data['topic']} {i+1}",
                    sample_task_data['description'],
                    sample_task_data['due'],
                    sample_task_data['status'],
                    sample_task_data['impact'],
                    sample_task_data['tractability'],
                    sample_task_data['uncertainty']
                )
                
                # Get the last inserted task
                tasks = get_all_tasks()
                task_ids.append(tasks.iloc[-1]['id'])
            
            # Verify IDs are sequential
            assert task_ids == [1, 2, 3]
            
            # Delete middle task and add new one
            delete_task(2)
            add_task(
                "New Task",
                sample_task_data['description'],
                sample_task_data['due'],
                sample_task_data['status'],
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            
            # Verify new task gets next available ID
            tasks = get_all_tasks()
            new_task_id = tasks.iloc[-1]['id']
            assert new_task_id == 4  # Should be 4, not 2
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_timestamp_handling(self, temp_db, sample_task_data):
        """Test that created_at and updated_at timestamps work correctly"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Add a task
            add_task(
                sample_task_data['topic'],
                sample_task_data['description'],
                sample_task_data['due'],
                sample_task_data['status'],
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            
            # Get the task
            tasks = get_all_tasks()
            task = tasks.iloc[0]
            
            # Verify timestamps exist and are the same initially
            assert task['created_at'] is not None
            assert task['updated_at'] is not None
            assert task['created_at'] == task['updated_at']
            
            # Update the task
            task_id = task['id']
            update_task(
                task_id,
                "Updated Topic",
                sample_task_data['description'],
                sample_task_data['due'],
                sample_task_data['status'],
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            
            # Get updated task
            updated_tasks = get_all_tasks()
            updated_task = updated_tasks.iloc[0]
            
            # Verify created_at didn't change but updated_at did
            assert updated_task['created_at'] == task['created_at']
            assert updated_task['updated_at'] != task['updated_at']
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_database_connection_handling(self, temp_db, sample_task_data):
        """Test that database connections are properly managed"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Add a task
            add_task(
                sample_task_data['topic'],
                sample_task_data['description'],
                sample_task_data['due'],
                sample_task_data['status'],
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            
            # Verify we can still connect and read
            tasks = get_all_tasks()
            assert len(tasks) == 1
            
            # Force garbage collection to close any lingering connections
            import gc
            gc.collect()
            
            # Verify we can still read after GC
            tasks_after_gc = get_all_tasks()
            assert len(tasks_after_gc) == 1
            assert tasks_after_gc.iloc[0]['topic'] == sample_task_data['topic']
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db) 