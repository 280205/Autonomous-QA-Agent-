# Product Specifications - E-Shop Checkout

## Version: 1.0
## Last Updated: November 2025

---

## Overview
This document outlines the detailed product specifications for the E-Shop Checkout system. All features must comply with these specifications for proper functionality and user experience.

---

## Product Catalog

### Available Products
The checkout system supports the following products:

1. **Wireless Headphones**
   - Product ID: 1
   - Price: $79.99
   - Category: Electronics
   - Stock Status: In Stock

2. **Smart Watch**
   - Product ID: 2
   - Price: $199.99
   - Category: Electronics
   - Stock Status: In Stock

3. **Bluetooth Speaker**
   - Product ID: 3
   - Price: $49.99
   - Category: Electronics
   - Stock Status: In Stock

---

## Shopping Cart Functionality

### Add to Cart
- Users can add products to cart by clicking the "Add to Cart" button
- If a product already exists in the cart, quantity should be incremented by 1
- Maximum quantity per item: 99 units
- Minimum quantity per item: 1 unit

### Cart Management
- Users can modify quantities using the quantity input field
- Users can remove items from cart using the "Remove" button
- Cart should display: Product Name, Unit Price, Quantity, and Remove option
- Empty cart should display message: "Your cart is empty"

### Cart Calculations
- Subtotal = Sum of (Unit Price × Quantity) for all items
- Discount = Subtotal × (Discount Percentage / 100)
- Total = Subtotal - Discount + Shipping Cost

---

## Discount Code System

### Valid Discount Codes
The system supports the following discount codes:

1. **SAVE15**
   - Discount Type: Percentage
   - Discount Value: 15% off
   - Applicable To: Entire order subtotal
   - Case Sensitivity: Not case-sensitive (SAVE15, save15, Save15 all work)
   - Usage Limit: Unlimited uses
   - Expiry: No expiration

### Discount Application Rules
- Discount code must be entered in the discount code input field
- User must click "Apply Discount" button to activate the code
- Valid code message: "Discount code applied! 15% off your order."
- Invalid code message: "Invalid discount code."
- Empty code message: "Please enter a discount code."
- Discount is applied to the subtotal before adding shipping costs
- Only one discount code can be applied per order
- Discount cannot exceed the subtotal amount

---

## Shipping Methods

### Standard Shipping
- Cost: Free ($0.00)
- Delivery Time: 5-7 business days
- Default Selection: Yes
- Radio Button ID: shipping-standard

### Express Shipping
- Cost: $10.00
- Delivery Time: 1-2 business days
- Default Selection: No
- Radio Button ID: shipping-express

### Shipping Rules
- Shipping cost is added to the order total after discount
- User must select one shipping method (required)
- Changing shipping method should update total price immediately
- Express shipping adds exactly $10.00 to the order

---

## Payment Methods

### Supported Payment Methods

1. **Credit Card**
   - Payment Type: Credit/Debit Card
   - Default Selection: Yes
   - Radio Button ID: payment-credit
   - Processing: Simulated (no actual payment processing)

2. **PayPal**
   - Payment Type: PayPal Account
   - Default Selection: No
   - Radio Button ID: payment-paypal
   - Processing: Simulated (no actual payment processing)

### Payment Rules
- User must select one payment method (required)
- Payment method selection is mandatory for checkout
- No actual payment processing occurs (demonstration system)

---

## Customer Information Requirements

### Required Fields

1. **Full Name**
   - Field ID: customer-name
   - Type: Text
   - Validation: Cannot be empty
   - Error Message: "Name is required"

2. **Email Address**
   - Field ID: customer-email
   - Type: Email
   - Validation: Must be valid email format (contains @ and domain)
   - Error Message: "Please enter a valid email address"
   - Valid Examples: user@example.com, john.doe@company.co.uk
   - Invalid Examples: userexample.com, @example.com, user@

3. **Shipping Address**
   - Field ID: customer-address
   - Type: Textarea
   - Validation: Cannot be empty
   - Error Message: "Address is required"

### Optional Fields

1. **Phone Number**
   - Field ID: customer-phone
   - Type: Tel
   - Validation: None (optional field)

---

## Form Validation Rules

### Validation Trigger
- Validation occurs when user clicks "Pay Now" button
- Invalid fields should display error messages in red text
- Form should not submit if any required field is invalid
- User should remain on the page until all errors are corrected

### Validation Requirements
1. All required fields must be filled
2. Email must match valid email pattern
3. Cart must contain at least one item
4. One shipping method must be selected
5. One payment method must be selected

### Error Display
- Error messages appear below the respective input field
- Error messages are styled in red color (#f44336)
- Error messages are hidden by default
- Error messages become visible only when validation fails

---

## Order Submission

### Successful Order Conditions
All of the following must be true:
1. Cart contains at least one item
2. All required fields are filled with valid data
3. Email address is in valid format
4. Shipping method is selected
5. Payment method is selected

### Success Behavior
When all validation passes:
1. Display success message: "Payment Successful! Thank you for your order."
2. Success message should have green background (#4CAF50)
3. Success message should be prominently displayed
4. Form should be hidden after successful submission
5. Page should scroll to top to show success message

### Failure Behavior
When validation fails:
1. Display appropriate error messages for each invalid field
2. Keep user on the checkout page
3. Do not show success message
4. If cart is empty, show alert: "Your cart is empty. Please add items before checkout."

---

## Price Display Rules

### Currency Format
- All prices must be displayed in USD ($)
- Format: $XX.XX (always show two decimal places)
- Examples: $79.99, $0.00, $199.99

### Price Updates
Prices should update automatically when:
- Items are added to cart
- Item quantities are changed
- Items are removed from cart
- Discount code is applied
- Shipping method is changed

### Price Breakdown Display
The system must show:
1. Subtotal (sum of all items)
2. Discount amount (negative value or $0.00)
3. Shipping cost ($0.00 or $10.00)
4. Total (final amount to pay)

---

## User Interface Behavior

### Button States
- "Add to Cart" buttons should be clickable at all times
- "Apply Discount" button should be clickable at all times
- "Pay Now" button should be enabled at all times (validation on click)

### Interactive Elements
- Product cards should have hover effect (slight lift)
- Buttons should have hover effect (darker shade)
- Form inputs should show focus state (green border)

### Responsive Behavior
- Products section uses grid layout with auto-fit columns
- Minimum column width: 250px
- Maximum container width: 1200px
- Mobile-friendly responsive design

---

## Edge Cases and Special Scenarios

### Empty Cart
- When cart is empty, show message: "Your cart is empty"
- Do not allow checkout with empty cart
- Show alert message if user tries to pay with empty cart

### Invalid Quantity
- Quantities below 1 should not be accepted
- Quantities above 99 should not be accepted
- Non-numeric values should be rejected

### Discount Code Scenarios
- Applying discount multiple times should not multiply discount
- Invalid codes should not affect pricing
- Empty discount field should show appropriate message

### Form Submission
- Form should not submit on Enter key in text fields (default behavior)
- Submission only occurs via "Pay Now" button click
- Page should not reload on submission

---

## Technical Requirements

### Element IDs
All interactive elements have specific IDs for testing purposes:
- Product buttons: add-product-1, add-product-2, add-product-3
- Discount input: discount-code
- Discount button: apply-discount-btn
- Customer fields: customer-name, customer-email, customer-phone, customer-address
- Shipping radios: shipping-standard, shipping-express
- Payment radios: payment-credit, payment-paypal
- Submit button: pay-now-btn
- Success message: success-message

### Data Attributes
Products have the following data attributes:
- data-product-id: Unique identifier
- data-product-name: Product name
- data-product-price: Product price (numeric)

---

## Testing Scenarios

### Positive Test Cases
1. Add single product to cart and verify price calculation
2. Add multiple products and verify subtotal
3. Apply valid discount code SAVE15 and verify 15% discount
4. Select express shipping and verify $10 charge
5. Fill valid form and complete successful checkout
6. Change quantities and verify price updates

### Negative Test Cases
1. Submit form with empty required fields
2. Submit form with invalid email format
3. Apply invalid discount code
4. Attempt checkout with empty cart
5. Enter quantity below 1 or above 99

---

## Business Rules Summary

1. Discount code "SAVE15" provides exactly 15% off the subtotal
2. Express shipping costs exactly $10.00, Standard shipping is free
3. All prices must include exactly 2 decimal places
4. Email validation must enforce standard email format
5. Cart must have at least one item for checkout
6. Success message only appears when ALL validations pass
7. Error messages appear in red (#f44336)
8. Success elements appear in green (#4CAF50)
