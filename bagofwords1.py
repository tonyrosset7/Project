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


    words = set(toabs)                          #bag of words from all the abstracts

    #print(words)

    synonyms = []
    already_found = set()
    unique_syn = set()
    for i, word in enumerate(list(words)):
        #print(f"{i}/{len(words)}, {word}")
        # the following function is the current culprit: if the list of synonyms is accurate and complete,
        # then we are ok, otherwise we may have distinct synonyms, such as in the case of summarization and summarize
        syns = wordnet.synsets(word)
        # the code below is ok in constructing the synonyms
        for syn in syns:
            lemmas = syn.lemmas()
            names = [x.name() for x in lemmas]
            current_syn = word

            for w in words:
                if w in already_found:
                    continue
                if w == word:
                    continue
                if w in names:
                    #print(f'find synonym: word "{word}" synonym "{w}"')
                    current_syn += '_' + w
                    already_found.add(w)
                    #print('synonyms: ', synonyms)
            #print(names)
            if '_' in current_syn:
                unique_syn.add(current_syn)
        #input()
    print(unique_syn)
    print(len(unique_syn))

    # here now we have to replace the original words in the abstracts with the synonyms


def main():
    process()


if __name__ == "__main__":
    main()
