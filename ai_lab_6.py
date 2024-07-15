import sys; args = sys.argv[1:]
#Vishal Kotha, 4

num = int(args[0]) - 40
if num == 0:
    print(r'/^[ox.]{64}$/i')
elif num == 1:
    print(r'/^[ox]*\.[ox]*$/i')
elif num == 2:
    print(r'/^(x+o*)?\.|\.(o*x+)?$/i')
elif num == 3:
    print(r'/^(..)*.$/s')
elif num == 4:
    print(r'/^(1?0|11)([01]{2})*$/')
elif num == 5:
    print(r'/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i')
elif num == 6:
    print(r'/^(1?0)*1*$/')
elif num == 7:
    print(r'/^\b[bc]*a?[bc]*$/')
elif num == 8:
    print(r'/^(a[bc]*a|b|c)+$/')
else:
    print(r'/^((1[02]*1|2)0*)+$/')

#Vishal Kotha, 4, 2023