from tkinter import *
from PIL import ImageTk, Image
from tkinter import scrolledtext, messagebox
import ollama
from datetime import datetime



##########################################################
# Reading the configuration
##########################################################e
with open('config.txt', 'r') as file:
    lines = file.readlines()

config = {}

for line in lines:

    key, value = line.strip().split('=')
    

    key = key.strip()
    value = value.strip()
    
    config[key] = value

if config['debug'] == 'true':
    print(config)

##########################################################
# Defining All the functions
##########################################################
def save_conversation():
    conversation = chat_display.get("1.0", END)
    with open(f"conversations/conversation{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt", "w") as file:
        file.write(conversation)
    messagebox.showinfo("Save Conversation", "Conversation saved successfully.")


def clear_conversation():
    chat_display.configure(state='normal')
    chat_display.delete('1.0', END)
    chat_display.configure(state='disabled')



def send_message(event=None):
    message = entry.get()
    if message:
        response = get_response(message)        
        chat_display.configure(state='normal')  
        chat_display.insert(END, "You: " + message + "\n")
        chat_display.insert(END, f"{config['name']}: " + response + "\n")
        chat_display.configure(state='disabled')  
        entry.delete(0, END)  
def get_response(message):
    try:
        response = ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': message}])
        return response['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Error: Failed to get response from model"

##########################################################
# Everything that has to do with the GUI
##########################################################
root = Tk()
root.title(config['title'])


# Menu Bar
menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=False)

file_menu.add_command(
    label='Save Conversation',
    command=save_conversation
)

file_menu.add_command(
    label='Clear Conversation',
    command=clear_conversation
)

file_menu.add_command(
    label='Exit',
    command=root.destroy
)


menubar.add_cascade(
    label="File",
    menu=file_menu
)

# loading the image
if config['image'] == 'true':
    img = ImageTk.PhotoImage(Image.open(f"images/{config['imagePath']}.png"))
    panel = Label(root, image=img)
    panel.pack(side="left", fill="both", expand="no")

# Inital Message
initial_message = f"\n---------- DEBUG ----------\nConnected To Ollama Server.\nRunning Version {config['version']}. Model: {config['model']}"
chat_display = scrolledtext.ScrolledText(root, wrap=WORD, width=40, height=15, state='normal')
if config['debug']:
    chat_display.insert(END, "Programm: " + initial_message + "\n")
chat_display.configure(state='disabled')  
chat_display.pack(padx=10, pady=10)

# user input
entry = Entry(root, width=40)
entry.pack(pady=5)


# send button
send_button = Button(root, text="Send", command=send_message)
send_button.pack(pady=5)


# Bind the Enter key to the send_message function
entry.bind("<Return>", send_message)

# Run the Tkinter event loop
root.mainloop()
