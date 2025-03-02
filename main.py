import tkinter as tk
from tkinter import ttk
import random
import time

# List of sample texts
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great programming language.",
    "Practice makes perfect, so keep typing fast and accurately.",
    "Consistency is key to success in any skill.",
    "Typing speed is measured in words per minute."
]

# Global variables for timing and test state
start_time = None
timer_started = False
sample_text = ""

def start_test():
    global start_time, timer_started, sample_text
    # Select and display a random sample text
    sample_text = random.choice(texts)
    sample_label.config(text=sample_text)
    
    # Reset input area and results
    input_text.config(state=tk.NORMAL)
    input_text.delete("1.0", tk.END)
    result_label.config(text="")
    start_time = None
    timer_started = False
    
    # Set focus and bind first key press to start the timer
    input_text.focus_set()
    input_text.bind("<Key>", start_timer)

def start_timer(event):
    global start_time, timer_started
    if not timer_started:
        start_time = time.time()
        timer_started = True
        input_text.unbind("<Key>")

def submit_test(event=None):
    global start_time, sample_text
    if start_time is None:
        result_label.config(text="You haven't started typing yet!")
        return

    finish_time = time.time()
    elapsed_time = finish_time - start_time

    # Get user input and compare word-by-word
    user_input = input_text.get("1.0", tk.END).strip()
    test_words = sample_text.split()
    input_words = user_input.split()

    correct_words = sum(1 for i in range(min(len(test_words), len(input_words))) if test_words[i] == input_words[i])
    wpm = (correct_words / elapsed_time) * 60

    result_label.config(text=f"Time: {elapsed_time:.2f}s | Correct: {correct_words}/{len(test_words)} | WPM: {wpm:.2f}")
    input_text.config(state=tk.DISABLED)

# Set up the main application window
root = tk.Tk()
root.title("WPM Typing Test")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Define fonts for a cleaner look
header_font = ("Helvetica", 18, "bold")
text_font = ("Helvetica", 14)
result_font = ("Helvetica", 16, "bold")

# Header frame for instructions
header_frame = tk.Frame(root, bg="#f0f0f0")
header_frame.pack(pady=20)

instruction_label = tk.Label(header_frame, text="Welcome to the WPM Typing Test!", font=header_font, bg="#f0f0f0")
instruction_label.pack()

sub_instruction = tk.Label(header_frame, text="Click 'Start Test' and type the text below as fast and accurately as you can.", font=text_font, bg="#f0f0f0")
sub_instruction.pack(pady=10)

# Frame to display the sample text
sample_frame = tk.Frame(root, bg="#f0f0f0")
sample_frame.pack(pady=10)

sample_label = tk.Label(sample_frame, text="", font=text_font, wraplength=700, justify="center",
                        bg="#ffffff", bd=2, relief="solid", padx=10, pady=10)
sample_label.pack()

# Text input frame for the user's typing
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=20)

input_text = tk.Text(input_frame, height=5, width=80, font=text_font, wrap="word", bd=2, relief="solid")
input_text.pack()

# Button frame for control buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

start_button = ttk.Button(button_frame, text="Start Test", command=start_test)
start_button.grid(row=0, column=0, padx=20)

submit_button = ttk.Button(button_frame, text="Submit", command=submit_test)
submit_button.grid(row=0, column=1, padx=20)

# Result label to display test outcomes
result_frame = tk.Frame(root, bg="#f0f0f0")
result_frame.pack(pady=10)

result_label = tk.Label(result_frame, text="", font=result_font, bg="#f0f0f0")
result_label.pack()

# Optionally bind the Enter key to submit the test
input_text.bind("<Return>", submit_test)

root.mainloop()
