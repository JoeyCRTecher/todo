# Todo
Filter out old tasks
Add tags


# Todo List Manager

A modern, feature-rich todo list application built with Python 3.13, Streamlit, and SQLite3. This application helps you manage tasks with priority scoring based on impact, tractability, and uncertainty.

## Features

- ✅ **Add Tasks**: Create new tasks with all required fields
- ✏️ **Edit Tasks**: Modify existing tasks
- 🗑️ **Delete Tasks**: Remove tasks from your list
- 🔍 **Search Tasks**: Search tasks by topic, description, or status
- 📊 **Priority Scoring**: Automatic score calculation based on impact, tractability, and uncertainty
- 📅 **Due Date Management**: Set and track due dates
- 📈 **Statistics Dashboard**: View task statistics and progress
- 🔄 **Status Tracking**: Track task status (Pending, In Progress, Completed, On Hold, Expired)
- ⏰ **Automatic Expiration**: Tasks older than 90 days are automatically marked as expired
- 🔍 **Expired Task Filtering**: Toggle visibility of expired tasks (hidden by default)

## Task Fields

Each task includes the following fields:

- **ID**: Auto-incrementing unique identifier
- **Topic**: Task title/name (required)
- **Description**: Detailed task description
- **Due**: Due date for the task
- **Status**: Current status (Pending, In Progress, Completed, On Hold, Expired)
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
- Use the status filters to show/hide different task statuses (including expired tasks)
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

### Searching Tasks
1. Use the **🔍 Quick Search** section in the sidebar
2. Enter your search term in the text field
3. Choose what to search by:
   - **All**: Search in topic, description, and status
   - **Topic**: Search only in task topics
   - **Description**: Search only in task descriptions
   - **Status**: Search only in task status
4. Click the **🔍 Search** button to find matching tasks
5. View search results with statistics
6. Click "← Back to Tasks" to return to the main interface

## Priority Scoring System

The application uses a sophisticated scoring system to help prioritize tasks:

**Score = (Impact × Tractability) ÷ Uncertainty**

- **High Impact + High Tractability + Low Uncertainty** = High Priority
- **Low Impact + Low Tractability + High Uncertainty** = Low Priority

This scoring system helps you focus on tasks that are both important and achievable.

## Automatic Task Expiration

The application automatically manages task expiration to help you keep your task list current:

- **90-Day Rule**: Tasks that are older than 90 days are automatically marked as "Expired"
- **Smart Updates**: Only tasks that are not already "Completed" or "Expired" are affected
- **Visual Feedback**: You'll see a notification when tasks are automatically expired
- **Filter Control**: Expired tasks are hidden by default but can be shown using the filter toggle
- **Manual Override**: You can manually change a task's status back from "Expired" if needed

This feature helps you maintain a clean, current task list by automatically identifying tasks that may no longer be relevant.

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
├── todo.db             # SQLite database (created automatically)
├── pytest.ini          # Pytest configuration
├── run_tests.py        # Test runner script
└── tests/              # Test directory
    ├── __init__.py     # Makes tests a Python package
    ├── conftest.py     # Pytest fixtures and configuration
    ├── test_integration.py  # Integration tests
    ├── test_database.py     # Database tests
    └── test_calculations.py # Business logic tests
```

## Testing

This project includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

1. **Install test dependencies**:
   ```bash
   python run_tests.py install
   ```

2. **Run all tests**:
   ```bash
   python run_tests.py all
   ```

3. **Run specific test types**:
   ```bash
   python run_tests.py integration  # Integration tests
   python run_tests.py database     # Database tests
   python run_tests.py calculations # Business logic tests
   ```

4. **Run tests with coverage**:
   ```bash
   python run_tests.py coverage
   ```

### Test Structure

- **Integration Tests** (`test_integration.py`): Test complete workflows and end-to-end functionality
- **Database Tests** (`test_database.py`): Test database operations, constraints, and data integrity
- **Calculation Tests** (`test_calculations.py`): Test the priority scoring system and business logic

### Test Features

- ✅ **Isolated Testing**: Uses temporary databases to avoid affecting development data
- ✅ **Comprehensive Coverage**: Tests all major functionality including edge cases
- ✅ **Automatic Cleanup**: Properly cleans up test data and restores original state
- ✅ **Easy Execution**: Simple commands to run different types of tests

## Contributing

Feel free to fork this project and submit pull requests for any improvements or bug fixes.

**Before submitting a pull request, please ensure all tests pass:**
```bash
python run_tests.py all
```

## License

This project is open source and available under the MIT License. 