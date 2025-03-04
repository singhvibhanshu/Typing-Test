import curses
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!\n")
    stdscr.addstr("Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm):
    stdscr.clear()
    stdscr.addstr(target + "\n")
    stdscr.addstr(f"WPM: {wpm}\n")
    
    for i, char in enumerate(current):
        if i < len(target):
            color = curses.color_pair(1 if char == target[i] else 2)
        else:
            color = curses.color_pair(2)  # Extra characters are always incorrect
        stdscr.addstr(char, color)

def load_text():
    with open("text.txt", "r") as f:
        return random.choice(f.readlines()).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        wpm = round((len(current_text) / max((time.time() - start_time) / 60, 1)) / 5)
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
            current_text.append(key)
        
        if "".join(current_text) == target_text:
            break  # Exit when correctly typed

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
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        
        try:
            key = stdscr.getkey()
        except curses.error:
            continue
        
        if key == "\x1b":
            break

curses.wrapper(main)