import random
import curses 

GRIDSIZE_X = 10
GRIDSIZE_Y = 10 

scr = curses.initscr()
curses.curs_set(0)

w = curses.newwin( GRIDSIZE_Y+3, GRIDSIZE_X+3, 0, 0)
w.keypad(1)
w.timeout(300)

# make grid 
for ii in range(0,GRIDSIZE_X+1):
    w.addch( 0, ii, '#')
    w.addch( GRIDSIZE_Y+1, ii, '#')

for jj in range(0,GRIDSIZE_Y+1):
    w.addch( jj, 0, '#')
    w.addch( jj, GRIDSIZE_X+1, '#')

food_position = [3, 4]
w.addch( food_position[1], food_position[0], 'o' )

# coordinates are 
snake = [
    [GRIDSIZE_X//2, GRIDSIZE_Y//2],
    [GRIDSIZE_X//2-1, GRIDSIZE_Y//2],
    [GRIDSIZE_X//2-2, GRIDSIZE_Y//2]
]


for ss in snake:
    w.addch( ss[1], ss[0], '*')
key = curses.KEY_RIGHT 

while True:
    # get new direction - and filter out unallowed moves
    new_key = w.getch()

    if new_key == curses.KEY_ENTER:
        curses.endwin()
        quit()

    # allowed moves:
    allowed_moves = {
        curses.KEY_LEFT: [curses.KEY_UP, curses.KEY_DOWN],
        curses.KEY_RIGHT: [curses.KEY_UP, curses.KEY_DOWN],
        curses.KEY_UP: [curses.KEY_LEFT, curses.KEY_RIGHT],
        curses.KEY_DOWN: [curses.KEY_LEFT, curses.KEY_RIGHT]
    }
    moving_direction = {
        curses.KEY_LEFT: [-1, 0],
        curses.KEY_RIGHT: [1, 0],
        curses.KEY_UP: [0, -1],
        curses.KEY_DOWN: [0, 1]   
    }

    if new_key in allowed_moves[key]:
        key = new_key


    # update position 
    new_head = [
        snake[0][0] + moving_direction[key][0],
        snake[0][1] + moving_direction[key][1],   
    ]

    # check if we lost:
    if (new_head in snake) or (new_head[0] in [0, GRIDSIZE_X+1]) or (new_head[1] in [0, GRIDSIZE_Y+1]):
        w.addch( 2, 2, 'G')
        w.addch( 2, 3, 'A')
        w.addch( 2, 4, 'M')
        w.addch( 2, 5, 'E')
        w.addch( 3, 2, 'O')
        w.addch( 4, 3, 'V')
        w.addch( 5, 4, 'E')
        w.addch( 6, 5, 'R')
        quit()
    
    w.addch( new_head[1], new_head[0], '*')
    snake.insert( 0, new_head)

    if food_position == new_head:
        while food_position in snake:
            food_position = [random.randint(1, GRIDSIZE_X), random.randint(1, GRIDSIZE_Y)] 
        w.addch( food_position[1], food_position[0], 'o' )
    else: 
        tail = snake.pop()
        w.addch( tail[1], tail[0], ' ')
    
