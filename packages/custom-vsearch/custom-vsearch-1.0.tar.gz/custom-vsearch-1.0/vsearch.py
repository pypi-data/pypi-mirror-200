def search4vowels(word):
    #The line below it's known as docstring
    """Display any vowels found in a provided word."""
    vowels = set('aeiou')
    found = sorted(vowels.intersection(set(word)))
    for vowel1 in found:
        print(vowel1)

def search4letters(phrase:str, letters:str = 'aeiou') -> set:
    #The argument details are called annotations
    #We specify the type of argument we expect and the return type this function gives.
    #The line below it's known as docstring
    """Display any letter found in a provided phrase."""
    return set(letters).intersection(set(phrase))
