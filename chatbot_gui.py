import openai
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import threading
import queue
from PIL import Image, ImageTk  # For handling images

# Set up the OpenAI API key
openai.api_key = 'sk-afxV2nceDeDw_4Xy-ENSmaV7sQBV6_u8BhgsNA7XGHT3BlbkFJmQUyfYX-_uKsiqCsSuoifia55SnhhTRH3XkSQUaw8A'  # Replace with your actual OpenAI API key

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()
speech_queue = queue.Queue()

# Set up the main application window
root = tk.Tk()
root.title("AI-Powered Health Chatbot")
root.geometry("600x600")  # Increased the height for better layout
root.config(bg="#f5f5f5")  # Set background color

# Correct path assignment for the background image
background_image_path = r'C:\Users\cmudh\Desktop\HIVChatBot\back.PNG'  # Correct path for background image
bg_image = Image.open(background_image_path)
bg_image = bg_image.resize((600, 600), Image.Resampling.LANCZOS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Add the background image to the window using a label, making sure it stays in the background
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Set the background to cover the entire window

# Title label (centered)
title_label = tk.Label(root, text="AI-Powered Health Chatbot: Your Personal Disease Diagnosis Assistant",
                       font=("Times New Roman", 18, "bold"), bg="#f5f5f5", fg="#333333")
title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="n")

# Chat display area (scrollable, centered)
chat_display = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD, font=("Times New Roman", 12))
chat_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
chat_display.config(state=tk.DISABLED)
chat_display.config(bg="#f7f7f7", fg="#333333")

# Input text area (centered)
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

user_input = tk.Entry(input_frame, width=45, font=("Times New Roman", 14))
user_input.grid(row=0, column=0, padx=10, pady=5)

# Healthcare Image (example, you can place a relevant image here)
healthcare_img_path = r'C:\Users\cmudh\Desktop\HIVChatBot\back.PNG'  # Corrected healthcare image path
healthcare_img = Image.open(healthcare_img_path)
healthcare_img = healthcare_img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize it
healthcare_photo = ImageTk.PhotoImage(healthcare_img)

# Place the healthcare image on the GUI
healthcare_image_label = tk.Label(root, image=healthcare_photo)
healthcare_image_label.grid(row=3, column=0, columnspan=2, pady=20)
healthcare_image_label.image = healthcare_photo  # Keep a reference to avoid garbage collection

# Function to send text input and get response from ChatGPT (updated for the correct endpoint)
def get_chatgpt_response(user_input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Updated to use the chat model 'gpt-3.5-turbo'
        messages=[{"role": "user", "content": user_input_text}]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to speak out the response (using the queue)
def speak(text):
    speech_queue.put(text)

# Function to display the conversation
def display_conversation(text, is_user=False):
    chat_display.config(state=tk.NORMAL)
    if is_user:
        chat_display.insert(tk.END, f"You: {text}\n\n")  # Added extra space for readability
    else:
        chat_display.insert(tk.END, f"Bot: {text}\n\n")  # Added extra space for readability
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)  # Scroll to the bottom

# Function to process user input
def process_input():
    input_text = user_input.get()
    if input_text.strip() != "":
        display_conversation(input_text, is_user=True)
        response = get_chatgpt_response(input_text)
        display_conversation(response, is_user=False)
        speak(response)  # Speak out the response
    user_input.delete(0, tk.END)  # Clear the input box

# Function for voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your voice command...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        user_input.insert(tk.END, text)  # Insert the recognized text into input field
        process_input()  # Process the input after recognition
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        speak("Sorry, there was an error with the voice input.")

# Function to handle the text-to-speech queue in the main thread
def process_speech():
    while True:
        text = speech_queue.get()  # Get the text from the queue
        engine.say(text)
        engine.runAndWait()

# Start the speech processing thread
speech_thread = threading.Thread(target=process_speech, daemon=True)
speech_thread.start()

# Function to create a round button with an icon using Unicode characters
def create_round_button(parent, command, icon, radius=30, bg_color="#4CAF50", icon_size=20, row=3, column=0):
    button = tk.Button(parent, text=icon, command=command, font=("Times New Roman", icon_size), width=3, height=2, relief="flat", 
                       bg=bg_color, activebackground="#4CAF50", fg="white", bd=0)
    button.grid(row=row, column=column, padx=10, pady=5)  # Use grid instead of pack
    return button

# Create Send button (Round with upward arrow)
send_button = create_round_button(input_frame, process_input, icon="↑", radius=30, bg_color="#4CAF50", icon_size=15, row=0, column=2)

# Create Voice button (Round with microphone icon)
voice_button = create_round_button(input_frame, listen, icon="🎤", radius=30, bg_color="#FF5722", icon_size=15, row=0, column=3)

# Run the GUI application
root.mainloop()
