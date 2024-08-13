import tkinter as tk
from tkinter import messagebox, Toplevel
from bingo import Bingo  # Ensure bingo.py is in the same directory or in your PYTHONPATH

class BingoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Game")
        self.root.iconbitmap("bingo.ico")

        # Set the window position (no size change)
        self.root.geometry("+200+100")  # Position the window at 200 pixels from the left and 100 pixels from the top

        # Set background color to black
        self.root.configure(bg='black')

        # Initialize the Bingo game
        self.bingo_game = Bingo()

        # Create a frame for the player's Bingo card with black background
        self.player_frame = tk.Frame(self.root, padx=10, pady=10, bg='black')
        self.player_frame.grid(row=0, column=0)

        # Create a label for the frame with white text
        tk.Label(self.player_frame, text="Your Bingo Card", font=("Helvetica", 16), fg='white', bg='black').grid(row=0, column=0, columnspan=5)

        # Create buttons for the player's Bingo card with white text, black background, and white border
        self.player_buttons = []
        for i in range(5):
            for j in range(5):
                button = tk.Button(self.player_frame, text=self.bingo_game.bingo_card.iloc[i, j], font=("Helvetica", 14),
                                   width=4, height=2, command=lambda x=i, y=j: self.player_move(x, y),
                                   fg='white', bg='black', highlightbackground='white', highlightcolor='white', highlightthickness=2)
                button.grid(row=i + 1, column=j)
                self.player_buttons.append(button)

    def player_move(self, x, y):
        number = self.bingo_game.bingo_card.iloc[x, y]
        if number != 'X':  # Make sure the number hasn't been selected already
            self.bingo_game.search_and_replace(self.bingo_game.bingo_card, self.bingo_game.sys_bingo_card, number)
            self.update_buttons()
            if self.bingo_game.check_bingo(self.bingo_game.bingo_card):
                self.show_computer_card()
                messagebox.showinfo("Bingo", "Player has won!")
            else:
                # Add a delay before the computer makes its move
                self.root.after(1000, self.computer_move)  # 1000 milliseconds = 1 second

    def computer_move(self):
        result = self.bingo_game.computer()
        self.update_buttons()
        if result:
            
            self.show_computer_card()
            messagebox.showinfo("Bingo", "Computer has won!")

    def update_buttons(self):
        for i in range(5):
            for j in range(5):
                player_num = self.bingo_game.bingo_card.iloc[i, j]
                self.player_buttons[i * 5 + j].config(text=player_num)
                if player_num == 'X':
                    self.player_buttons[i * 5 + j].config(state=tk.DISABLED, bg='lightblue')

    def show_computer_card(self):
        # Create a new window to show the computer's Bingo card
        comp_window = Toplevel(self.root)
        comp_window.title("Computer's Bingo Card")

        # Set the window position (no size change)
        comp_window.geometry("+900+100")  # Position the window at 800 pixels from the left and 100 pixels from the top
        comp_window.iconbitmap("bingo.ico")
        # Set background to black for the computer's Bingo card window
        comp_window.configure(bg='black')

        comp_frame = tk.Frame(comp_window, padx=10, pady=10, bg='black')
        comp_frame.grid(row=0, column=0)

        tk.Label(comp_frame, text="Computer's Bingo Card", font=("Helvetica", 16), fg='white', bg='black').grid(row=0, column=0, columnspan=5)

        for i in range(5):
            for j in range(5):
                comp_button = tk.Button(comp_frame, text=self.bingo_game.sys_bingo_card.iloc[i, j],
                                        font=("Helvetica", 14), width=4, height=2, state=tk.DISABLED,
                                        fg='white', bg='black', highlightbackground='white', highlightcolor='white', highlightthickness=2)
                comp_button.grid(row=i + 1, column=j)
                if self.bingo_game.sys_bingo_card.iloc[i, j] == 'X':
                    comp_button.config(bg='lightcoral')

        # Close the main game window
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoGUI(root)
    root.mainloop()
