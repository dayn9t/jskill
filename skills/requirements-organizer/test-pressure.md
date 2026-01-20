# Pressure Test: Requirements Organizer Skill

## Test Scenario

**Context**: A user is working on an e-commerce project. They have some existing requirements scattered in different files, and during a conversation, they've mentioned several new requirement changes. The requirements are growing large and need to be reorganized.

## Existing Files (Before Test)

### File: `docs/requirements.md` (800 lines, mixed content)
```markdown
# E-Commerce Platform Requirements

## User Management
- Users can register with email
- Users can login
- Users can reset password

## Product Catalog
- Display products with images
- Search products by name
- Filter by category
- Sort by price

## Shopping Cart
- Add items to cart
- Update quantities
- Remove items
- Calculate total

## Payment
- Support credit card payment
- Support PayPal
- Generate invoice after payment
```

### File: `specs/api-requirements.txt` (200 lines)
```
API Endpoints needed:
- POST /api/users/register
- POST /api/users/login
- GET /api/products
- POST /api/cart/add
- POST /api/payment/process
```

## Conversation Changes (New Requirements)

During the conversation, the user mentioned:
1. "We need to add social login - Google and Facebook"
2. "The shopping cart should persist across sessions"
3. "Add wishlist functionality"
4. "Payment should also support Stripe and cryptocurrency"
5. "We need an admin panel to manage products"
6. "Add product reviews and ratings"
7. "Implement order tracking"
8. "Add email notifications for order status"
9. "Support multiple shipping addresses"
10. "Add coupon and discount code functionality"

## Expected Behavior WITHOUT Skill

**Predicted violations:**

1. **No systematic discovery** - Agent might miss existing files in different locations
2. **Incomplete extraction** - Agent might not capture all conversation changes
3. **Poor organization** - Agent might dump everything into one large file
4. **No size management** - Agent might create files exceeding 1000 lines
5. **Inconsistent structure** - Different modules might have different formats
6. **Missing cross-references** - No links between related modules
7. **No splitting strategy** - Even if file is too large, no intelligent splitting
8. **Rationalization**: "I'll just update the existing file" (ignoring modularization)
9. **Rationalization**: "I'll create one comprehensive document" (ignoring size limits)
10. **Rationalization**: "I'll organize by implementation order" (not by functional modules)

## Expected Behavior WITH Skill

**Compliant behavior:**

1. ✅ Searches for existing requirement files in multiple locations
2. ✅ Reads and analyzes all existing requirements
3. ✅ Extracts all 10 new requirements from conversation
4. ✅ Merges existing + new requirements
5. ✅ Organizes into functional modules (User Management, Product Catalog, Shopping Cart, Payment, Admin, Orders, Notifications)
6. ✅ Uses consistent structure for each module (Overview, Requirements, Implementation Notes, Acceptance Criteria, Dependencies)
7. ✅ Checks file sizes and splits if needed
8. ✅ Creates proper directory structure: `requirements/[module-name]/`
9. ✅ Adds cross-references between related modules
10. ✅ Creates root README.md with navigation
11. ✅ Reports what was organized and where files are located

## Test Execution Plan

### Phase 1: RED (Baseline without skill)
1. Create the existing files
2. Simulate conversation with requirement changes
3. Ask agent to "organize the requirements" WITHOUT invoking the skill
4. Document violations and rationalizations

### Phase 2: GREEN (With skill)
1. Reset to same initial state
2. Simulate same conversation
3. Invoke requirements-organizer skill
4. Verify compliant behavior

### Phase 3: REFACTOR (Close loopholes)
1. Identify any new rationalizations or shortcuts
2. Update skill to close those loopholes
3. Re-test to confirm fixes

## Success Criteria

The skill passes if:
- All existing requirements are discovered and preserved
- All conversation changes are captured
- Requirements are organized into logical modules
- No file exceeds 1000 lines
- Consistent structure across all modules
- Clear navigation between modules
- No rationalizations bypass the process
