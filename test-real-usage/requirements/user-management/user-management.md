# User Management

## Overview
Handles user registration, authentication, profile management, and user following functionality. Provides the foundational user system for the blog platform.

## Requirements

### Functional Requirements
- **REQ-USER-001**: Users can register with email and password
  - Acceptance: User can create account with valid email and password, receive confirmation
  - Priority: High

- **REQ-USER-002**: Users can login with credentials
  - Acceptance: Registered user can authenticate and access their account
  - Priority: High

- **REQ-USER-003**: Users can manage their profile
  - Acceptance: User can view and edit profile information (name, bio, avatar)
  - Priority: Medium

- **REQ-USER-004**: Users can follow other users
  - Acceptance: User can follow/unfollow other users, see list of followers and following
  - Priority: Medium

### Non-Functional Requirements
- **NFR-USER-001**: Passwords must be securely hashed
  - Acceptance: Passwords stored using bcrypt or similar with appropriate salt rounds
  - Priority: High

- **NFR-USER-002**: User sessions must be secure
  - Acceptance: Sessions use secure tokens, expire after inactivity
  - Priority: High

## Implementation Notes

### Architecture Decisions
- Use JWT tokens for session management
- Implement email verification for new registrations
- Store user relationships in separate following/followers table

### Technical Constraints
- Email must be unique across the system
- Username must be unique and alphanumeric
- Password minimum length: 8 characters

### Data Models
- User entity: id, email, username, password_hash, bio, avatar_url, created_at, updated_at
- UserFollow entity: follower_id, following_id, created_at

## Acceptance Criteria

- [ ] User can successfully register with email and password
- [ ] User can login with valid credentials
- [ ] User can edit their profile information
- [ ] User can follow another user
- [ ] User can unfollow a user
- [ ] User can view their followers list
- [ ] User can view their following list
- [ ] Passwords are securely hashed and never stored in plain text
- [ ] Sessions expire appropriately

## Dependencies

### Internal Dependencies
- None (foundational module)

### External Dependencies
- Email service for registration confirmation
- JWT library for token generation
- Password hashing library (bcrypt)

## Change History

- 2026-01-20: Added user following functionality (REQ-USER-004)
