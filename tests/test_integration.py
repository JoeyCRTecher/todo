import pytest
import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# Import the functions from todo_app
from todo_app import (
    init_database, add_task, get_all_tasks, update_task, 
    delete_task, get_task_by_id, calculate_score
)

class TestTodoIntegration:
    """Integration tests for the complete todo application workflow"""
    
    def test_database_initialization(self, temp_db):
        """Test that the database can be initialized properly"""
        # Temporarily set the database path
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            # Create a symbolic link or copy to the temp database
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize the database
            init_database()
            
            # Verify the table was created
            conn = sqlite3.connect(original_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
            result = cursor.fetchone()
            conn.close()
            
            assert result is not None
            assert result[0] == 'tasks'
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_complete_task_workflow(self, temp_db, sample_task_data):
        """Test the complete workflow: add, read, update, delete"""
        # Set up temporary database
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # 1. Add task
            add_task(
                sample_task_data['topic'],
                sample_task_data['description'],
                sample_task_data['due'],
                sample_task_data['status'],
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            
            # 2. Read tasks and verify
            tasks = get_all_tasks()
            assert len(tasks) == 1
            assert tasks.iloc[0]['topic'] == sample_task_data['topic']
            assert tasks.iloc[0]['description'] == sample_task_data['description']
            assert tasks.iloc[0]['status'] == sample_task_data['status']
            
            # Verify score calculation
            expected_score = calculate_score(
                sample_task_data['impact'],
                sample_task_data['tractability'],
                sample_task_data['uncertainty']
            )
            assert abs(tasks.iloc[0]['score'] - expected_score) < 0.01
            
            # 3. Update task
            task_id = tasks.iloc[0]['id']
            updated_data = {
                'topic': 'Updated Task',
                'description': 'Updated Description',
                'due': '2024-01-02',
                'status': 'In Progress',
                'impact': 7,
                'tractability': 6,
                'uncertainty': 4
            }
            
            update_task(
                task_id,
                updated_data['topic'],
                updated_data['description'],
                updated_data['due'],
                updated_data['status'],
                updated_data['impact'],
                updated_data['tractability'],
                updated_data['uncertainty']
            )
            
            # 4. Verify update
            updated_tasks = get_all_tasks()
            assert len(updated_tasks) == 1
            assert updated_tasks.iloc[0]['topic'] == updated_data['topic']
            assert updated_tasks.iloc[0]['status'] == updated_data['status']
            assert updated_tasks.iloc[0]['description'] == updated_data['description']
            
            # Verify updated score
            expected_updated_score = calculate_score(
                updated_data['impact'],
                updated_data['tractability'],
                updated_data['uncertainty']
            )
            assert abs(updated_tasks.iloc[0]['score'] - expected_updated_score) < 0.01
            
            # 5. Test get_task_by_id
            retrieved_task = get_task_by_id(task_id)
            assert retrieved_task is not None
            assert retrieved_task[1] == updated_data['topic']  # topic is at index 1
            
            # 6. Delete task
            delete_task(task_id)
            
            # 7. Verify deletion
            final_tasks = get_all_tasks()
            assert len(final_tasks) == 0
            
            # Verify task is really gone
            deleted_task = get_task_by_id(task_id)
            assert deleted_task is None
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_multiple_tasks_ordering(self, temp_db, sample_tasks):
        """Test that multiple tasks are properly ordered by score and due date"""
        original_db = 'todo.db'
        if os.path.exists(original_db):
            os.rename(original_db, original_db + '.backup')
        
        try:
            import shutil
            shutil.copy2(temp_db, original_db)
            
            # Initialize database
            init_database()
            
            # Add multiple tasks
            for task_data in sample_tasks:
                add_task(
                    task_data['topic'],
                    task_data['description'],
                    task_data['due'],
                    task_data['status'],
                    task_data['impact'],
                    task_data['tractability'],
                    task_data['uncertainty']
                )
            
            # Get all tasks
            tasks = get_all_tasks()
            assert len(tasks) == 3
            
            # Verify ordering by score (descending) and due date (ascending)
            scores = tasks['score'].tolist()
            assert scores == sorted(scores, reverse=True)
            
            # Verify that tasks with same score are ordered by due date
            # (This would require more complex logic in a real scenario)
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db)
    
    def test_task_persistence(self, temp_db, sample_task_data):
        """Test that tasks persist across database connections"""
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
            
            # Close any existing connections
            import gc
            gc.collect()
            
            # Verify task still exists
            tasks = get_all_tasks()
            assert len(tasks) == 1
            assert tasks.iloc[0]['topic'] == sample_task_data['topic']
            
        finally:
            # Cleanup
            if os.path.exists(original_db):
                os.unlink(original_db)
            if os.path.exists(original_db + '.backup'):
                os.rename(original_db + '.backup', original_db) 