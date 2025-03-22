from datetime import date, datetime, timedelta
import random

# Pre-set all text file paths
user_file = "userTxtFile.txt"
vehicle_file = "vehicleTxtFile.txt"
feedbacks_file = "feedbacksTxtFile.txt"
orders_file = "ordersTxtFile.txt"
cancel_orders_file = "cancelledOrdersTxtFile.txt"
completed_orders_file = "completedOrdersTxtFile.txt"
drivers_file = "driverTxtFile.txt"
journeys_file = "journeysHistoryTxtFile.txt"
assigned_journeys_file = "assignedJourneysTxtFile.txt"
completed_journeys_file = "completedJourneysTxtFile.txt"
fuel_file = "fuelTxtFile.txt"
revenue_file = "revenueTxtFile.txt"
daily_roundtrips_file = "dailyRoundtripsTxtFile.txt"

# ADMIN INFO
mainAdminName = "adminName"
mainAdminPwd = "123456"

# TP081506's Task


def user_features():  # TODO:
  """
  Main Function of user features
  """
  loggedinUser = None

  while True:
    if not loggedinUser:
      print("\n--- Sign Up OR Log In ---")
      createAcc = get_valid_input("1: Log in\n2: Create new account\n0: Exit\n-> ", ["1", "2", "0"])
      if createAcc == "1":
        loggedinUser = login(user_file)
      elif createAcc == "2":
        sign_up()
      else:
        print("<< Exiting User Features. >>")
        break
    else:
      print(f"\n--- Users Features ({loggedinUser[0]}) ---\n")
      userFeatures = get_valid_input("1: Order Management\n2: Feedback \n0: Log Out\n-> ", ["1", "2", "0"])
      userId = loggedinUser[2].strip("\n")
      userName = loggedinUser[0].strip("\n")
      if userFeatures == "1":

        print("\n--- Users Features: Order Management features ---")
        orderFeatures = get_valid_input(
            "1: Place a new order\n2: View Order History\n3: Reorder\n4: Cancel order\n5: Track your orders\n0: Exit Order Management feature\n-> ",
            ["1", "2", "3", "4", "5", "0"])

        if orderFeatures == "1":
          print(f"\n--- Placing a new order for User Id ({userId}) ---")
          place_order(userId)
        elif orderFeatures == "2":
          print(f"\n--- {loggedinUser[0]}'s order history ---")
          view_order_history(userId)
        elif orderFeatures == "3":
          print(f"\n--- {loggedinUser[0]} ({userId})'s past order ---")
          reorder(userId)
        elif orderFeatures == "4":
          print("\n--- Cancelling an order ---")
          cancel_order(userId)
        elif orderFeatures == "5":
          print("\n--- Tracking order ---")
          track_order(userId)
        else:
          continue

      elif userFeatures == "2":
        print("\n--- Users Features: Feedback features ---")
        feedbacks(userName)
      else:
        print("<< Logged Out >>")
        loggedinUser = None


def is_username_available(username):
  """
  Check if the entered username already exists in the userTxtFile or not.
  """
  try:
    with open(user_file, "r") as userTxtFile:
      users = userTxtFile.readlines()
      for user in users:
        tempArr = user.split(",")
        if tempArr[0] == username:
          return False
    return True
  except FileNotFoundError:
    return True


def sign_up():
  """
  New user sign-up and create a new account
  """
  print("\n--- Creating new account ---")
  accCreated = False
  while accCreated != True:
    with open(user_file, "a+") as userTxtFile:
      print("<< Your username and password cannot be changed once created. >>")
      inputName = input("Enter your username (Press Enter to exit): ")
      if inputName == "":
        print("<< Exiting... >>")
        accCreated = True
      else:
        if is_username_available(inputName) == True:
          inputPwd = input("Enter your password: ")
          while len(inputPwd) < 6:
            inputPwd = input("Enter your password (Min 6-digit): ")
          random_num = f"{random.randint(0, 999):03d}"
          print(f"Your User ID: {inputName}{random_num}")
          userTxtFile.write(f"{inputName},{inputPwd},{inputName}{random_num}\n")
          accCreated = True
          print("\n<< --- Account Created. Please Log in. --- >>")
        else:
          print("<< Username already exists. Please choose a different username. >>")


def payment_options():
  """
  User choose a valid payment option
  """
  validOptions = [[1, "Credit/Debit Card"], [2, "Bank Transfer"],
                  [3, "Cash on Delivery"], [4, "UPI"], [5, "mobile wallets"]]
  for options in validOptions:
    print(f"{options[0]}: {options[1]}")
  choice = get_valid_input("Select your payment method: ", [
      "1", "2", "3", "4", "5"])  # Input with Validation

  # Map the selected choice to the payment method name
  selected_method = {str(option[0]): option[1]
                     for option in validOptions}[choice]
  print(f"You selected: {selected_method}. Payment setup is complete.")
  return selected_method


def choose_route():
  """
  User selects a route for the order
  """
  print("Please choose from two available routes:\n1. Route 1: Johor – Kuala Lumpur – Butterworth - Kedah – Perlis\n2. Route 2: Johor – Kuala Lumpur – Terengganu – Kelantan")
  print("<< If one or both of your desired locations aren't available, your ordering cannot be processed. >>")
  # User selects a route
  route_choice = get_valid_input("1. Route 1\n2. Route 2\n3: Exit\n-> ", ["1", "2", "3"])
  # Set hubs based on the selected route
  if route_choice == '1':
    hubs = ["Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis"]
  elif route_choice == '2':
    hubs = ["Johor", "Kuala Lumpur", "Terengganu", "Kelantan"]
  else:
    print("<< We sincererly apologise as your order cannot be made  at the moment. Exiting the ordering process... >>\n")
    return "", "", ""

  # Display available hubs for the selected route
  print("Available hubs for your selected route:")

  def select_location(prompt, validHubs):
    for index, hub in enumerate(validHubs, start=1):
      print(f"{index}. {hub}")
    while True:
      try:
        choice = int(input(prompt).strip())
        if 1 <= choice <= len(validHubs):
          return validHubs[choice - 1]  # Return the selected hub name
        else:
          print(f"Please enter a number between 1 and {len(validHubs)}.")
      except ValueError:
        print("<< Invalid input. Please enter a valid number. >>")

  # Get pickup and drop-off locations using the helper function
  pickupLocation = select_location(
      "Select item pick up location by entering the corresponding number: ", hubs)
  while pickupLocation == hubs[-1]:
    print("\n<< No valid drop-off locations available after your selected pickup location. >>")
    exit = input(
        "Press 0 to exit or 1 to select a different pick up location: ")
    if exit == "0":
      print("<< We sincererly apologise as your order cannot be made  at the moment. Exiting the ordering process... >>\n")
      return "", "", ""
    elif exit == "1":
      pickupLocation = select_location(
          "Select item pick up location by entering the corresponding number: ", hubs)

  pickup_index = hubs.index(pickupLocation)
  validDHubs = hubs[pickup_index + 1:]
  dropoffLocation = select_location(
      "Select item drop off location by entering the corresponding number: ", validDHubs)
  return route_choice, pickupLocation, dropoffLocation


def get_last_order_id(textfile):
  """
  Get the last order ID from the text file
  """
  try:
    with open(textfile, 'r') as fp:
      lines = [line.strip() for line in fp.readlines() if line.strip()]
      if not lines:
        return 0
      last_order_line = lines[-1].strip()
      order_details = last_order_line.split(',')
      return int(order_details[-1])

  except FileNotFoundError:
    return 0
  except IndexError:
    print("<< Error: Order details are incomplete. >>")
    return None
  except ValueError:
    print(f"{last_order_line, order_details}=>Error: Invalid data format for order ID.")
    return None


def calculate_shipping_cost(order_data_str):
  """
  Calculate the shipping cost based on the order data string
  """
  routes = {
      "1": {
          "hubs": ["Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis"],
          "distance_per_hub": 100  # Assuming each hub is 100 km apart
      },
      "2": {
          "hubs": ["Johor", "Kuala Lumpur", "Terengganu", "Kelantan"],
          "distance_per_hub": 100  # Assuming each hub is 100 km apart
      }
  }
  order_data = order_data_str.split(",")

  # Extracting only necessary order details
  weight = float(order_data[2])
  route_number = order_data[3]
  origin = order_data[4]
  destination = order_data[5]
  fragile = order_data[7] == 'y'
  hazardous = order_data[8] == 'y'

  # Get hub information for the selected route
  route_info = routes.get(route_number)
  if route_info is None:
    print(f"Price cannot be calculate. Invalid route: {route_number}. Valid routes are {list(routes.keys())}")
    return 0

  # Calculate number of hubs between origin and destination
  if origin in route_info['hubs'] and destination in route_info['hubs']:
    origin_index = route_info['hubs'].index(origin)
    destination_index = route_info['hubs'].index(destination)

    # Number of hubs traveled (excluding origin)
    number_of_hubs_traveled = abs(destination_index - origin_index)

    # Calculate total distance based on number of hubs
    total_distance = number_of_hubs_traveled * route_info['distance_per_hub']
  else:
    print(f"Origin or destination not found in route {route_number}")
    return 0

  # Cost factors
  base_cost_per_km_per_kg = 0.05
  fragile_surcharge = 10 if fragile else 0
  hazardous_surcharge = 20 if hazardous else 0

  # Calculate base shipping cost
  base_cost = weight * total_distance * base_cost_per_km_per_kg

  # Add surcharges if applicable
  total_cost = base_cost + fragile_surcharge + hazardous_surcharge

  return total_cost


def place_order(userId):
  """
  User place a new order and the order is added to the ordersTxtFile
  """
  while True:
    lastID = get_last_order_id(orders_file)
    if lastID == None:
      print("<< Order cannot be placed at the moment. Please try again later. >>\nReason: There's an error with orders text file.")
      break
    itemName = input("Enter shipping item's description: ").strip()
    while itemName == "":
      itemName = input("Item description cannot be empty. Please enter a valid item description: ").strip()
    while True:
      try:
        itemWeight = float(input("Enter item's weight: ").strip())
        float_weight = float(itemWeight)
        if 0 < float_weight <= 100:  # Weight Limit
          break
        print("<< Weight must be between 0 and 100 kg. >>")
      except ValueError:  # Ensure only numbers entry
        print("<< Please enter a valid number for weight. >>")

    routeChoice, pickupLocation, dropoffLocation = choose_route()
    if pickupLocation == "" or dropoffLocation == "":
      print("Order has not been placed successfully. Exiting the ordering process...")
      break

    orderDate = date.today()
    print("-- Extra information to inform the driver --")
    fragileItem = get_valid_input("Is the item fragile (y/n): ", ["y", "n"]).strip()
    hazardousItem = get_valid_input("Is the item hazardous (y/n): ", ["y", "n"]).strip()
    print("\n-- Payment Options ---")
    paymentOption = payment_options()

    # Confirm Order
    print("\nOrder Summary:")
    print(f"{'Item':<20} {'Weight (kg)':<12} {'Pickup':<15} {'Dropoff':<15} {'Fragile?':<12} {'Hazardous?':<12} {'Payment':<20} {'Shipping Status':<0}")
    print("=" * 150)
    print(f"{itemName:<20} {itemWeight:<12} {pickupLocation:<15} {dropoffLocation:<15} {'Yes' if fragileItem == 'y' else 'No':<12} {'Yes' if hazardousItem == 'y' else 'No':<12} {paymentOption:<20} {'Pending':<10}")

    # Example usage with the provided order data string
    order_data_str = f"{userId},{itemName},{itemWeight},{routeChoice},{pickupLocation},{dropoffLocation},{orderDate},{fragileItem},{hazardousItem},{paymentOption},Pending,{lastID + 1}"
    shipping_cost = calculate_shipping_cost(order_data_str)
    print(f"Shipping Cost: RM{shipping_cost:.2f}")

    confirm = get_valid_input("Confirm order? (y/n): ", ["y", "n"]).strip()

    if confirm == 'y':
      with open(orders_file, "a") as ordersTxtFile:
        ordersTxtFile.write(f"{userId},{itemName},{itemWeight},{routeChoice},{pickupLocation},{
            dropoffLocation},{orderDate},{fragileItem},{hazardousItem},{paymentOption},Pending,{lastID + 1}\n")
      print("Order placed successfully!")

      break
    elif confirm == 'n':
      retry = get_valid_input("Do you want to start over? (y/n): ", ["y", "n"]).strip()
      if retry != 'y':
        print("Order has not been placed successfully. Exiting the ordering process...")
        break


def view_order_history(userId):
  """
  Show users their respective order history
  """
  orders = read_file_contents(orders_file)
  userOrders = [order for order in orders if order.startswith(userId)]
  if not userOrders:
    print("No orders found for your User ID.")
  else:
    print(f"{'Order ID':<10} {'Item description':<20} {'Weight (kg)':<15} {'Origin':<15} {
        'Destination':<15} {'Order Date':<15} {'Payment Method':<20}")
    print("=" * 130)
    for order_line in userOrders:
      orderArr = order_line.split(',')
      print(f"{orderArr[-1]:<10} {orderArr[1]:<20} {orderArr[2]:<15} {orderArr[4]:<15} {orderArr[5]:<15} {orderArr[6]:<15} {orderArr[9]:<20}")
  rejected_orders = [o.split(',')[-1] for o in orders if o.startswith(userId) and o.split(',')[-2] == 'Rejected']
  print(f"Rejected Order ID(s): {', '.join(rejected_orders)}")
  input("Enter any key to continue: ")


def reorder(userID):
  """
  User can reorder past order with same choices
  """
  orders = read_file_contents(orders_file)
  userOrders = [order.strip() for order in orders if order.startswith(userID)]
  userOrdersID = [order.strip().split(',')[-1]
                  for order in orders if order.startswith(userID)]

  if not userOrdersID:
    print("No orders found for your User ID.")
    return

  print("Your Orders:")
  print(
      f"{'Order ID':<10} {'Item description':<20} {'Weight (kg)':<15} {'Origin':<15} {'Destination':<15} {'Payment Method':<10}")
  print("=" * 120)

  for order_line in userOrders:
    orderArr = order_line.split(',')
    print(
        f"{orderArr[11]:<10} {orderArr[1]:<20} {orderArr[2]:<15} {orderArr[4]:<15} {orderArr[5]:<15} {orderArr[9]:<10}")

  while True:
    try:
      selected_order = input(
          "Enter the number of the order to reorder (Press Enter to exit): ")
      if selected_order == '':
        break

      if not selected_order in userOrdersID:
        raise ValueError("Invalid order number.")

    except ValueError:
      print("Invalid Input. Please enter a valid order number.")
      continue

    print(f"Reordering Order ID {selected_order}...")

    confirm = get_valid_input("Confirm order? (y/n): ", ["y", "n", "Y", "N"]).strip()

    lastID = get_last_order_id(orders_file)

    if confirm.lower() == 'y':
      matching_order_line = None
      for order in userOrders:
        if order.split(',')[-1] == selected_order:
          matching_order_line = order
          break
      orderArr = matching_order_line.split(',')

      with open(orders_file, "a") as ordersTxtFile:
        ordersTxtFile.write(
            f"{orderArr[0]},{orderArr[1]},{orderArr[2]},{orderArr[3]},{orderArr[4]},{orderArr[5]},{date.today()},{orderArr[7]},{orderArr[8]},{orderArr[9]},Pending,{lastID + 1}\n")
        print("Reordering completed.")
    else:
      print("Reordering unsuccessful.")

    break  # Exit the loop after successful reordering


def cancel_order(userID):
  """
  User can choose one order to cancel
  """
  orders = read_file_contents(orders_file)
  userOrders = [
      order for order in orders
      if order.startswith(userID) and order.split(",")[-2] == "Pending"
  ]
  userOrdersID = [
      order.strip().split(',')[-1] for order in orders
      if order.startswith(userID) and order.split(",")[-2] == "Pending"
  ]

  if not userOrders:
    print("No orders found for your User ID that can be cancelled.\n")
    return

  # Display orders
  print(
      f"{'Order ID':<10} {'Item description':<20} {'Weight (kg)':<15} {'Origin':<15} {'Destination':<15} {'Order Date':<15} {'Payment Method':<10}")
  print("=" * 120)
  for order_line in userOrders:
    orderArr = order_line.split(',')
    print(
        f"{orderArr[11]:<10} {orderArr[1]:<20} {orderArr[2]:<15} {orderArr[4]:<15} {orderArr[5]:<15} {orderArr[6]:<15} {orderArr[9]:<10}")

  while True:
    try:
      print("\nTo prevent accidental cancelling, You may only cancel one order at a time.")
      selected_order = input(
          "Enter the number of a single Order ID to cancel (Press Enter to exit): ")

      if selected_order == '':
        break

      # Validate order number
      if not selected_order in userOrdersID:
        raise ValueError("Invalid order number.")

      # Get the specific order to cancel
      matching_order_line = None
      for order in userOrders:
        if order.split(',')[-1] == selected_order:
          matching_order_line = order
          break

      # Find and remove only the FIRST matching order
      remaining_orders = []

      for order in orders:
        if order == matching_order_line:
          # Write the cancelled order to cancelledOrdersTxtFile text file
          with open(cancel_orders_file, "a") as cancelled_orders_file:
            cancelled_orders_file.write(order + '\n')
          continue  # Skip adding this line to remaining_orders
        remaining_orders.append(order)

      # Write remaining orders back to file
      with open(orders_file, "w") as ordersTxtFile:
        for order in remaining_orders:
          ordersTxtFile.write(order + '\n')

      print("Order cancelled.")
      break

    except ValueError:
      print(f"Invalid Input.")
    except IndexError:
      print("Error: Invalid order number.")


def track_order(userId):
  """
  Allow user to track their orders
  """
  currentLocation = ""
  orders = read_file_contents(orders_file)
  completed_orders = read_file_contents(completed_orders_file)
  completed_orders_ids = [order.split(',')[-1] for order in completed_orders]
  user_completed_orders = [order for order in completed_orders if order.startswith(userId)]
  userOrders = [
      order for order in orders
      if order.startswith(userId) and order.split(",")[-2].lower() not in ["pending", "rejected", "dropped off"] and order.split(",")[-1] not in completed_orders_ids
  ]
  pendingOrdersCount = sum(
      1 for order in orders
      if order.startswith(userId) and order.split(",")[-2].lower() == "pending"
  )
  rejectedOrdersCount = sum(
      1 for order in orders
      if order.startswith(userId) and order.split(",")[-2].lower() == "rejected"
  )
  completededOrdersCount = len(user_completed_orders)
  print(f"\n<< You have {pendingOrdersCount} pending orders to be confirmed by admin. >>")
  print(f"<< You have {rejectedOrdersCount} orders that have been rejected by admin. >>")
  print(f"<< You have {completededOrdersCount} completed orders that have been dropped off and paid for. >>\n")
  if not userOrders:
    print("No orders to be tracked for your User ID.")
  else:
    print(f"{'Order ID':<10}{'Item description':<25}{'Current Location':<20}{'Destination':<15}{'Order Date':<15} {'Status':<10}")
    print("=" * 100)

    assignedJourneys = read_file_contents(assigned_journeys_file)

    # Prepare a list to hold assigned order IDs
    assignedOrderIDs = []

    for journey in assignedJourneys:
      journey_parts = journey.split(',')
      # Extracting assigned order IDs from each journey
      assignedOrderIDs.append(list(map(int, journey_parts[5:])))  # Convert to integers
    updated_orders = []
    notLoaded = []
    for order_line in userOrders:
      orderArr = order_line.split(',')
      status = orderArr[-2].lower()
      origin = orderArr[4]
      destination = orderArr[5]  # Destination location
      id = int(orderArr[-1])  # Convert ID from string to integer

      found = False

      # Check if this ID matches any of the assignedOrderIDs
      for i, assignedIDs in enumerate(assignedOrderIDs):
        if id in assignedIDs:
          driverJourney = assignedJourneys[i]  # Get corresponding journey
          driverLocation = driverJourney.split(
              ',')[3]  # Get driver's location
          route = int(driverJourney.split(',')[4])  # Get route

          # Set hubs based on route
          if route == 1:
            hubs = ["Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis"]
          elif route == 2:
            hubs = ["Johor", "Kuala Lumpur", "Terengganu", "Kelantan"]

          if driverLocation == "null":
            currentLocation = origin
          elif hubs.index(driverLocation) == hubs.index(origin):
            currentLocation = origin
            status = "Picked Up"  # Order has been picked up yet
          elif hubs.index(driverLocation) < hubs.index(origin):
            currentLocation = origin  # Order has not been picked up yet
            status = "In-progress"
          elif hubs.index(driverLocation) >= hubs.index(destination):
            currentLocation = destination
            status = "Dropped Off"  # Order has been dropped off

          found = True
          break

      if not found:
        print(f"{orderArr[11]:<10}{orderArr[1]:<25}{orderArr[4]:<20}{orderArr[5]:<15}{orderArr[6]:<15}{orderArr[10]:<10}")
        notLoaded.append(id)
        continue  # Skip this iteration or handle as needed

      print(f"{orderArr[11]:<10}{orderArr[1]:<25}{currentLocation:<20}{orderArr[5]:<15}{orderArr[6]:<15}{status.capitalize():<10}")
      # Update the status (assuming it's the second last element)
      orderArr[-2] = status.capitalize()
      updated_orders.append(",".join(orderArr))
    if notLoaded:
      print("\nAdditional Info:")
      for id in notLoaded:
        print(f"<< Order ID {id} has been confirmed but it has yet to be loaded onto a vehicle. >>")
    updated_orders_ids = [order.split(',')[-1] for order in updated_orders]
    with open(orders_file, 'w') as f:
      for line in orders:
        # Only update lines for this user
        if line.startswith(userId) and line.strip().endswith(tuple(updated_orders_ids)):
          f.write(updated_orders.pop(0) + "\n")  # Write updated line
        else:
          f.write(line + "\n")  # Write original line

  input("\nEnter any key to continue: ")


def feedbacks(userId):
  """
  User can give feedback and view others' feedbacks
  """
  feedbackOptions = get_valid_input("1: Give feedback\n2: View others' feedbacks.\n0: Exit feedback feature\n-> ", ["1", "2", "0"])

  if feedbackOptions == "1":
    username = input("Press Enter to give anonymous feedback: ")
    if username == "":
      username = "Anonymous"
    else:
      username = userId
    while True:
      try:
        rating = float(input("Please rate our service from 1 to 5: "))
        if 1 <= rating <= 5:
          break
        else:
          print("<< Rating must be between 1 and 5. >>")
      except ValueError:
        print("<< Invalid input. Please enter a number between 1 and 5. >>")

    while True:
      review = input(
          "Enter your reviews and give feedback for improvement: ").strip()
      if review:
        break
      else:
        print("<< Review cannot be empty. Please give us your feedback. >>")

      # Append feedback to file
    try:
      with open(feedbacks_file, "a") as feedbackFile:
        feedbackFile.write(f"{username},{rating},{review}\n")
        print("<< Thank you for your feedback! :) >>")
    except IOError:
      print("<< An error occurred while saving your feedback. Please try again. >>")

  elif feedbackOptions == "2":
    feedbackContents = read_file_contents(feedbacks_file)
    if feedbackContents:
      print("\nPrevious Ratings and Reviews:")
      for item in feedbackContents:
        name, rate, review = item.split(",")
        print(f"{name:<{15}}->\tRating: {rate:<5} || Review: {review}")
    else:
      print("\n<< No feedbacks available yet. :( >>")
    input("Enter any key to continue: ")
  else:
    return


# TP081967's Task
def driver_features():  # TODO:
  """
  Main Function of driver features
  """
  loggedIn = None
  driverFileCreated = None
  while True:
    driverFileCreated = read_file_contents(drivers_file)
    if driverFileCreated == []:
      print(f"<< Admin has not registered any drivers yet. Please try again later. >>")
      break
    print("\n--- Driver Features ---")
    # Call the function
    options = get_valid_input("1: Login\n0: Exit\n-> ", ["1", "0"])
    if options == "1":
      """Driver Features Entry Point."""
      while True:
        if not loggedIn:
          loggedIn = login(drivers_file)
          if loggedIn == None:
            exit = input("Enter 0 to exit log in: ")
            if exit == "0":
              break
        else:
          driverJourneys = journey_check(
              assigned_journeys_file, loggedIn)
          if driverJourneys != None:
            print("\nDriver Features Menu:")
            feature = get_valid_input(
                "1: Profile Management\n2: View Delivery Details\n3: Update Journey Status\n0: Log Out\n-> ",
                ["1", "2", "3", "0"])  # Input with Validation
            # Get the main feature selection

            if feature == "1":
              profile_management(loggedIn)

            elif feature == "2":
              display_freight_details(orders_file, driverJourneys)

            elif feature == "3":
              lastId = 0
              try:
                with open(journeys_file, 'r') as file:
                  for line in file:
                    values = line.strip().split(',')
                    # Check if there are 5 fields (indicating turnaround time is present)
                    if len(values) == 6:
                      lastId = values[-1]
              except FileNotFoundError:
                lastId = 0
              start_journey(driverJourneys, False, lastId)

            else:
              print("Logged Out.")
              loggedIn = None
              break
          elif driverJourneys == None:
            print(f"No journey has been assigned to {loggedIn[0]} yet.\n")
            feature = get_valid_input("1: Profile Management\n0: Log Out\n-> ",
                                      ["1", "0"])
            if feature == "1":
              profile_management(loggedIn)
            else:
              print("Logged Out.")
              loggedIn = None
              break
    else:
      print("Exiting driver features.")
      break


def journey_check(file_path, driverInfo):
  """
  Check journey assigned to driver
  """
  driverName = driverInfo[0]
  driverPwd = driverInfo[1]
  try:
    with open(file_path, "r") as TxtFile:
      data = TxtFile.readlines()
    if len(data) == 0:
      return None

    for line in data:
      activeData = line.strip().split(',')
      # Check if both driver name and password match
      if activeData[0] == driverName and activeData[1] == driverPwd:
        return activeData  # Return the matched data
    return None
  except FileNotFoundError:
    print("Admin has not assigned any journey yet.")
    return None


def display_driver_profiles(filename, loggedIn):
  """
  Display the driver profiles.
  """
  print(f"\n-- Viewing {loggedIn[0]}'s Profile --")
  try:
    with open(filename, "r") as file:
      for line in file:
        # Remove newline characters and split data by commas
        details = line.strip().split(",")
        driverName, pwd = details[:2]

        # Unpack the details (or use "Unknown" for missing data)
        username, pwd, contact_info, address, availability, license_status, health_issues = details

        # Display the profile in a readable format
        if loggedIn[0] == driverName and pwd == loggedIn[1]:
          print(
              f"Driver Username: {username}\nPassword: {pwd}\nContact Info: {contact_info if contact_info != "null" else "Not Provided"}\nAddress: {address if address != "null" else "Not Provided"}\nAvailability Status: {availability if availability != "null" else "Not Provided"}\nDriving License: {license_status if license_status != "null" else "Not Provided"}\nHealth Issues: {health_issues if health_issues != "null" else "Not Provided"}")
  except FileNotFoundError:
    print(f"Error: The file '{filename}' does not exist.")
  except Exception as e:
    print(f"An error occurred: {e}")


def edit_profile(profile):
  """
  Edit the driver's profile.
  """
  # Provide options for editing
  print("\nWhat do you want to edit?")

  fields = ["Name", "Password", "Contact Info", "Address",
            "Availability Status", "Driving License", "Health Issues"]
  driversData = read_file_contents(drivers_file)

  updated = False

  for i, line in enumerate(driversData):
    # Check if the line contains the profile details
    for item in line.split(","):
      # If the profile name matches (for example, profile[0] is the username)
      if profile[0] in item:
        print("\nProfile Found:")
        for j, field in enumerate(fields):
          value = profile[j] if profile[j] != "None" else "Not Set"
          print(f"-> {field}: {value}")

        print("\nWhat do you want to edit?")
        for j, field in enumerate(fields[2:], 1):
          print(f"{j}. {field}")

        try:
          choice = int(input("\nEnter your choice: "))
          if 1 <= choice <= len(fields) - 2:
            field_index = choice + 1
            new_value = input(f"Enter new value for {fields[field_index]}: ")
            profile[field_index] = new_value
            driversData[i] = ",".join(profile)  # Update the line in the file
            updated = True
            print(f"\n{fields[field_index]} updated successfully!")
          else:
            print("\nInvalid choice. Try again.")
        except ValueError:
          print("\nInvalid input. Please enter a number.")
        break

  if updated:
    with open(drivers_file, "w") as file:
      for data in driversData:
        file.write(f"{data}\n")


def check_driver_insurance_qualification(driver_info):
  """
  Check if a driver qualifies for insurance based on the provided information.
  """
  name = driver_info[0]
  age = int(driver_info[1])
  valid_license = driver_info[2]
  availability_status = driver_info[3]

  # Initialize qualification status
  qualifies = True
  reasons = []

  # Check age
  if age < 18:
    qualifies = False
    reasons.append("Driver must be at least 18 years old.")

  # Check valid license
  if not valid_license:
    qualifies = False
    reasons.append("Driver must have a valid driver's license.")

  # Check availability status
  if not availability_status:
    qualifies = False
    reasons.append("Driver must be available for driving.")

  # Insurance types qualified for if eligible
  insurance_types = []

  if qualifies:
    insurance_types = [
        "Standard Auto Insurance",
        "Full Coverage Insurance",
        "Personal Injury Protection (PIP)",
        "Uninsured/Underinsured Motorist Coverage",
        "Roadside Assistance"
    ]

  # Print the qualification result in a user-friendly format
  if qualifies:
    print(f"{name}, you qualify for insurance! Here are your options:")
    for insurance in insurance_types:
      print(f"- {insurance}")
  else:
    print(f"{name}, you do not qualify for insurance. Reasons:")
    for reason in reasons:
      print(f"- {reason}")


def profile_management(loggedIn):
  """
  Driver's Profile Management Features
  """
  while True:
    print("\nProfile Management Features")
    sub_feature = get_valid_input(
        "1: Edit Your Profile\n2: View Your Profile\n3: Check Your Insurance Status\n0: Exit Profile Management Features\n-> ",
        ["1", "2", "3", "0"])  # Input with Validation

    if sub_feature == "1":
      print(f"Editing {loggedIn[0]}'s Profile")
      display_driver_profiles(drivers_file, loggedIn)

      while True:
        edit_profile(loggedIn)
        another_edit = get_valid_input("\nDo you want to edit something else? (y/n): ", ["y", "n", "Y", "N"])
        # another_edit = input("\nDo you want to edit something else? (yes/no): ").strip().lower()
        if another_edit.lower() != "y":
          break

    elif sub_feature == "2":
      display_driver_profiles(drivers_file, loggedIn)
      input("Press ENTER to continue: ")

    elif sub_feature == "3":
      print("\n-- Driver's Insurance --")
      while True:
        age = input("Enter your age: ")
        try:
          age = int(age)
          if age <= 0:
            print("Invalid age. Age cannot be zero or negative.")
            continue
        except ValueError:
          print("Invalid input for age. Please enter a valid number.")
          continue
        break
      driver_info = [loggedIn[0], age]
      try:
        with open(drivers_file, "r") as file:
          for line in file:
            # Remove newline characters and split data by commas
            details = line.strip().split(",")
            driverName, pwd = details[:2]

            # Unpack the details (or use "Unknown" for missing data)
            username, pwd, contact_info, address, availability, license_status, health_issues = details

            # Display the profile in a readable format
            if loggedIn[0] == driverName and pwd == loggedIn[1]:
              driver_info.append(True if license_status != "null" else False)
              driver_info.append(True if availability != "null" else False)
      except FileNotFoundError:
        print(f"<< Error: The file for Driver Data does not exist. >>")
      except Exception as e:
        print(f"<< An error occurred: {e} >>")
      check_driver_insurance_qualification(driver_info)

    elif sub_feature == "0":
      print("Exiting Profile Management Features\n")
      break


def display_freight_details(filename, driverJourneys):
  """
  Display the freight details for each order in the driver's journey.
  """
  try:
    for i in driverJourneys[5:]:
      with open(filename, 'r') as file:
        for line in file:
          columns = line.strip().split(',')
          if len(columns) >= 12:  # Ensure all required columns are available
            if columns[11] == i:
              # Extract details from the columns
              description = columns[1]  # Second column (e.g., "Tablet", "Bed")
              weight = columns[2] + " kg"  # Third column (weight)
              is_fragile = "Yes" if columns[7].lower(
              ) == 'y' else "No"  # Fragile info
              is_hazardous = "Yes" if columns[8].lower(
              ) == 'y' else "No"  # Hazardous info

              # Display the freight details
              print(f"\nOrder {i}")
              print(f"-> Description: {description}")
              print(f"-> Weight: {weight}")
              print("-> Special requirement")
              print(f"-->Is the item fragile?: {is_fragile}")
              print(f"-->Is the item hazardous?: {is_hazardous}")
  except FileNotFoundError:
    print(f"Error: The file '{filename}' does not exist.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  input("Enter any key to continue: ")


def get_route_summary(driverJourneys):
  """
  Construct the route summary string
  """
  route_1 = "Johor – Kuala Lumpur – Butterworth – Kedah – Perlis"
  route_2 = "Johor – Kuala Lumpur – Terengganu – Kelantan"

  assigned_order_ids = driverJourneys[5:]
  route_assigned = route_2 if driverJourneys[4] == "2" else route_1

  if not assigned_order_ids:
    print("<< No journeys assigned to you yet. >>")
    return

  route_stops = route_assigned.split(" – ")
  pickUp = []
  dropOff = []

  try:
    for i in assigned_order_ids:
      with open(orders_file, 'r') as file:
        for line in file:
          columns = line.strip().split(',')
          if len(columns) >= 12:  # Ensure all required columns are available
            if columns[11] == i:
              pickUp.append([columns[4], i])
              dropOff.append([columns[5], i])
  except FileNotFoundError:
    print(f"Error: The file '{orders_file}' does not exist.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  formatted_stops = []

  # Iterate through the route stops to format them
  for stop in route_stops:
    drop_offs = [f"Order {do[1]}" for do in dropOff if do[0] == stop]
    pick_ups = [f"Order {pu[1]}" for pu in pickUp if pu[0] == stop]
    formatted_stop = stop

    if drop_offs:
      formatted_stop += f"(Drop off {', '.join(drop_offs)})"

    if pick_ups:
      formatted_stop += f"(Pick up {', '.join(pick_ups)})"

    formatted_stops.append(formatted_stop)

  output = " – ".join(formatted_stops)
  return output


def parse_route_summary(route_summary):
  """
  Split the route summary into parts
  """
  parts = route_summary.split('–')

  # Extract locations and actions
  locations = []
  actions = []

  for part in parts:
    part = part.strip()  # Remove leading/trailing whitespace
    # Check if there are any actions in parentheses
    if '(' in part and ')' in part:
      # Split on the first '(' only to get the location
      location = part.split('(')[0].strip()
      # Extract all actions within parentheses
      action_parts = part.split('(')[1:]  # Get everything after the first '('
      action_list = [ap.split(')')[0].strip()
                     for ap in action_parts]  # Extract actions
      action = ', '.join(action_list)  # Join actions with a comma
      locations.append(location)
      actions.append(action)
    else:
      locations.append(part)
      actions.append('')  # No action specified

  return locations, actions


def update_assigned_journeys(file_path, driver_journeys):
  """
  Update the assigned journeys file
  """
  driver_name = driver_journeys[0]
  vehicle_id = driver_journeys[2]

  with open(file_path, 'r') as file:
    lines = file.readlines()

  # Remove blank lines
  lines = [line for line in lines if line.strip()]

  # Update the matching line
  for i in range(len(lines)):
    # Assuming the first element in each line is the driver's name and vehicle ID is somewhere in the line
    if driver_name in lines[i] and vehicle_id in lines[i]:
      # Split the line by commas and update the location
      current_line = lines[i].strip().split(',')
      current_line[3] = driver_journeys[3]  # Update location to update
      # Join the updated line back into a string
      lines[i] = ','.join(current_line) + '\n'
      break  # Exit after updating the first matching line

  # Write the updated content back to the file
  with open(file_path, 'w') as file:
    file.writelines(lines)


def get_end_location(routeArray):
  """
  Get the end location from the route summary
  """
  locations = routeArray[0]  # First list contains locations
  actions = routeArray[1]  # Second list contains actions

  # Start from the end of the actions list and find the last action
  for i in range(len(actions) - 1, -1, -1):
    if actions[i]:
      return locations[i]
  return locations[-1]


def start_journey(driverJourneys, maintain, lastId):

  stopover_time_min = 10  # Fixed Stopover Time for all state hubs
  travel_time_min = 20  # Fixed Travel Time one hub to the next

  journeyEnd = False
  current_location = driverJourneys[3]
  route_summary = get_route_summary(driverJourneys)

  routeArray = parse_route_summary(route_summary)
  end_hub = get_end_location(routeArray)

  stopover_hub = 1  # Initialize stopover_hub
  journey_found = False
  updated_lines = []
  # Check if the history file exists and read the stopover count
  try:
    with open(journeys_file, 'r') as file:
      for line in file:
        line = line.strip()  # Remove leading and trailing whitespace
        if line:  # Only process non-empty lines
          data = line.split(',')

          if data[0] == driverJourneys[0] and data[1] == driverJourneys[1] and data[2] == driverJourneys[2]:
            if len(data) < 5:
              # Get the stopover_hub from the file
              stopover_hub = int(data[3]) + 1
              journey_found = True
              # Update the entry with the new stopover count
              updated_lines.append(f"{data[0]},{data[1]},{data[2]},{stopover_hub}\n")
          else:
            updated_lines.append(line + '\n')
  except FileNotFoundError:
    print("<< Journey history file not found. Starting a new journey. >>")
  while journeyEnd == False:
    print("\n--- Your Shipment Journey ---")
    startDelivering = None

    print(f"Route Summary: {route_summary}")

    if current_location == "null" and not journey_found:
      roundTrips = read_file_contents(daily_roundtrips_file)

      # Two round trips using Route 1 and one round trip using Route 2
      today_date = datetime.now().strftime('%Y-%m-%d')
      max_route1_trip = 2
      max_route2_trip = 1
      route1_trip_count = len([trip for trip in roundTrips if trip.startswith(today_date) and trip.endswith(',1')])
      route2_trip_count = len([trip for trip in roundTrips if trip.startswith(today_date) and trip.endswith(',2')])
      maxTrip = True
      print(f"\n<< You've been assigned to deliver orders using Route {driverJourneys[4]} today. >>")
      if driverJourneys[4] == '1':
        print(f"Max round trips using Route {driverJourneys[4]} each day: {max_route1_trip}, Total round trips made on {today_date}: {route1_trip_count}\n")
        if route1_trip_count < max_route1_trip:
          maxTrip = False
      elif driverJourneys[4] == '2':
        print(f"Max round trips using Route {driverJourneys[4]} each day: {max_route2_trip}, Total round trips made on {today_date}: {route2_trip_count}\n")
        if route2_trip_count < max_route2_trip:
          maxTrip = False
      if maxTrip == True:
        print("<< Maximum round trips reached for today. No more journey can be made on this route. >>")
        return
      startDelivering = get_valid_input("1: Start Journey\n0: Exit\n-> ", ["1", "0"])
      if startDelivering == "0":
        break
      with open(journeys_file, 'a') as file:
        initial_data = f"{driverJourneys[0]},{driverJourneys[1]},{driverJourneys[2]},{stopover_hub}\n"
        file.write(initial_data)
      print("<< Starting your journey... >>")

      with open(daily_roundtrips_file, "a") as file:
        today_date = datetime.now().strftime("%Y-%m-%d")
        # Append to the file
        file.write(f"{today_date},{driverJourneys[4]}\n")

      current_location = routeArray[0][0]
      driverJourneys[3] = current_location
      update_assigned_journeys(assigned_journeys_file, driverJourneys)
      print(f"Journey started at {current_location}!")
      if routeArray[1][0] != "":
        print(f"{routeArray[1][0]} at {routeArray[0][0]}")
      break
    elif current_location != end_hub:
      if current_location in routeArray[0]:
        current_index = routeArray[0].index(current_location)
        # Iterate through hubs starting from the next hub
        for next_hub in routeArray[0][current_index + 1:]:
          print(f"Your current location: {current_location}")
          input(f"Press Enter when you arrive at {next_hub}...")
          driverJourneys[3] = next_hub  # Update current hub in driverJourneys
          update_assigned_journeys(assigned_journeys_file, driverJourneys)
          # stopover_hub += 1  # Increment stopover_hub
          with open(journeys_file, 'r') as file:
            existing_lines = file.readlines()
          with open(journeys_file, 'w') as file:
            for index, line in enumerate(existing_lines):
              if line.startswith(f"{driverJourneys[0]},{driverJourneys[1]},{driverJourneys[2]},"):
                if index == len(existing_lines) - 1:
                  file.write(f"{driverJourneys[0]},{driverJourneys[1]},{
                      driverJourneys[2]},{stopover_hub}\n")
                else:
                  file.write(line)
              else:
                file.write(line)

          if routeArray[1][routeArray[0].index(next_hub)] != "":
            print(
                f"{routeArray[1][routeArray[0].index(next_hub)]} at {next_hub}")
          break
        break
    elif current_location == end_hub:
      print("<< You've reached the end of your journey. >>\n<< All data will be updated accordingly... >>")

      journeyEnd = True
    else:
      print("<< An error occured. >>")
      break
  while journeyEnd == True:
    # Flag to check if turnaround time has been added
    turnaround_time_added = False
    last_matching_line = None
    with open(journeys_file, 'r') as file:
      for line in file:
        if line.startswith(f"{driverJourneys[0]},{driverJourneys[1]},{driverJourneys[2]},"):
          last_matching_line = line.strip()
    if last_matching_line is not None:
      values = last_matching_line.split(',')
      if len(values) == 5:
        print("<< Trip log is completed. Turnaround time has already been added and maintenance is completed. >>\n")
        turnaround_time_added = True
        break  # Exit the for loop since we found the entry
      else:
        shippingOrderId = driverJourneys[5:]

        with open(orders_file, 'r') as file:
          orders = file.readlines()

        # Step 2: Find and process each order ID
        completed_orders = []
        processed_order_ids = set()

        for order_id in shippingOrderId:
          for order in orders:
            # Split the line into components
            components = order.strip().split(',')
            # Check if the last element matches the current order ID
            if components[-1] == order_id:
              # Prepare the order data string
              components[-2] = "Dropped Off"
              order_data_str = ','.join(components)
              cost = calculate_shipping_cost(order_data_str)
              # Write to revenueTxtFile only if not already processed
              if order_id not in processed_order_ids:
                with open(revenue_file, 'a') as revenueFile:
                  revenueFile.write(f"{components[-1]},{cost}\n")
                print(f"-> Added the cost of Order ID {order_id} (RM{
                    cost}) to {revenue_file}.")
                processed_order_ids.add(order_id)
              completed_orders.append(order_data_str)
        with open(completed_orders_file, 'a') as file:
          for order_data in completed_orders:
            file.write(f"{order_data}\n")
            print(f"-> Added completed order ({order_data}) to {completed_orders_file}.")

        updated_assigned_journeys = []
        completed_journeys = []
        updated_vehicles = []
        journeys = read_file_contents(assigned_journeys_file)
        vehicles = read_file_contents(vehicle_file)

        for journey in journeys:

          # Split the line into components
          journey_components = journey.strip().split(',')
          if driverJourneys == journey_components:
            completed_journeys.append(journey.strip() + "\n")
          else:
            updated_assigned_journeys.append(journey + "\n")

        # Write updated journeys back to assignedJourneysTxtFile
        with open(assigned_journeys_file, 'w') as file:
          for updated_journey in updated_assigned_journeys:
            file.write(updated_journey)

        # Write completed journeys to completedJourneysTxtFile
        with open(completed_journeys_file, 'a') as file:
          for completed_journey in completed_journeys:
            print(f"\n<< Journey completed: {completed_journey} >>\n")
            file.write('\n' + completed_journey)

        for vehicle in vehicles:
          vehicle_components = vehicle.strip().split(',')
          if driverJourneys[2] == vehicle_components[0]:
            updated_vehicle = ','.join(vehicle_components[:7])
            updated_vehicles.append(updated_vehicle)
          else:
            updated_vehicles.append(vehicle.strip())

        with open(vehicle_file, 'w') as file:
          for updated_vehicle in updated_vehicles:
            file.write(updated_vehicle + '\n')

        # Calculate Turnaround Time and add it in journetsHistoryTxtFile
        a_stopover_hub = int(values[3])
        final_stopover_hub = a_stopover_hub - 1  # Adjust for zero-based index
        turnaround_time = ((final_stopover_hub *
                           (stopover_time_min + travel_time_min)) * 2) - stopover_time_min
        # Update journeys_history_file with turnaround time
        updated_lines_with_turnaround = []

        with open(journeys_file, 'r') as file:
          lines = file.readlines()
        for index, line in enumerate(lines):
          line = line.strip()
          if index == len(lines) - 1:
            updated_line = f"{line},{turnaround_time},{int(lastId) + 1}\n"
            updated_lines_with_turnaround.append(updated_line)
          else:
            updated_lines_with_turnaround.append(line + '\n')
        # Write back all lines including the updated one with turnaround time
        with open(journeys_file, 'w') as file:
          file.writelines(updated_lines_with_turnaround)

        if maintain != True:
          print("<< Please perform maintenance at the end of your journey >>")
          maintain = maintenance_features(driverJourneys)
        else:
          print("<< Maintenance completed >>")
        break  # Exit the for loop after processing

    if turnaround_time_added:
      break  # Exit the while loop if turnaround time has already been added


def maintenance_features(driverJourneys):
  """
  Handles Maintenance Features with sub-options.
  """
  while True:
    print("\nMaintenance Features:\n")
    print("Performing Safety and Cleaning Checks... ")
    input("Press any key when checking is complete: ")
    print("<< Safey and Cleaning check completed! >>")
    print("\nRefuelling... ")

    def is_valid_number(value):  # Validate fuel quantity
      try:
        num = float(value)
        return num > 0  # Ensure it's a positive number
      except ValueError:
        return False  # Not a valid number
    while True:
      fuel_quantity = input("Enter Fuel Quantity (in liters): ").strip()
      fuel_cost = input("Enter total cost of fuel (RM): ").strip()
      if not is_valid_number(fuel_quantity):
        print("Invalid input for fuel quantity. Please enter a positive number.")
        continue
      # Validate fuel cost
      if not is_valid_number(fuel_cost):
        print("Invalid input for fuel cost. Please enter a positive number.")
        continue
      break
    try:
      with open(fuel_file, "a") as fuelTxtFile:
        fuelTxtFile.write(f"{driverJourneys[2]},{fuel_quantity},{fuel_cost}\n")
        print("<< Refueling completed! :) >>")
    except IOError:
      print("<< An error occurred. Please try again later. >>")
      return False
    return True


# TP081763's Task
def admin_features():  # TODO:
  """
  Main Function of admin features
  """
  loggedin = None

  while True:
    if not loggedin:
      print("\n--- Log in to access Admin Features ---\n")
      options = get_valid_input("1: Login\n0: Exit\n-> ", ["1", "0"])
      if options == "1":
        username_input = input("Enter your username: ")
        password_input = input("Enter your password: ")
        if username_input == mainAdminName and password_input == mainAdminPwd:
          print("Log In Successful!")
          loggedin = True
        else:
          print("Invalid Username or Password. Please try again.")
      elif options == "0":
        print("<< Exiting Admin Features. >>")
        break
    else:
      print(f"\n--- Admin Features ({mainAdminName.upper()}) ---\n")
      admin_features = get_valid_input(
          "1: Vehicle Management and Maintenance\n"
          "2: Load orders on vehicles\n"
          "3: Manage Fuel & Vehicle Consumption\n"
          "4: Driver Management\n"
          "5: Reports\n"
          "0: Log Out\n-> ",
          ["1", "2", "3", "4", "5", "0"]
      )
      if admin_features == "1":
        manage_vehicles(vehicle_file)
      elif admin_features == "2":
        print("-- Loading Orders --")
        load_orders()
      elif admin_features == "3":
        manage_fuel_and_consumption(fuel_file)
      elif admin_features == "4":
        driver_management(drivers_file, assigned_journeys_file)
      elif admin_features == "5":
        menu_generate_reports()
      elif admin_features == "0":
        loggedin = None
        print("<< Logged Out. >>")


def manage_vehicles(vehicle_file):
  """
  Vehicle Management and Maintenance Features
  """
  while True:
    print("\n--- Vehicle Management and Maintenance ---\n")
    choice = get_valid_input(
        "1: Add Vehicle\n2: Edit Vehicle Details\n3: View All Vehicle Details\n4: Maintenance Alerts\n5: Inspection Alerts\n6: Edit Inspection and Maintenance Details\n0: Back to Admin Menu\n-> ",
        ["1", "2", "3", "4", "5", "6", "0"])

    if choice == "1":
      add_vehicle(vehicle_file)
    elif choice == "2":
      edit_vehicle(vehicle_file)
    elif choice == "3":
      view_vehicle_details(vehicle_file)
    elif choice == "4":
      maintenance_alerts(vehicle_file)
      input("Enter any key to continue: ")
    elif choice == "5":
      inspection_alerts(vehicle_file)
      input("Enter any key to continue: ")
    elif choice == "6":
      print("\n--- Editing Maintenance and Inspection Details ---")
      schedule_maintenance_inspection(vehicle_file)
    elif choice == "0":
      print("Returning to Admin Menu.")
      break


def load_orders():
  """
  Load orders on vehicles
  """
  print("--- Confirming Orders and Assigning Vehicles ---")
  activeOrderID = []
  loadedOrderID = []
  orderToProcess = []
  assignedOrderID = []
  failedOrderID = []
  orders = read_file_contents(orders_file)
  vehicleData = read_file_contents(vehicle_file)
  availableVehicles = []
  for o in orders:
    order = o.split(',')
    if order[10].lower() == "pending":
      activeOrderID.append(order[-1])
  for v in vehicleData:
    vehicle = v.split(',')
    if len(vehicle) > 7:
      loadedOrderID.extend(vehicle[7:])
    else:
      availableVehicles.append(v)
  for a in activeOrderID:
    if a not in loadedOrderID:
      orderToProcess.append(a)
  print(f"All Order IDs        : {activeOrderID}")
  print(f"Confirmed Order IDs  : {loadedOrderID}")
  print(f"Processing Order IDs : {orderToProcess}")
  for p in orderToProcess:
    for o in orders:
      order = o.split(',')
      if order[-1] == p:
        weightOK = False
        RouteOK = False
        SpecialOK = False
        print(f"\nOrder ID {p} is being processed...")
        for vehicle in availableVehicles:
          data = vehicle.split(',')
          if float(order[2]) < float(data[2]):
            weightOK = True
            if order[3] == data[3]:
              RouteOK = True
              if order[7] == 'y' or order == 'y':
                if data[4] == 'y':
                  SpecialOK = True
                  vehicleID = vehicle.split(',')[0]
                  assignedOrderID.append([p, vehicleID])
                  break
              else:
                if data[4] == 'n':
                  SpecialOK = True
                  vehicleID = vehicle.split(',')[0]
                  assignedOrderID.append([p, vehicleID])
                  break

        # print(f"Order ID {p}'s weight: {weightOK}, route: {RouteOK}, special: {SpecialOK}.")
        if weightOK == True and RouteOK == True and SpecialOK == True:
          print(f"Order ID {p} has been assigned to {assignedOrderID[-1][1]}.")
        else:
          failedOrderID.append(p)
          print(f"Order ID {p} has not been assigned.")
          if weightOK != True:
            print(f"<< No vehicle available to accommodate Order ID {
                p}'s weight. >>")
          elif RouteOK != True:
            print(f"<< No vehicle available to accommodate Order ID {
                p}'s selected route. >>")
          elif SpecialOK != True:
            print(f"<< No vehicle available to accommodate Order ID {
                p}'s special requirements. >>")
  assigned_ids = {order[0] for order in assignedOrderID}
  print(f"\nAssigned order: {assignedOrderID}")
  print(f"Rejected order: {failedOrderID}")
  if failedOrderID:
    print("<< Some orders could not be assigned due to lack of suitable vehicle. Please add a new vehicle. >>")

  # Create a dictionary to hold order numbers for each vehicle ID
  order_dict = {}

  # Populate order_dict with assigned orders
  for order in assignedOrderID:
    order_number, vehicle_id = order
    if vehicle_id not in order_dict:
      order_dict[vehicle_id] = []
    order_dict[vehicle_id].append(order_number)

  # Update vehicle_data by appending order numbers to relevant entries
  updated_vehicle_data = []
  for line in vehicleData:
    parts = line.strip().split(',')
    vehicle_id = parts[0]

    if vehicle_id in order_dict:
      parts.extend(order_dict[vehicle_id])

    updated_vehicle_data.append(','.join(parts))

  # Write the updated data back to the file
  with open(vehicle_file, 'w') as file:
    for line in updated_vehicle_data:
      file.write(line + '\n')

  # Update orders data based on assigned order IDs
  updated_orders_data = []
  for line in orders:
    parts = line.strip().split(',')
    order_id = parts[-1]  # Get the last item (order ID)

    # Check if the order ID is in the assigned or failed IDs
    if order_id in assigned_ids:
      parts[-2] = 'Confirmed'
    elif order_id in failedOrderID:
      parts[-2] = 'Rejected'
    updated_orders_data.append(','.join(parts))

  # Write the updated data back to the file
  with open(orders_file, 'w') as file:  # Change this path as needed
    for line in updated_orders_data:
      file.write(line + '\n')
  input("Enter any key to continue: ")


def is_valid_date(date_str):
  """
  Check if the provided date string is in YYYY-MM-DD format.
  """
  if len(date_str) != 10:
    return False
  year, month, day = date_str.split('-')
  return (year.isdigit() and month.isdigit() and day.isdigit() and
          len(year) == 4 and len(month) == 2 and len(day) == 2 and
          1 <= int(month) <= 12 and 1 <= int(day) <= 31)


def add_vehicle(vehicle_file):
  """
  Add a new vehicle to the vehicleTxtFile.
  """
  vehicle_data = get_vehicle_data_input()
  with open(vehicle_file, "a") as file:
    file.write(vehicle_data + "\n")
  print("Vehicle details added successfully!")


def edit_vehicle(vehicle_file):
  """
  Edit an existing vehicle's details and handle duplicate Vehicle IDs.
  """
  vehicle_id = input("Enter Vehicle ID to edit: ").strip()
  try:
    with open(vehicle_file, "r") as file:
      vehicles = file.readlines()

    updated_vehicles = []
    found = False
    duplicates_removed = False

    for vehicle in vehicles:
      details = vehicle.strip().split(",")
      if details[0] == vehicle_id:
        if not found:
          # Allow editing for the first matching Vehicle ID
          print("\nExisting Details:")
          if len(details) <= 8:
            print(f"Vehicle ID: {details[0]}, Type: {details[1]}, Item Weight Limit: {details[2]}\n"
                  f"Route: {details[3]}, Specialised: {details[4]}, Maintenance: {details[5]}\n"
                  f"Inspection Date: {details[6]}, Order ID: None")
          elif len(details) >= 8:
            print(f"Vehicle ID: {details[0]}, Type: {details[1]}, Item Weight Limit: {details[2]}\n"
                  f"Route: {details[3]}, Specialised: {details[4]}, Maintenance: {details[5]}\n"
                  f"Inspection Date: {details[6]}, Order ID: {details[7:]}")
          print("\n<< Enter new details (leave blank to keep existing) >>")

          updated_data = get_vehicle_data_input(details)
          updated_vehicles.append(updated_data + "\n")
          found = True
        else:
          # Skip duplicate records
          duplicates_removed = True
      else:
        updated_vehicles.append(vehicle)

    if found:
      # Save updated list back to the file
      save_vehicle_file(vehicle_file, updated_vehicles)
      print("Vehicle details updated successfully!")
      if duplicates_removed:
        print("Duplicate records for the same Vehicle ID have been removed.")
    else:
      print("Vehicle ID not found.")
  except FileNotFoundError:
    print("<< No vehicle file found. Please add vehicles first. >>")


def get_vehicle_data_input(existing_data=None):
  """
  Collect vehicle data from the user, allowing for updates.
  """
  if existing_data is None:
    try:
      with open(vehicle_file, 'r') as file:
        lines = file.readlines()
        if lines:
          # Extract the last vehicle ID and increment it
          last_entry = lines[-1].strip()
          last_vehicle_id = last_entry.split(',')[0]
          # Extract numeric part and increment
          new_id_number = int(last_vehicle_id[1:]) + 1
          vehicle_id = f"V{new_id_number:03d}"  # Format to V001, V002, etc.
        else:
          vehicle_id = "V001"
    except FileNotFoundError:
      vehicle_id = "V001"  # Starting ID if file does not exist
  else:
    vehicle_id = existing_data[0]  # Use existing vehicle ID

  print(f"Current Vehicle ID is {vehicle_id}.")

  vehicle_type = input("Enter Vehicle Type: ") or (
      existing_data[1] if existing_data else "")
  item_weight_limit = input("Enter Item Weight Limit: ") or (
      existing_data[2] if existing_data else "")
  route_assigned = get_valid_input("Assign route for this vehicle (1 or 2): ", ["1", "2", ""]) or (
      existing_data[3] if existing_data else "")
  special_order = get_valid_input("Is the vehicle suitable for special order (y/n): ", ["y", "n", ""]) or (
      existing_data[4] if existing_data else "")
  maintenance = input("Enter Last Maintenance Date (YYYY-MM-DD): ") or (
      existing_data[5] if existing_data else "")
  while not is_valid_date(maintenance):
    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    maintenance = input("Enter Last Maintenance Date (YYYY-MM-DD): ") or (
        existing_data[5] if existing_data else "")
  inspection_date = input(
      "Enter Inspection Date (YYYY-MM-DD): ") or (existing_data[6] if existing_data else "")
  while not is_valid_date(inspection_date):
    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    inspection_date = input(
        "Enter Inspection Date (YYYY-MM-DD): ") or (existing_data[6] if existing_data else "")
  # order_id = input("Enter Order ID: ") or (existing_data[7] if existing_data else "")

  return f"{vehicle_id},{vehicle_type},{item_weight_limit},{route_assigned},{special_order},{maintenance},{inspection_date}"


def save_vehicle_file(vehicle_file, vehicles):
  """
  Save the vehicle data to the file.
  """
  with open(vehicle_file, "w") as file:
    file.writelines(vehicles)
  print("Vehicle data saved successfully.")


def view_vehicle_details(vehicle_file):
  """
  View all vehicle details.
  """
  try:
    with open(vehicle_file, "r") as file:
      vehicles = file.readlines()
      if not vehicles:
        print("<< No vehicles found. >>")
        return

      print("\n--- All Vehicle Details ---\n")
      print(f"{'Vehicle ID':<12} {'Type':<15} {'Item Weight Limit':<20} {'Route Assigned':<20} "
            f"{'Special Order':<15} {'Maintenance':<20} {'Inspection Date':<15} {'Order ID':<10}")
      print("-" * 120)
      for vehicle in vehicles:
        details = vehicle.strip().split(",")
        if len(details) < 8:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<20} {details[6]:<15} {"None":<10}")
          continue
        print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
              f"{details[4]:<15} {details[5]:<20} {details[6]:<15} {' '.join(details[7:]):<10}")
      input("Enter any key to continue: ")
  except FileNotFoundError:
    print("<< No vehicle file found. Please add vehicles first. >>")


def maintenance_alerts(vehicle_file):
  """
  Alert for vehicles that have maintenance due or overdue, with specific days number.
  """
  try:
    with open(vehicle_file, "r") as file:
      vehicles = file.readlines()

    due_vehicles = []
    upcoming_vehicles = []  # Vehicles with maintenance due within a certain period
    for vehicle in vehicles:
      details = vehicle.strip().split(",")
      if len(details) >= 7:
        # Maintenance Date is at index 5
        last_maintenance_date_str = details[5].strip()
        try:
          last_maintenance_date = datetime.strptime(last_maintenance_date_str, "%Y-%m-%d")
          # Set maintenance interval (e.g., 180 days = 6 months)
          # Adjust based on your maintenance schedule
          maintenance_interval = timedelta(days=180)

          # Calculate the next maintenance due date
          next_maintenance_date = last_maintenance_date + maintenance_interval
          today = datetime.today()
          # If the next maintenance date is today or in the past, it's overdue
          if next_maintenance_date < today:
            overdue_days = (today - next_maintenance_date).days
            due_vehicles.append((details, overdue_days))
          # Alert for upcoming maintenance within the next 7 days
          elif next_maintenance_date <= today + timedelta(days=7):
            upcoming_days = (next_maintenance_date - today).days
            upcoming_vehicles.append((details, upcoming_days))
        except ValueError:
          print(f"Invalid maintenance date format for vehicle {details[0]}. Skipping.")

    # Display overdue maintenance alerts
    if due_vehicles:
      print("\n--- Maintenance Alerts ---")
      print("Vehicles with maintenance due or overdue:\n")
      print(f"{'Vehicle ID':<12} {'Type':<15} {'Item Weight Limit':<20} {'Route':<20} "
            f"{'Specialised':<15} {'Maintenance Date':<15} {'Inspection Date':<15} {'Order ID':<10} {'Overdue Days':<12}")
      print("-" * 130)
      for details, overdue_days in due_vehicles:
        if len(details) >= 8:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {details[7]:<10} {overdue_days:<12}")
        elif len(details) <= 7:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {"None":<10} {overdue_days:<12}")
      print(f"ALERT: Vehicle ID(s) {', '.join([v[0][0] for v in due_vehicles])} are overdue for maintenance!")
      if not upcoming_vehicles:
        return

    # Display upcoming maintenance alerts
    if upcoming_vehicles:
      print("\n--- Upcoming Maintenance Alerts ---")
      print("Vehicles with maintenance due in the next 7 days:\n")
      print(f"{'Vehicle ID':<12} {'Type':<15} {'Item Weight Limit':<20} {'Route':<20} "
            f"{'Specialised':<15} {'Maintenance Date':<15} {'Inspection Date':<15} {'Order ID':<10} {'Upcoming Days':<12}")
      print("-" * 130)
      for details, upcoming_days in upcoming_vehicles:
        if len(details) >= 8:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {details[7]:<10} {upcoming_days:<12}")
        elif len(details) <= 7:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {"None":<10} {upcoming_days:<12}")
      print(f"ALERT: Vehicle ID(s) {', '.join([v[0][0] for v in upcoming_vehicles])} are due for maintenance soon!")
      return
    else:
      print("<< No vehicles have maintenance due or overdue. >>")
  except FileNotFoundError:
    print("<< No vehicle file found. Please add vehicles first. >>")


def inspection_alerts(vehicle_file):
  """
  Alert for vehicles that have inspection due or overdue, with specific days number.
  """
  try:
    with open(vehicle_file, "r") as file:
      vehicles = file.readlines()
      vehicles = [line.strip() for line in vehicles if line.strip()]

    overdue_vehicles = []
    upcoming_vehicles = []  # Vehicles with inspections due within a certain period
    today = datetime.today()

    for vehicle in vehicles:
      details = vehicle.strip().split(",")
      if len(details) >= 7:
        # Inspection Date is at index 6
        inspection_date_str = details[6].strip()
        try:
          inspection_date = datetime.strptime(inspection_date_str, "%Y-%m-%d")

          # If the inspection date is today or in the past, it's overdue
          if inspection_date <= today:
            overdue_days = (today - inspection_date).days
            overdue_vehicles.append((details, overdue_days))
          # Alert for upcoming inspections within the next 7 days
          elif inspection_date <= today + timedelta(days=7):
            upcoming_days = (inspection_date - today).days
            upcoming_vehicles.append((details, upcoming_days))
        except ValueError:
          print(f"Invalid inspection date format for vehicle {details[0]}. Skipping.")

    # Display overdue inspection alerts
    if overdue_vehicles:
      print("\n--- Inspection Alerts ---")
      print("Vehicles with overdue inspections:\n")
      print(f"{'Vehicle ID':<12} {'Type':<15} {'Item Weight Limit':<20} {'Route':<20} "
            f"{'Specialised':<15} {'Maintenance Date':<15} {'Inspection Date':<15} {'Order ID':<10} {'Overdue Days':<12}")
      print("-" * 150)
      for details, overdue_days in overdue_vehicles:
        if len(details) >= 8:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {details[7]:<10} {overdue_days:<12}")
        elif len(details) <= 7:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {"None":<10} {overdue_days:<12}")
      print(f"ALERT: Vehicle ID(s) {', '.join([v[0][0] for v in overdue_vehicles])} are overdue for inspection!")
      if not upcoming_vehicles:
        return

    # Display upcoming inspection alerts
    if upcoming_vehicles:
      print("\n--- Upcoming Inspection Alerts ---")
      print("Vehicles with inspections due in the next 7 days:\n")
      print(f"{'Vehicle ID':<12} {'Type':<15} {'Item Weight Limit':<20} {'Route':<20} "
            f"{'Specialised':<15} {'Maintenance Date':<15} {'Inspection Date':<15} {'Order ID':<10} {'Upcoming Days':<12}")
      print("-" * 150)
      for details, upcoming_days in upcoming_vehicles:
        if len(details) >= 8:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {details[7]:<10} {upcoming_days:<12}")
        elif len(details) <= 7:
          print(f"{details[0]:<12} {details[1]:<15} {details[2]:<20} {details[3]:<20} "
                f"{details[4]:<15} {details[5]:<15} {details[6]:<15} {"None":<10} {upcoming_days:<12}")
      print(f"ALERT: Vehicle ID(s) {', '.join([v[0][0] for v in upcoming_vehicles])} are due for inspection soon!")
    else:
      print("<< No vehicles have overdue inspections. >>")
  except FileNotFoundError:
    print("<< No vehicle file found. Please add vehicles first. >>")


def schedule_maintenance_inspection(vehicle_file):
  try:
    with open(vehicle_file, "r") as file:
      vehicles = file.readlines()

    updated_vehicles = []
    found = False

    for vehicle in vehicles:
      details = vehicle.strip().split(",")
      if len(details) >= 7:
        vehicle_id = details[0]
        print(
            f"\nCurrent details for Vehicle {vehicle_id}: Maintenance Date: {details[5]} | Inspection Date: {details[6]}\n")

        maintenance_date = input(
            "Enter next maintenance (YYYY-DD-MM) [Press ENTER to skip]: ")
        proceed = False
        while maintenance_date != "":
          while not is_valid_date(maintenance_date):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            maintenance_date = input("Enter next maintenance (YYYY-DD-MM) [Press ENTER to skip]: ")
            if maintenance_date == "":
              proceed = True
              break
          if proceed:
            break
          else:
            details[5] = maintenance_date
            break
        inspection_date = input(
            "Enter next inspection date (YYYY-MM-DD)  [Press ENTER to skip]: ")
        while inspection_date != "":
          while not is_valid_date(inspection_date):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            inspection_date = input(
                "Enter next inspection date (YYYY-MM-DD) [Press ENTER to skip]: ")
            if inspection_date == "":
              proceed = True
              break
          if proceed:
            break
          else:
            details[6] = inspection_date
            break

        updated_vehicles.append(','.join(details) + "\n")
        found = True
      else:
        updated_vehicles.append(vehicle)

    if found:
      save_vehicle_file(vehicle_file, updated_vehicles)
      print("Maintenance and Inspection dates updated successfully.")
    else:
      print("<< No vehicle found to update. >>")
  except FileNotFoundError:
    print("<< No vehicle file found. Please add vehicles first. >>")


def manage_fuel_and_consumption(fuel_file):
  """
  Manage fuel and vehicle consumption and display total fuel cost.
  """
  while True:
    print("\n--- Manage Fuel & Vehicle Consumption ---\n")
    choice = get_valid_input("1: View Total Fuel Cost\n2: Add Fuel Record\n0: Back to Admin Menu\n-> ",
                             ["1", "2", "0"])

    if choice == "1":
      view_total_fuel_cost(fuel_file)
    elif choice == "2":
      add_fuel_record(fuel_file)
    elif choice == "0":
      print("Returning to Admin Menu.")
      return


def view_total_fuel_cost(fuel_file):
  """
  Display the total fuel cost for all vehicles.
  """
  try:
    with open(fuel_file, "r") as file:
      fuel_data = file.readlines()

    total_fuel_cost = 0
    for record in fuel_data:
      details = record.strip().split(",")
      # Assuming the last column in the fuel record is the cost
      fuel_cost = float(details[-1])  # Assuming the cost is the last field
      total_fuel_cost += fuel_cost

    print(f"\n--- Total Fuel Cost for All Vehicles ---\n")
    print(f"Total Fuel Cost: RM{total_fuel_cost:.2f}")
  except FileNotFoundError:
    print("<< No fuel records found. Please add fuel records first. >>")


def add_fuel_record(fuel_file):
  """
  Add a new fuel record to the fuelTxtFile.
  """
  vehicle = read_file_contents(vehicle_file)
  vehicle_ids = [v.split(',')[0] for v in vehicle]
  vehicle_id = input("Enter Vehicle ID (Press ENTER to exit.): ").strip()
  if vehicle_id == "":
    print("Returning to Fuel Menu.")
    return
  while vehicle_id not in vehicle_ids:
    print(f"Vehicle ID not found. Please enter a valid Vehicle ID from {vehicle_ids}")
    vehicle_id = input("Enter Vehicle ID: ").strip()

  def is_valid_number(value):  # Validate fuel quantity
    try:
      num = float(value)
      return num > 0  # Ensure it's a positive number
    except ValueError:
      return False  # Not a valid number
  while True:
    fuel_quantity = input("Enter Fuel Quantity (in liters): ").strip()
    fuel_cost = input("Enter total cost of fuel (RM): ").strip()
    if not is_valid_number(fuel_quantity):
      print("Invalid input for fuel quantity. Please enter a positive number.")
      continue
    # Validate fuel cost
    if not is_valid_number(fuel_cost):
      print("Invalid input for fuel cost. Please enter a positive number.")
      continue
    break
  # Assuming the fuel record format: Vehicle ID, Fuel Quantity, Fuel Cost
  fuel_data = f"{vehicle_id},{fuel_quantity},{fuel_cost}\n"

  with open(fuel_file, "a") as file:
    file.write(fuel_data)

  print("Fuel record added successfully!")


def driver_management(driver_file, assigned_journey_file):
  """
  Manage drivers, assign journeys, and view driver details.
  """
  while True:
    print("\n--- Driver Management ---\n")
    choice = get_valid_input(
        "1: Add Driver\n2: Remove Driver\n3: View All Drivers\n4: Assign Journey to Driver\n0: Back to Admin Menu\n-> ",
        ["1", "2", "3", "4", "0"])

    if choice == "1":
      create_or_append_driver_txt()
    elif choice == "2":
      remove_driver(driver_file)
    elif choice == "3":
      view_drivers(driver_file)
    elif choice == "4":
      assign_journey_to_driver(driver_file, assigned_journey_file)
    elif choice == "0":
      print("Returning to Admin Menu.")
      break


def create_or_append_driver_txt():
  """
  Create or append driver details to the driverTxtFile.
  """
  try:
    with open(drivers_file, 'r'):
      file_exists = True
  except FileNotFoundError:
    file_exists = False

  if not file_exists:
    # Create the file and add the first driver
    print("File not found. Creating new file and adding the first driver.")
    driver_name = input("Enter driver's name: ")
    while driver_name == "":
      driver_name = input("Enter driver's name: ")
    driver_pwd = input("Enter driver's password (minimum 6-digit): ")
    while len(driver_pwd) < 6:
      driver_pwd = input("Enter driver's password: ")

    # Collect optional fields
    contact_info = input(
        "Enter contact info (or press ENTER to skip): ") or 'null'
    address = input("Enter address (or press ENTER to skip): ") or 'null'
    availability_status = input(
        "Enter availability status (True/False or press ENTER to skip): ") or 'null'
    driving_license = input(
        "Enter driving license status (True/False or press ENTER to skip): ") or 'null'
    health_report = input(
        "Enter health report (or press ENTER to skip): ") or 'null'

    # Write to file
    with open(drivers_file, 'w') as file:
      file.write(f"{driver_name},{driver_pwd},{contact_info},{address},{availability_status},{driving_license},{health_report}\n")

    print(f"Driver {driver_name} added successfully.")

  else:
    # Append new driver to existing file
    print("File found. Adding a new driver.")
    driver_name = input("Enter driver's name: ")
    while driver_name == "":
      driver_name = input("Enter driver's name (required): ")
    driver_pwd = input("Enter driver's password (minimum 6-digit): ")
    while len(driver_pwd) < 6:
      driver_pwd = input("Enter driver's password (minimum 6-digit): ")

    # Collect optional fields
    contact_info = input(
        "Enter contact info (or press ENTER to skip): ") or 'null'
    address = input("Enter address (or press ENTER to skip): ") or 'null'
    availability_status = input(
        "Enter availability status (True/False or press ENTER to skip): ") or 'null'
    driving_license = input(
        "Enter driving license status (True/False or press ENTER to skip): ") or 'null'
    health_report = input(
        "Enter health report (or press ENTER to skip): ") or 'null'

    # Append to file
    with open(drivers_file, 'a') as file:
      file.write(f"\n{driver_name},{driver_pwd},{contact_info},{address},{availability_status},{driving_license},{health_report}\n")

    print(f"Driver {driver_name} added successfully.")


def remove_driver(driver_file):
  """
  Remove a driver from the driverTxtFile.
  """
  drivers = read_file_contents(driver_file)

  # Display current drivers to the user
  if drivers != []:
    print("Current Drivers:")
    for index, driver in enumerate(drivers):
      # Displaying driver info without extra newline
      print(f"{index + 1}: {driver.strip()}")

    # Ask user for the driver number to remove
    try:
      choice = int(
          input("Enter the number of the driver you want to remove: ")) - 1

      if choice < 0 or choice >= len(drivers):
        print("Invalid choice. Please select a valid driver number.")
        return
      confirm = input("Press ENTER to confirm removal: ")
      if confirm == "":
        # Remove the selected driver
        removed_driver = drivers.pop(choice)
        print(f"Removed Driver: {removed_driver.strip()}")
        # Write updated drivers back to the file
        with open(driver_file, 'w') as file:
          for line in drivers:
            file.write(line)
            file.write("\n")

        print("<< Driver list updated successfully. >>")
      else:
        print("<< No driver removed. >>")
    except ValueError:
      print("<< Please enter a valid input. >>")


def view_drivers(driver_file):
  """
  View all drivers' details.
  """
  try:
    with open(driver_file, "r") as file:
      drivers = file.readlines()
      drivers = [line.strip() for line in drivers if line.strip()]
      if not drivers:
        print("No drivers found.")
        return

      print("\n--- All Driver Details ---\n")
      print(f"{'Driver Name':<12} {'Driver Password':<15} {
          'Availability':<15} {'License':<10}")
      print("-" * 55)
      for driver in drivers:
        details = driver.strip().split(",")
        print(f"{details[0]:<12} {details[1]:<15} {
            details[4]:<15} {details[5]:<10}")
      input("Enter any key to continue: ")
  except FileNotFoundError:
    print("<< No driver file found. Please add drivers first. >>")


def assign_journey_to_driver(driver_file, assigned_journey_file):
  """
  Assign a journey to a driver, ensuring the driver is available.
  """
  while True:
    drivers = read_file_contents(driver_file)
    vehicles = read_file_contents(vehicle_file)
    journeys = read_file_contents(assigned_journey_file)

    if drivers == []:
      print("<< No available drivers. >>")
      return
    else:
      available_drivers = [driver.strip().split(
          ",") for driver in drivers if driver.strip().split(",")[5] == "True"]

      assigned_driver_ids = {journey.split(',')[0]: journey.split(',')[
          1] for journey in journeys}
      available_drivers = [
          driver.strip().split(",") for driver in drivers
          if driver.strip().split(",")[5] == "True" and
          driver.strip().split(",")[0] not in assigned_driver_ids
      ]
      if not available_drivers:
        print("<< No available drivers. >>")
        return
      exit = False
      while True:
        print("\n--- Available Drivers ---")
        for driver in available_drivers:
          print(f"Driver Name: {driver[0]}, License: {driver[4]}")
        driver_id = input("Enter Driver Name to assign the journey (Press ENTER to exit): ")
        if driver_id == "":
          print("<< No journey has been assigned. Exiting... >>")
          exit = True
          break
        # Check if the driver is available
        driver_found = False
        selected_driver = None
        for driver in available_drivers:
          if driver[0] == driver_id:
            driver_found = True
            selected_driver = driver
            break

        if not driver_found:
          print(f"<< Driver Name {driver_id} is not available. >>")
          again = input("Press ENTER to exit or any KEY to choose again: ")
          if again == "":
            print("<< No journey has been assigned. Exiting... >>")
            exit = True
            break
        else:
          break
      if exit:
        break
    # If the driver is found, create the assigned journey
      assign_journey = [selected_driver[0], selected_driver[1]]

      # Check for available vehicles with orders assigned
      vehicleAssigned = [vehicle.split(',')[2] for vehicle in journeys]
      journeys = [vehicle for vehicle in vehicles if len(
          vehicle.split(',')) > 7 and vehicle.split(',')[0] not in vehicleAssigned]
      if journeys:
        first_journey = journeys[0].split(',')
        # Append order details (e.g., '2,8')
        assign_journey.append(first_journey[3])
        assign_journey.extend(first_journey[7:])

        # Prepare content for output
        output_content = f"{assign_journey[0]},{assign_journey[1]},{
            first_journey[0]},null,{','.join(assign_journey[2:])}"
        print(f"<< Journey to be assigned: {output_content} >>")
        confirm = input("Press ENTER to confirm: ")
        if confirm == "":
          # Write to the assigned journeys text file
          with open(assigned_journey_file, 'a') as file:
            file.write(output_content + '\n')

          print(f"<< Journey assigned: {output_content} >>")
        else:
          print("<< No journey has been assigned. >>")
      else:
        print("<< No vehicles with assigned orders found. There is no journeys to assign. Please try again later. >>")


# Reports


def generate_metrics_report(orders, completed_orders, journeys, revenue_data, fuel_data):
  """
  Generate key metrics report based on the provided data.
  """
  report = {
      "inventory_turnover_ratio": None,
      "truck_turnaround_time": None,
      "average_transportation_cost": None,
      "operating_ratio": None
  }

  # Calculate metrics
  total_completed_orders = len(completed_orders)
  total_orders = len(orders) - total_completed_orders

  # Calculate Inventory Turnover Ratio
  if total_orders > 0:
    report["inventory_turnover_ratio"] = total_completed_orders / total_orders

  # Calculate Truck Turnaround Time (dummy calculation)
  if journeys:
    report["truck_turnaround_time"] = sum(
        [int(journey.split(',')[-1]) for journey in journeys]) / len(journeys)

  # Average Transportation Cost calculation
  total_cost = 0
  for revenue in revenue_data:
    # Add cost from revenue data
    total_cost += float(revenue.split(',')[1])

  report["average_transportation_cost"] = total_cost / \
      total_orders if total_orders > 0 else 0

  # Operating Ratio (fuel spending / revenue)
  total_fuel_cost = sum([float(fuel.split(',')[2])
                         for fuel in fuel_data])

  total_revenue = sum([float(revenue.split(',')[1])
                       for revenue in revenue_data])
  report["operating_ratio"] = total_fuel_cost / \
      total_revenue if total_revenue > 0 else 0

  return report


def display_metrics_report(report):
  # Display Key Metrics Report
  print("\nKey Metrics Report:")
  print("=" * 60)
  print(f"{'Metric':<35}{'Value'}")
  print("-" * 60)

  # Display each metric with formatting
  print(f"{'Inventory Turnover Ratio':<35}{
      report['inventory_turnover_ratio']:.2f}")
  print(f"{'Average Turnaround Time (hours)':<35}{
      report['truck_turnaround_time']:.2f}")
  print(f"{'Average Revenue (RM)':<35}{
      report['average_transportation_cost']:.2f}")
  print(f"{'Operating Ratio':<35}{report['operating_ratio']:.2f}")
  print("=" * 60)
  input("Enter any key to continue: ")


def display_order_logs(orders):
  """
  Display order logs report.
  """
  order_logs = []

  for order in orders:
    details = order.split(',')
    order_log = {
        "Route Details": f"{details[4]} to {details[5]}",
        "Timestamp": details[6],
        "Item Description": details[1],
        "User ID": details[0]
    }
    order_logs.append(order_log)

  print("\nOrder Logs Report:")
  print("=" * 90)
  print(f"{'Route Details':<30}{'Timestamp':<20}{
      'Item Name':<25}{'User ID':<15}")
  print("-" * 90)

  for log in order_logs:
    print(f"{log['Route Details']:<30}{log['Timestamp']:<20}{
        log['Item Description']:<25}{log['User ID']:<15}")

  print("=" * 90)
  input("Enter any key to continue: ")


def generate_trip_log_report(orders, assigned_journeys, completed_journeys):
  """
  Generate and display the trip logs report.
  """
  all_journeys = assigned_journeys + completed_journeys

  orders_data = [order.split(',') for order in orders]

  # Display Trip Logs report
  print("\nTrip Logs Report:")
  print("=" * 80)
  print(f"{'Route Details':<20}{'Timestamp':<20}{
      'Item Name':<25}{'Driver Name':<15}")
  print("-" * 80)
  orders_shipped = []

  for j in all_journeys:
    journey = j.split(',')
    orders = journey[5:]
    orderArr = []
    for order in orders_data:
      if order[-1] in orders:
        orderArr.append(order)
    orders_shipped.append(orderArr)
  for order in orders_shipped:
    if len(order) == 1:
      order = order[0]
      print(f"{'Johor-' + order[5]:<20}{order[6]:<20}{order[1]:<25}{journey[0]:<15}")
    else:
      date = []
      locations = []
      route = []
      item = ''
      for o in order:
        date.append(o[6])
        locations.append(o[4])
        locations.append(o[5])
        route.append(o[3])
        if item == '':
          item += o[1]
        else:
          item += ', ' + o[1]
      selected_date = max(date)
      if route[0] == "1":
        hubs = ["Johor", "Kuala Lumpur", "Butterworth", "Kedah", "Perlis"]
      elif route[0] == "2":
        hubs = ["Johor", "Kuala Lumpur", "Terengganu", "Kelantan"]
      route_string = f"{hubs[0]}-{hubs[-1]}"
      print(f"{route_string:<20}{selected_date:<20}{item:<25}{journey[0]:<15}")
  input("\nEnter any key to continue: ")


def menu_generate_reports():
  """
  Display the Reports Menu and process admin's choice.
  """
  while True:
    print("\n--- Reports Menu ---\n")
    choice = get_valid_input(
        "1: Key Metrics Report\n2: Order Logs Report\n3: Trip Logs Report\n0: Back to Admin Menu\n-> ",
        ["1", "2", "3", "0"])
    orders = read_file_contents(orders_file)
    completed_orders = read_file_contents(completed_orders_file)
    journeys = read_file_contents(journeys_file)
    fuel_data = read_file_contents(fuel_file)
    revenue_data = read_file_contents(revenue_file)
    assigned_journeys = read_file_contents(assigned_journeys_file)
    completed_journeys = read_file_contents(completed_journeys_file)

    if choice == "1":
      report_data = generate_metrics_report(
          orders, completed_orders, journeys, revenue_data, fuel_data)
      has_none = None in report_data.values()
      if has_none != True:
        display_metrics_report(report_data)
      else:
        print("<< Insufficient data to generate report. >>")
        input("Enter any key to continue: ")
    elif choice == "2":
      display_order_logs(orders)
    elif choice == "3":
      generate_trip_log_report(orders, assigned_journeys, completed_journeys)
    elif choice == "0":
      print("Returning to Admin Menu.")
      break


# Main Program TODO:
def main_program():
  """
  Main Program of SMA, Get user's choice on which feature of the App they want to use
  """
  while True:
    print("\n--- Welcome To Main Menu ---\n")
    userInput = get_valid_input("1: User features\n2: Driver features\n3: Admin features\n0: Exit Program\n-> ",
                                ["1", "2", "3", "0"])

    if userInput == "1":  # -- Perform functions according to user's input --
      user_features()
    elif userInput == "2":
      driver_features()
    elif userInput == "3":
      admin_features()
    else:
      print("<<< Thank you for using our 'Shipment Management System'! >>>\n")
      break


def login(file_path):
  """
  Log in to access features
  """
  try:
    print("\n--- Logging in ---")
    with open(file_path, "r") as TxtFile:
      data = TxtFile.readlines()

    if len(data) == 0:
      print(f"There is no record in {file_path} file.")
      return None
    else:
      checkName = input("Enter your username: ")
      for line in data:
        activeData = line.strip().split(',')
        if activeData[0] == checkName:
          pwdAttempt = 3
          while pwdAttempt > 0:
            checkPwd = input("Enter your password: ")
            if activeData[1] == checkPwd:
              print(f"Welcome, {checkName}!")
              return activeData
            else:
              print(f"<< Wrong password. You have {
                  pwdAttempt - 1} attempts left. >>")
              pwdAttempt -= 1
          print("<< Failed to log in. Please try again. >>")
          return None
      print("<< Name doesn't exist. >>")
      return None
  except FileNotFoundError:
    print("<< No relevant records found. >>\n")
    return None


def get_valid_input(prompt, valid_options):
  """
  Prompts the user for input and ensures it's one of the valid options in the array received as parameter.
  """
  while True:
    user_input = input(prompt).strip()
    if user_input in valid_options:
      return user_input
    print("<< Invalid input. Please try again. >>")


def read_file_contents(filename):
  """
  Read file contents with error handling and return lines or empty list
  """
  try:
    with open(filename, "r") as file:
      return [line.strip() for line in file if line.strip()]
  except FileNotFoundError:
    print(f"<< No {filename} records found. >>")
    return []


# Execute main_menu() when program is run
if __name__ == "__main__":
  main_program()
