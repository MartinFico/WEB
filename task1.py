import threading
import random
import time

# Shared resources
number_list = []
list_filled_event = threading.Event()

def fill_list():
    global number_list
    print("Filling the list with random numbers...")
    for _ in range(10):  # Adjust the range for the desired list size
        number_list.append(random.randint(1, 100))
        time.sleep(0.1)  # Adding a small delay for demonstration
    print("List filled with random numbers.")
    list_filled_event.set()  # Signal that the list is filled

def calculate_sum():
    print("Waiting to calculate sum...")
    list_filled_event.wait()  # Wait until the list is filled
    total_sum = sum(number_list)
    print(f"Sum of list elements: {total_sum}")

def calculate_average():
    print("Waiting to calculate average...")
    list_filled_event.wait()  # Wait until the list is filled
    average = sum(number_list) / len(number_list)
    print(f"Average of list elements: {average:.2f}")

# Create threads
filler_thread = threading.Thread(target=fill_list)
sum_thread = threading.Thread(target=calculate_sum)
average_thread = threading.Thread(target=calculate_average)

# Start threads
filler_thread.start()
sum_thread.start()
average_thread.start()

# Wait for all threads to complete
filler_thread.join()
sum_thread.join()
average_thread.join()

print(f"Final list: {number_list}")