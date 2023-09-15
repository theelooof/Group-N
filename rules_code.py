from textwrap import wrap

sentence = '''This game is a two-player board game,
consisting of a 7x7 (seven-by-seven) grid
board with 24 intersections forming 24  dotted
spaces(or available slots) for the pieces to be
placed on. The game consists of 18 board pieces, 9 for each player.The pieces are represented as
X(BLACK)s and O(WHITE)s. Black begins.'''
width = 50

print('+-' + '-' * width + '-+')

for line in wrap(sentence, width):
    print('| {0:^{1}} |'.format(line, width))

print('+-' + '-'*(width) + '-+')
