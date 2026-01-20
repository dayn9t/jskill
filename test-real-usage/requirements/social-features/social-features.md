# Social Features

## Overview
Provides social interaction features including comments, likes, and engagement functionality for blog posts.

## Requirements

### Functional Requirements
- **REQ-SOCIAL-001**: Users can comment on posts
  - Acceptance: User can add comments to any post, comments are displayed below the post
  - Priority: High

- **REQ-SOCIAL-002**: Users can like posts
  - Acceptance: User can like/unlike posts, like count is displayed
  - Priority: Medium

- **REQ-SOCIAL-003**: Users can edit their own comments
  - Acceptance: User can modify their own comments
  - Priority: Medium

- **REQ-SOCIAL-004**: Users can delete their own comments
  - Acceptance: User can remove their own comments
  - Priority: Medium

### Non-Functional Requirements
- **NFR-SOCIAL-001**: Comment loading must be efficient
  - Acceptance: Comments load within 1 second for up to 50 comments
  - Priority: Medium

## Implementation Notes

### Architecture Decisions
- Comments are threaded (can reply to comments)
- Likes are stored in separate table to track who liked what
- Real-time updates for new comments using WebSocket

### Technical Constraints
- Comment length limited to 2000 characters
- Users can only like a post once

### Data Models
- Comment entity: id, post_id, user_id, parent_comment_id, content, created_at, updated_at
- Like entity: id, post_id, user_id, created_at

## Acceptance Criteria

- [ ] User can add comment to a post
- [ ] User can like a post
- [ ] User can unlike a post
- [ ] Like count displays correctly
- [ ] Comments display in chronological order
- [ ] User can edit their own comments
- [ ] User can delete their own comments

## Dependencies

### Internal Dependencies
- User Management (for authentication)
- Content Management (for post association)

### External Dependencies
- WebSocket library for real-time updates

## Change History

- 2026-01-20: Initial creation with comments and likes functionality
