# Todo List Manager

A modern, feature-rich todo list application built with Python 3.13, Streamlit, and SQLite3. This application helps you manage tasks with priority scoring based on impact, tractability, and uncertainty.

## Features

- ✅ **Add Tasks**: Create new tasks with all required fields
- ✏️ **Edit Tasks**: Modify existing tasks
- 🗑️ **Delete Tasks**: Remove tasks from your list
- 📊 **Priority Scoring**: Automatic score calculation based on impact, tractability, and uncertainty
- 📅 **Due Date Management**: Set and track due dates
- 📈 **Statistics Dashboard**: View task statistics and progress
- 🔄 **Status Tracking**: Track task status (Pending, In Progress, Completed, On Hold)

## Task Fields

Each task includes the following fields:

- **ID**: Auto-incrementing unique identifier
- **Topic**: Task title/name (required)
- **Description**: Detailed task description
- **Due**: Due date for the task
- **Status**: Current status (Pending, In Progress, Completed, On Hold)
- **Impact**: Importance of the task (1-10 scale)
- **Tractability**: How easy the task is to accomplish (1-10 scale)
- **Uncertainty**: How uncertain we are about the task (1-10 scale)
- **Score**: Calculated priority score (Impact × Tractability ÷ Uncertainty)
- **Created At**: Timestamp when task was created
- **Updated At**: Timestamp when task was last modified

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run todo_app.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## Usage

### Viewing Tasks
- Navigate to "View Tasks" in the sidebar
- Tasks are displayed in expandable sections, sorted by score and due date
- View summary statistics at the bottom

### Adding Tasks
1. Go to "Add Task" in the sidebar
2. Fill in the required fields:
   - **Topic** (required): Enter the task name
   - **Description**: Add detailed description
   - **Due Date**: Set when the task is due
   - **Status**: Choose current status
   - **Impact**: Rate importance (1-10)
   - **Tractability**: Rate ease of completion (1-10)
   - **Uncertainty**: Rate uncertainty level (1-10)
3. The score will be calculated automatically
4. Click "Add Task" to save

### Editing Tasks
1. Go to "Edit Task" in the sidebar
2. Select the task you want to edit from the dropdown
3. Modify any fields as needed
4. Click "Update Task" to save changes

### Deleting Tasks
1. Go to "Delete Task" in the sidebar
2. Select the task you want to delete
3. Review the task details
4. Click "Delete Task" to confirm

## Priority Scoring System

The application uses a sophisticated scoring system to help prioritize tasks:

**Score = (Impact × Tractability) ÷ Uncertainty**

- **High Impact + High Tractability + Low Uncertainty** = High Priority
- **Low Impact + Low Tractability + High Uncertainty** = Low Priority

This scoring system helps you focus on tasks that are both important and achievable.

## Database

The application uses SQLite3 for data storage. The database file (`todo.db`) will be created automatically when you first run the application. All data is stored locally on your machine.

## Requirements

- Python 3.13+
- Streamlit 1.28.1+
- Pandas 2.1.3+

## File Structure

```
todo/
├── todo_app.py          # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── todo.db             # SQLite database (created automatically)
```

## Contributing

Feel free to fork this project and submit pull requests for any improvements or bug fixes.

## License

This project is open source and available under the MIT License. 