# Test Scenarios and Requirements

## Document Purpose
This document outlines recommended test scenarios for the E-Shop Checkout system to ensure comprehensive test coverage.

---

## Functional Test Scenarios

### Cart Management Tests

**TC-CART-001: Add Single Product to Cart**
- Action: Click "Add to Cart" for Wireless Headphones
- Expected: Product appears in cart with quantity 1, price $79.99
- Verify: Subtotal updates to $79.99

**TC-CART-002: Add Multiple Different Products**
- Action: Add Wireless Headphones, Smart Watch, and Bluetooth Speaker
- Expected: All three products appear in cart
- Verify: Subtotal = $79.99 + $199.99 + $49.99 = $329.97

**TC-CART-003: Add Same Product Multiple Times**
- Action: Click "Add to Cart" for Smart Watch three times
- Expected: Smart Watch quantity increases to 3
- Verify: Only one cart item for Smart Watch with quantity 3

**TC-CART-004: Update Quantity via Input Field**
- Action: Add product, then change quantity input to 5
- Expected: Quantity updates to 5
- Verify: Subtotal = unit_price × 5

**TC-CART-005: Remove Product from Cart**
- Action: Add product, then click "Remove" button
- Expected: Product is removed from cart
- Verify: Cart updates, subtotal recalculates

**TC-CART-006: Empty Cart After Removing All Items**
- Action: Remove all items from cart
- Expected: Message "Your cart is empty" appears
- Verify: Subtotal shows $0.00

---

### Discount Code Tests

**TC-DISC-001: Apply Valid Discount Code SAVE15**
- Precondition: Cart has items with subtotal $100
- Action: Enter "SAVE15" and click "Apply Discount"
- Expected: Message "Discount code applied! 15% off your order."
- Verify: Discount amount = $15.00 (15% of $100)
- Verify: Total = $100 - $15 + shipping

**TC-DISC-002: Apply Valid Code (Case Insensitive)**
- Action: Enter "save15" (lowercase)
- Expected: Code accepted, 15% discount applied
- Verify: Same result as SAVE15

**TC-DISC-003: Apply Invalid Discount Code**
- Action: Enter "INVALID" and click "Apply Discount"
- Expected: Message "Invalid discount code." in red
- Verify: No discount applied, prices unchanged

**TC-DISC-004: Apply Empty Discount Code**
- Action: Click "Apply Discount" with empty field
- Expected: Message "Please enter a discount code." in red
- Verify: No discount applied

**TC-DISC-005: Discount Applied to Subtotal Only**
- Precondition: Cart subtotal $100, Express shipping selected
- Action: Apply SAVE15
- Expected: Discount = $15 (15% of subtotal)
- Verify: Total = $100 - $15 + $10 (shipping) = $95

---

### Shipping Method Tests

**TC-SHIP-001: Default Shipping Selection**
- Action: Load page
- Expected: Standard Shipping is selected by default
- Verify: Shipping cost = $0.00

**TC-SHIP-002: Select Express Shipping**
- Action: Select "Express Shipping" radio button
- Expected: Shipping cost updates to $10.00
- Verify: Total increases by $10.00

**TC-SHIP-003: Switch Between Shipping Methods**
- Action: Select Express, then switch back to Standard
- Expected: Shipping cost updates accordingly
- Verify: Total recalculates correctly each time

**TC-SHIP-004: Express Shipping with Discount**
- Precondition: Cart subtotal $100, SAVE15 applied
- Action: Select Express shipping
- Expected: Total = $100 - $15 + $10 = $95
- Verify: Calculation order: subtotal → discount → shipping

---

### Form Validation Tests

**TC-FORM-001: Submit with All Valid Fields**
- Precondition: Cart has items
- Action: Fill all required fields with valid data, click "Pay Now"
- Expected: Success message appears
- Verify: "Payment Successful! Thank you for your order."

**TC-FORM-002: Submit with Empty Name**
- Action: Leave name field empty, fill others, click "Pay Now"
- Expected: Error message "Name is required" in red
- Verify: Form does not submit

**TC-FORM-003: Submit with Empty Email**
- Action: Leave email field empty, fill others, click "Pay Now"
- Expected: Error message "Please enter a valid email address"
- Verify: Form does not submit

**TC-FORM-004: Submit with Invalid Email Format**
- Action: Enter "invalidemail" (no @ or domain)
- Expected: Error message appears
- Verify: Email validation fails

**TC-FORM-005: Submit with Valid Email Formats**
- Test Cases:
  - user@example.com (valid)
  - john.doe@company.co.uk (valid)
  - test_user@domain.org (valid)
- Expected: All pass validation

**TC-FORM-006: Submit with Invalid Email Formats**
- Test Cases:
  - userexample.com (no @)
  - @example.com (no user)
  - user@ (no domain)
  - user @example.com (space)
- Expected: All fail validation

**TC-FORM-007: Submit with Empty Address**
- Action: Leave address field empty, fill others
- Expected: Error message "Address is required"
- Verify: Form does not submit

**TC-FORM-008: Submit with Empty Cart**
- Action: Fill form with no items in cart, click "Pay Now"
- Expected: Alert "Your cart is empty. Please add items before checkout."
- Verify: Form does not submit

**TC-FORM-009: Optional Phone Field**
- Action: Leave phone field empty, fill required fields
- Expected: Form submits successfully
- Verify: Phone is truly optional

---

### Payment Method Tests

**TC-PAY-001: Default Payment Method**
- Action: Load page
- Expected: Credit Card is selected by default
- Verify: Payment method radio button state

**TC-PAY-002: Select PayPal Payment**
- Action: Select "PayPal" radio button
- Expected: PayPal is selected
- Verify: Selection persists through form interaction

**TC-PAY-003: Payment Method in Checkout**
- Action: Select payment method, complete checkout
- Expected: Checkout succeeds regardless of payment method
- Verify: Both Credit Card and PayPal work

---

### Integration Tests

**TC-INT-001: Complete Purchase Flow - Standard Shipping**
- Steps:
  1. Add Wireless Headphones ($79.99)
  2. Apply discount code SAVE15
  3. Select Standard Shipping
  4. Fill customer information
  5. Select Credit Card payment
  6. Click "Pay Now"
- Expected Results:
  - Subtotal: $79.99
  - Discount: -$12.00 (15%)
  - Shipping: $0.00
  - Total: $67.99
  - Success message appears

**TC-INT-002: Complete Purchase Flow - Express Shipping**
- Steps:
  1. Add Smart Watch ($199.99) and Bluetooth Speaker ($49.99)
  2. Apply discount code SAVE15
  3. Select Express Shipping
  4. Fill customer information
  5. Select PayPal payment
  6. Click "Pay Now"
- Expected Results:
  - Subtotal: $249.98
  - Discount: -$37.50 (15%)
  - Shipping: $10.00
  - Total: $222.48
  - Success message appears

**TC-INT-003: Complete Purchase Flow - No Discount**
- Steps:
  1. Add all three products
  2. Do not apply discount
  3. Select Express Shipping
  4. Complete checkout
- Expected Results:
  - Subtotal: $329.97
  - Discount: $0.00
  - Shipping: $10.00
  - Total: $339.97

---

## Negative Test Scenarios

### Boundary Value Tests

**TC-BOUND-001: Minimum Quantity**
- Action: Set quantity to 0
- Expected: Value rejected or item removed

**TC-BOUND-002: Maximum Quantity**
- Action: Set quantity to 99
- Expected: Value accepted, calculation correct

**TC-BOUND-003: Exceed Maximum Quantity**
- Action: Attempt to set quantity to 100
- Expected: Value capped at 99 or rejected

**TC-BOUND-004: Negative Quantity**
- Action: Attempt to enter negative number
- Expected: Value rejected

---

### Error Handling Tests

**TC-ERR-001: Multiple Validation Errors**
- Action: Submit form with empty name, invalid email, empty address
- Expected: All three error messages appear
- Verify: Each error appears below its field

**TC-ERR-002: Apply Invalid Discount Multiple Times**
- Action: Apply invalid code, then try different invalid codes
- Expected: Error message updates each time
- Verify: No discount ever applied

**TC-ERR-003: Change Cart After Applying Discount**
- Action: Apply discount, then add more items
- Expected: Discount percentage remains but amount recalculates
- Verify: 15% discount applies to new subtotal

---

## UI/UX Test Scenarios

### Visual Validation Tests

**TC-UI-001: Product Card Hover Effect**
- Action: Hover over product card
- Expected: Card lifts up (translateY -5px), shadow appears
- Verify: Smooth transition (0.2s)

**TC-UI-002: Button Hover Effects**
- Test all buttons:
  - "Add to Cart" - green darkens
  - "Apply Discount" - blue darkens
  - "Remove" - red darkens
  - "Pay Now" - green darkens
- Expected: All show hover state

**TC-UI-003: Error Message Styling**
- Action: Trigger validation errors
- Expected: Error text in red (#f44336), font size 12px
- Verify: Appears below field with 5px margin-top

**TC-UI-004: Success Message Styling**
- Action: Complete successful checkout
- Expected: Green background (#4CAF50), white text, centered
- Verify: Page scrolls to top smoothly

**TC-UI-005: Price Display Format**
- Action: View all prices
- Expected: All show $ symbol with 2 decimal places
- Verify: Format: $XX.XX

---

### Responsive Design Tests

**TC-RESP-001: Products Grid on Mobile**
- Action: View on mobile screen (<768px)
- Expected: Products display in single column
- Verify: Cards stack vertically

**TC-RESP-002: Form on Mobile**
- Action: View form on mobile
- Expected: Full-width inputs, readable text
- Verify: No horizontal scrolling

**TC-RESP-003: Cart Items on Mobile**
- Action: View cart on small screen
- Expected: Cart items remain readable
- Verify: Layout adjusts appropriately

---

## Performance Tests

**TC-PERF-001: Price Calculation Speed**
- Action: Add/remove items, change quantities rapidly
- Expected: Prices update immediately (< 100ms)
- Verify: No lag or delay

**TC-PERF-002: Form Validation Speed**
- Action: Submit form
- Expected: Validation completes instantly
- Verify: Error messages appear immediately

---

## Accessibility Tests

**TC-ACCESS-001: Keyboard Navigation**
- Action: Navigate form using Tab key
- Expected: Logical tab order through all fields
- Verify: All interactive elements reachable

**TC-ACCESS-002: Focus States**
- Action: Tab to form inputs
- Expected: Green border appears on focus
- Verify: Focus visible on all inputs

**TC-ACCESS-003: Form Labels**
- Action: Review all form fields
- Expected: All inputs have associated labels
- Verify: Labels positioned above inputs

**TC-ACCESS-004: Required Field Indicators**
- Action: Review form
- Expected: Required fields marked with asterisk (*)
- Verify: Visual indication present

---

## Cross-Browser Compatibility Tests

**TC-BROWSER-001: Chrome Compatibility**
- Action: Test all functionality in Chrome
- Expected: All features work correctly

**TC-BROWSER-002: Firefox Compatibility**
- Action: Test all functionality in Firefox
- Expected: All features work correctly

**TC-BROWSER-003: Safari Compatibility**
- Action: Test all functionality in Safari
- Expected: All features work correctly

**TC-BROWSER-004: Edge Compatibility**
- Action: Test all functionality in Edge
- Expected: All features work correctly

---

## Security Tests (Client-Side)

**TC-SEC-001: XSS Prevention in Name Field**
- Action: Enter <script>alert('XSS')</script> in name
- Expected: Treated as plain text, no script execution

**TC-SEC-002: SQL Injection Prevention**
- Action: Enter SQL injection strings in form
- Expected: Treated as plain text (no backend, but good practice)

**TC-SEC-003: HTML Injection in Address**
- Action: Enter HTML tags in address field
- Expected: Displayed as plain text, not rendered

---

## Test Data Requirements

### Valid Test Data

**Customer Information:**
- Name: "John Doe", "Jane Smith", "Robert Johnson"
- Email: "john@example.com", "jane.smith@company.org"
- Phone: "+1-555-0123", "555-123-4567", ""
- Address: "123 Main St, Anytown, ST 12345"

**Discount Codes:**
- Valid: "SAVE15", "save15", "Save15", "SAVE15"
- Invalid: "SAVE10", "INVALID", "DISCOUNT", "TEST123"

### Invalid Test Data

**Email Formats:**
- "invalidemail" (no @ or domain)
- "@example.com" (no user)
- "user@" (no domain)
- "user @example.com" (space)

**Quantities:**
- -1 (negative)
- 0 (zero)
- 100 (exceeds max)
- "abc" (non-numeric)

---

## Test Execution Priority

**Priority 1 (Critical):**
- Cart functionality (add, update, remove)
- Price calculations (subtotal, discount, shipping, total)
- Form validation (all required fields)
- Discount code validation (SAVE15)
- Successful checkout flow

**Priority 2 (High):**
- Shipping method selection
- Payment method selection
- Email format validation
- Error message display
- Success message display

**Priority 3 (Medium):**
- UI hover effects
- Price format display
- Empty cart handling
- Optional field behavior

**Priority 4 (Low):**
- Browser compatibility
- Responsive design
- Accessibility features
- Performance optimization

---

## Automated Testing Recommendations

### Selenium Test Scripts Should Cover:
1. End-to-end checkout flow (happy path)
2. Form validation errors
3. Cart management operations
4. Discount code application
5. Price calculation verification
6. Shipping method selection
7. Error message validation

### Manual Testing Should Cover:
1. Visual appearance and styling
2. Responsive design on real devices
3. Browser compatibility
4. Accessibility with screen readers
5. User experience evaluation

---

## Expected Test Results Format

For each test case, document:
- Test ID
- Test Description
- Preconditions
- Test Steps
- Expected Result
- Actual Result
- Pass/Fail Status
- Screenshots (if applicable)
- Notes/Comments

---

## Regression Testing Checklist

After any code changes, verify:
- [ ] All products can be added to cart
- [ ] Cart calculations are correct
- [ ] SAVE15 discount code works
- [ ] Express shipping adds $10
- [ ] Standard shipping is free
- [ ] Form validation works for all fields
- [ ] Email validation is correct
- [ ] Empty cart shows correct message
- [ ] Success message appears on valid submission
- [ ] Error messages appear in red
- [ ] Prices display with 2 decimal places
- [ ] Page scrolls to top on success
