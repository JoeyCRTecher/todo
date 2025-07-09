import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import os

def get_status_color(status):
    """Get the color for a given status."""
    status_colors = {
        'Pending': 'orange',
        'In Progress': 'green', 
        'On Hold': 'grey',
        'Completed': 'orange',
        'Expired': 'red'
    }
    return status_colors.get(status, 'blue')  # default to blue if status not found

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

def check_and_update_expired_tasks():
    """Check for tasks older than 90 days and mark them as expired."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    # Calculate the date 90 days ago
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=90)
    
    # Update tasks that are older than 90 days and not already expired or completed
    cursor.execute('''
        UPDATE tasks 
        SET status = 'Expired', updated_at = CURRENT_TIMESTAMP
        WHERE created_at < ? 
        AND status NOT IN ('Expired', 'Completed')
    ''', (cutoff_date,))
    
    updated_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    return updated_count

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
    
    # Search functionality with magnifying glass icon
    st.sidebar.markdown("### 🔍 Quick Search")
    
    # Use a form to enable Enter key functionality
    with st.sidebar.form("search_form"):
        search_term = st.text_input("Search tasks", placeholder="Enter search term... (Press Enter to search)", key="quick_search")
        search_by = st.selectbox("Search by", ["all", "topic", "description", "status"], key="search_by")
        
        # Form submit button (can be triggered by Enter key)
        search_submitted = st.form_submit_button("🔍 Search", use_container_width=True)
    
    if search_submitted:
        if search_term and search_term.strip():
            # Store search parameters in session state with different keys
            st.session_state.search_term_value = search_term
            st.session_state.search_by_value = search_by
            st.session_state.show_search = True
            st.rerun()
        else:
            st.sidebar.warning("Please enter a search term.")
    
    st.sidebar.markdown("---")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose an action:",
        ["View Tasks", "Add Task", "Edit Task", "Delete Task"]
    )
    
    # Check if search is active
    if hasattr(st.session_state, 'show_search') and st.session_state.show_search:
        search_tasks_page()
        # Clear search state after displaying results
        if st.button("← Back to Tasks", key="back_button"):
            st.session_state.show_search = False
            st.rerun()
    # Check if quick add navigation is active
    elif hasattr(st.session_state, 'navigate_to_add') and st.session_state.navigate_to_add:
        add_task_page()
        # Clear navigation state after displaying add page
        if st.button("← Back to Tasks", key="back_add_button"):
            st.session_state.navigate_to_add = False
            st.session_state.quick_add_task_name = ""
            st.rerun()
    # Check if edit mode is active
    elif hasattr(st.session_state, 'edit_task_id') and st.session_state.edit_task_id:
        edit_task_page()
        # Clear edit state after editing
        if st.button("← Back to Tasks", key="back_edit_button"):
            st.session_state.edit_task_id = None
            st.rerun()
    else:
        if page == "View Tasks":
            view_tasks_page()
        elif page == "Add Task":
            add_task_page()
        elif page == "Edit Task":
            edit_task_page()
        elif page == "Delete Task":
            delete_task_page()

def view_tasks_page():
    st.header("📋 Current Tasks")
    
    # Check for expired tasks
    expired_count = check_and_update_expired_tasks()
    if expired_count > 0:
        st.info(f"📅 {expired_count} task(s) have been automatically marked as expired (older than 90 days).")
    
    # Quick add task field
    st.markdown("### ➕ Quick Add Task")
    with st.form("quick_add_form"):
        quick_task_name = st.text_input("Task name", placeholder="Enter task name and press Enter...", key="quick_add_task")
        quick_add_submitted = st.form_submit_button("Add Task", use_container_width=True)
        
        if quick_add_submitted and quick_task_name.strip():
            # Store the task name in session state and navigate to add task page
            st.session_state.quick_add_task_name = quick_task_name.strip()
            st.session_state.navigate_to_add = True
            st.rerun()
    
    st.markdown("---")
    
    # Get all tasks
    df = get_all_tasks()
    
    if len(df) == 0:
        st.info("No tasks found. Add some tasks to get started!")
        return
    
    # Status filter controls
    st.markdown("### 🔍 Filter by Status")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        show_pending = st.checkbox("Pending", value=True, key="filter_pending")
    with col2:
        show_in_progress = st.checkbox("In Progress", value=True, key="filter_in_progress")
    with col3:
        show_on_hold = st.checkbox("On Hold", value=True, key="filter_on_hold")
    with col4:
        show_completed = st.checkbox("Completed", value=False, key="filter_completed")
    with col5:
        show_expired = st.checkbox("Expired", value=False, key="filter_expired")
    
    # Filter tasks based on selected statuses
    selected_statuses = []
    if show_pending:
        selected_statuses.append("Pending")
    if show_in_progress:
        selected_statuses.append("In Progress")
    if show_on_hold:
        selected_statuses.append("On Hold")
    if show_completed:
        selected_statuses.append("Completed")
    if show_expired:
        selected_statuses.append("Expired")
    
    # Apply filter
    if selected_statuses:
        filtered_df = df[df['status'].isin(selected_statuses)]
    else:
        filtered_df = df  # Show all if no filters selected
    
    st.markdown("---")
    
    # Display filtered tasks
    if len(filtered_df) == 0:
        st.info("No tasks found matching the selected filters.")
        return
    
    for _, task in filtered_df.iterrows():
        status_color = get_status_color(task['status'])
        with st.expander(f"**{task['topic']}** - :{status_color}[{task['status']}] (Score: {task['score']:.2f})"):
            # Display task details in read-only format
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {task['description']}")
                due_date = task['due']
                if due_date is not None and str(due_date) not in ['NaT', 'None', 'nan']:
                    st.write(f"**Due Date:** {due_date}")
                st.write(f"**Impact:** {task['impact']} | **Tractability:** {task['tractability']} | **Uncertainty:** {task['uncertainty']}")
            
            with col2:
                st.write(f"**ID:** {task['id']}")
                st.write(f"**Created:** {task['created_at']}")
                if task['updated_at'] != task['created_at']:
                    st.write(f"**Updated:** {task['updated_at']}")
            
            st.markdown("---")
            
            # Edit form directly in the expander
            st.markdown("### ✏️ Edit Task")
            with st.form(f"edit_task_form_{task['id']}"):
                topic = st.text_input("Topic *", value=task['topic'], key=f"edit_topic_{task['id']}")
                description = st.text_area("Description", value=task['description'] or "", key=f"edit_description_{task['id']}")
                
                # Handle due date
                due_date = None
                if task['due'] is not None and str(task['due']) not in ['NaT', 'None', 'nan']:
                    try:
                        due_date = datetime.strptime(str(task['due']), '%Y-%m-%d').date()
                    except:
                        due_date = None
                
                due = st.date_input("Due Date", value=due_date, key=f"edit_due_{task['id']}")
                status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "On Hold", "Expired"], 
                                    index=["Pending", "In Progress", "Completed", "On Hold", "Expired"].index(str(task['status'])), 
                                    key=f"edit_status_{task['id']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    impact = st.slider("Impact (1-10)", 1, 10, int(task['impact']), key=f"edit_impact_{task['id']}")
                
                with col2:
                    tractability = st.slider("Tractability (1-10)", 1, 10, int(task['tractability']), key=f"edit_tractability_{task['id']}")
                
                with col3:
                    uncertainty = st.slider("Uncertainty (1-10)", 1, 10, int(task['uncertainty']), key=f"edit_uncertainty_{task['id']}")
                
                # Calculate and display score
                score = calculate_score(impact, tractability, uncertainty)
                st.info(f"**Calculated Score:** {score:.2f} (Impact × Tractability ÷ Uncertainty)")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submitted = st.form_submit_button("Update Task", use_container_width=True)
                
                with col2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.rerun()
                
                if submitted:
                    if topic and topic.strip():
                        update_task(task['id'], topic, description, due, status, impact, tractability, uncertainty)
                        st.success("Task updated successfully!")
                        st.rerun()
                    else:
                        st.error("Topic is required!")
    
    # Show summary statistics for filtered results
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Tasks", len(filtered_df))
    
    with col2:
        pending_count = len(filtered_df[filtered_df['status'] == 'Pending'])
        st.metric("Pending", pending_count)
    
    with col3:
        completed_count = len(filtered_df[filtered_df['status'] == 'Completed'])
        st.metric("Completed", completed_count)
    
    with col4:
        avg_score = filtered_df['score'].mean()
        st.metric("Avg Score", f"{avg_score:.2f}")

def add_task_page():
    st.header("➕ Add New Task")
    
    # Check if we have a quick add task name from session state
    quick_task_name = st.session_state.get('quick_add_task_name', '')
    
    with st.form("add_task_form"):
        topic = st.text_input("Topic *", value=quick_task_name, placeholder="Enter task topic")
        description = st.text_area("Description", placeholder="Enter task description")
        due = st.date_input("Due Date", value=None)
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "On Hold", "Expired"])
        
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
                # Clear quick add session state variables
                if hasattr(st.session_state, 'quick_add_task_name'):
                    st.session_state.quick_add_task_name = ""
                if hasattr(st.session_state, 'navigate_to_add'):
                    st.session_state.navigate_to_add = False
                st.rerun()
            else:
                st.error("Topic is required!")

def edit_task_page():
    st.header("✏️ Edit Task")
    
    # Check if we have a specific task ID from session state
    if hasattr(st.session_state, 'edit_task_id') and st.session_state.edit_task_id:
        selected_task_id = st.session_state.edit_task_id
    else:
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
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "On Hold", "Expired"], 
                                index=["Pending", "In Progress", "Completed", "On Hold", "Expired"].index(task[4]), 
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
                if topic and topic.strip():
                    update_task(selected_task_id, topic, description, due, status, impact, tractability, uncertainty)
                    st.success("Task updated successfully!")
                    # Clear edit task ID from session state
                    if hasattr(st.session_state, 'edit_task_id'):
                        st.session_state.edit_task_id = None
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
        status_color = get_status_color(task[4])
        st.write(f"**Status:** :{status_color}[{task[4]}]")
        st.write(f"**Score:** {task[8]}")
        
        if st.button("🗑️ Delete Task", type="primary"):
            delete_task(selected_task_id)
            st.success("Task deleted successfully!")
            st.rerun()

def search_tasks_page():
    st.header("🔍 Search Results")
    
    # Get search parameters from session state
    search_term = st.session_state.get('search_term_value', '')
    search_by = st.session_state.get('search_by_value', 'all')
    
    # Display search criteria
    st.info(f"Searching for: **{search_term}** in **{search_by}**")
    
    # Perform search
    results = search_tasks(search_term, search_by)
    
    if len(results) == 0:
        st.info("No tasks found matching the search criteria.")
    else:
        st.success(f"Found {len(results)} task(s) matching your search.")
        
        # Display search results
        for _, task in results.iterrows():
            status_color = get_status_color(task['status'])
            with st.expander(f"**{task['topic']}** - :{status_color}[{task['status']}] (Score: {task['score']:.2f})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {task['description']}")
                    due_date = task['due']
                    if due_date is not None and str(due_date) not in ['NaT', 'None', 'nan']:
                        st.write(f"**Due Date:** {due_date}")
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

if __name__ == "__main__":
    main() 