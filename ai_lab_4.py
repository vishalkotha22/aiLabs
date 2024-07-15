import sys; args = sys.argv[1:]
#Vishal Kotha, 4

num = int(args[0])
if num == 30:
    print(r'/^0$|^10[01]$/')
elif num == 31:
    print(r'/^[01]*$/')
elif num == 32:
    print(r'/0$/')
elif num == 33:
    print(r'/\w*[aeiou]\w*[aeiou]\w*/i')
elif num == 34:
    print(r'/^0$|^1[01]*0$/')
elif num == 35:
    print(r'/^[01]*110[01]*$/')
elif num == 36:
    print(r'/^.{2,4}$/s')
elif num == 37:
    print(r'/^\d{3} *-? *\d\d *-? *\d{4}$/')
elif num == 38:
    print(r'/^.*?d\w*/im')
else:
    print(r'/^[01]?$|^0[01]*0$|^1[01]*1$/')

#Vishal Kotha, 4, 2023