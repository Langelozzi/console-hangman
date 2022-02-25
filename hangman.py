#Author: Lucas Angelozzi
#Date: 01/17/22

'''This file contains classes that together make the game hangman'''

#imports
import random

#secret word class
class SecretWord:
    """Class that creates a secret word for hangman and 
    contains methods pertaining to that word.
    """
    
    def __init__(self, word=None):
        if word is not None:
            self._secret_word = word.upper()
        
        else:
            #This will select a random word from the words file if the user does not input a word manually when creating the instance
            with open("words.txt") as words:
                reader = words.readlines()
                word_list = []

                for line in reader:
                    word = line.upper().strip()
                    word_list.append(word)
            
            self._secret_word = random.choice(word_list)

    def show_letters(self, letters):
        """This method will return any correct letters that were guessed 
        by the player and underscores for those that are still to be guessed.

        Args:
            letters (set): list of letters that the user has guessed

        Returns:
            string: the string containing correct letters and underscores
        """

        #placing letters in a list before converting to string in return statment
        my_string = []

        for letter in self._secret_word.upper():
            if letter in letters:
                my_string.append(letter)
            else:
                my_string.append("_")

        return " ".join(my_string)

    def check_letters(self, letters):
        """This method checks if all the letters have been guessed by the player to
        determine if they have won or not.

        Args:
            letters (set): the letters that have been guessed so far

        Returns:
            bool: whether or not all the letters have been guessed
        """
        
        current_word = self.show_letters(letters)
        secret_word_letters = current_word.split(" ")

        #checking to see if all of the letters that have been guessed are part of the word using the issubest method
        if set(secret_word_letters).issubset(letters):
            return True
        else:
            return False
    
    def check(self, word):
        """Checks to see if the word that was guessed is the secret word

        Args:
            word (string): the full word the user guessed

        Returns:
            bool: whether or not the guess is the same as the secret word
        """
        return (word.upper() == self._secret_word)

#actual gameplay class
class Game:
    """This class creates a game object that will actually run the hangman game.
    """
    
    def __init__(self, turns) -> None:
        self.word = SecretWord()
        self.turns_remaining = turns
        self.letters = set()

    def play_one_round(self):
        """This method will allow the user to guess a letter or a full word 
        and then uses methods from the SecretWord class to check if the user
        is correct

        Returns:
            bool: whether or not the user has guessed the word/all the letters
        """
        
        #shows the initial blank spaces for the user
        print(self.word.show_letters(self.letters), "\n")

        user_in = input("Please enter a letter: ").upper()

        #reprompts for letter if its already been said or if its not a letter
        while user_in in self.letters or user_in.isalpha() == False:
            user_in = input("Please enter a valid letter you have not previously guessed: ").upper()

        #functionality to allow user to guess the full word
        if user_in == "CHECK":
            full_word = input("Please enter what you think the word is: ").upper()
            correct = self.word.check(full_word)
            return correct

        #adds the users guessed word to the set of letters 
        self.letters.add(user_in)
        
        return self.word.check_letters(self.letters)

    def play(self):
        """This function loops through the play_one_round function as many times as 
        the object is specified for turns. It also prints statements if the user wins
        or loses.
        """
        
        #will leave loop once user runs out of turns
        while self.turns_remaining > 0:
            #printing a dotted line to visually seperate each turn
            print("\n<----------------------------New Turn------------------------------->")
            print(f"Turns left: {self.turns_remaining}\n")
            
            #play_one_round will return true if the user has guess all letters
            victory = self.play_one_round()

            if victory == True:
                print("\nCongratulations, you guessed the word!!")
                exit()
            
            #decrementing the turns so the player loses a turn each round
            self.turns_remaining -= 1

        print(f"\nYou Lose :(\nThe word was: {self.word._secret_word}")


#runs a normal game of 10 turns if this file is run
if __name__ == "__main__":
    game = Game(10)
    game.play()