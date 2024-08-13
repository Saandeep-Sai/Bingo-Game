import random
import pandas as pd
import numpy as np
import time

class Bingo:
    def __init__(self):
        # Initialize the game
        self.value = None  # Instance attribute to store the current value
        self.game_numbers = np.random.choice(range(1, 26), size=25, replace=False)
        self.bingo_card = pd.DataFrame(self.game_numbers.reshape((5, 5)), columns=['B', 'I', 'N', 'G', 'O'])
        
        self.sys_game_numbers = np.random.choice(range(1, 26), size=25, replace=False)
        self.sys_bingo_card = pd.DataFrame(self.sys_game_numbers.reshape((5, 5)), columns=['B', 'I', 'N', 'G', 'O'])
        self.sys_values = list(range(1, 26))
    
    def check_bingo(self, df):
        remaining_lines = [1, 2, 3, 4, 5]  # Array to track remaining lines

        def pop_line():
            """Pop an element from remaining_lines array."""
            if remaining_lines:
                remaining_lines.pop()

        # Check completed rows
        for i in range(5):
            if df.iloc[i].eq('X').all():
                pop_line()  # Pop an element when a row is completed
        
        # Check completed columns
        for j in range(5):
            if df.iloc[:, j].eq('X').all():
                pop_line()  # Pop an element when a column is completed
        
        # Check main diagonal (top-left to bottom-right)
        if all(df.iloc[i, i] == 'X' for i in range(5)):
            pop_line()  # Pop an element for the main diagonal
        
        # Check anti-diagonal (top-right to bottom-left)
        if all(df.iloc[i, 4-i] == 'X' for i in range(5)):
            pop_line()  # Pop an element for the anti-diagonal

        # Return True if the array is empty (i.e., len(remaining_lines) == 0)
        return len(remaining_lines) == 0

    def sys_search_and_replace(self, b1, b2, number):
        if (b1 == number).any().any():
            b1.replace(number, 'X', inplace=True)
            b2.replace(number, 'X', inplace=True)
            self.sys_values.remove(number)
            return self.check_bingo(b2)

    def search_and_replace(self, b1, b2, number):
        if (b1 == number).any().any():
            b1.replace(number, 'X', inplace=True)
            b2.replace(number, 'X', inplace=True)
            self.sys_values.remove(number)
            return self.check_bingo(b1)

    def player(self):
        self.value = int(input("Enter the number: "))
        result = self.search_and_replace(self.bingo_card, self.sys_bingo_card, self.value)
        return result

    def computer(self):
        self.value = random.choice(self.sys_values)
        print("I chose:", self.value)
        result = self.sys_search_and_replace(self.bingo_card, self.sys_bingo_card, self.value)
        return result

    def play_game(self):
        while True:
            print("Your Bingo Card:")
            print(self.bingo_card.to_string(index=False))

            player_result = self.player()
            if player_result:
                print("Player has won")
                break
            
            time.sleep(5)
            sys_result = self.computer()
            if sys_result:
                print("Computer has won")
                break

        print("\nFinal Bingo Cards:")
        print("\nYour Bingo Card:")
        print(self.bingo_card.to_string(index=False))
        print("\nComputer's Bingo Card:")
        print(self.sys_bingo_card.to_string(index=False))
