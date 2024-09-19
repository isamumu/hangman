import operator
wordFreq = {}
priors = {}

# load the data into a dictionary
def loadFile():
    f = open('hw1_word_counts_05-2.txt') 
    lines = f.readlines()
    
    for index, line in enumerate(lines):
        #print(line.strip().split(' '))
        pair = line.strip().split(' ')
        wordFreq[pair[0]] = float(pair[1])
    
    print('done loading txt file!')

# load the prior statistics for each word frequency
def loadPriors():
    # P(w) = count(w) / sum(count(w))
    totalCount = 0
    for w in wordFreq:
        totalCount = totalCount + wordFreq[w]

    for w in wordFreq:
        priors[w] = float(wordFreq[w]) / totalCount 
    
    print('done loading priors!')

# identified function for P(i | w) which sees if char belongs in position of word
def letterInWord(word, letter):
    
    for i in range(1, 6):
        if(letter == word[i-1]):
            return 1
    
    return 0

# determins P(E | W) which is basically an identifier function
# failedLetters: a single list of attempted, but failed letters
# presentLetters: a list of pairs containing letter present (key) and index of letter (value)
def evidencePosterior(failedLetters, presentLetters, word):
    present = {}
    for p in presentLetters:
        letter = p[0]
        if(letter in present):
            present[letter] = present[letter] + 1
        else:
            present[letter] = 1
    
    # check if already failed letters do not belong to the word
    for c in failedLetters:
        # if the letter is a failed guess, it should not belong to the word
        if(c in word):
            return 0

    # check if the currently present letters belong to the word
    for pair in presentLetters:
        index = pair[1]
        letter = pair[0]

        # if the position is greater than the candidate size or
        # if the letter at the position does not match that of the word or
        if(index > len(word) - 1):
            return 0
        if(letter != word[index]):
            return 0

    # check if the letter is present, but missing in another position
    index = 0
    for c in word:
        if(c in present):
            if(present[c] <= 0):
                return 0
            else:
                present[c] = present[c] - 1

    # otherwise, the evidence so far matches the candidate word
    return 1

# determins P(W | E) 
def wordPosteriors(word, presentLetters, failedLetters):
    num = evidencePosterior(failedLetters, presentLetters, word) * priors[word]
    den = float(0)

    for w in wordFreq:
        den = den + priors[w] * evidencePosterior(failedLetters, presentLetters, w)
        
    return (num / den)

# applies for any available position, collective probability
def computePosterior(letter, presentLetters, failedLetters):
    sum = 0

    for w in wordFreq:
        sum = sum + letterInWord(w, letter) * wordPosteriors(w, presentLetters, failedLetters)
    
    return sum

def findMostLikelyLetter(presentLetters, failedLetters):
    letters = {}
    present = []

    for p in presentLetters:
        present.append(p[0])

    for i in range(65, 91):
        letter = chr(i)
        if letter not in present and letter not in failedLetters:
            letters[letter] = computePosterior(letter, presentLetters, failedLetters)
            print(letter, letters[letter])

    mostLikely = max(letters, key=letters.get)
    return [mostLikely, letters[mostLikely]]

def main():
    loadFile()
    loadPriors()

    # print 15 most frequent words
    # decreasingOrder = sorted(priors.items(), key=operator.itemgetter(1), reverse=True)
    
    # index = 0
    # for e in decreasingOrder:
    #     if(index == 15):
    #         break
    #     print(e[0])
    #     index = index + 1

    # print 14 least frequent words
    # increasingOrder = sorted(priors.items(), key=operator.itemgetter(1))
    # index = 0
    # for e in increasingOrder:
    #     if(index == 14):
    #         break
    #     print(e[0])
    #     index = index + 1
    
    # find most likely letter
    f = findMostLikelyLetter([],[])
    print(f)
    
if __name__ == "__main__":
    main()