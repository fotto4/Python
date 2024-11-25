import string
import time

text = 'Hello World'  #Text der uasgegeben wird
temp = ''
repetitions = 3  # Anzahl der Wiederholungen

for _ in range(repetitions):
    temp = ''  
    for ch in text:
        for i in string.printable:
            if i == ch:
                time.sleep(0.009)
                print(temp + i, end='\r')
                temp += ch
                break
            else:
                time.sleep(0.009)
                print(temp + i, end='\r')
    print()  
    time.sleep(1)  

print()  