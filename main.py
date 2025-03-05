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
        tk.Label(self.root, text="Choose Difficulty:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Easy", command=lambda: self.start_test("easy")).pack()
        tk.Button(self.root, text="Medium", command=lambda: self.start_test("medium")).pack()
        tk.Button(self.root, text="Hard", command=lambda: self.start_test("hard")).pack()

    def start_test(self, difficulty):
        self.text = random.choice(self.text_options)
        if difficulty == "easy":
            self.text = self.text.lower()
        self.start_time = time.time()

        self.clear_screen()
        
        self.label = tk.Label(self.root, text=self.text, font=("Arial", 14), fg="grey")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.entry.pack()
        self.entry.bind("<space>", self.process_word)
        self.entry.bind("<Return>", self.process_word)
        self.entry.focus_set()

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.pack()

        self.typed_words = []  # Store words typed so far
        self.index = 0         # Track word index

    def process_word(self, event):
        typed_text = self.entry.get().strip()
        words_original = self.text.split()

        if self.index < len(words_original):
            correct_word = words_original[self.index]
            if typed_text != correct_word:
                self.typed_words.append(f"[{typed_text}]")  # Mark incorrect words
            else:
                self.typed_words.append(typed_text)

            self.index += 1  # Move to the next word
            self.entry.delete(0, tk.END)  # Clear input field

        # Update displayed text
        updated_text = " ".join(self.typed_words) + " " + " ".join(words_original[self.index:])
        self.label.config(text=updated_text, fg="grey")

        # Update WPM
        time_elapsed = max(time.time() - self.start_time, 1)
        wpm = round((len(" ".join(self.typed_words)) / 5) / (time_elapsed / 60))
        self.wpm_label.config(text=f"WPM: {wpm}")

        # If all words are typed, finish the test
        if self.index >= len(words_original):
            self.show_results()

    def show_results(self):
        self.clear_screen()
        total_time = max(time.time() - self.start_time, 1)
        final_wpm = round((len(self.text) / 5) / (total_time / 60))

        result_label = tk.Label(self.root, text=f"Typing Test Completed!\nFinal WPM: {final_wpm}\nIncorrect Words: {' '.join(self.typed_words)}", font=("Arial", 14))
        result_label.pack(pady=10)

        tk.Button(self.root, text="Restart", command=self.create_start_screen).pack()

    def load_texts(self):
        return ["The quick brown fox jumps over the lazy dog", "Practice makes perfect", "Speed typing is fun and challenging"]

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()
