# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    sw = list(secret_word) 
    seen = {}
    sw[:] = [seen.setdefault(l, l) for l in sw if l not in seen]
    all_letters_guessed = False
    
    for letter in sw:
        if len(letters_guessed) < len(sw):
            break
        for i, guess in enumerate(letters_guessed):
            if guess == letter:
                all_letters_guessed = True
                break
            elif (len(letters_guessed)-1) == i:
                return False
            else:
                continue

    return all_letters_guessed   


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word_list = list(secret_word)
    guessed_string = ''
    
    for letter in secret_word_list:
        for i, guess in enumerate(letters_guessed):
            if letter == guess:
                guessed_string += guess
                break
            elif (len(letters_guessed)-1) == i:
                guessed_string +=  '_ '
            else:
                continue
    return guessed_string



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    alphabet = string.ascii_lowercase
    alphabet_list = list(alphabet)
    
    for letter in letters_guessed:
        if letter in alphabet_list:
            alphabet_list.remove(letter)
        else:
            continue
    available_letters = ''.join(alphabet_list)
    return available_letters
 

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''        
    def is_game_over(is_word_guessed, guesses, warnings) :
        is_over = False
        if any([is_word_guessed, guesses <= 1, warnings <= 0]):
            is_over = True
        return is_over
    
    def is_vowel(guess) :
        vowels= ['a','e','i','o']
        return guess in vowels
        
    def has_been_guessed(guess, guess_list) :
        guess_set = set(guess_list)
        return guess in guess_set
        
    def is_guess_in_word(guess, secret_word) :
        return guess in secret_word
        
    def guesses_cap(guesses, num) :
        if guesses + num >= 6:
            guesses = 6
        else:
            guesses += num
        return guesses
    
         
    guesses, guessed_letters, warnings = 6, [], 3
    length = len(secret_word)
    break_line = '\n-------------'
    print('Welcome to the game Hangman!\nI am thinking of a word that is %d letters long.'%(length)+break_line)   
    word_comp = is_word_guessed(secret_word, guessed_letters)
    game_is_over = is_game_over(word_comp, guesses, warnings)
    
    while not game_is_over:
        
        available_letters = get_available_letters(guessed_letters)
        word_string = get_guessed_word(secret_word, guessed_letters)
        print('You have %d guesses left.\nAvailable letters: %s'%(guesses, available_letters))
        guess = str.lower(input('Please guess a letter: '))
        
        
        if str.isalpha(guess):
            if has_been_guessed(guess, guessed_letters):
                warnings -= 1
                game_is_over = is_game_over(word_comp, guesses, warnings)
                if game_is_over:
                    break
                else:
                    print('guessed before, warning', warnings)
            else:
                guessed_letters.append(guess)
                word_comp = is_word_guessed(secret_word, guessed_letters)
                word_string = get_guessed_word(secret_word, guessed_letters)
                game_is_over = is_game_over(word_comp, guesses, warnings)
                if is_vowel(guess):                    
                    if is_guess_in_word(guess, secret_word):
                        guesses = guesses_cap(guesses, 2)
                        if game_is_over:
                            break
                        else:
                            print('vowel correct', word_string)
                    else:
                        guesses -= 2
                        print('vowel incorrect')
                else:
                    if is_guess_in_word(guess, secret_word):
                        if game_is_over:
                            print('hit')
                            break
                        else:
                            print('const correct', word_string)
                    else:
                        guesses -= 1
                        print('const incorrect', word_string)
        else:
            warnings -= 1
            game_is_over = is_game_over(word_comp, guesses, warnings)
            if game_is_over:
                break
            else:
                print('non alpha character', warnings)
#
#        if guess_string.find(guess) > -1:
#            guessed_letters.append(guess)
#            boolean = is_word_guessed(secret_word, guessed_letters)
#            if boolean:
#                break
#            else:
#                print('Good guess: %s' %(guess_string) + break_line)
#        else:
#            print('Oops! That letter is not in my word: %s' %(guess_string) + break_line)
#
#        guesses -= 1
        
    if is_word_guessed(secret_word, guessed_letters):
        print('Congratulations, you won!')
    else:
        print('Sorry, you ran out of guesses. The word was %s'%(secret_word))
        
        
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    secret_word = 'apple'
    #secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
