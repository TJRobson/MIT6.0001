# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.    
    '''
    permutations_list = []
    
    def perm_sec(string):
        
        reverse = string[::-1]
        permutations_list.append(reverse)
        first_letter = reverse[0]
        cut_string = reverse[1:]
        cut_reverse = cut_string[::-1]
        the_next_string = first_letter+cut_reverse
        permutations_list.append(the_next_string)
        
        if the_next_string == sequence:
            return
        else:
            return perm_sec(the_next_string)
    
    perm_sec(sequence)
      
    return permutations_list      


if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    print('for letters', get_permutations('a'))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


