import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import os

# Page configuration
st.set_page_config(
    page_title="Todo List Manager",
    page_icon="✅",
    layout="wide"
)

# Database setup
def init_database():
    """Initialize the SQLite database and create the tasks table if it doesn't exist."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            description TEXT,
            due DATE,
            status TEXT DEFAULT 'Pending',
            impact INTEGER DEFAULT 1,
            tractability INTEGER DEFAULT 1,
            uncertainty INTEGER DEFAULT 1,
            score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def calculate_score(impact, tractability, uncertainty):
    """Calculate the score based on impact, tractability, and uncertainty."""
    if tractability == 0 or uncertainty == 0:
        return 0.0
    return (impact * tractability) / uncertainty

def get_all_tasks():
    """Retrieve all tasks from the database."""
    conn = sqlite3.connect('todo.db')
    query = "SELECT * FROM tasks ORDER BY score DESC, due ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_task(topic, description, due, status, impact, tractability, uncertainty):
    """Add a new task to the database."""
    score = calculate_score(impact, tractability, uncertainty)
    
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (topic, description, due, status, impact, tractability, uncertainty, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, description, due, status, impact, tractability, uncertainty, score))
    
    conn.commit()
    conn.close()

def update_task(task_id, topic, description, due, status, impact, tractability, uncertainty):
    """Update an existing task in the database."""
    score = calculate_score(impact, tractability, uncertainty)
    
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks 
        SET topic=?, description=?, due=?, status=?, impact=?, tractability=?, uncertainty=?, score=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    ''', (topic, description, due, status, impact, tractability, uncertainty, score, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    """Get a specific task by ID."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    
    conn.close()
    return task

def search_tasks(search_term, search_by="all"):
    """Search tasks by topic, description, or status."""
    conn = sqlite3.connect('todo.db')
    
    if search_by == "all":
        query = """
        SELECT * FROM tasks 
        WHERE topic LIKE ? OR description LIKE ? OR status LIKE ?
        ORDER BY score DESC, due ASC
        """
        search_pattern = f"%{search_term}%"
        df = pd.read_sql_query(query, conn, params=[search_pattern, search_pattern, search_pattern])
    elif search_by == "topic":
        query = "SELECT * FROM tasks WHERE topic LIKE ? ORDER BY score DESC, due ASC"
        search_pattern = f"%{search_term}%"
        df = pd.read_sql_query(query, conn, params=[search_pattern])
    elif search_by == "description":
        query = "SELECT * FROM tasks WHERE description LIKE ? ORDER BY score DESC, due ASC"
        search_pattern = f"%{search_term}%"
        df = pd.read_sql_query(query, conn, params=[search_pattern])
    elif search_by == "status":
        query = "SELECT * FROM tasks WHERE status LIKE ? ORDER BY score DESC, due ASC"
        search_pattern = f"%{search_term}%"
        df = pd.read_sql_query(query, conn, params=[search_pattern])
    else:
        df = pd.DataFrame()
    
    conn.close()
    return df

# Initialize database
init_database()

# Main app
def main():
    st.title("📋 Todo List Manager")
    st.markdown("---")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose an action:",
        ["View Tasks", "Add Task", "Edit Task", "Delete Task", "Search Tasks"]
    )
    
    if page == "View Tasks":
        view_tasks_page()
    elif page == "Add Task":
        add_task_page()
    elif page == "Edit Task":
        edit_task_page()
    elif page == "Delete Task":
        delete_task_page()
    elif page == "Search Tasks":
        search_tasks_page()

def view_tasks_page():
    st.header("📋 Current Tasks")
    
    # Get all tasks
    df = get_all_tasks()
    
    if len(df) == 0:
        st.info("No tasks found. Add some tasks to get started!")
        return
    
    # Display tasks in a nice format
    for _, task in df.iterrows():
        with st.expander(f"**{task['topic']}** - {task['status']} (Score: {task['score']:.2f})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {task['description']}")
                if task['due']:
                    st.write(f"**Due Date:** {task['due']}")
                st.write(f"**Impact:** {task['impact']} | **Tractability:** {task['tractability']} | **Uncertainty:** {task['uncertainty']}")
            
            with col2:
                st.write(f"**ID:** {task['id']}")
                st.write(f"**Created:** {task['created_at']}")
                if task['updated_at'] != task['created_at']:
                    st.write(f"**Updated:** {task['updated_at']}")
    
    # Show summary statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", len(df))
    
    with col2:
        pending_count = len(df[df['status'] == 'Pending'])
        st.metric("Pending", pending_count)
    
    with col3:
        completed_count = len(df[df['status'] == 'Completed'])
        st.metric("Completed", completed_count)
    
    with col4:
        avg_score = df['score'].mean()
        st.metric("Avg Score", f"{avg_score:.2f}")

def add_task_page():
    st.header("➕ Add New Task")
    
    with st.form("add_task_form"):
        topic = st.text_input("Topic *", placeholder="Enter task topic")
        description = st.text_area("Description", placeholder="Enter task description")
        due = st.date_input("Due Date", value=None)
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "On Hold"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            impact = st.slider("Impact (1-10)", 1, 10, 5, help="How important is this task?")
        
        with col2:
            tractability = st.slider("Tractability (1-10)", 1, 10, 5, help="How easy is this to accomplish?")
        
        with col3:
            uncertainty = st.slider("Uncertainty (1-10)", 1, 10, 5, help="How uncertain are we about this task?")
        
        # Calculate and display score
        score = calculate_score(impact, tractability, uncertainty)
        st.info(f"**Calculated Score:** {score:.2f} (Impact × Tractability ÷ Uncertainty)")
        
        submitted = st.form_submit_button("Add Task")
        
        if submitted:
            if topic.strip():
                add_task(topic, description, due, status, impact, tractability, uncertainty)
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error("Topic is required!")

def edit_task_page():
    st.header("✏️ Edit Task")
    
    # Get all tasks for selection
    df = get_all_tasks()
    
    if len(df) == 0:
        st.info("No tasks found to edit.")
        return
    
    # Task selection
    task_options = {f"{row['topic']} (ID: {row['id']})": row['id'] for _, row in df.iterrows()}
    selected_task_label = st.selectbox("Select task to edit:", list(task_options.keys()))
    selected_task_id = task_options[selected_task_label]
    
    # Get task details
    task = get_task_by_id(selected_task_id)
    
    if task:
        with st.form("edit_task_form"):
            topic = st.text_input("Topic *", value=task[1], key="edit_topic")
            description = st.text_area("Description", value=task[2] or "", key="edit_description")
            
            # Handle due date
            due_date = None
            if task[3]:
                try:
                    due_date = datetime.strptime(task[3], '%Y-%m-%d').date()
                except:
                    due_date = None
            
            due = st.date_input("Due Date", value=due_date, key="edit_due")
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "On Hold"], 
                                index=["Pending", "In Progress", "Completed", "On Hold"].index(task[4]), 
                                key="edit_status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                impact = st.slider("Impact (1-10)", 1, 10, task[5], key="edit_impact")
            
            with col2:
                tractability = st.slider("Tractability (1-10)", 1, 10, task[6], key="edit_tractability")
            
            with col3:
                uncertainty = st.slider("Uncertainty (1-10)", 1, 10, task[7], key="edit_uncertainty")
            
            # Calculate and display score
            score = calculate_score(impact, tractability, uncertainty)
            st.info(f"**Calculated Score:** {score:.2f} (Impact × Tractability ÷ Uncertainty)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                submitted = st.form_submit_button("Update Task")
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.rerun()
            
            if submitted:
                if topic.strip():
                    update_task(selected_task_id, topic, description, due, status, impact, tractability, uncertainty)
                    st.success("Task updated successfully!")
                    st.rerun()
                else:
                    st.error("Topic is required!")

def delete_task_page():
    st.header("🗑️ Delete Task")
    
    # Get all tasks for selection
    df = get_all_tasks()
    
    if len(df) == 0:
        st.info("No tasks found to delete.")
        return
    
    # Task selection
    task_options = {f"{row['topic']} (ID: {row['id']})": row['id'] for _, row in df.iterrows()}
    selected_task_label = st.selectbox("Select task to delete:", list(task_options.keys()))
    selected_task_id = task_options[selected_task_label]
    
    # Get task details for confirmation
    task = get_task_by_id(selected_task_id)
    
    if task:
        st.warning("⚠️ **Task to be deleted:**")
        st.write(f"**Topic:** {task[1]}")
        st.write(f"**Description:** {task[2]}")
        st.write(f"**Status:** {task[4]}")
        st.write(f"**Score:** {task[8]}")
        
        if st.button("🗑️ Delete Task", type="primary"):
            delete_task(selected_task_id)
            st.success("Task deleted successfully!")
            st.rerun()

def search_tasks_page():
    st.header("🔍 Search Tasks")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Enter search term", placeholder="Enter topic, description, or status")
    
    with col2:
        search_by = st.selectbox("Search by", ["all", "topic", "description", "status"])
    
    # Search button
    if st.button("🔍 Search", type="primary"):
        if search_term and search_term.strip():
            results = search_tasks(search_term, search_by)
            
            if len(results) == 0:
                st.info("No tasks found matching the search criteria.")
            else:
                st.success(f"Found {len(results)} task(s) matching your search.")
                
                # Display search results
                for _, task in results.iterrows():
                    with st.expander(f"**{task['topic']}** - {task['status']} (Score: {task['score']:.2f})"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Description:** {task['description']}")
                            if task['due']:
                                st.write(f"**Due Date:** {task['due']}")
                            st.write(f"**Impact:** {task['impact']} | **Tractability:** {task['tractability']} | **Uncertainty:** {task['uncertainty']}")
                        
                        with col2:
                            st.write(f"**ID:** {task['id']}")
                            st.write(f"**Created:** {task['created_at']}")
                            if task['updated_at'] != task['created_at']:
                                st.write(f"**Updated:** {task['updated_at']}")
                
                # Show search result statistics
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Search Results", len(results))
                
                with col2:
                    pending_count = len(results[results['status'] == 'Pending'])
                    st.metric("Pending", pending_count)
                
                with col3:
                    completed_count = len(results[results['status'] == 'Completed'])
                    st.metric("Completed", completed_count)
                
                with col4:
                    avg_score = results['score'].mean()
                    st.metric("Avg Score", f"{avg_score:.2f}")
        else:
            st.warning("Please enter a search term.")

if __name__ == "__main__":
    main() 