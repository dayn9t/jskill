# Example Usage

This example demonstrates how the requirements-organizer skill transforms scattered requirements into structured documentation.

## Scenario

You're building a task management application. You have some existing requirements in a file, and during a conversation, several new requirements are mentioned.

## Before: Scattered Requirements

### Existing file: `docs/requirements.txt`
```
Task Management App Requirements

- Users can create tasks
- Users can mark tasks as complete
- Tasks have due dates
- Users can see a list of their tasks
```

### Conversation changes:
1. "Add the ability to assign tasks to team members"
2. "We need task priorities - high, medium, low"
3. "Add comments on tasks"
4. "Users should get email notifications for task assignments"
5. "Add a dashboard showing task statistics"

## After: Organized with Skill

### Structure created:
```
requirements/
├── README.md
├── task-management/
│   └── task-management.md
├── team-collaboration/
│   └── team-collaboration.md
├── notifications/
│   └── notifications.md
└── dashboard/
    └── dashboard.md
```

### Sample output: `requirements/task-management/task-management.md`

```markdown
# Task Management

## Overview
Core task management functionality allowing users to create, organize, and track tasks with priorities and due dates.

## Requirements

### Functional Requirements
- **REQ-TASK-001**: Users can create tasks
  - Acceptance: User can create a new task with title and description
  - Priority: High

- **REQ-TASK-002**: Users can mark tasks as complete
  - Acceptance: User can toggle task completion status, completed tasks are visually distinct
  - Priority: High

- **REQ-TASK-003**: Tasks have due dates
  - Acceptance: User can set and edit due dates, overdue tasks are highlighted
  - Priority: High

- **REQ-TASK-004**: Users can see a list of their tasks
  - Acceptance: User can view all their tasks in a list, with filtering options
  - Priority: High

- **REQ-TASK-005**: Tasks have priority levels (high, medium, low)
  - Acceptance: User can assign priority to tasks, tasks can be sorted by priority
  - Priority: Medium

## Implementation Notes

### Architecture Decisions
- Use database indexes on user_id and due_date for efficient querying
- Implement soft delete for tasks (mark as deleted rather than removing)

### Technical Constraints
- Task titles limited to 200 characters
- Task descriptions limited to 5000 characters
- Due dates must be in the future when created

### Data Models
- Task entity: id, user_id, title, description, due_date, priority, completed, created_at, updated_at

## Acceptance Criteria

- [ ] User can create a task with title, description, and due date
- [ ] User can mark task as complete/incomplete
- [ ] User can set task priority (high/medium/low)
- [ ] User can view list of all their tasks
- [ ] Tasks can be filtered by completion status
- [ ] Tasks can be sorted by due date or priority
- [ ] Overdue tasks are visually highlighted

## Dependencies

### Internal Dependencies
- Authentication module (for user identification)

### External Dependencies
- Database (PostgreSQL or similar)
- Date/time library for due date handling

## Change History

- 2026-01-20: Added priority levels requirement (REQ-TASK-005)
```

### Sample output: `requirements/README.md`

```markdown
# Task Management App - Requirements

## Overview
Requirements documentation for the task management application, organized by functional modules.

## Modules

### Core Functionality
- **[Task Management](task-management/task-management.md)** - Core task CRUD operations, priorities, due dates
- **[Team Collaboration](team-collaboration/team-collaboration.md)** - Task assignment, team member management, comments

### Supporting Features
- **[Notifications](notifications/notifications.md)** - Email notifications for task assignments and updates
- **[Dashboard](dashboard/dashboard.md)** - Task statistics and analytics visualization

## Quick Links

- [All Requirements by Priority](#)
- [Implementation Roadmap](#)
- [API Documentation](#)

## Change Log

- 2026-01-20: Initial requirements organization
  - Added team collaboration features
  - Added notification system
  - Added dashboard requirements
```

## Benefits

1. **Clear organization** - Requirements grouped by functional area
2. **Consistent structure** - Every module follows the same template
3. **Testable** - Acceptance criteria for every requirement
4. **Traceable** - Requirement IDs for tracking
5. **Maintainable** - Small files, easy to update
6. **Navigable** - README provides overview and links

## How to Invoke

In Claude Code:
```
User: I have some requirement changes. Can you organize them using the requirements-organizer skill?
```

Or simply describe your requirements and the skill will be invoked automatically when appropriate.
