import sys; args = sys.argv[1:]
#Vishal Kotha, 4

num = int(args[0]) - 50
if num == 0:
    print(r'/\b\w*(\w)\w*\1\w*/i')
elif num == 1:
    print(r'/\b\w*(\w)(\w*\1){3}\w*\b/i')
elif num == 2:
    print(r'/^$/i')
elif num == 3:
    print(r'/\b(?=\w*cat)\w{6}\b/i')
elif num == 4:
    print(r'/\b(?=\w*bri)(?=\w*ing)\w{5,9}\W/im')
elif num == 5:
    print(r'/\b(?!cat)\w{6}\b/i')
elif num == 6:
    print(r'/\b((\w)(?!\1))*\b/i')
elif num == 7:
    print(r'/^(?!.*10011).*$/ms')
elif num == 8:
    print(r'/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i')
else:
    print(r'/^(?!.*101)(?!.*111).*$/ms')

'''
Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.
'''

#Vishal Kotha, 4, 2023