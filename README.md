# Project Title: Shipment Management Program (PYTHON)

## Overview
This project is a **Shipment Management Program** developed for a group assignment for Programming with Python Module. Since then, it has been updated and reprogrammed by me as a solo project. It is designed to handle various logistics-related functionalities such as user account management, order placement, route selection, payment processing, and order tracking. The system aims to streamline logistics operations by providing a user-friendly interface for customers and administrators.

## Features
### User Features
1. **Account Management**:
   - Sign up for a new account.
   - Log in to an existing account.
   - Log out of the system.

2. **Order Management**:
   - Place new orders with customizable options (e.g., route, weight, fragile/hazardous items).
   - View order history.
   - Reorder previously placed orders.
   - Cancel orders.
   - Track the status of current orders.

3. **Feedback System**:
   - Submit feedback about the service.

4. **Payment Options**:
   - Choose from multiple payment methods: Credit/Debit Card, Bank Transfer, Cash on Delivery, UPI, or Mobile Wallets.

### Admin Features
1. Admin login (Username, Password) credentials are saved in the program.

2. Manage user accounts and monitor overall system performance.

### Logistics Operations
1. **Route Selection**:
   - Two predefined routes:
     - Route 1: Johor → Kuala Lumpur → Butterworth → Kedah → Perlis
     - Route 2: Johor → Kuala Lumpur → Terengganu → Kelantan

2. **Shipping Cost Calculation**:
   - Based on weight, distance (number of hubs), and additional surcharges for fragile or hazardous items.

3. **Order Processing**:
   - Assign unique order IDs.
   - Update order status (e.g., Pending, Completed).

4. **Data Storage**:
   - All data is stored in text files for simplicity and easy retrieval:
     - `userTxtFile.txt`: User accounts.
     - `ordersTxtFile.txt`: Active orders.
     - `cancelledOrdersTxtFile.txt`: Canceled orders.
     - `completedOrdersTxtFile.txt`: Completed orders.
     - Additional files for vehicles, drivers, journeys, revenue, etc.

## File Structure
- **Main Python Script**: Contains all the core functionalities such as user features, admin features, and utility functions.
- **Text Files**: Used for storing persistent data:
  - `userTxtFile.txt`: Stores user credentials and IDs.
  - `ordersTxtFile.txt`: Tracks ongoing orders.
  - `completedOrdersTxtFile.txt`: Logs completed orders.
  - `cancelledOrdersTxtFile.txt`: Logs canceled orders.
  - Other files for vehicles, drivers, journeys, fuel usage, revenue tracking, etc.

## How to Use
1. **For Users**:
   - Run the program and create a new account or log in with an existing one.
   - Navigate through the menu to place orders, track shipments, or provide feedback.

2. **For Admin**:
   - Log in using the admin credentials written in the program.
   - Access administrative functionalities to monitor and manage system operations.
     
2. **For Driver**:
   - Log in using the driver credentials given by the admin.
   - Access driver-related functionalities to carry out shipping operations.

## Key Functions
### User Features
- `user_features()`: Main entry point for user-related operations.
- `sign_up()`: Allows users to create new accounts.
- `place_order(userId)`: Facilitates placing a new order with detailed options like route and payment method.
- `view_order_history(userId)`: Displays the user's past orders.
- `reorder(userId)`: Enables reordering of previous shipments with the same details.
- `cancel_order(userId)`: Allows cancellation of active orders.

### Utility Functions
- `calculate_shipping_cost(order_data_str)`: Computes shipping costs based on weight, distance, and item type (fragile/hazardous).
- `choose_route()`: Guides users in selecting a valid route for their shipment.

## Future Enhancements
1. Implement a database system for better scalability and security instead of text files.
2. Add real-time tracking using GPS integration for shipments.
3. Expand route options and allow dynamic route creation by admins.
4. Introduce automated notifications (via email or SMS) for order updates.

## Authors
This project was originally developed by Group 32:
- Mi Yoonadi Mon (Main Developer)
- Felisha Khan
- Sharizad
