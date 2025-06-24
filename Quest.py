import pgzrun #Imports Pygame Zero Functionality
import random #makes the functionality in the random madule available

GRID_WIDTH = 16 #Lines 3-5: Define the width and height of the game grid and the size of each tile
GRID_HEIGHT = 12
GRID_SIZE = 50
GUARD_MOVE_INTERVAL = 0.5 #sets the time interval for a guard to move onscreen
PLAYER_MOVE_INTERVAL = 0.25 #time it takes for the player actor to move from one position to another
BACKGROUND_SEED = 123456

WIDTH = GRID_WIDTH * GRID_SIZE #Lines 7 and 8: define the size of the game window
HEIGHT = GRID_HEIGHT * GRID_SIZE
MAP = ["WWWWWWWWWWWWWWWW", #W's represent wall tiles
       "W              W",
       "W              W",
       "W  W  KG       W", #K's are Keys and G's are Guards
       "W  WWWWWWWWWW  W",
       "W              W",
       "W       P      W", #P is for Player
       "W  WWWWWWWWWW  W",
       "W       GK  W  W",
       "W              W",
       "W              D", #D is Door
       "WWWWWWWWWWWWWWWW",] #Dungeon has 12 row and 16 colums of wall tiles

def screen_coords(x, y): #this function converts grid coordinates to screen coordinates
    return (x * GRID_SIZE, y * GRID_SIZE)
def grid_coords(actor): 
    return (round(actor.x / GRID_SIZE), round(actor.y / GRID_SIZE)) #Determins the position of an actor on the grid
def setup_game():
    global game_over, player_won, player, keys_to_collect, guards #Defines "game_over", "player_won", "player", "keys_to_collect" and "guards" as a gloabl variables
    game_over = False
    player_won = False
    player = Actor("player", anchor=("left", "top")) #Creates new Actor Object and sets its anchor position
    keys_to_collect = [] #Sets keys_to_collect to an empty list initially
    guards = [] #Sets guards to an empty list initally
    for y in range(GRID_HEIGHT): #Lines 28 and 29: Loops over each grid position
        for x in range (GRID_WIDTH):
            square = MAP[y][x] #Extracts the character from the map representing this grid position
            if square == "P": #Checks if this grid position is the player
                player.pos = screen_coords(x, y) #Sets the postion of player to the screen coordinates of this grid position
            elif square == "K": #creates a key if the square is "K"
                key = Actor("key", anchor=("left", "top"), pos=screen_coords(x, y)) #creates the Key actor with an imiage, anchor and position
                keys_to_collect.append(key) #adds this actor to the list of keys created above
            elif square == "G": #creates a guard if square is G
                guard = Actor("guard", anchor=("left", "top"), pos=screen_coords(x, y)) #creates the guard actor
                guards.append(guard) #adds this actor to the list of guards created above
def draw_background():
    random.seed(BACKGROUND_SEED)
    for y in range(GRID_HEIGHT): #loops over each grid row
        for x in range(GRID_WIDTH): #loops over each grid column
            if x % 2 == y % 2:
                screen.blit("floor1", screen_coords(x, y)) #screen.blit draws the name image at the given screen position
            else:
                screen.blit("floor2", screen_coords(x, y))
            n = random.randint(0, 99)
            if n < 5:
                screen.blit("crack1", screen_coords(x, y))
            elif n < 10:
                screen.blit("crack2", screen_coords(x, y))
def draw_scenery():
    for y in range(GRID_HEIGHT): #lines 30 and 31: loops over each grid postion
        for x in range(GRID_WIDTH):
            square = MAP[y][x] #Extracts the character from the map represented by this grid position
            if square == "W": #Draws a wall tile at the screen position represented by W
                screen.blit("wall", screen_coords(x, y))
            elif square == "D" and len(keys_to_collect) > 0: #Draws a door tile at position D, but only if all keys have been collected
                screen.blit("door", screen_coords(x, y))
def draw_actors():
    player.draw() #Draws the player onscreen at it's current location
    for key in keys_to_collect:
        key.draw()
    for guard in guards:
        guard.draw()
def draw_game_over():
    screen_middle = (WIDTH / 2, HEIGHT / 2) #sets the position of the Game over message onscreen
    if player_won:
        screen.draw.text("You won!", midbottom=screen_middle, fontsize=GRID_SIZE, color="green", owidth=1)
    else:
        screen.draw.text("You lost", midbottom=screen_middle, fontsize=GRID_SIZE, color="red", owidth=1)
    screen.draw.text("press SPACE to play again", midtop=(WIDTH / 2, HEIGHT / 2 + GRID_SIZE), fontsize=GRID_SIZE /2, color="cyan", owidth=1)
def draw(): #The draw handler funtion is called automatically from the game loop
    draw_background() #draws the dungeon floor as a background onscreen
    draw_scenery() #Draws the scenery after (on top of) the gackground has be drawn
    draw_actors() #Draws the actors after (on top of) the background and scenery have been drawn
    if game_over:
        draw_game_over()
def on_key_up(key):
    if key == key.SPACE and game_over:
        setup_game()
def on_key_down(key): #reacts when user press down on a key
    if key == keys.LEFT:
        move_player(-1, 0)
    elif key == keys.UP:
        move_player(0, -1)
    elif key == keys.RIGHT:
        move_player(1, 0)
    elif key == keys.DOWN:
        move_player(0, 1)
def move_player(dx, dy):
    global game_over, player_won
    if game_over: #check if Game_over is set
        return #returns immediately without moving
    (x, y) = grid_coords(player) #Gets the current grid position of player
    x += dx #adds the X axis distance to x
    y += dy #adds the y axis distance to y
    square = MAP[y][x] #gives the tile at this position
    if square == "W":
        return #Stops the executions of the move_player() fuctions if the player touches a wall
    elif square == "D":
        if len(keys_to_collect) > 0: #check is the keys to collect list is not empty
            return #returns immediately if list is no empty
        else:
            game_over = True
            player_won = True
    for key in keys_to_collect: #loops over each of the key actors in the list
        (key_x, key_y) = grid_coords(key) #gets the grid position of a key actor
        if x == key_x and y == key_y: #checks if the new player position matches the key position
            keys_to_collect.remove(key) #removes this key from the list if player position matches the key position
            break #breaks out of the for loop as each square can only contain one key
    animate(player, pos=screen_coords(x, y), duration=PLAYER_MOVE_INTERVAL, on_finished=repeat_player_move)
def repeat_player_move():
    if keyboard.left:
        move_player(-1, 0)
    elif keyboard.up:
        move_player(0, -1)
    elif keyboard.right:
        move_player(1, 0)
    elif keyboard.down:
        move_player(0, 1)
def move_guard(guard):
    global game_over #defines game_over as a global variable
    if game_over: #returns immediately without moving if the game is over
        return
    (player_x, player_y) = grid_coords(player) #gets grid position of player actor
    (guard_x, guard_y) = grid_coords(guard) #getts the grid position of the guard actor
    if player_x > guard_x and MAP[guard_y][guard_x + 1] != "W": #checks if the player is to the right of the guard and whether the square to the right is a wall
        guard_x += 1 #increases the grid position of this guard actor by 1 if the above condition is true
    elif player_x < guard_x and MAP[guard_y][guard_x - 1] != "W": #checks if the player is to the left of the guard and whether the square to the left is a wall
        guard_x -= 1 #moves the grid position of this gards actor by -1 if the above condition is true
    elif player_y > guard_y and MAP[guard_y + 1][guard_x] != "W": #checks if player is above the guard
        guard_y += 1 #moves the guard_y by 1 if true
    elif player_y < guard_y and MAP[guard_y - 1][guard_x] != "W": #checks if player is below the guard
        guard_y -= 1 #moves the guard_y by -1 if true
    animate(guard, pos=screen_coords(guard_x, guard_y), duration=GUARD_MOVE_INTERVAL)
    if guard_x == player_x and guard_y == player_y: #checks it the guard position is the same as the players position
        game_over = True #sets game_over to true if above condition is true
def move_guards():
    for guard in guards:
        move_guard(guard)

setup_game()
clock.schedule_interval(move_guards, GUARD_MOVE_INTERVAL) #schedules regular calls to the move_guards() function
pgzrun.go() #Starts Pygame Zero
