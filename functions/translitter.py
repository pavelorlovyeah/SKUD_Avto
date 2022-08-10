# from datetime import datetime
# from time import sleep

# start = datetime.now()
# sleep(2)
# delta = datetime.now() - start
# print(delta.total_seconds() > 5)

letters = {
    'A' : 'А',
    'B' : 'В',
    'E' : 'Е',
    'K' : 'К',
    'M' : 'М',
    'H' : 'Н',
    'O' : 'О',
    'P' : 'Р',
    'C' : 'С',
    'T' : 'Т',
    'Y' : 'У',
    'X' : 'Х',
    }

def translitter(plate):
    for l in plate:
        if l in letters.keys():
            plate = plate.replace(l, letters[l])
    return plate

# print(translitter('CB23'))