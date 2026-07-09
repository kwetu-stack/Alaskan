# ALASKAN SALES™
# Receipt-X POS
# V2 Production Playbook

Version: 2.0

---

# 1. Project Vision

ALASKAN SALES™ Receipt-X is a distributor-focused Point of Sale and receipt management system.

The goal is to replace manual receipt books with a controlled digital workflow while maintaining simplicity for invoicers.

The system must provide:

- Accurate receipts
- User accountability
- Product master control
- VAT compliance
- Receipt printing
- Sales reporting

---

# 2. Current Status

## V1 Training Version

Completed:

- Flask application
- Product master
- Supplier master
- Receipt creation
- Receipt items
- Product import from Excel
- Railway deployment
- Basic receipt printing workflow

Purpose:

Allow client staff to learn the system and provide feedback.

---

# 3. V2 Production Goals

The production version will introduce:

- User authentication
- Role-based access
- Receipt accountability
- VAT engine
- Improved receipt numbering
- Receipt history
- Reports
- Production-ready workflow

---

# 4. User Roles

## Administrator

Full system access.

Permissions:

- Manage users
- Manage products
- Manage suppliers
- View all receipts
- View reports
- Configure settings


## Invoicer

Limited operational access.

Initial users:

- BALOZI
- ERIC
- PRUDENCE
- TUVA

Permissions:

- Login
- Create receipts
- Print receipts
- View own receipts

---

# 5. Receipt Accountability

Every receipt must record:

- Receipt number
- Date
- Time
- Customer
- Sold By (logged-in invoicer)

The invoicer name must never be manually typed.

The system captures the logged-in user automatically.

---

# 6. Product Master V2

Product fields:

- Supplier
- Brand
- Variant
- Display Name
- Selling Price
- Tax Code
- VAT Rate
- Active Status

---

# 7. VAT System

Products will not be taxed by category.

Each product will have its own tax classification.

Example:

| Product | Tax Code | VAT |
|---|---|---|
| Cooking Oil | STANDARD | 16% |
| Cereals | EXEMPT | 0% |
| Sanitary Products | EXEMPT | 0% |

---

# 8. Receipt Numbering

New format:

Example:

R260708-0001

Structure:

R + Date + Daily Sequence

---

# 9. Receipt Printing

Printed receipt must show:

- Company details
- Receipt number
- Date
- Customer
- Sold By
- Items
- VAT
- Total

Footer:

Served by: USER NAME

---

# 10. Development Strategy

Development branch:

feature/receipt-x-v2-production

Testing process:

1. Build feature
2. Test locally
3. Test Railway deployment
4. Merge into main

---

# 11. Future Enhancements

- Payment methods
- Customer database
- Credit sales
- Stock management
- Sales reports
- Dashboard analytics