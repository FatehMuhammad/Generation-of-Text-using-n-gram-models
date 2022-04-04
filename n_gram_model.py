################################################################
# Imports (Numpy and NLTK not allowed)
import string
import random
################################################################
# Reference: Given as a Homework at University of Pennsylvania
# Author: Fateh Muhammad
# You can only use it for study or teaching Purposes
################################################################

def tokenize(text):
    Text = text.strip()
    punct = list(string.punctuation)
    tokens = []
    for letter in Text:
        if letter in punct:
            tokens.append(letter)
            Text = Text.replace(letter, " ")
    tokens =  Text.split(' ') + tokens
    tokens = [token for token in tokens if token != ""]
    return tokens

def ngrams(n, tokens):
    tokens = tokens + ['<END>']
    n_grams = []
    for idx in range(len(tokens)):
        idx1 = idx - (n-1)
        if(idx1 < 0):
            start_edit = ['<START>'] * abs(idx1)
            n_grams.append((tuple(start_edit+tokens[:idx]), tokens[idx]))
        else:
            n_grams.append((tuple(tokens[(idx-n)+1:idx]), tokens[idx]))
    return n_grams

class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.n_grams = []

    def update(self, sentence):
        self.n_grams = self.n_grams + ngrams(self.order, tokenize(sentence))

    def prob(self, context, token):
        count = 0
        for n_gram in self.n_grams:
            if(n_gram == (context, token)):
                count += 1
        return ( count / len(self.n_grams) )
    
    def random_token(self, context):
        Set_Of_Tokens = []
        all_tokens = []
        r = random.random()
        if(self.order != 1):
            context = context

        for token in self.n_grams:
            if(token[0] == context):
                all_tokens.append(token[1])
                Set_Of_Tokens.append(token[1])
        all_tokens = sorted(set(all_tokens))
        try:
            return random.choice(all_tokens)
        except:
            return ""
        
    def random_text(self, token_count):
        generated_text  = ""
        if(self.order != 1):
            context = tuple( ['<START>'] * ( self.order - 1))
        else:
            context = ()
        for idx in range(token_count):
            
            generated_text = generated_text + " " + self.random_token(context)
            if(self.order != 1):
                context = random.choice(self.n_grams)[0]
                if(context == tuple( ['<END>'] * ( self.order - 1)) ):
                    context = tuple( ['<START>'] * ( self.order - 1))
                    
        return generated_text.strip()

    def perplexity(self, sentence):
        all_tokens = tokenize(sentence)
        n_gramms = ngrams(self.order, all_tokens)
        probab = 0.0
        for n_gram in n_gramms:
            probab += self.prob(n_gram[0], n_gram[1])
        return (1/probab)**(1/len(all_tokens) + 1)
        
def create_ngram_model(n, path):
    m = NgramModel(n)
    file_handler = open(path)
    for line in file_handler.readlines():
        m.update(line)
    return m.random_text(15)

def main():

    print()
    print('Testing Started ...')
    print()

    # # Test1
    print('Test1 for Function1 started.')
    print()
    print(tokenize("   This is an example.   "))
    print(tokenize(" 'Medium-rare,' she said."))
    print()

    # # Test 2
    print('Test2 for Function2 started.')
    print()

    print(ngrams(1, ["a","b","c"]))
    print(ngrams(2, ["a","b","c"]))
    print(ngrams(3, ["a","b","c"]))
    print()

    # # Test 3
    print('Test3 for Function3 started.')
    print()

    m = NgramModel(1)
    m.update("a b c d")
    m.update("a b a b")
    print(m.prob((),"a"))
    print(m.prob((),"c"))
    print(m.prob((),"<END>"))
    print()

    m=NgramModel(2)
    m.update("a b c d")
    m.update("a b a b")
    print(m.prob(("<START>",),"a"))
    print(m.prob(("a",),"x"))
    print()

    # # Test 4
    print('Test4 for Function4 started.')
    print()

    m=NgramModel(1)
    m.update("a b c d")
    m.update("a b a b")
    random.seed(1)
    print([m.random_token(()) for i in range(25)])
    print()

    m=NgramModel(2)
    m.update("a b c d")
    m.update("a b a b")
    random.seed(2)
    print([m.random_token(("<START>",)) for i in range(6)])
    print()
    print([m.random_token(("b",)) for i in range(6)])
    print()

    # # Test 5
    print('Test5 for Function5 started.')
    print()

    m=NgramModel(1)
    m.update("a b c d")
    m.update("a b a b")
    random.seed(1)
    print(m.random_text(13))
    print()

    m=NgramModel(2)
    m.update("a b c d")
    m.update("a b a b")
    random.seed(2)
    print(m.random_text(15))
    print()

    # # Test 6
    print('Test6 for Function6 started.')
    print()

    print(create_ngram_model(1,"text.txt"))
    print()
    print(create_ngram_model(2,"text.txt"))
    print()
    print(create_ngram_model(3,"text.txt"))
    print()
    print(create_ngram_model(4,"text.txt"))
    print()
    
    # # Test 7
    print('Test7 for Function7 started.')
    print()

    m=NgramModel(1)
    m.update("a b c d")
    m.update("a b a b")
    print(m.perplexity("a b"))
    print()

    m=NgramModel(2)
    m.update("a b c d")
    m.update("a b a b")
    print(m.perplexity("a b"))
    print()

if (__name__ == "__main__"):
    main()