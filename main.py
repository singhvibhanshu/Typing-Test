import curses
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!\n")
    stdscr.addstr("Choose difficulty: [1] Easy | [2] Medium | [3] Hard\n")
    stdscr.refresh()
    key = stdscr.getkey()
    return key

def display_text(stdscr, target, current, wpm):
    stdscr.clear()
    stdscr.addstr(target + "\n")
    stdscr.addstr(f"WPM: {wpm}\n")
    
    target_words = target.split()
    current_words = "".join(current).split()
    
    for i, word in enumerate(current_words):
        if i < len(target_words):
            color = curses.color_pair(1 if word == target_words[i] else 2)
        else:
            color = curses.color_pair(2)
        stdscr.addstr(word + " ", color)

def load_text(mode):
    with open("text.txt", "r") as f:
        lines = f.readlines()
        text = random.choice(lines).strip()
    
    if mode == "1":  # Easy mode (ignore case sensitivity)
        return text.lower()
    elif mode == "2":  # Medium mode (case-sensitive)
        return text
    elif mode == "3":  # Hard mode (include symbols)
        return text + "!@#$%^&*()"  # Add some random symbols for difficulty
    return text

def wpm_test(stdscr, mode):
    target_text = load_text(mode)
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        wpm = round((len("".join(current_text)) / max((time.time() - start_time) / 60, 1)) / 5)
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except curses.error:
            continue

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif key == "\x1b":
            return  # Exit on ESC
        else:
            if mode == "1":  # Easy mode ignores case sensitivity
                current_text.append(key.lower())
            else:
                current_text.append(key)

        if len("".join(current_text)) >= len(target_text):
            break  # Exit when typed enough characters

    # Calculate final WPM
    total_time = max(time.time() - start_time, 1)
    final_wpm = round((len(target_text) / (total_time / 60)) / 5)
    
    stdscr.nodelay(False)  # Disable nodelay before showing completion message
    stdscr.clear()
    display_text(stdscr, target_text, current_text, final_wpm)
    stdscr.addstr(f"\nYou completed the text!\nYour final WPM: {final_wpm}\n")
    stdscr.addstr("Press any key to continue or ESC to quit...")
    stdscr.refresh()
    stdscr.getkey()

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    mode = start_screen(stdscr)
    while True:
        wpm_test(stdscr, mode)
        
        try:
            key = stdscr.getkey()
        except curses.error:
            continue
        
        if key == "\x1b":
            break

curses.wrapper(main)
