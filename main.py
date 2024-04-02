from tkinter import *
from PIL import ImageTk, Image
from tkinter import scrolledtext, messagebox
import ollama
from datetime import datetime



# Open and read the contents of the config.txt file
with open('config.txt', 'r') as file:
    lines = file.readlines()

# Create an empty dictionary to store the configuration
config = {}

# Process each line of the config file
for line in lines:
    # Split the line into key and value using the '=' separator
    key, value = line.strip().split('=')
    
    # Strip whitespace from the key and value
    key = key.strip()
    value = value.strip()
    
    # Set the value to the corresponding key in the config dictionary
    config[key] = value

# Print the entire config dictionary
print(config)


def save_conversation():
    conversation = chat_display.get("1.0", END)
    with open(f"conversations/conversation{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt", "w") as file:
        file.write(conversation)
    messagebox.showinfo("Save Conversation", "Conversation saved successfully.")



def send_message(event=None):
    global message_count
    message = entry.get()
    if message:
        message_count += 1
        response = get_response(message)
        chat_display.configure(state='normal')  # Enable editing
        chat_display.insert(END, "You: " + message + "\n")
        chat_display.insert(END, f"{config['name']}: " + response + "\n")
        chat_display.configure(state='disabled')  # Disable editing
        entry.delete(0, END)  # Clear the entry field

def get_response(message):
    try:
        response = ollama.chat(model='llama2-uncensored', messages=[{'role': 'user', 'content': message}])
        return response['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Error: Failed to get response from model"

# Create the main window
root = Tk()
root.title(config['title'])

# Load and display the initial image
print(str(config['image']))
if config['image'] == 'true':
    img = ImageTk.PhotoImage(Image.open(f"images/{config['imagePath']}.png"))
    panel = Label(root, image=img)
    panel.pack(side="left", fill="both", expand="no")

# Display a message in the chat window when the program starts
initial_message = f"\n---------- DEBUG ----------\nConnected To Ollama Server. Running Version {config['version']}. Model: {config['model']}"
chat_display = scrolledtext.ScrolledText(root, wrap=WORD, width=40, height=15, state='normal')
if config['debug']:
    chat_display.insert(END, "Programm: " + initial_message + "\n")
chat_display.configure(state='disabled')  # Disable editing
chat_display.pack(padx=10, pady=10)

# Create an Entry widget for user input
entry = Entry(root, width=40)
entry.pack(pady=5)

save_button = Button(root, text="Save Conversation", command=save_conversation)
save_button.pack(pady=5)
# Create a button to send messages
send_button = Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Bind the Enter key to the send_message function
entry.bind("<Return>", send_message)

# Message count variable
message_count = 0





# Run the Tkinter event loop
root.mainloop()
