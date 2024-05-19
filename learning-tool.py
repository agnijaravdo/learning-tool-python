from simple_term_menu import TerminalMenu

def main():
    show_starting_menu()

def show_starting_menu():
    options = ["Add Questions", "View Statistics", "Disable/Enable Questions", "Practice Mode", "Test Mode"]
    terminal_menu = TerminalMenu(options, title= "\nUse ↓ or ↑ arrow keys to navigate and 'Enter' to select:\n", menu_cursor_style = ("fg_green", "bold"))
    menu_entry_index = terminal_menu.show()
    print(f"\nYou have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()
