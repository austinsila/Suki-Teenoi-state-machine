# Function Define Mapโต๊ะในร้าน 
def get_table_location(table_id):
    if table_id == 1:
        return "Zone A - Row 1"
    elif table_id == 2:
        return "Zone A - Row 2"
    elif table_id == 3:
        return "Zone B - Row 1"
    elif table_id == 4:
        return "Zone B - Row 2"
    elif table_id == 5:
        return "Zone C - Row 1"
    elif table_id == 6:
        return "Zone C - Row 2"
    elif table_id == 7:
        return "Zone D - Row 1"
    elif table_id == 8:
        return "Zone D - Row 2"
    else:
        return "Unknown Location"

# Define actions for each state
def show_state_action(state):
    if state == "IDLE":
        print("[ACTION] Robot standby at kitchen. Wait for staff.")
    elif state == "LOADING":
        print("[ACTION] Staff place food on trays and assign table IDs.")
    elif state == "NAVIGATING":
        print("[ACTION] Robot is moving to the next table.")
    elif state == "AVOIDING_OBSTACLE":
        print("[ACTION] Obstacle detected! Robot stops and finds an alternate path.")
    elif state == "NOTIFYING":
        print("[ACTION] Robot has arrived! Play sound + show tray info on screen.")
    elif state == "WAIT_FOR_CUSTOMER":
        print("[ACTION] Wait for customer to take food and press [Received] button.")
    elif state == "CHECKING_TRAYS":
        print("[ACTION] Checking if more tables are in the delivery queue.")
    elif state == "RETURNING":
        print("[ACTION] All deliveries done! Robot is returning to the kitchen.")
    elif state == "ERROR":
        print("[ACTION] Error detected! Please reset the robot manually.")

# Define the state transition function
def transition(event, state):
    next_state = ""

    if event == "staff_assigns_food" and state == "IDLE":
        next_state = "LOADING"
    elif event == "loading_complete" and state == "LOADING":
        next_state = "NAVIGATING"
    elif event == "arrived_at_table" and state == "NAVIGATING":
        next_state = "NOTIFYING"
    elif event == "obstacle_detected" and state == "NAVIGATING":
        next_state = "AVOIDING_OBSTACLE"
    elif event == "path_cleared" and state == "AVOIDING_OBSTACLE":
        next_state = "NAVIGATING"
    elif event == "noti_sent" and state == "NOTIFYING":
        next_state = "WAIT_FOR_CUSTOMER"
    elif event == "food_received_pressed" and state == "WAIT_FOR_CUSTOMER":
        next_state = "CHECKING_TRAYS"
    elif event == "more_tables_remain" and state == "CHECKING_TRAYS":
        next_state = "NAVIGATING"
    elif event == "all_tables_done" and state == "CHECKING_TRAYS":
        next_state = "RETURNING"
    elif event == "arrived_at_kitchen" and state == "RETURNING":
        next_state = "IDLE"
    elif event == "error_detected":
        next_state = "ERROR"
    elif event == "error_reset" and state == "ERROR":
        next_state = "IDLE"
    else:
        print(f"\n[INVALID] Event '{event}' cannot happen in state '{state}'")
        return state

    print("\n[EVENT]", event)
    print("[STATE]", state, "→", next_state)
    show_state_action(next_state)
    

    return next_state


#  Main Simulation 
print("Suki Teenoi Robot - state machine simulation")

# Step 1: Staff เตรียมอาหารใส่ถาด
print("\nStaff assigning food to trays")

num_trays = int(input("How many trays to load? (1-4): "))

delivery_queue = []

tray_number = 1
while tray_number <= num_trays:
    print(f"\nTray {tray_number}:")
    table_id = int(input("Enter table number (1-8): "))
    food_name = input("Enter food name: ")

    order = {   #dictionary
        "tray": tray_number,
        "table": table_id,
        "food": food_name,
        "location": get_table_location(table_id)
    }
    delivery_queue.append(order) #เพิ่ม order ลงใน delivery_queue เรื่อยๆ
    tray_number = tray_number + 1

# Step 2: เริ่ม State Machine
print("\n")
print("STARTING DELIVERY SEQUENCE")

state = "IDLE"

state = transition("staff_assigns_food", state)
input("Press Enter when trays are loaded: ")
state = transition("loading_complete", state)

# Step 3: ส่งอาหารไปแต่ละโต๊ะตามคิว
current_index = 0

while current_index < len(delivery_queue):
    order = delivery_queue[current_index]

    print(f"\nNext delivery → Table {order['table']} ({order['location']})")
    print(f"   Food: {order['food']}  |  Tray: {order['tray']}")
    print("-" * 40)

    obstacle = input("Obstacle on the way? (y/n): ")

    if obstacle == "y":
        state = transition("obstacle_detected", state)
        input("Press Enter when path is clear:")
        state = transition("path_cleared", state)

    state = transition("arrived_at_table", state)
    state = transition("noti_sent", state)

    print(f"\nScreen: 'Table {order['table']} — Your {order['food']} is on Tray {order['tray']}!'")
    input("Customer: Press Enter to receive food:")
    state = transition("food_received_pressed", state)

    current_index = current_index + 1

    if current_index < len(delivery_queue):
        state = transition("more_tables_remain", state)
    else:
        state = transition("all_tables_done", state)

# ---------- Step 4: กลับครัว ----------
input("\nPress Enter when robot arrives back at kitchen:")
state = transition("arrived_at_kitchen", state)

print("\nDELIVERY COMPLETE! Robot is back on standby.")


