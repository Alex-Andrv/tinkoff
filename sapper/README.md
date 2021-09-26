## sapper

Run Game: `python3 sapper-cli.py`

Interface:

```
>>> Creation of the directory saves failed
#######Menu##########
1) new game
2) load game
3) exit

1
#######Menu##########
1) default game
2) custom game

2
>>> Enter the length of the field. Where 0 < length < 10.
6
>>> Enter the width of the field. Where 0 < length < 10.
6
>>> Enter the count of mines. Where 0 < mines <= length * width / 2.
10
[state : game_running | last_move :  | length : 6 | width 6 | mines : 10 | remains open 26]
XXXXXX
XXXXXX
XXXXXX
XXXXXX
XXXXXX
XXXXXX

>>> Enter command : ['move', 'save', 'exit']
move
>>> Enter [x] [y]
5 5
>>> Enter [action]
open
[state : win | last_move : 5 5 open | length : 6 | width 6 | mines : 10 | remains open 0]
X102X2
2313X2
X3X222
X4211X
2X1133
1111XX

>>> You successfully win!
```

