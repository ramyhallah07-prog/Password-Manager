import random
trys = 10
while trys>0:
    bot_hand = random.choice(['rock', 'paper', 'sisor']).lower()
    your_hand = input('rock, paper, sisor choose ').lower()
    s= 'sisor'
    r = 'rock'
    p = 'paper'
    if your_hand == s and bot_hand == r:
        print('you lose')
        trys -= 1
    elif your_hand == r and bot_hand == p:
        print('you lose')
        trys -= 1
    elif your_hand == p and bot_hand == s:
        print('you lose')
        trys -= 1
    elif your_hand == bot_hand:
        print('tie')
        trys -=1
    elif your_hand == r and bot_hand == s:
        print('you win')
        trys -=1
    elif your_hand == p and bot_hand == r:
        print('you win')
        trys -=1
    elif your_hand == s and bot_hand == p:
        print('you win')
        trys -=1
    else:
        print('tool does not exist')
        