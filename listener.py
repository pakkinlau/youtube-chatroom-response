import pytchat  # Import the pytchat library for interacting with YouTube live chat
import time  # Import the time module for working with timestamps
from random import randint  # Import randint function for generating random sleep times

# Define a synchronous function to listen to the live chat
def listen_livechat(
    video_id: str, cond_trigger_func, keyword_list: list = ["無雙", "!bet 0 100", "!bet 1 100", "!bet 2 100", "maze", "抽"]
):
    # Create a dictionary to keep track of the last times each keyword was detected
    last_times = {keyword: time.time() - 20 for keyword in keyword_list}
    
    # Create a chat object for the specified YouTube video
    chat = pytchat.create(video_id=video_id)
    
    # Continuously listen to the live chat while it is active
    while chat.is_alive():
        # Loop through chat messages received
        for c in chat.get().sync_items():
            # Print the date, author's name, and message content of each chat message
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
            
            # Check if any of the specified keywords are present in the message
            for keyword in keyword_list:
                if keyword in c.message:
                    last_time = last_times[keyword]

                    # Check if it has been more than 30 seconds since the last interaction with this keyword
                    if time.time() - last_time > 30:
                        print("!!!!!! Keyword detected")
                        rand = randint(8, 10)
                        time.sleep(rand)  # Introduce a random sleep time (between 8 and 10 seconds)
                        print(f"{c.datetime} [{c.author.name}]- {c.message}")
                        cond_trigger_func(keyword)  # Call a custom function when a keyword is detected
                        last_times[keyword] = time.time()  # Update the last interaction time
                    else:
                        print(f"Already interacted in the last 20 seconds. Since last time: {time.time() - last_time} seconds")
                    break  # Exit the loop after processing the first keyword match

# Entry point of the script
if __name__ == "__main__":
    listen_livechat(video_id="d-cHsZzZ0Ww")  # Start listening to the live chat of the specified YouTube video
