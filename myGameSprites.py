

import pygame, random, math

class Basket(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((40, 40))
        self.image.fill((0,0,0))
        self.image = self.image.convert()
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2 
        self.rect.centery = self.__screen.get_height() - 15
        self.__dx = 0
        
    def set_direction(self, xy_change):
        '''This method changes the x direction of the basket based on the 
        received tuple parameter.'''
        self.__dx = xy_change[0]
    
    def get_direction(self):
        '''This method returns the current direction of the basket.'''
        return self.__dx
    
    def get_pos(self):
        return self.rect.right, self.rect.centery
    
    def update(self):
        '''This method updates the position of the basket and moves it
        within the limits of the screen.'''
           
        self.__center = self.rect.center
           
        if (self.rect.left > 0) and (self.__dx < 0) or \
           (self.rect.right < self.__screen.get_width()) and (self.__dx > 0):
            self.rect.right += self.__dx*12   
            

class GameBoard(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("game_board.png")
        self.image = self.image.convert()
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2
        self.rect.centery = self.__screen.get_height()/2
        self.__width = self.rect.right - self.rect.left
        self.__height = self.rect.bottom - self.rect.top
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
        

class Crosshair(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("crosshair.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert()
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2
        self.rect.centery = self.__screen.get_height()/2
    
    def get_pos(self):
        return (self.rect.centerx, self.rect.centery)
        
    def update(self):
        # Move the center of the circle to where the mouse is pointing
        self.rect.center = pygame.mouse.get_pos()
        
        
class Hole(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("hole1.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        
class PowerUp(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((20, 20))
        self.image.fill((0,0,0))
        self.image = self.image.convert()
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.reset()
        self.set_movement()
        self.__powerups = ["+7 sec", "2 multiplier", "+4 bonus"] 
        
    
    def set_image(images, powerup):
        self.image = pygame.image.load(images[powerup])
        
    def get_powerup(self):
        return self.__powerup
    
    def set_powerup(self, index):
        self.__powerup = self.__powerups[index]
        
    def get_powerup_list(self):
        return self.__powerups
    
    def set_movement(self):
        self.__dy = random.randrange(7,11)
        
    def reset(self):
        self.__powerup = None
        self.rect.bottom = 0 
        self.rect.left = random.randrange(self.__screen.get_width() - 10)
        
    def update(self):
        
        if self.rect.top > self.__screen.get_height():
            self.reset()
        self.rect.bottom += self.__dy
        
class Creature(pygame.sprite.Sprite):
    
    def __init__(self, index):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__images = [pygame.image.load("Mole.png"), \
                         pygame.image.load("Rat.png")]
        self.image = self.__images[0]
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert()
        self.__spawn_counter = 60
        self.rect = self.image.get_rect()
        self.set_identity(index)
        self.reset_hit_streak()
        self.reset_miss_streak()
        self.reset()
        
    def spawn(self, x_pos, y_pos, index):
        self.__onscreen = True
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.set_identity(index)
    
    def get_onscreen(self):
        return self.__onscreen 
    
    def increase_hit_streak(self):
        self.__hit_streak += 1
    
    def reset_hit_streak(self):
        self.__hit_streak = 0
    
    def increase_miss_streak(self):
        self.__miss_streak += 1
        
    def reset_miss_streak(self):
        self.__miss_streak = 0
        
    def set_identity(self, index):
        if index == 0:
            self.__identity = "mole"
            
        else:
            self.__identity = "rat"
        self.image = self.__images[index]
        self.image.set_colorkey((255, 255, 255))
        
    def killed_mole(self):
        self.__mole_killed = True
            
    def get_identity(self):
        return self.__identity
    
    def get_hit_streak(self):
        return self.__hit_streak
    
    def get_miss_streak(self):
        return self.__miss_streak
        
    def reduce_spawn_counter(self, value):
        self.__spawn_counter -= value
    
    def get_spawn_counter(self):
        return self.__spawn_counter
    
    def get_pos(self):
        return (self.rect.centerx, self.rect.centery)
    
    def reset(self):
        self.__onscreen = False
        self.rect.centerx = -60
        self.rect.centery = 5
        self.__counter = 0
    
    def update(self):
        if self.__onscreen:
            self.__counter += 1
            #print self.__counter
        # Disappears after set amount of time
        if self.__counter >= self.__spawn_counter:
            self.reset()
                
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class inherits from the Sprite class and keeps track of the current 
    score.'''
    
    def __init__(self):
        '''This method initializes the ScoreKeeper class and sets the unique
        __score attribute.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initializes the font and score attributes
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__score = 0
        
    def change_points(self, points):
        '''This method changes the total number of points by a certain number, 
        based on the received parameter.'''
        self.__score += points
    
    def get_score(self):
        '''This method returns the player's current score.'''
        return self.__score
    
    def update(self):
        '''This method updates the score constantly, renders the font and 
        initializes the rect attributes for the ScoreKeeper class.'''
        
        score = "SCORE: %d" % self.__score
        self.image = self.__font.render(score, 1, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 25
            
class Timer(pygame.sprite.Sprite):
    '''This class inherits from the Sprite class and keeps track of the number
    of lives left.'''
    
    def __init__(self):
        '''This method initializes the LivesCounter class and sets the unique
        __lives attribute.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initializes the font and __lives attributes
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__time = 60
        
    def set_time(self, time):
        '''This method sets the time remaining in the game.'''
        self.__time = time
    
    def get_time_left(self):
        '''This method returns the amount of time left in the game.'''
        return self.__time
    
    def update(self):
        '''This method constantly updates the number of lives left, renders the 
        system font and initializes the rect attributes for the LivesCounter
        class.'''

        score = "TIME: %d" % self.__time
        self.image = self.__font.render(score, 1, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 520
        
class ComboTracker(pygame.sprite.Sprite):
    '''This class inherits from the Sprite class and keeps track of the current 
    combo.'''
    
    def __init__(self):
        '''This method initializes the ComboTracker class and sets the unique
        __combo attribute.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initializes the font and score attributes
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__combo = 0
        
    def set_combo(self, combo):
        '''This method increases the total number of points by a certain number, 
        based on the received parameter.'''
        self.__combo = combo
    
    def update(self):
        '''This method updates the score constantly, renders the font and 
        initializes the rect attributes for the ScoreKeeper class.'''
        
        combo = "COMBO: %d" % self.__combo
        self.image = self.__font.render(combo, 1, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 300
        
class Gun(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos, screen):
        
        pygame.sprite.Sprite.__init__(self)
             
        self.orig_image = pygame.image.load("Gun.png")
        self.image = self.orig_image
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.centerx= x_pos
        self.rect.bottom = y_pos
        self.__screen = screen
        self.__dx = 0
    
    def rotate_image(self):
        self.image = pygame.transform.rotate(self.orig_image, self.__rot_angle)
        self.image.set_colorkey((255, 255, 255))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
        
    def set_rot_angle(self, angle):
        self.__rot_angle = angle
   
    def set_direction(self, xy_change):
        '''This method changes the x direction of the gun based on the 
        received tuple parameter.'''
        self.__dx = xy_change[0]
       
    def update(self):
        '''This method updates the position of the gun and moves it
        within the limits of the screen.'''
        
        self.__center = self.rect.center
        
        # Rotate the gun image
        self.rotate_image()
    
        if (self.rect.left > 0) and (self.__dx < 0) or \
           (self.rect.right < self.__screen.get_width()) and (self.__dx > 0):
            self.rect.right += self.__dx*12    
        
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos, screen, dx, dy, endpoint):
        
        pygame.sprite.Sprite.__init__(self)
             
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 200, 200))
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.centerx= x_pos
        self.rect.centery = y_pos
        self.__screen = screen
        self.__dx = dx
        self.__dy = dy
        self.__endpointx = endpoint[0]
        self.__endpointy = endpoint[1]

    def update(self):
        
        # Checks if bullet has reached close to endpoint (due to uncertainty)
        if abs(self.rect.centerx - self.__endpointx) < 5 and \
           abs(self.rect.centery - self.__endpointy) < 5:
            self.kill()
        else:
            self.rect.centerx += self.__dx
            self.rect.centery += self.__dy
        
        