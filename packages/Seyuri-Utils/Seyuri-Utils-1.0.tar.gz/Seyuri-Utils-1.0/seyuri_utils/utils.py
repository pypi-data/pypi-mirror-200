import random, string, json

def randomString(upper: int, lower: int, symbol: int, number: int) -> str:
    return ''.join(random.sample(
        random.sample(string.ascii_uppercase, upper) +
        random.sample(string.ascii_lowercase, lower) +
        random.sample(string.punctuation, symbol) +
        random.sample(string.digits, number),
        upper + lower + symbol + number
    ))

def printDict(rawDict: dict, indent: int=4) -> None:
    print(json.dumps(rawDict, indent=indent))