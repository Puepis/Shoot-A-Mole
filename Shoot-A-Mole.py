"""Name: Philips Xu
   Date: May 30, 2018
   Description: Shoot-A-Mole is a single player game where the player shoots 
   moles that appear from holes on a game board.
   
"""

import pygame, myGameSprites, random, math
pygame.init()
pygame.mixer.init()


def create_holes(game_board):
    
    # Create holes list
    holes = []
    
    # Create 6 holes 
    y_pos = game_board.rect.top + game_board.get_height()/3.0
    for y in range(2):
        x_pos = game_board.rect.left + game_board.get_width()/4.0
        for x in range(3):
            hole = myGameSprites.Hole(x_pos, y_pos)
            holes.append(hole)
            x_pos += game_board.get_width()/4.0
        y_pos += game_board.get_height()/3.0
    return holes
    
def spawn_random_creature(holes, creature):
    
    # Get a random index
    index = random.randrange(6)
    
    # Set the spawn position to be one of the random holes
    x_pos = holes[index].rect.centerx
    y_pos = holes[index].rect.centery
    
    # Mole spawns if index is 0-3, Rat spawns if index is 4-5
    if index < 4:
        # Spawns a mole in the spawn position
        creature.spawn(x_pos, y_pos, 0)
    else:
        creature.spawn(x_pos, y_pos, 1)
    #print creature.get_pos()
    return creature

def fire_bullet(gun, bullets, screen, allSprites, mouse_pos):
    
    # Fires bullet in direction of crosshair
    dx = (mouse_pos[0] - gun.rect.centerx)/4.0
    dy = (mouse_pos[1] - gun.rect.centery)/4.0
    
    # Create a bullet
    bullet = myGameSprites.Bullet(gun.rect.centerx, gun.rect.centery, \
                                  screen, dx, dy, mouse_pos)
    
    # Add bullet to list and allSprites group
    bullets.append(bullet)
    allSprites.add(bullet)

def check_creature_collision(creature, mouse_pos, score_keeper, shot, \
                             bonus, multiplier):
    
    identity = creature.get_identity()
    
    # If the crosshair/mouse is on the creature, counts as a hit 
    if creature.rect.collidepoint(mouse_pos) and shot:
        
        # Makes the creature disappear off-screen
        creature.reset()
        
        if identity == "mole":
            
            creature.killed_mole()
            creature.increase_hit_streak()
            creature.reset_miss_streak()
            
        elif identity == "rat":
            
            creature.reset_hit_streak()
            creature.increase_miss_streak()
        return change_score(creature, score_keeper, multiplier, bonus)
              
def change_score(creature, score_keeper, multiplier, bonus):
    
    points = 0 
    bonus_applied = False
    # If a mole is hit
    if creature.get_miss_streak() == 0:
        points = (4 + creature.get_hit_streak())* multiplier + bonus
        if multiplier > 1 or bonus > 1:
            bonus_applied = True 
    # If a rat is hit
    elif creature.get_hit_streak() == 0:
        points = -2 - creature.get_miss_streak()
    score_keeper.change_points(points)
    return bonus_applied
        
def reduce_spawn_time(creature):
    creature.reduce_spawn_counter(4)

def set_gun_rotation_angle(gun, mouse_pos):
    
    # x and y coordinates for the gun
    gun_centerx = gun.rect.centerx
    gun_centery = gun.rect.centery 
    
    # x and y coordinates for the mouse
    mouse_xcord = mouse_pos[0]
    mouse_ycord = mouse_pos[1]
    
    # Find the angle of the two points relative to the x axis
    dx = mouse_xcord - gun_centerx
    dy = mouse_ycord - gun_centery
    new_angle = (math.atan2(dy, dx))*180/math.pi + 90
    
    # Set the angle 
    gun.set_rot_angle(-new_angle)

def set_powerup(powerup):
    powerups_list = powerup.get_powerup_list()
    index = random.randrange(len(powerups_list))
    powerup.set_powerup(index)
    return powerup.get_powerup()

def save_score(score):
    score_file = open("scores.txt", "a")
    score_file.write(str(score) + "\n")
    score_file.close()

def display_game_over(screen, score):
    
    # Black background
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    score_message = "YOUR SCORE: %d" % score
    
    # Game Over Message
    game_over_message = "GAME OVER!"
    game_over_font = pygame.font.SysFont("Arial", 50)
    g_o_text = game_over_font.render(game_over_message, 1, (255, 255, 255))
    
    # Score message
    score_message = "YOUR SCORE: %d" % score
    score_text = game_over_font.render(score_message, 1, (255, 255, 255))
    
    # Blit onto screen
    screen.blit(background, (0,0))
    screen.blit(g_o_text, (320, 310))
    screen.blit(score_text, (300, 350))
    pygame.display.flip()
    
    # Display for 3 seconds 
    pygame.time.delay(3000)
    
def introduction(screen):
    
    # Initialize score values  
    score_file = open("scores.txt", "r")
    score_list = []
    highscore = 0
    
    for line in score_file:
        score_list.append(int(line))
    
    # If there are existing scores, get the max score
    if score_list:
        highscore = max(score_list)
   
    # Entities
    background = pygame.image.load("instruc_background.png")
    screen.blit(background, (0,0))
    
    # Assign values
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Game title
    title = "SHOOT-A-MOLE!"
    title_font = pygame.font.SysFont("Arial", 60)
    title_text = title_font.render(title, 1, (255, 255, 255))
    title_rect = title_text.get_rect()
    title_rect.center = (screen.get_width()/2, screen.get_height()/2 - 50)
    
    # Highscore
    message = "HIGH SCORE: %d" % highscore
    highscore_font = pygame.font.SysFont("Arial", 40)
    highscore_text = highscore_font.render(message, 1, (255, 255, 255))
    highscore_rect = highscore_text.get_rect()
    highscore_rect.center = (screen.get_width()/2, screen.get_height()/2 + 50)
    
    # Instructions on how to start
    instructions = "Press spacebar to start" 
    instructions_font = pygame.font.SysFont("Arial", 30)
    instructions_text = instructions_font.render(instructions, 1, (255, 255, 255))
    instructions_rect = instructions_text.get_rect()
    instructions_rect.center = (screen.get_width()/2, screen.get_height()/2 + 120)
    
    game_start = False
    counter = 0
    
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        counter += 1
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    game_start = True
            
        if counter == 60:
            counter = 0
        
        screen.blit(title_text, title_rect)
        screen.blit(highscore_text, highscore_rect)           
        if counter <= 30:
            screen.blit(instructions_text, instructions_rect)   
        pygame.display.flip()
    
    # Close file and return game status        
    score_file.close()
    return game_start 
    
def game(screen):
    
    # Entities
    background = pygame.image.load("background.png")
    background = background.convert()
    screen.blit(background, (0,0))
    
    # Initiate class sprites
    basket = myGameSprites.Basket(screen)
    score_keeper = myGameSprites.ScoreKeeper()
    timer = myGameSprites.Timer()
    game_board = myGameSprites.GameBoard(screen)
    crosshair = myGameSprites.Crosshair(screen)
    powerup = myGameSprites.PowerUp(screen)
    combo_tracker = myGameSprites.ComboTracker()
    holes = create_holes(game_board)
    bullets = []
    
    # Spawn the gun beside the character
    gun = myGameSprites.Gun(basket.rect.right, basket.rect.centery, screen)
    
    # Spawn a mole off-screen
    creature = myGameSprites.Creature(0)
    
    # Initiate class groups
    holeGroup = pygame.sprite.Group(holes)
    allSprites = pygame.sprite.OrderedUpdates(score_keeper, timer, combo_tracker, basket, gun, game_board, \
                                              holes, creature, crosshair, bullets, \
                                              powerup)
    
    # Assign values
    keepGoing = True
    time_counter = 0
    counter = 0
    counter_max = 150
    bonus_score = 0
    multiplier = 1
    bonus_used = False 
    game_end = False
    score = 0
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    
    
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Increase the counter by 1 every loop
        time_counter += 1
        counter += 1
        
        # Assign value for player shooting (if gun was shot)
        shot = False
        
        # Resets the bonuses 
        if bonus_used:
            bonus_score = 0
            multiplier = 1 
            bonus_used = False
            
        # Update the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Keeps track of the time left
        time_left = 60 - (time_counter/30)
        timer.set_time(time_left)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            # User clicks left or right
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    basket.set_direction((-1,0))
                    gun.set_direction((-1,0))
                if event.key == pygame.K_d:
                    basket.set_direction((1,0))
                    gun.set_direction((1,0))
            
            # Fire a bullet when user clicks 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shot = True
                fire_bullet(gun, bullets, screen, allSprites, mouse_pos)
            
            # User releases a key 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and basket.get_direction() < 0 \
                   or event.key == pygame.K_d and basket.get_direction() > 0:
                    basket.set_direction((0,0))
                    gun.set_direction((0,0))
     
        # Gun rotation
        set_gun_rotation_angle(gun, mouse_pos)
        
        # Spawn a random creature
        if counter >= counter_max:
            #print counter_max 
            creature = spawn_random_creature(holes, creature)
            counter = 0
            
        # Game progression - gets harder every 5 seconds
        if time_counter % 150 == 0:
            # Spawn time decreases by 30% of a second 
            counter_max -= 8
            reduce_spawn_time(creature)        
   
        # Checking bullet collision with creatures
        if bullets:
            if check_creature_collision(creature, mouse_pos, score_keeper, \
                                     shot, bonus_score, multiplier):
                bonus_used = True
        
        # Stops the game after 60 seconds
        if time_left == 0:
            game_end = True
            keepGoing = False
        
        # Gets powerup             
        if pygame.sprite.collide_rect(basket, powerup):
            powerup.reset()
            bonus = set_powerup(powerup)
            if bonus == "+7 sec":
                time_counter -= 210
            elif bonus == "2 multiplier":
                multiplier = 2
            elif bonus == "+4 bonus":
                bonus_score = 4
        
        # Update the score
        score = score_keeper.get_score()
        
        # Set the hit streak
        combo_tracker.set_combo(creature.get_hit_streak())
        
        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    
    if game_end:
        display_game_over(screen, score)
    pygame.mouse.set_visible(True)
    return game_end, score

def main():
    '''This function defines the mainline logic for the game.'''
    
    # Display
    screen = pygame.display.set_mode((900, 680))
    pygame.display.set_caption("Shoot-A-Mole")
    
    # Check if game starts 
    game_status = introduction(screen)
    game_ended = False
    
    if game_status:
        game_ended, score = game(screen)
    if game_ended:
        save_score(score)
    
    # Close game window
    pygame.quit()
        
main()        
        
    
    
    