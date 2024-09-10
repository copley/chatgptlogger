
import pychrome
import os
from datetime import datetime

# File paths for log files
query_response_log = "chatgptresponselength.txt"
query_count_log = "countgptqueries.txt"

# Function to ensure the log files exist
def ensure_log_files():
    # Check if the query/response length log exists, create if not
    if not os.path.exists(query_response_log):
        with open(query_response_log, 'w') as f:
            f.write("ChatGPT Query and Response Length Log\n")
    
    # Check if the query count log exists, create if not
    if not os.path.exists(query_count_log):
        with open(query_count_log, 'w') as f:
            f.write("ChatGPT Query Count Log\n")

# Function to log the query and response word counts
def log_query_response_length(query_word_count, response_word_count):
    now = datetime.now().strftime("%d,%m,%y %H:%M:%S")
    log_entry = f"{now} Q '{query_word_count}' A '{response_word_count}'\n"
    with open(query_response_log, 'a') as f:
        f.write(log_entry)

# Function to initialize or read the daily query count from the file
def initialize_or_read_file():
    today = datetime.now().strftime("%d,%m,%y")
    current_count = 0
    
    if not os.path.exists(query_count_log):
        # If the file doesn't exist, create it with today's date and initial count 0
        with open(query_count_log, 'w') as f:
            f.write(f"{today} number of queries sent to https://chatgpt.com/ today: 0\n")
        return 0

    with open(query_count_log, 'r') as f:
        lines = f.readlines()

    # Check if today's entry already exists
    for line in lines:
        if line.startswith(today):
            # Extract the count from today's entry
            current_count = int(line.split(":")[-1].strip())
            break
    else:
        # If no entry for today, append a new entry with count 0
        with open(query_count_log, 'a') as f:
            f.write(f"{today} number of queries sent to https://chatgpt.com/ today: 0\n")

    return current_count

# Function to increment and log the number of requests
def increment_query_count():
    today = datetime.now().strftime("%d,%m,%y")
    
    # Check the current count, or start with 0 if not found
    current_count = initialize_or_read_file()

    # Increment the count
    current_count += 1

    # Append the updated count for today
    with open(query_count_log, 'a') as f:
        f.write(f"{today} number of queries sent to https://chatgpt.com/ today: {current_count}\n")

# Function to handle network request event and filter relevant requests
def request_will_be_sent(event, count):
    # Check if the 'request' key exists in the event dictionary
    if 'request' in event:
        url = event['request']['url']
        print(f"Request detected to: {url}")  # Log every request
        if '/conversation' in url and 'chatgpt.com' in url:
            print(f"Detected query to {url}")
            count += 1
            increment_query_count()

            # Example: log word counts (in a real scenario, you'd extract actual text)
            query_word_count = 10  # placeholder for query word count
            response_word_count = 20  # placeholder for response word count
            log_query_response_length(query_word_count, response_word_count)

    else:
        print(f"Event without 'request' key: {event}")
    return count

# Main function to set up the Chrome DevTools connection and monitor requests
def main():
    # Ensure log files are set up correctly
    ensure_log_files()

    # Initialize or read the query count
    count = initialize_or_read_file()

    # Connect to the running Chrome instance on localhost:9222
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    tab = browser.new_tab()

    # Enable network tracking in the DevTools Protocol
    tab.start()
    tab.Network.enable()

    # Set up event handler for network requests
    tab.Network.requestWillBeSent = lambda **kwargs: request_will_be_sent(kwargs, count)

    # Start the monitoring
    try:
        tab.start()
        input("Press Enter to stop monitoring...\n")  # Keep the script running until you stop it
    finally:
        tab.stop()
        browser.close_tab(tab)

if __name__ == "__main__":
    main()
