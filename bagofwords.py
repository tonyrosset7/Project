import pandas as pd
import nltk
from nltk.corpus import wordnet

def process():
    data = 'abstracts_part.csv'
    df = pd.read_csv(data)
    abs = df['abstract_lem'].squeeze()    #to take the column and convert to series
    tabs = []
    toabs = []
    for n in abs.iteritems():
        for m in n:
            tabs.append(m)                #all column cells in a single list

    for i in tabs:
        if type(i) == str:                  #to remove the index numbers
            strings = i.split()
            for l in strings:
                if l == '@':
                    continue
                toabs.append(l)

    setabs = set(toabs)                         #bag of all abstract
    babs = list(setabs)                         #list of all the words in the abstract

    tok = {}
    for val in babs:
        synonyms = []
        for syn in wordnet.synsets(val):
            for l1 in syn.lemmas():
                synonyms.append(l1.name())

        s_synonyms = set(synonyms)
        count = 1
        word = []
        word.append(val)
        for val1 in babs:                                                  #comparing the synonyms with words
            if val1 == '@': continue
            for val3 in s_synonyms:
                if val3 == val1:
                    word.append(val1)
                    count = count + 1
                    babs = list(map(lambda x: x.replace(val1, '@'), babs))  #replacing the already found word with @

        if count > 2:
            words = val
            for l3 in word:                                            #joining the synonyms with underscore
                if l3 == val: continue
                words = '_'.join([words, l3])

            for l4 in word:                                            #making the synonyms and tokens
                tok[l4] = words
    print(tok)

    for token, syns in tok.items():
        for i in range(len(abs)):
            abs[i] = abs[i].replace(token, syns)
    print(abs)

    df['abstract_syns_replaced'] = abs
    print(df)

def main():
    process()


if __name__ == "__main__":
    main()

