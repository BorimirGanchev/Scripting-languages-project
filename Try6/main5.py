from nltk.stem import PorterStemmer

def check_root(word1, word2):
    stemmer = PorterStemmer()
    root1 = stemmer.stem(word1)
    root2 = stemmer.stem(word2)
    
    if root1 in root2 or root2 in root1:
        return True
    else:
        return False

# Example usage
word1 = "head"
word2 = "pain"
result = check_root(word1, word2)
print(result)  # Output: True
