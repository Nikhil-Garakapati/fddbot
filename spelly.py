import re
from collections import counter

def correction(word): 
    return max(candidates(word), key=P)

    while True:
    	word=raw_input(">>")
    	matches=correction(word)
    	for match in matches:
    		print match
