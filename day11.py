from copy import deepcopy

oldInp = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''

inp = '''Monkey 0:
  Starting items: 71, 56, 50, 73
  Operation: new = old * 11
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 7

Monkey 1:
  Starting items: 70, 89, 82
  Operation: new = old + 1
  Test: divisible by 7
    If true: throw to monkey 3
    If false: throw to monkey 6

Monkey 2:
  Starting items: 52, 95
  Operation: new = old * old
  Test: divisible by 3
    If true: throw to monkey 5
    If false: throw to monkey 4

Monkey 3:
  Starting items: 94, 64, 69, 87, 70
  Operation: new = old + 2
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 6

Monkey 4:
  Starting items: 98, 72, 98, 53, 97, 51
  Operation: new = old + 6
  Test: divisible by 5
    If true: throw to monkey 0
    If false: throw to monkey 5

Monkey 5:
  Starting items: 79
  Operation: new = old + 7
  Test: divisible by 2
    If true: throw to monkey 7
    If false: throw to monkey 0

Monkey 6:
  Starting items: 77, 55, 63, 93, 66, 90, 88, 71
  Operation: new = old * 7
  Test: divisible by 11
    If true: throw to monkey 2
    If false: throw to monkey 4

Monkey 7:
  Starting items: 54, 97, 87, 70, 59, 82, 59
  Operation: new = old + 8
  Test: divisible by 17
    If true: throw to monkey 1
    If false: throw to monkey 3'''

round = 1


bigMod = 1

class Monkey:
    def __init__(self):
        self.startingItems = []
        self.testMod = 0
        self.trueMonke = 0
        self.falseMonke = 0
        self.modVal = 0
        self.argSelf = False
        self.addOrMul = 0
        self.val = 0
        self.inspected = 0

    def op(self, x):
        if self.addOrMul == 0:
            if self.argSelf:
                return (x + x) % bigMod
            else:
                return (self.val + x) % bigMod
        else:
            if self.argSelf:
                return (x * x) % bigMod
            else:
                return (self.val * x) % bigMod

            
monkes: list[Monkey] = []



# Init monkes

inpLines = inp.splitlines()
for line in inpLines:
    words = line.split()
    if len(words) == 0:
        continue
    
    if words[0] == 'Monkey':
        monkes.append(Monkey())
        
    elif words[0] == 'Starting':
        for word in words[2:]:
            monkes[-1].startingItems.append(int(word.replace(',', '')))

    elif words[0] == 'Operation:':
        thing = words[5]
        if words[5] == 'old':
            monkes[-1].argSelf = True
        else:
            monkes[-1].val = int(words[5])
        if words[4] == '*':
            monkes[-1].addOrMul = 1

    elif words[0] == 'Test:':
        monkes[-1].modVal = int(words[3])
        bigMod *= int(words[3])

    elif words[1] == 'true:':
        monkes[-1].trueMonke = int(words[5])

    elif words[1] == 'false:':
        monkes[-1].falseMonke = int(words[5])
        

while round < 10001:
    print(round)
    for monke in monkes:
        while len(monke.startingItems) > 0:
            item = monke.startingItems.pop()
            item = int(monke.op(item))
            if (item % monke.modVal == 0):
                monkes[monke.trueMonke].startingItems.append(item)
            else:
                monkes[monke.falseMonke].startingItems.append(item)
            monke.inspected += 1
    
    round += 1

for monke in monkes:
    print(monke.inspected)
