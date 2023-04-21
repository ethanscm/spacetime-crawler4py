import sys
import re

# Time Complexity: linear time
    # The function will iterate through each character: O(n)
        # Building the token character by character will take O(1)
        # In each iteration, when a token is fully built, adding the token 
        # to the list will on average run in constant time: O(1)
    # O(n*(1+1)) = O(n)
def tokenize(text):
    tokens = []

    alphanum = re.compile("^[a-z]|[0-9]&")

    stop_words = []

    #reads character by character to minimize ram usage
    #reads in byte mode so that the file pointer is moved on read

    word = ""
    for char in text:    
        char = char.lower()
        # O(1) since char will always be 1 character long
        if(alphanum.search(char)): 
            # builds tokens as it iterates through each character
            word += char
        else:
            # add fully built token to list
            if(word != ""):
                tokens.append(word)
                word = ""
            if(char == ""):
                break

    return tokens

# Time Complexity: linear time
    # The function will iterate through each token: O(n)
        # Each iteration will update the dictionary value: O(1)
        # dictionary access takes constant time due to hashing
    # O(n*1) = O(n)
def computeWordFrequencies(tokens):
    # Use a dictionary to map tokens to frequency count
    freq = {}

    #increments the count of each token
    for t in tokens:
        if(t not in freq):
            freq[t] = 1
        else:
            freq[t] += 1

    return freq

# Time Complexity: quadratic time
    # The function first converts the dictionary into a list: O(n)
    # Then it sorts the list via selection sort: O(n^2)
    # Lastly it prints each token and their frequency: O(n)
    # O(n + n^2 + n) = O(n^2)
def printFreq(freq):
    # convert into list to make sorting work
    tokens = [f for f in freq]

    #insertion sort
    for i in range(1, len(tokens)):
        j = i
        #compares frequency first then alphabetical order
        while(j > 0 and freq[tokens[j]] >= freq[tokens[j-1]]):
            if(freq[tokens[j]] == freq[tokens[j-1]] and tokens[j] > tokens[j-1]):
                j -= 1
                continue

            temp = tokens[j-1]
            tokens[j-1] = tokens[j]
            tokens[j] = temp
            j -= 1
    
    #print sorted tokens
    for t in tokens:
        print(f'{t} {freq[t]}')