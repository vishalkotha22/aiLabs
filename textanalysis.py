import nltk, re
#nltk.download()

book = open('mobydick.txt', 'r').read()
book = book.replace('\n', ' ')

words = book.split()
'''
willRemove = set()
for i, word in enumerate(words):
    if not re.match('^'+'\w'*len(word)+'$', word):
        if '.org' or 'gutenberg' in word.lower():
            willRemove.add(i)
for i, idx in enumerate(willRemove):
    del words[idx-i]
'''
typesCount = {}
wordCount = {}
types = nltk.pos_tag(words)
for type in types:
    if type[1] not in typesCount:
        typesCount[type[1]] = 0
    typesCount[type[1]] = typesCount[type[1]] + 1
    if len(type[0]) not in wordCount:
        wordCount[len(type[0])] = 0
    wordCount[len(type[0])] = wordCount[len(type[0])] + 1
print(wordCount)
print(typesCount)
quotes = []
for i in range(len(book)):
    if book[i] == '"':
        quote = '"'
        while i+1 < len(book) and book[i+1] != '"':
            quote += book[i+1]
            i += 1
        if i+1 < len(book):
            quote += book[i+1]
            i += 1
        quotes.append(quote)
print(len(quotes)-50)

#print(nltk.pos_tag(words))