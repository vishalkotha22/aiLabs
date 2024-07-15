import math, random, re, sys, time; args = sys.argv[1:]
#words = open(args[0], 'r').read().splitlines()
words = open('wordsRE5.txt', 'r').read().splitlines()

s = '--s--###-sss-###ssss-###-ss-s---'
s2 = s + s[::-1]
print(s2)
startTime = time.time()
print('A:', len(words))
countB, countC, countD, countE = 0, 0, 0, 0
fWords = []
for word in words:
    if re.match('^[a-z]*$', word):
        countB += 1
    if re.match('^[a-z]{5}$', word):
        countC += 1
    if re.match('^[a-z]{5}$', word):
        init = False
        for letter in word:
            if word.index(letter) != word.rindex(letter):
                countD += 1
                init = True
                break
        if init:
            all = True
            for word2 in words:
                if word2 != word and re.match('^[a-z]{5}$', word2):
                    works = True
                    for c in word:
                        if c not in word2:
                            works = False
                            break
                    if works:
                        all = False
                        break
            if all:
                countE += 1
                fWords.append(word)
print('B:', countB)
print('C:', countC)
print('D:', countD)
print('E:', countE)
print('F:', sorted(fWords))
countG = 0
for word in fWords:
    works = True
    for i, c in enumerate(word):
        if i < len(word)-1 and word[i+1] == c:
            works = False
            break
    if works:
        countG += 1
print('G:', countG)
print('H:', str(time.time()-startTime)[:4]+'s')