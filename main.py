import tkinter as tk
import time
import random

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Test")
        self.text_options = self.load_texts()
        
        self.create_start_screen()
    
    def create_start_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Choose Difficulty:", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.easy_button = tk.Button(self.root, text="Easy", command=lambda: self.start_test("easy"))
        self.easy_button.pack()
        
        self.medium_button = tk.Button(self.root, text="Medium", command=lambda: self.start_test("medium"))
        self.medium_button.pack()
        
        self.hard_button = tk.Button(self.root, text="Hard", command=lambda: self.start_test("hard"))
        self.hard_button.pack()
    
    def start_test(self, difficulty):
        self.difficulty = difficulty
        self.text = random.choice(self.text_options)
        if difficulty == "easy":
            self.text = self.text.lower()
        self.words = self.text.split()
        self.current_word_index = 0
        self.typed_text = ""
        self.start_time = time.time()
        
        self.clear_screen()
        self.label = tk.Label(self.root, text=self.text, font=("Arial", 14), fg="grey")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack()
        self.entry.bind("<space>", self.check_word)
        self.entry.focus_set()
        
        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.pack()
    
    def check_word(self, event):
        typed_word = self.entry.get().strip()
        correct_word = self.words[self.current_word_index]
        
        if self.difficulty == "easy":
            typed_word = typed_word.lower()
            correct_word = correct_word.lower()
        
        if typed_word == correct_word:
            self.typed_text += correct_word + " "
        else:
            self.typed_text += typed_word + " "
        
        self.current_word_index += 1
        self.entry.delete(0, tk.END)
        
        self.update_display()
        
        if self.current_word_index >= len(self.words):
            self.show_results()
    
    def update_display(self):
        displayed_text = ""
        for i, word in enumerate(self.words):
            if i < self.current_word_index:
                displayed_text += word + " "
            elif i == self.current_word_index:
                displayed_text += "_" * len(word) + " "
            else:
                displayed_text += word + " "
        
        self.label.config(text=displayed_text, fg="grey")
        
        time_elapsed = max(time.time() - self.start_time, 1)
        wpm = round((len(self.typed_text) / 5) / (time_elapsed / 60))
        self.wpm_label.config(text=f"WPM: {wpm}")
    
    def show_results(self):
        self.clear_screen()
        total_time = max(time.time() - self.start_time, 1)
        final_wpm = round((len(self.typed_text) / 5) / (total_time / 60))
        
        result_label = tk.Label(self.root, text=f"Typing Test Completed!\nFinal WPM: {final_wpm}", font=("Arial", 14))
        result_label.pack(pady=10)
        
        restart_button = tk.Button(self.root, text="Restart", command=self.create_start_screen)
        restart_button.pack()
    
    def load_texts(self):
        return ["The quick brown fox jumps over the lazy dog", "Practice makes perfect", "Speed typing is fun and challenging"]
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()