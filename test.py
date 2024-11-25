import string
import time

text = 'Hello World'
temp = ''

for ch in text:
    for i in string.printable:
        if i == ch:
            temp += ch
            print(temp)
            time.sleep(0.2)  # Zeit in Sekunden, die zwischen den einzelnen Zeichen vergeht
            break
        else:
            print(temp + i, end='\r')
            time.sleep(0.02)  # Kürzere Verzögerung für den Suchprozess
    print()  # Zeilenumbruch, um das nächste Zeichen in einer neuen Zeile zu starten

print()  # Zeilenumbruch am Ende des Textes
