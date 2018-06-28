import datefinder

while True:
    sentence=raw_input(">>")
    matches=datefinder.find_dates(sentence)
    for match in matches:
            print match
