# Todo List Manager

A modern, feature-rich todo list application built with Python 3.13, Streamlit, and SQLite3. This application helps you manage tasks with intelligent priority scoring based on impact, tractability, and uncertainty factors.

## ✨ Key Features

### Core Task Management
- ✅ **Add Tasks**: Create new tasks with comprehensive details
- ✏️ **Inline Editing**: Edit tasks directly from any view with expandable forms
- 🗑️ **Delete Tasks**: Remove tasks with confirmation dialogs
- 🔍 **Advanced Search**: Multi-field search with real-time filtering
- ⚡ **Quick Add**: Instantly add tasks from the main view and navigate to full form

### Smart Organization
- 📊 **Priority Scoring**: Automatic score calculation using (Impact × Tractability) ÷ Uncertainty
- 📅 **Due Date Management**: Set and track due dates with visual indicators
- 🔄 **Status Tracking**: Full lifecycle management (Pending, In Progress, Completed, On Hold, Expired)
- 🎯 **Status Filtering**: Toggle visibility of different task statuses with checkboxes
- 📈 **Statistics Dashboard**: Real-time metrics and progress tracking

### Intelligent Automation
- ⏰ **Automatic Expiration**: Tasks older than 90 days are automatically marked as expired
- � **Expired Task Links**: Clickable links in expiration notifications for direct editing
- 🔍 **Smart Defaults**: Intelligent form defaults and session state management
- 💾 **Configurable Database**: Environment-aware database path resolution

### Enhanced User Experience
- 🚀 **Session Management**: Persistent UI state across interactions
- 📱 **Responsive Design**: Wide layout optimized for productivity
- 🎨 **Color-Coded Status**: Visual status indicators with distinct colors
- ⚡ **Quick Navigation**: Seamless transitions between views and actions
- 📋 **Done Today View**: Dedicated view for recently completed tasks with date range selection

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

## 🚀 Usage Guide

### Main Dashboard (View Tasks)
The primary interface provides comprehensive task management:

- **Task Display**: Expandable cards showing tasks sorted by priority score and due date
- **Status Filtering**: Use checkboxes to show/hide specific task statuses (Pending, In Progress, On Hold, Completed, Expired)
- **Quick Add**: Enter a task name in the quick add field and press Enter to navigate to the full add form
- **Inline Editing**: Each task expander includes a full edit form for immediate updates
- **Statistics**: Real-time metrics showing task counts, averages, and completion rates
- **Expired Task Notifications**: When tasks auto-expire, clickable links allow direct navigation to edit them

### Quick Search (Sidebar)
Powerful search functionality accessible from any view:

1. Enter search terms in the sidebar search field
2. Select search scope:
   - **All**: Search across topic, description, and status
   - **Topic**: Search only task titles
   - **Description**: Search only task descriptions  
   - **Status**: Search only task statuses
3. Press Enter or click Search to view results
4. Apply additional status filters to search results
5. Edit tasks directly from search results with inline forms

### Adding Tasks
**Method 1 - Quick Add:**
1. Type task name in the "Quick Add Task" field on main view
2. Press Enter to navigate to full form with pre-filled name

**Method 2 - Full Form:**
1. Select "Add Task" from sidebar navigation
2. Fill in all fields:
   - **Topic** (required): Task name/title
   - **Description**: Detailed task description
   - **Due Date**: Optional due date
   - **Status**: Initial status (defaults to Pending)
   - **Impact**: Importance rating (1-10, affects priority score)
   - **Tractability**: Ease of completion (1-10, affects priority score)
   - **Uncertainty**: Risk/uncertainty level (1-10, affects priority score)
3. Review calculated priority score
4. Click "Add Task" to save

### Editing Tasks
**Method 1 - Inline Editing (Recommended):**
- Expand any task card from View Tasks or Search Results
- Use the built-in edit form within the expander
- Make changes and click "Update Task"

**Method 2 - Dedicated Edit Page:**
- Select "Edit Task" from sidebar
- Choose task from dropdown or use direct navigation from expired task links
- Modify fields and save changes

### Done Today View
Track your recent accomplishments:

- Use the slider to select date range (1-31 days back)
- View all tasks completed within the selected timeframe
- See completion timestamps and task details
- Review completion statistics and insights
- Identify high-impact and high-scoring completed tasks

### Deleting Tasks
1. Navigate to "Delete Task" in sidebar
2. Select task from dropdown menu
3. Review task details in confirmation view
4. Click "🗑️ Delete Task" to permanently remove

## Priority Scoring System

The application uses a sophisticated scoring system to help prioritize tasks:

**Score = (Impact × Tractability) ÷ Uncertainty**

- **High Impact + High Tractability + Low Uncertainty** = High Priority
- **Low Impact + Low Tractability + High Uncertainty** = Low Priority

This scoring system helps you focus on tasks that are both important and achievable.

## 🤖 Intelligent Task Management

### Automatic Expiration System
The app includes sophisticated automatic task lifecycle management:

- **90-Day Auto-Expiration**: Tasks older than 90 days are automatically marked as "Expired"
- **Smart Filtering**: Only affects tasks that aren't already "Completed" or "Expired"
- **Interactive Notifications**: When tasks expire, you'll see a banner with clickable task links
- **Direct Navigation**: Click any expired task link to jump directly to its edit form
- **Status Control**: Expired tasks are hidden by default but can be toggled visible
- **Manual Override**: Easily change status back from "Expired" if tasks become relevant again

### Configurable Database Connection
Enterprise-ready database configuration with multiple fallback options:

1. **Explicit Path**: Pass database path directly to connection functions
2. **Session State**: Use `st.session_state["DB_PATH"]` for runtime configuration  
3. **Streamlit Secrets**: Configure via `st.secrets["DB_PATH"]` for deployment
4. **Environment Variable**: Set `TODO_DB_PATH` environment variable
5. **Default Fallback**: Uses `todo.db` in current directory

This flexible system supports development, testing, and production deployments.

## 💾 Database Architecture

The application uses SQLite3 with intelligent path resolution and automatic schema management:

- **Auto-Creation**: Database and tables are created automatically on first run
- **Local Storage**: All data stored locally on your machine for privacy and performance
- **Configurable Location**: Database path can be customized via multiple configuration methods
- **Schema Management**: Automatic table creation with proper constraints and indexes
- **Transaction Safety**: All database operations use proper transaction handling
- **Connection Pooling**: Centralized connection management through `connect_to_db()` function

### Database Schema
```sql
CREATE TABLE tasks (
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
);
```

## Requirements

- Python 3.13+
- Streamlit 1.28.1+
- Pandas 2.1.3+

## 📁 Project Structure

```
todo/
├── todo_app.py              # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # Documentation (this file)
├── todo.db                 # SQLite database (auto-created)
├── run_app.bat             # Windows batch file to run app
├── pytest.ini             # Pytest configuration
├── run_tests.py            # Comprehensive test runner
├── test_colors.py          # Color utility tests
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot configuration
├── tests/                  # Comprehensive test suite
│   ├── __init__.py         # Python package marker
│   ├── conftest.py         # Pytest fixtures and test database setup
│   ├── test_integration.py # End-to-end workflow tests
│   ├── test_database.py    # Database operations and integrity tests
│   └── test_calculations.py # Business logic and scoring tests
└── tmp/                    # Temporary files and development notes
    ├── blocked_tasks.md    # Development task tracking
    └── fixing_tests.md     # Test development notes
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