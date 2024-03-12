"""Crumpets, by smallCabbage333 smallCabbage33@gmail.com
based on Al Sweigart's deductive logic game 'Bagels' where you 
must guess a number based on clues. His code is available at:
https://nostarch.com/big-book-small-python-programming
"""

import random
import string

class CrumpetsGame:
    def __init__(self, num_digits=8, max_guesses=10):
        self.NUM_DIGITS = num_digits
        self.MAX_GUESSES = max_guesses
        self.reset_game()


    def reset_game(self):
        """Resets the game state for a new game."""
        self.tested_chars = set()
        self.foundFermis = {} # Empty dict for found fermis in their positions.
        self.guessedPicos = {} # Empty dict for guessed picos in their last guessed positions.
        self.foundCrumpets = set()
        self.secret_code = self.get_secret_code()
        self.possibleChars = [char for char in string.ascii_lowercase + string.digits] # Initialize possibleChars.
        self.unmatched = {char: self.secret_code.count(char) for char in set(self.secret_code)} # Create dict to track unique instances per char in the secret_code.


    def get_secret_code(self):
        """Generates a secret code of random characters and digits."""
        characters = string.ascii_lowercase + string.digits
        # return ''.join(random.choice(characters) for _ in range(self.NUM_DIGITS))
        return '248cyuu8'


    def get_clues(self, guess):       
        clues = [''] * len(guess) # Initialize all clues empty.
        checkOver = {char: self.secret_code.count(char) for char in set(self.secret_code)} # Create dict to track unique instances per char in secret_code for 'Over's.
        
        # First pass for 'Fermi' clues
        for i, char in enumerate(guess):
            if char == self.secret_code[i]:
                clues[i] = 'Fermi'
                checkOver[char] -= 1
                self.foundFermis[i] = char
                self.unmatched[char] -= 1
                # code_counts[char] -= 1

        # Second pass for 'Pico' and 'Over' clues
        for i, char in enumerate(guess):
            if clues[i] == '':
                if char in self.secret_code:
                    # Check if additional occurrences of char are valid ('Pico') or excessive ('Over')
                    if checkOver[char] > 0:
                        clues[i] = 'Pico'
                        checkOver[char] -= 1
                        self.guessedPicos[i] = char
                        # code_counts[char] -= 1
                    else:
                        clues[i] = 'Over'
                else:
                    clues[i] = 'Crumpet'
                    self.foundCrumpets.add(char)
                    if clues[i] in self.possibleChars:
                        self.possibleChars.remove(char)

        if all(clue == 'Crumpet' for clue in clues):
            return 'Bagels'
        return ' '.join(clues)


    def get_hint(self):
        hint_options = []

        for _ in range(3):  # Generate 3 hint options.
            hint = ['_'] * self.NUM_DIGITS

            # Place found Fermis.
            for pos, char in self.foundFermis.items():
                hint[pos] = char
            
            # Insert 1 new unrevealed secret code character.
            unrevealed_chars = [char for char in self.secret_code if self.secret_code.count(char) > hint.count(char) and char not in self.foundCrumpets]
            if unrevealed_chars:
                available_positions = [i for i, ch in enumerate(hint) if ch == '_']
                new_char = random.choice(unrevealed_chars)
                new_pos = random.choice(available_positions)
                hint[new_pos] = new_char

            # Place guessed Picos at new positions.
            for pos, char in self.guessedPicos.items():
                available_positions = [i for i, ch in enumerate(hint) if ch == '_' and i != pos]  # Exclude original Pico positions.
                if available_positions:
                    new_pos = random.choice(available_positions)
                    hint[new_pos] = char

            # Fill the rest of the hint.
            for i in range(self.NUM_DIGITS):
                if hint[i] == '_':
                    # Exclude chars exceeding available instances.
                    possible_chars = [char for char in self.possibleChars
                                      if self.secret_code.count(char) > hint.count(char)]
                    if possible_chars:
                        hint[i] = random.choice(possible_chars)

            hint_options.append(''.join(hint))

        return hint_options


    def calculate_percentage_solved(self, clues):
        # Calculate the percentage of the secret code that's been correctly solved.
        if self.NUM_DIGITS == 0:  # Prevent division by zero.
            return 0
        percentage_solved = ((clues.count('Fermi')) / self.NUM_DIGITS) * 100
        return percentage_solved


    def play(self):
        print('''Crumpets, a deductive logic game.
              
By smallCabbage333 smallCabbage33@gmail.com
          
I am thinking of a {} secret code made up of letters and numbers.
Try to guess what it is. Here are some clues:
When I say:     That means:
Crumpets        The character does not exist in the code.      
Fermi           The character is a perfect match.
Pico            The character is in the wrong place.      
Over            There are too many of this character.      
Bagels          No characters are in the code.
          
For example, if the secret number was 248cyuu8 and your guess was c88uzt3c, the
clues would be Pico Pico Fermi Pico Crumpet Crumpet Crumpet Over'''.format(self.NUM_DIGITS) + '\n')
        
        # print(f"Guess the {self.NUM_DIGITS} character code. It could be any combination of digits or characters.\n")
        # print('The secret code: ' + str(self.secret_code) + '\n')  # Consider hiding in the final game.
        guesses = 0

        while guesses < self.MAX_GUESSES:
            guess = input(f"Guess #{guesses + 1}/{self.MAX_GUESSES}: ").lower()
            # guess = '9taa1z6g'
            # print(guess)
            if len(guess) != self.NUM_DIGITS:
                print(f"Please enter a {self.NUM_DIGITS}-character code.\n")
                continue

            guesses += 1
            clues = self.get_clues(guess)
            print(f"Clues: {clues}\n")

            # Calculate and display the percentage solved.
            percentage_solved = self.calculate_percentage_solved(clues)
            print(f"Percentage solved: {percentage_solved:.2f}%\n")

            if guess == self.secret_code:
                print("You got it!\n")
                break
            
            # Print a line separator for visual separation.
            print("-" * 100)  # Adjust the number of dashes based on your preferred width.

            hints = self.get_hint()
            print(f"Hints: {hints[0]}, {hints[1]}, {hints[2]}\n")

            if guesses == self.MAX_GUESSES:
                print(f"You ran out of guesses. The secret code was {self.secret_code}.\n")
                break  # Ensure the loop exits

        # Ask if player wants to play again.
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again.startswith('y'):
            print()  # Adding space before starting a new game.
            self.reset_game()  # Reset the game state.
            self.play()  # Start a new game.


if __name__ == '__main__':
    game = CrumpetsGame()
    game.play()
