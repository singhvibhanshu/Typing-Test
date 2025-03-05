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
        self.difficulty = difficulty
        self.text = random.choice(self.text_options[difficulty])
        self.start_time = time.time()
        self.correct_characters = 0  # Track correct characters

        self.clear_screen()
        
        self.label = tk.Label(self.root, text=self.text, font=("Arial", 14), fg="grey")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.update_wpm)  # Update WPM on each key release
        self.entry.bind("<space>", self.process_word)
        self.entry.bind("<Return>", self.process_word)
        self.entry.focus_set()

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.pack()

        self.typed_words = []
        self.index = 0

    def process_word(self, event):
        typed_text = self.entry.get().strip()
        words_original = self.text.split()

        if self.index < len(words_original):
            correct_word = words_original[self.index]
            is_correct = False

            if self.difficulty == "easy":
                is_correct = typed_text.lower() == correct_word.lower()
            else:
                is_correct = typed_text == correct_word

            if is_correct:
                self.typed_words.append(correct_word)
                self.correct_characters += len(correct_word)
            else:
                self.typed_words.append(f"[{typed_text}]")

            self.index += 1
            self.entry.delete(0, tk.END)

            # Update displayed text
            updated_text = " ".join(self.typed_words) + " " + " ".join(words_original[self.index:])
            self.label.config(text=updated_text.strip(), fg="grey")

            # Check if all words are typed
            if self.index >= len(words_original):
                self.show_results()

    def update_wpm(self, event=None):
        if hasattr(self, 'start_time'):
            time_elapsed = max(time.time() - self.start_time, 1)
            wpm = round((self.correct_characters / 5) / (time_elapsed / 60))
            self.wpm_label.config(text=f"WPM: {wpm}")

    def show_results(self):
        self.clear_screen()
        total_time = max(time.time() - self.start_time, 1)
        final_wpm = round((self.correct_characters / 5) / (total_time / 60))

        result_text = f"Typing Test Completed!\nFinal WPM: {final_wpm}\n"
        result_text += f"Incorrect Words: {' '.join([word for word in self.typed_words if word.startswith('[')])}"
        
        result_label = tk.Label(self.root, text=result_text, font=("Arial", 14))
        result_label.pack(pady=10)

        tk.Button(self.root, text="Restart", command=self.create_start_screen).pack()

    def load_texts(self):
        return {
            "easy": [
                "The cat sat on the mat", 
                "I love to read books", 
                "Sun is shining bright"
            ],
            "medium": [
                "Typing fast requires consistent Practice.", 
                "A quick brown Fox jumps over the lazy Dog.", 
                "Good habits make Learning easier."
            ],
            "hard": [
                "Complex algorithms & data structures optimize performance!", 
                "AI is revolutionizing the world in 2025 with #DeepLearning.", 
                "C0d!ng is fun @3AM, but Debugging is a nightmare!"
            ]
        }

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()