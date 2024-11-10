import pygame
import math
import random
import time
class TastyTrails():
    VELOCITY = 3
    
    def __init__(self, screen):     
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = screen
        
        self.width, self.height = 850, 700
        self.velocity = self.VELOCITY

        self.font = pygame.font.Font("assets/font.ttf", 36)

        self.MENU, self.PLAYING, self.GAME_OVER = "menu", "playing", "game_over"
        self.state = self.MENU

        self.image_player = self.scale_image("assets/chickenidle.png", 0.1)
        self.image_player_jump = self.scale_image("assets/chickenjump.png", 0.1)
        self.image_cloud = [self.scale_image(f"assets/cloud{i+1}.png", 1) for i in range(2)]
        self.image_obstacle = self.scale_image("assets/fence.png", 0.12)
        self.image_menu = self.scale_image("assets/tastytrailsbg.png", 1)
        self.image_background = self.scale_image("assets/grass.png", 1)
        self.image_sky = self.scale_image("assets/sky.png", 1)

        self.effect_images = [pygame.transform.rotate(self.scale_image(f"assets/chickeneffect{i+1}.png", 0.05), -10) for i in range(4)]

        self.background_x1 = 0
        self.background_x2 = self.image_background.get_width()

        self.scale_factor = 0.2

        self.obstacles = []
        self.clouds = []
        self.last_x = 900
        obstacle_rect = self.image_obstacle.get_rect()
        self.obstacleOffset = obstacle_rect.width

        self.active_effects = []
        
        self.player = self.Player(200, 650 + self.image_player.get_height(), self.image_player.get_width(),
                self.image_player.get_height(), self.image_player, self.image_player_jump, self)
       

        self.presents = []
        self.last_present_time = time.time()
        self.last_tick = pygame.time.get_ticks()

        self.jump_sound = pygame.mixer.Sound("assets/jump_sound.mp3")
        self.jump_sound.set_volume(0.5)

        self.count = 0


    def scale_image(self, path, scale_factor):
        image = pygame.image.load(path).convert_alpha()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        return pygame.transform.scale(image, (new_width, new_height))  
    

    class Player:
        def __init__(self, x, y, width, height, image, jump_image, game_instance):
            self.body = pygame.Rect(x, y, width, height)
            self.image = image
            self.original_image = image
            self.flipped_image = pygame.transform.flip(image, True, False)
            self.jump_image = jump_image
            self.can_jump = True
            self.speed = 0
            self.gravity = 0.7
            self.y = y
            self.game_instance = game_instance

        def draw(self, screen):
            self.speed += self.gravity
            self.y += self.speed
            if self.y >= 650 - self.image.get_height():
                self.y = 650 - self.image.get_height()
                self.can_jump = True
                self.image = self.original_image
            self.body.y = self.y
            screen.blit(self.image, (self.body.x, self.body.y))

        def jump(self, jump_sound):
            if self.can_jump:
                self.speed = -14
                self.can_jump = False
                self.game_instance.display_effect((self.body.centerx, self.body.bottom))
                jump_sound.play()
                self.image = self.jump_image

    class Obstacle:
        def __init__(self, x, y, width, height, image):
            self.body = pygame.Rect(x, y, width, height)
            self.image = image

        def draw(self, screen):
            screen.blit(self.image, (self.body.x, self.body.y))
            

        def update(self):
            self.body.x -= TastyTrails.VELOCITY
            if self.body.right <= 0:
                self.body.x = 850 + random.randint(100, 400)

    class Cloud:
        def __init__(self, x, y, width, height, image):
            self.body = pygame.Rect(x, y, width, height)
            self.image = image

        def draw(self, screen):
            screen.blit(self.image, (self.body.x, self.body.y))

        def update(self):
            self.body.x -= TastyTrails.VELOCITY - 2
            if self.body.right <= 0:
                self.body.x = 850 + random.randint(100, 400)

    class Present:
        def __init__(self, x, y):
            self.original_image = pygame.image.load("assets/egg.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (20, 20))
            self.image = self.original_image
            self.body = self.image.get_rect(topleft=(x, y))
            self.angle = 0

        def draw(self, screen):
            screen.blit(self.image, self.body.topleft)

        def update(self):
            self.body.y += 3
            self.body.x -= TastyTrails.VELOCITY - 2
            self.angle = (self.angle + 5) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.body = self.image.get_rect(center=self.body.center)
            if self.body.y > 700 and self.body.x < 0:
                return True
            return False

    def spawn_present(self):
        current_time = time.time()
        if current_time - self.last_present_time >= 10:
            eligible_clouds = [cloud for cloud in self.clouds if 200 <= cloud.body.x <= 700 - cloud.body.width]
            if eligible_clouds:
                cloud = random.choice(eligible_clouds)
                present_x = cloud.body.x + random.randint(0, cloud.body.width - 30)
                present_y = cloud.body.y + cloud.body.height
                self.presents.append(self.Present(present_x, present_y))
                self.last_present_time = current_time
                

    def update_background(self, screen):
        self.background_x1 -= TastyTrails.VELOCITY
        self.background_x2 -= TastyTrails.VELOCITY

        if self.background_x1 <= -self.image_background.get_width():
            self.background_x1 = self.background_x2 + self.image_background.get_width()

        if self.background_x2 <= -self.image_background.get_width():
            self.background_x2 = self.background_x1 + self.image_background.get_width()

        screen.blit(self.image_background, (self.background_x1, 0))
        screen.blit(self.image_background, (self.background_x2, 0))
        

    def spawn_objects(self, cls):
        speed = random.uniform(1, 3)
        if issubclass(cls, self.Obstacle):
            image = self.image_obstacle
            x = random.randint(900, 2000)
            y = 650 - self.image_obstacle.get_height()
            width = image.get_width() * 1
            height = image.get_height() * 1
            scaled_image = pygame.transform.scale(image, (width, height))
            return cls(x, y, width, height, scaled_image)
        elif issubclass(cls, self.Cloud):
            image = random.choice(self.image_cloud)
            x = random.randint(100, 1700)
            y = random.randint(50, 300)
            width = image.get_width() * self.scale_factor
            height = image.get_height() * self.scale_factor
            scaled_image = pygame.transform.scale(image, (width, height))
            return cls(x, y, width, height, scaled_image)


    def update_objects(self, screen, obj, object_list, maximum):
        if len(object_list) < maximum:
            object_list.append(self.spawn_objects(obj))

        for obj in object_list[:]:
            obj.update()
            obj.draw(screen)
            if isinstance(obj, self.Obstacle): 
                if obj.body.right <= 0:
                    object_list.remove(obj)
                if obj.body.inflate(-10, -10).colliderect(self.player.body.inflate(-20, -20)):
                    self.state = self.GAME_OVER
                    pygame.mixer.music.stop()
            elif isinstance(obj, self.Cloud) and obj.body.right <= 0:
                object_list.remove(obj)


    def collide_obs(self):
        if any(pygame.Rect.colliderect(self.player.body, obs.body) for obs in self.obstacles):
            self.state = self.GAME_OVER


    def increase_speed(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.last_tick >= 100:
            TastyTrails.VELOCITY += 0.01
            self.last_tick = current_tick

    def display_effect(self, position):
        effect = {
            'images': self.effect_images,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'current_image': 0
        }
        self.active_effects.append(effect)

    def update_effects(self, screen):
        current_time = pygame.time.get_ticks()
        for effect in self.active_effects[:]:
            elapsed_time = current_time - effect['start_time']
            if elapsed_time > 50 * (effect['current_image'] + 1):
                effect['current_image'] += 1
                if effect['current_image'] >= len(effect['images']):
                    self.active_effects.remove(effect)
                    continue

            image = effect['images'][effect['current_image']]
            screen.blit(image, image.get_rect(center=effect['position']))

    
    def render_text_with_border(self, text, font, x, y, color, border_color=(0, 0, 0), border_width=2):
        border_text = font.render(text, True, border_color)
        offsets = [
            (-border_width, 0), (border_width, 0), 
            (0, -border_width), (0, border_width),
            (-border_width, -border_width), (-border_width, border_width),
            (border_width, -border_width), (border_width, border_width)
        ]
        for dx, dy in offsets:
            border_rect = border_text.get_rect(center=(x + dx, y + dy))
            self.screen.blit(border_text, border_rect.topleft)

        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        self.screen.blit(rendered_text, text_rect.topleft)


    def render_text_with_hover(self, text, font, x, y, color, hover_color, Gx, Gy, click):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))

        if text_rect.collidepoint(Gx, Gy):
            rendered_text = font.render(text, True, hover_color)
            if click:
                return True

        self.screen.blit(rendered_text, text_rect.topleft)
        return False
    

    def render_text_with_both(self, text, font, x, y, color, hover_color, Gx, Gy, click, border_color=(0, 0, 0), border_width=2):
        self.render_text_with_border(text, font, x, y, color, border_color, border_width)
        return self.render_text_with_hover(text, font, x, y, color, hover_color, Gx, Gy, click)


    def fonts(self, size):
            return pygame.font.Font("assets/font.ttf", size)


    def check_presents_click(self, Gx, Gy, click, Add_Credits):
        for present in self.presents[:]:
            if (present.body.x <= Gx <= present.body.x + present.body.width and
                present.body.y <= Gy <= present.body.y + present.body.height) and click:
                self.presents.remove(present)
                Add_Credits(50)
                self.count += 1
                return True
        return False


    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        if self.state == self.MENU:
            screen.blit(self.image_menu, (0, 0))

            self.render_text_with_border("TASTY TRAILS", self.fonts(60), 
                self.width//2, 80, (255, 255, 255), border_color=(0, 0, 0), border_width=2)

            if self.render_text_with_both("PLAY", self.fonts(40), 
                self.width // 2, self.height // 2 + self.fonts(40).get_height() // 2, (255, 255, 255), (90, 191, 23), Gx, Gy, click, border_color=(0, 0, 0), border_width=2):
                self.reset_game()
                self.state = self.PLAYING

        if self.state == self.GAME_OVER:
            screen.blit(self.image_menu, (0, 0))

            self.render_text_with_border(f'Eggs cracked: {self.count}', self.fonts(20),
                self.width // 2, self.height - 100, (255, 255, 255), border_color=(0, 0, 0), border_width=2)
            
            self.render_text_with_border("YOU LOST", self.fonts(60), 
                self.width // 2, 80, (255, 255, 255), border_color=(0, 0, 0), border_width=2)

            if self.render_text_with_both("TRY AGAIN", self.fonts(40), 
                self.width // 2, self.height // 2 + self.fonts(40).get_height() // 2, (255, 255, 255), (90, 191, 23), Gx, Gy, click, border_color=(0, 0, 0), border_width=2):
                self.reset_game()
                self.state = self.PLAYING

            if held_keys.get("Escape"):
                self.state = self.MENU
                pygame.mixer.music.stop()

        if self.state == self.PLAYING:
            screen.blit(self.image_sky, (0, 0))

            if held_keys.get("space"):
                self.player.jump(self.jump_sound)

            if held_keys.get("Escape"):
                self.state = self.MENU

            self.check_presents_click(Gx, Gy, click, Add_Credits)

            self.increase_speed()

            self.update_objects(screen, self.Obstacle, self.obstacles, 3)
            self.update_objects(screen, self.Cloud, self.clouds, 6)

            self.spawn_present()
            self.presents = [present for present in self.presents if not present.update()]

            for present in self.presents:
                present.draw(screen)

            self.update_background(screen)
            self.player.draw(screen)
            self.update_effects(screen)

            self.render_text_with_border(f'Eggs cracked: {self.count}', self.fonts(20), self.width // 2, 40,
                (255, 255, 255), border_color=(0, 0, 0), border_width=2)

            self.collide_obs()


    def reset_game(self):
        TastyTrails.VELOCITY = 3
        self.last_tick = pygame.time.get_ticks()

        self.obstacles = []
        self.clouds = []
        self.player = self.Player(200, 650 + self.image_player.get_height(), self.image_player.get_width(),
                self.image_player.get_height(), self.image_player, self.image_player_jump, self)

        self.presents = []
        self.last_present_time = time.time()

        self.background_x1 = 0
        self.background_x2 = self.image_background.get_width()

        pygame.mixer.music.load("assets/tastytrails_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.count = 0

class HungryMouth():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PLAYER_COLOR = (255, 0, 255)
    FOOD_COLOR = (255, 0, 0)
    SCREEN_WIDTH = 850
    SCREEN_HEIGHT = 700
    PLAYER_VELOCITY = 10
    SPAWN_INTERVAL = 30
    SPAWN_INTERVAL_TRASH = 60
    MAX_FOOD = 6
    MAX_TRASH = 2

    def __init__(self, screen):
        pygame.init()
        self.width = self.SCREEN_WIDTH
        self.height = self.SCREEN_HEIGHT
        self.screen = screen

        self.MENU, self.PLAYING, self.GAME_OVER = "menu", "playing", "game_over"
        self.state = self.MENU

        self.image_background = self.scale_image("assets/foodbg1.jpg", 0.19)

        self.image_player = self.scale_image("assets/playerfood1.png", 0.2)
        self.image_food = [self.scale_image(f"assets/strokefood{i+1}.png", 1) for i in range(4)]
        self.image_trash = self.scale_image("assets/trash.png", 1)

        self.effect_images = [self.scale_image(f"assets/effect{i+1}.png", 0.15) for i in range(5)]

        self.velocity = self.PLAYER_VELOCITY
        self.falling_food = []
        self.falling_trash = []
        self.food = 0
        self.spawn_timer = 0

        self.active_effects = []

        self.player = self.Player(self.width // 2, self.height - self.image_player.get_height(),
            self.image_player.get_width(),  self.image_player.get_height(),self.image_player)
        
        self.highscore = 0
        self.highscore_file = "assets/highscore.txt"
        self.load_highscore()

    def load_highscore(self):
        try:
            with open(self.highscore_file, "r") as file:
                self.highscore = int(file.read().strip())
        except FileNotFoundError:
            self.highscore = 0

    def save_highscore(self):
        with open(self.highscore_file, "w") as file:
            file.write(str(self.highscore))



    class Player:
        def __init__(self, x, y, width, height, image):
            self.rect = pygame.Rect(x, y, width, height)
            self.image = image
            self.original_image = image
            self.flipped_image = pygame.transform.flip(image, True, False)
            self.collider = pygame.Rect(x, y, width, height - 640*0.2)

        def draw(self, screen):
            screen.blit(self.image, self.rect.topleft)

        def move(self, velocity, held_keys):
            if held_keys.get("a"):
                self.rect.x -= velocity
                self.collider.x -= velocity
                self.image = self.flipped_image
            elif held_keys.get("d"):
                self.rect.x += velocity
                self.collider.x += velocity
                self.image = self.original_image
        
   
    class FallingFood:
        def __init__(self, x, y, width, height, speed, image):
            self.rect = pygame.Rect(x, y, width, height)
            self.speed = speed
            self.image = image
            self.angle = 0
            self.spin_direction = random.choice([-1, 1])

        def update(self):
            self.rect.y += self.speed
            self.angle += 4 * self.spin_direction
            if self.angle >= 360 or self.angle <= -360:
                self.angle = 0

        def draw(self, screen):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, new_rect.topleft)

        def off_screen(self):
            return self.rect.y > HungryMouth.SCREEN_HEIGHT


    class Trash:
        def __init__(self, x, y, width, height, speed, image):
            self.rect = pygame.Rect(x, y, width, height)
            self.speed = speed
            self.image = image
            self.angle = 0
            self.spin_direction = random.choice([-1, 1])
            self.dx = random.choice([-1, 1]) * (speed+2)

        def update(self):
            self.rect.y += self.speed+2
            self.rect.x += self.dx
            self.angle += 4 * self.spin_direction
            if self.angle >= 360 or self.angle <= -360:
                self.angle = 0

            if self.rect.left <= 0 or self.rect.right >= HungryMouth.SCREEN_WIDTH:
                self.dx *= -1

        def draw(self, screen):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, new_rect.topleft)

        def off_screen(self):
            return self.rect.y > HungryMouth.SCREEN_HEIGHT  


    def spawn1(self, cls):
        x = random.randint(80, self.width - 80)
        y = random.randint(100, 300) * -1
        speed = random.uniform(1, 3)
        if issubclass(cls, self.FallingFood):
            image = random.choice(self.image_food)
        elif issubclass(cls, self.Trash):
            image = self.image_trash
        width = image.get_width() * 0.8
        height = image.get_height() * 0.8
        scaled_image = pygame.transform.scale(image, (width, height))
        return cls(x, y, width, height, speed, scaled_image)
    
    
    def update_objects(self, screen, obj, object_list, spawn_rate, maximum, Add_credits):
        self.spawn_timer += 1
        if self.spawn_timer >= spawn_rate and len(object_list) < maximum:
            object_list.append(self.spawn1(obj))
            self.spawn_timer = 0

        for obj in object_list[:]:
            obj.update()
            obj.draw(screen)
            if obj.off_screen():
                object_list.remove(obj)
            elif obj.rect.colliderect(self.player.collider):
                object_list.remove(obj)
                if isinstance(obj, self.FallingFood):
                    self.food += 1
                    self.collect_sound.play()
                    self.display_effect(obj.rect.center)
                elif isinstance(obj, self.Trash):
                    self.state = self.GAME_OVER
                    self.credits_score(Add_credits)
                    pygame.mixer.music.stop()
                    if self.food > self.highscore:
                        self.highscore = self.food
                        self.save_highscore()
    
    def display_effect(self, position):
        effect = {
            'images': self.effect_images,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'current_image': 0
        }
        self.active_effects.append(effect)

    def update_effects(self, screen):
        current_time = pygame.time.get_ticks()
        for effect in self.active_effects[:]:
            elapsed_time = current_time - effect['start_time']
            if elapsed_time > 50 * (effect['current_image'] + 1):
                effect['current_image'] += 1
                if effect['current_image'] >= len(effect['images']):
                    self.active_effects.remove(effect)
                    continue

            image = effect['images'][effect['current_image']]
            screen.blit(image, image.get_rect(center=effect['position']))

    
    def fonts(self, size):
            return pygame.font.Font("assets/font.ttf", size)
    
    def credits_score(self, Add_Credits):
        Add_Credits(int(self.food)*10)
        

    def scale_image(self, path, scale_factor):
        image = pygame.image.load(path).convert_alpha()
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        return pygame.transform.scale(image, (new_width, new_height))  


    def render_text_with_border(self, text, font, x, y, color, border_color=(0, 0, 0), border_width=2):
        border_text = font.render(text, True, border_color)
        offsets = [
            (-border_width, 0), (border_width, 0), 
            (0, -border_width), (0, border_width),
            (-border_width, -border_width), (-border_width, border_width),
            (border_width, -border_width), (border_width, border_width)
        ]
        for dx, dy in offsets:
            border_rect = border_text.get_rect(center=(x + dx, y + dy))
            self.screen.blit(border_text, border_rect.topleft)

        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        self.screen.blit(rendered_text, text_rect.topleft)


    def render_text_with_hover(self, text, font, x, y, color, hover_color, Gx, Gy, click):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))

        if text_rect.collidepoint(Gx, Gy):
            rendered_text = font.render(text, True, hover_color)

        self.screen.blit(rendered_text, text_rect.topleft)
        
    
    def render_text_with_both(self, text, font, x, y, color, hover_color, Gx, Gy, click, border_color=(0, 0, 0), border_width=2):
        self.render_text_with_border(text, font, x, y, color, border_color, border_width)
        return self.render_text_with_hover(text, font, x, y, color, hover_color, Gx, Gy, click)


    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        if self.state == self.MENU:
            screen.blit(self.image_background, (0, 0))

            self.render_text_with_border(f'Highscore: {self.highscore}', self.fonts(20), self.width // 2, 150,
                self.WHITE, border_color=self.BLACK, border_width=2)

            self.render_text_with_border("HUNGRY MOUTH", self.fonts(60), self.width // 2, 80,
                                          self.WHITE, border_color=self.BLACK, border_width=2)

            self.render_text_with_both("PLAY", self.fonts(40), self.width // 2, self.height // 2 + self.fonts(40).get_height() // 2,
                                           self.WHITE, (90, 191, 23), Gx, Gy, click, border_color=self.BLACK, border_width=2) 
            if click:
                self.state = self.PLAYING
                self.reset_game()

        elif self.state == self.GAME_OVER:
            screen.blit(self.image_background, (0, 0))


            

            self.render_text_with_border("YOU LOST", self.fonts(60), self.width // 2, 80,
                self.WHITE, border_color=self.BLACK, border_width=2)

            self.render_text_with_border(f'Highscore: {self.highscore}', self.fonts(20), self.width // 2, self.height - 50,
                self.WHITE, border_color=self.BLACK, border_width=2)

            self.render_text_with_both("TRY AGAIN", self.fonts(40), self.width // 2, self.height // 2 + self.fonts(40).get_height() // 2,
                self.WHITE, (90, 191, 23), Gx, Gy, click, border_color=self.BLACK, border_width=2) 
            if click:
                self.reset_game()
                self.state = self.PLAYING
                pygame.mixer.music.play()
                

            if held_keys.get("Escape"):
                self.state = self.MENU
                pygame.mixer.music.stop()

        elif self.state == self.PLAYING:
            screen.blit(self.image_background, (0, 0))

            if held_keys.get("Escape"):
                self.state = self.MENU

            self.player.move(self.velocity, held_keys)

            self.update_objects(screen, self.FallingFood, self.falling_food, self.SPAWN_INTERVAL, self.MAX_FOOD, Add_Credits)
            self.update_objects(screen, self.Trash, self.falling_trash, self.SPAWN_INTERVAL_TRASH, self.MAX_TRASH, Add_Credits)

            self.render_text_with_border(f'Food: {self.food}', self.fonts(20), self.width // 2, 40,
                                          self.WHITE, border_color=self.BLACK, border_width=2)

            self.player.draw(screen)
            self.update_effects(screen)


    def reset_game(self):
        self.falling_food = []
        self.falling_trash = []
        self.food = 0
        self.spawn_timer = 0
        self.trash_spawn_timer = 0
        
        self.player = self.Player(self.width // 2, self.height - self.image_player.get_height(),
            self.image_player.get_width(),  self.image_player.get_height(),self.image_player)

        
        pygame.mixer.music.load("assets/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        self.collect_sound = pygame.mixer.Sound("assets/collect_sound.mp3")
        self.collect_sound.set_volume(0.5)
        pygame.mixer.music.play(-1)

class ForestFire():

    
    class Dog:
        def __init__(self,screen ):
            self.screen = screen
            
            self.dogx = 650
            self.dogy = 500
            self.width = 150
            self.height = 150
            self.color = (0,255,0)
            self.image = pygame.image.load("assets/tammy1.png")
            self.image1 = pygame.image.load('assets/tammyleft.png')
            self.faceDown =  pygame.transform.flip(self.image, False, True) 

            self.faceLeft= pygame.transform.flip(self.image, False, False) 

            self.faceUP = pygame.transform.flip(self.image, True, True) 
            self.faceRight = pygame.transform.flip(self.image1, True, False) 
           
            self.dogBody = pygame.Rect(self.dogx , self.dogy , self.width , self.height)

        def draw(self , held_keys):
            
            was = False

            if held_keys.get('Left' , True) and was == False:
                was = True
                self.screen.blit(self.image1, self.dogBody)

            if held_keys.get('Right' , True) and was == False:
                was = True
                self.screen.blit(self.faceRight, self.dogBody)

            if held_keys.get('Up' , True) and was == False:
                was = True
                self.screen.blit(self.faceUP, self.dogBody)

            if held_keys.get('Down' , True) and was == False:
                was = True
                self.screen.blit(self.faceDown, self.dogBody)

            if was == False:
                self.screen.blit(self.faceLeft, self.dogBody)
            
            






    class ArrowsKeys:
        def __init__(self,screen,arrowx,arrowy,key):
            self.screen = screen
            self.arrowx = arrowx
            self.arrowy = arrowy
            self.arrowWidth = 80
            self.arrowHeight = 80
            self.key = key
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.arrowBody = pygame.Rect(self.arrowx , self.arrowy , self.arrowWidth , self.arrowHeight)

            self.faceUp = pygame.image.load("assets/arrowUp.png")
            self.faceLeft = pygame.image.load("assets/arrowLeft.png")
            self.faceDown =  pygame.transform.flip(self.faceUp, False, True) 
            self.faceRight = pygame.transform.flip(self.faceLeft, True, False) 

            self.pressedUp = pygame.image.load("assets/pressedUp.png")
            self.pressedLeft = pygame.image.load("assets/pressedLeft.png")
            self.pressedDown =  pygame.transform.flip(self.pressedUp, False, True) 
            self.pressedRight = pygame.transform.flip(self.pressedLeft, True, False) 
        
        
        def draw(self, key , key_hold):

            if key == 'Left' and key_hold.get('Left',True):
                self.screen.blit(self.pressedLeft, self.arrowBody)
            elif key == 'Left':
                self.screen.blit(self.faceLeft, self.arrowBody)

            elif key == 'Down' and key_hold.get('Down',True):
                self.screen.blit(self.pressedDown, self.arrowBody)
            elif key == 'Down':
                self.screen.blit(self.faceDown, self.arrowBody)

            elif key == 'Up' and key_hold.get('Up',True):
                self.screen.blit(self.pressedUp, self.arrowBody)
            elif key == 'Up':
                self.screen.blit(self.faceUp, self.arrowBody)

            elif key == 'Right' and key_hold.get('Right',True):
                self.screen.blit(self.pressedRight, self.arrowBody)
            elif key == 'Right':
                self.screen.blit(self.faceRight, self.arrowBody)





    def GenerateArrows(self,screen,arrowList) : 
            self.arrowList = arrowList
            self.screen = screen
            for i, direction in enumerate(['Left', 'Down', 'Up', 'Right']): 
                arrow = self.ArrowsKeys(self.screen, i * 125 + 40 , 560, direction)
                self.arrowList.append(arrow)
            




    

        
            

    def __init__(self, screen):

        self.screen = screen
        self.dogg = self.Dog(screen)
        self.streak = 2
        self.width = 850
        self.counter = 0
        self.height = 700
        self.colorScreen = (0, 0, 0)  
        self.clickedX = 20
        self.clickedY = 20
        self.clicked = 0
        self.lives = 3

        self.title_font = pygame.font.Font("assets/Daydream.ttf", 60)

        self.faceUp = pygame.image.load("assets/burningUp.png")
        self.faceLeft = pygame.image.load("assets/burningLeft.png")
        self.faceDown =  pygame.transform.flip(self.faceUp, False, True) 
        self.faceRight = pygame.transform.flip(self.faceLeft, True, False) 

        self.startImg = pygame.image.load("assets/startBack.png")
        self.startRect = self.startImg.get_rect()

        self.endImg = pygame.image.load("assets/lostBack.png")
        self.endRect= self.startImg.get_rect()
        
        self.sadSong = pygame.mixer.Sound("assets/sadSound.mp3")
        self.thud1 = pygame.mixer.Sound("assets/thud2.mp3")
        pygame.mixer.music.load("assets/ost.mp3") 
        pygame.mixer.music.set_volume(0.5) 
        

        self.fallingList = []
        self.heldKeysPrev = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
        self.arrowList = []
        self.GenerateArrows(self.screen , self.arrowList)
        self.MENU, self.PLAYING , self.LOST = "menu" , "playing" , "lost"
        self.state = self.MENU
        self.font = pygame.font.SysFont("assets/Daydream.ttf", 48)
        self.text_surface = self.font.render(str(self.clicked), True, (0,255,0))
        
        
        self.background_image2 = pygame.image.load("assets/backtest5_2.png")
        self.background_image1 = pygame.image.load("assets/backtest5_1.png")

    

    class fallingSquare:
        def __init__(self,screen,x,y,id):
            self.screen = screen
            self.x = x
            self.y = y
            self.id = id
            self.width = 80
            self.height = 80
            self.color = (0,255,0)
            self.speed = 5
            self.body = pygame.Rect(self.x , self.y , self.width , self.height)

        def draw(self,faceUp,faceLeft,faceDown,faceRight):
            self.y += self.speed
            self.body = pygame.Rect(self.x , self.y , self.width , self.height)
            if self.id == 0:
                self.screen.blit(faceLeft, self.body)
            elif self.id ==1:
                self.screen.blit(faceDown, self.body)
            elif self.id ==2:
                self.screen.blit(faceUp, self.body)
            elif self.id ==3:
                self.screen.blit(faceRight, self.body)
            
    def render_text_with_border(self, text, font, x, y, color, border_color=(0, 0, 0), border_width=2):
        border_text = font.render(text, True, border_color)
        offsets = [
            (-border_width, 0), (border_width, 0), 
            (0, -border_width), (0, border_width),
            (-border_width, -border_width), (-border_width, border_width),
            (border_width, -border_width), (border_width, border_width)
        ]
        for dx, dy in offsets:
            border_rect = border_text.get_rect(center=(x + dx, y + dy))
            self.screen.blit(border_text, border_rect.topleft)

        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        self.screen.blit(rendered_text, text_rect.topleft)

    def render_text_with_hover(self, text, font, x, y, color, hover_color, Gx, Gy, click):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))

        if text_rect.collidepoint(Gx, Gy):
            rendered_text = font.render(text, True, hover_color)

        self.screen.blit(rendered_text, text_rect.topleft)
        
    
    def render_text_with_both(self, text, font, x, y, color, hover_color, Gx, Gy, click, border_color=(0, 0, 0), border_width=2):

        self.render_text_with_border(text, font, x, y, color, border_color, border_width)
        return self.render_text_with_hover(text, font, x, y, color, hover_color, Gx, Gy, click)
        
    def spawnNotes(self):
            i = random.randint(0,3)
            y = random.randint(-1000,-500)
            
            self.pog = self.fallingSquare(self.screen , i*125+40 , y, i)
            self.fallingList.append(self.pog)
            return y 

    
    def checkIfallIn(self):
        pog = True
        for sqr in self.fallingList:
            if sqr.y <=0:
                pog = False
        return pog
    
    def checkCollision(self,body):
        for i,sqr in enumerate(self.fallingList):
            if sqr.body.colliderect(body) and sqr.body.y >= body.y :
                self.thud1.play()
                self.streak += 1 
                self.fallingList.pop(i)
    
    

    def renderStreak(self,streak):
        self.render_text_with_border(f"{str(streak-2)}",self.title_font, x=750 ,y=75 , color = (255,255,255), border_color=(0,0,0),border_width = 4)

    def resetGame(self):
        self.fallingList = []
        self.lives = 3 
        self.streak = 2

    

    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        if self.state == self.PLAYING:
            self.counter +=1
            if self.counter <=20:
                screen.blit(self.background_image1,(0,0))
            else:
                screen.blit(self.background_image2,(0,0))
            if self.counter == 40:
                self.counter = 1
            self.dogg.draw(held_keys)

            self.renderStreak(self.streak)


            for i,arrow in enumerate(self.arrowList) :
                arrow.draw(arrow.key, held_keys)

            for i,fallSqr in enumerate(self.fallingList):
                fallSqr.draw(self.faceUp,self.faceLeft,self.faceDown,self.faceRight)
                if fallSqr.y >700:
                    self.lives -=1
                    self.fallingList.pop(i)
                    if self.lives  == 0 :
                        pygame.mixer.music.stop()
                        Add_Credits(int(self.streak*5))
                        self.lives = 3
                        self.fallingList = []
                        self.sadSong.play()
                        self.state = self.LOST

            

            if self.lives == 0:
                self.resetGame()

            for arrow in self.arrowList:
                for direction, status in held_keys.items():
                    
                    if arrow.key == direction and status == True and self.heldKeysPrev[direction] == False :
                        print(arrow.arrowBody)
                        try:
                            self.checkCollision(arrow.arrowBody)
                        except:
                            pass
                    
                        

                    
                    self.heldKeysPrev[status] = status
            


        
            if self.checkIfallIn() and not self.fallingList:
                for i in range(int(self.streak/2)+1):
                    self.spawnNotes()
        
        if self.state == self.LOST:
            screen.blit(self.endImg , self.endRect)
            
            self.title_font = pygame.font.Font("assets/Daydream.ttf", 60)


            title_text = self.title_font.render("YOU LOST", True, (0, 0, 0))

        
            self.render_text_with_border("YOU LOST", self.title_font , self.width//2 - title_text.get_width()//2+225, 75, (255,255,255), border_width = 4 )

            title_text1 = self.title_font.render(f"SCORE : {str(self.streak-2)}", True, (0, 0, 0))
            self.render_text_with_border(f"SCORE : {str(self.streak-2)}", self.title_font , self.width//2 - title_text1.get_width()//2+225, 225, (255,255,255), border_width = 4 )

            held_keys = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
            smaller_font = pygame.font.Font("assets/Daydream.ttf", 40)
            smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))
            smaller_text_x = self.width // 2 - smaller_text.get_width() // 2-100
            smaller_text_y = self.height // 2 

            if (smaller_text_x <= Gx <= smaller_text_x + smaller_text.get_width() +200 and
                smaller_text_y <= Gy <= smaller_text_y + smaller_text.get_height()):
                smaller_text = smaller_font.render("PLAY AGAIN", True, (140, 140, 139))

                if click:

                    self.resetGame()

                    for i in range(int(self.streak/2)+1):
                        pygame.mixer.music.play(-1)

                        self.spawnNotes()
                    held_keys = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
                    self.heldKeysPrev = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
                    self.state = self.PLAYING
            else:
                smaller_text = smaller_font.render("PLAY AGAIN", True, (0, 0, 0))
            self.render_text_with_both("PLAY AGAIN",smaller_font , smaller_text_x+175,smaller_text_y , (255,255,255), (105,105,105),Gx ,Gy ,click ,border_width= 4)


        if self.state == self.MENU:
            screen.blit(self.startImg , self.startRect)

            

            title_font = pygame.font.Font("assets/Daydream.ttf", 60)
            title_text = title_font.render("Forest Fire!", True, (0, 0, 0))

            self.render_text_with_border("Forest Fire!",self.title_font, self.width//2 - title_text.get_width()//2+300 ,80 , color = (255,255,255), border_color=(0,0,0),border_width = 4)
            held_keys = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
            smaller_font = pygame.font.Font("assets/Daydream.ttf", 50)

            smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))
            smaller_text_x = self.width // 2 - smaller_text.get_width() // 2
            smaller_text_y = self.height // 2 - 50


            if (smaller_text_x <= Gx <= smaller_text_x + smaller_text.get_width() and
                smaller_text_y <= Gy <= smaller_text_y + smaller_text.get_height()):
                smaller_text = smaller_font.render("PLAY", True, (140, 140, 139))

                if click:
                    self.resetGame()
                    pygame.mixer.music.play(-1)
                    for i in range(int(self.streak/2)+1):
                        self.spawnNotes()
                    held_keys = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
                    self.heldKeysPrev = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False}
                    self.state = self.PLAYING
            else:
                smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))

            self.render_text_with_both("PLAY",smaller_font , smaller_text_x+100,smaller_text_y , 
                                       (255,255,255), (105,105,105),Gx ,Gy ,click ,border_width= 4)


class EppyMilo():
    class CreateCat:
        def __init__(self, screen):
            self.screen = screen
            self.catnapx = 250
            self.catnapy = 270
            self.catnapWidth = 325
            self.catnapHeight = 200
            self.catnapHealth = 3
            
            self.catnapBody = pygame.Rect(self.catnapx,self.catnapy , self.catnapWidth , self.catnapHeight)

            self.background_image1 = pygame.image.load("assets/caca.png")
            self.background_image1 = pygame.transform.scale(self.background_image1, (self.catnapWidth, self.catnapHeight))

            self.background_image2 = pygame.image.load("assets/caca2.png")
            self.background_image2 = pygame.transform.scale(self.background_image2, (self.catnapWidth, self.catnapHeight))

            self.background_image3 = pygame.image.load("assets/caca3.png")
            self.background_image3 = pygame.transform.scale(self.background_image3, (self.catnapWidth, self.catnapHeight))
            self.color = (255, 0, 0)  


        def draw(self):
            
            match self.catnapHealth:
                case 1 :
                    self.screen.blit(self.background_image3, self.catnapBody)
                case 2 :
                    self.screen.blit(self.background_image2, self.catnapBody)
                case 3 :
                    self.screen.blit(self.background_image1, self.catnapBody)
            pass
    
    class createFlea:
        def __init__(self,screen ):
            self.screen = screen
            self.fleaHeight = 30
            self.fleaWidth = 30
            self.fleaid = random.randint(1,3)
            self.frames = 1
            self.catRect = pygame.Rect(375,320 , 100 , 100)
            self.offset = random.randint(1,20)

            self.fleaSpeed = 5
            
            self.color = (128,128,128)
            self.presetSpawn = random.randint(1,4)

            match self.presetSpawn:
                case 1:
                    self.fleax = random.randint(-100 , -50)
                    self.fleay = random.randint(-100,800)
                case 2:
                    self.fleax = random.randint(-100,950)
                    self.fleay = random.randint(-100,-50)
                case 3:
                    self.fleax = random.randint(900 , 950)
                    self.fleay = random.randint( -100,800)
                case 4:
                    self.fleax = random.randint(-100,950)
                    self.fleay = random.randint(750,800)

            self.background_image1 = pygame.image.load("assets/fly1.png")
            self.background_image1 = pygame.transform.scale(self.background_image1, (self.fleaWidth, self.fleaHeight))

            self.background_image2 = pygame.image.load("assets/fly2.png")
            self.background_image2 = pygame.transform.scale(self.background_image2, (self.fleaWidth, self.fleaHeight))

            self.background_image3 = pygame.image.load("assets/fly3.png")
            self.background_image3 = pygame.transform.scale(self.background_image3, (self.fleaWidth, self.fleaHeight))

                
            print(self.fleax,self.fleay)
            
            self.background_image4 = pygame.image.load("assets/fly1r.png")
            self.background_image1 = pygame.transform.scale(self.background_image1, (self.fleaWidth, self.fleaHeight))

            self.background_image5 = pygame.image.load("assets/fly2r.png")
            self.background_image2 = pygame.transform.scale(self.background_image2, (self.fleaWidth, self.fleaHeight))

            self.background_image6 = pygame.image.load("assets/fly3r.png")
            self.background_image3 = pygame.transform.scale(self.background_image3, (self.fleaWidth, self.fleaHeight))

            self.distance_from_centre = math.sqrt((425  - self.fleax) ** 2 + (370 - self.fleay) ** 2)
            self.fleaBody = pygame.Rect (self.fleax , self.fleay ,self.fleaWidth , self.fleaHeight)
                
        
        def checkCollisonCat(self):
            if self.fleaBody.colliderect(self.catRect):
                return 1
            return 0

        def frameCalc(self):
            if self.fleax>400:
                if self.frames == 1:
                    self.screen.blit(self.background_image1, self.fleaBody)
                    self.frames += 1
                elif self.frames == 2:
                    self.screen.blit(self.background_image2, self.fleaBody)
                    self.frames +=1
                elif self.frames == 3:
                    self.screen.blit(self.background_image3, self.fleaBody)
                    self.frames = 1
            else:
                if self.frames == 1:
                    self.screen.blit(self.background_image4, self.fleaBody)
                    self.frames += 1
                elif self.frames == 2:
                    self.screen.blit(self.background_image5, self.fleaBody)
                    self.frames +=1
                elif self.frames == 3:
                    self.screen.blit(self.background_image6, self.fleaBody)
                    self.frames = 1
        
        def moveTowardsCat (self):
            dx = 415 - self.fleax
            dy = 360 - self.fleay

            distance = math.sqrt(dx**2 + dy**2)

            if distance != 0:
                dx /= distance
                dy /= distance
                self.fleax += dx * self.fleaSpeed
                self.fleay += dy * self.fleaSpeed
            

            self.fleaBody = pygame.Rect (self.fleax , self.fleay ,self.fleaWidth , self.fleaHeight)
            
            self.frameCalc()
        
        def fiboMoveRev(self):
            self.speed = 1
            
            angle = pygame.time.get_ticks() / 1000 * self.speed  + self.offset
            self.fleax = 425 + self.distance_from_centre * math.cos(angle)
            self.fleay = 370 + self.distance_from_centre * math.sin(angle)

            self.distance_from_centre = math.sqrt((425  - self.fleax) ** 2 + (370 - self.fleay) ** 2)

            if self.distance_from_centre > 50/2:
                self.distance_from_centre -= 2

            self.fleaBody = pygame.Rect (self.fleax , self.fleay ,self.fleaWidth , self.fleaHeight)
            self.frameCalc()

        def fiboMove(self):
            self.speed = 1
            
            angle = pygame.time.get_ticks() / 1000 * self.speed  + self.offset
            self.fleax = 425 + self.distance_from_centre * math.sin(angle)
            self.fleay = 370 + self.distance_from_centre * math.cos(angle)

            self.distance_from_centre = math.sqrt((425  - self.fleax) ** 2 + (370 - self.fleay) ** 2)

            if self.distance_from_centre > 50/2:
                self.distance_from_centre -= 2

            self.fleaBody = pygame.Rect (self.fleax , self.fleay ,self.fleaWidth , self.fleaHeight)            
            self.frameCalc()


        def draw(self):
            if self.fleaid == 1 :
                self.moveTowardsCat()
            elif self.fleaid == 2:
                self. fiboMove()
            else:
                self.fiboMoveRev()
           
    def __init__(self, screen):
        self.screen = screen
        self.gotReward = False
        self.k = 0
        self.width = 850
        self.height = 700
        self.fleaList = []
        self.fleaAlive = 0
        self.clickedX = 20
        self.clickedY = 20

        self.fleaWave = 0
        self.clicked = 0
        self.colorScreen = (0, 0, 0) 

        self.MENU, self.PLAYING , self.LOST = "menu" , "playing" , "lost"
        self.state = self.MENU
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.Font("assets/Daydream.ttf", 60)
        self.text_surface = self.font.render(str(self.clicked), True, (0,255,0))
        self.catnapMain = self.CreateCat(screen)

        self.bugSquash = pygame.mixer.Sound("assets/squashBug.mp3")
        self.bugSquash.set_volume(0.5)

        self.angryCat = pygame.mixer.Sound("assets/angryCat.mp3")
        self.angryCat.set_volume(0.5)

        self.startImg = pygame.image.load("assets/startPicCat.png")
        self.startRect = self.startImg.get_rect()

        self.endImg = pygame.image.load("assets/endPiccat.png")
        self.endRect= self.startImg.get_rect()
            
        pygame.mixer.music.load("assets/heartost.mp3")
        pygame.mixer.music.set_volume(0.5) 
        
        

        self.background_image = pygame.image.load("assets/backgrs.png")
    
    def spawnWave(self):
            for i in range(self.fleaWave+2):
                self.pog = self.createFlea(self.screen )
                self.fleaList.append(self.pog)
                self.fleaAlive +=1   
                print(self.fleaAlive)
    

    def render_text_with_border(self, text, font, x, y, color, border_color=(0, 0, 0), border_width=2):
        border_text = font.render(text, True, border_color)
        offsets = [
            (-border_width, 0), (border_width, 0), 
            (0, -border_width), (0, border_width),
            (-border_width, -border_width), (-border_width, border_width),
            (border_width, -border_width), (border_width, border_width)
        ]
        for dx, dy in offsets:
            border_rect = border_text.get_rect(center=(x + dx, y + dy))
            self.screen.blit(border_text, border_rect.topleft)

        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        self.screen.blit(rendered_text, text_rect.topleft)


    def render_text_with_hover(self, text, font, x, y, color, hover_color, Gx, Gy, click):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))

        if text_rect.collidepoint(Gx, Gy):
            rendered_text = font.render(text, True, hover_color)

        self.screen.blit(rendered_text, text_rect.topleft)
        
    
    def render_text_with_both(self, text, font, x, y, color, hover_color, Gx, Gy, click, border_color=(0, 0, 0), border_width=2):
        self.render_text_with_border(text, font, x, y, color, border_color, border_width)
        return self.render_text_with_hover(text, font, x, y, color, hover_color, Gx, Gy, click)


    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        if self.state == self.PLAYING:
            screen.blit(self.background_image,(0,0))

            self.catnapMain.draw()

            if self.fleaAlive == 0 :
                self.fleaWave += 1 
                self.spawnWave()
                self.gotReward = False
            
            if self.fleaWave > 3 and self.gotReward == False:
                self.gotReward = True
                Add_Credits(50)
            
            try:
                for i,flea in enumerate(self.fleaList) :
                    flea.draw()
                    if flea.checkCollisonCat():
                        self.fleaList.pop(i)
                        self.angryCat.play()
                        self.fleaAlive -= 1
                        self.catnapMain.catnapHealth -= 1

                        if self.catnapMain.catnapHealth == 0:
                            self.state = self.LOST
                            self.text_surface = self.font.render(str(self.clicked), True, (0,255,0))
                            print("entered")
                            self.fleaList = []
                            self.catnapMain.catnapHealth = 3
                            self.fleaWave = 0
                            self.fleaAlive = 0
                            pygame.mixer.music.stop()
                                
                        print (self.catnapMain.catnapHealth)
            except: 
                pass

            
            self.render_text_with_border(str(self.clicked), self.title_font ,70, 70, (255,255,255), border_width = 4 )


            
            if click :
                try:
                    for i, flea in enumerate(self.fleaList):
                        if Gx >= flea.fleax-10 and Gx <= flea.fleax+10 + flea.fleaWidth and Gy >= flea.fleay-10 and Gy <= flea.fleay+10 + flea.fleaHeight:
                            print("Flea collided")
                            self.clicked += 1
                            self.text_surface = self.font.render(str(self.clicked), True, (0,255,0))
                            self.fleaList.pop(i)
                            self.bugSquash.play()
                            self.fleaAlive -= 1
                            break
                except:
                    pass

        if self.state == self.LOST:
            screen.blit(self.endImg , self.endRect)

            title_font = pygame.font.Font("assets/Daydream.ttf", 60)
            title_text = title_font.render("YOU LOST", True, (0, 0, 0))
            self.render_text_with_border("YOU LOST", title_font , self.width//2 - title_text.get_width()//2+225, 75,
                                          (255,255,255), border_width = 4 )

            title_text1 = self.title_font.render(f"SCORE : {str(self.clicked)}", True, (0, 0, 0))
            self.render_text_with_border(f"SCORE : {str(self.clicked)}", self.title_font , self.width//2 - title_text1.get_width()//2+225, 250, (
                255,255,255), border_width = 4 )
            
            smaller_font = pygame.font.Font("assets/Daydream.ttf", 40)
            smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))
            smaller_text_x = self.width // 2 - smaller_text.get_width() // 2-100
            smaller_text_y = self.height // 2 + 50

            if (smaller_text_x <= Gx <= smaller_text_x + smaller_text.get_width()+200 and
                smaller_text_y <= Gy <= smaller_text_y + smaller_text.get_height()):
                smaller_text = smaller_font.render("PLAY AGAIN", True, (140, 140, 139))
                if click:
                    pygame.mixer.music.play(-1)
                    self.clicked = 0
                    self.state = self.PLAYING
            else:
                smaller_text = smaller_font.render("PLAY AGAIN", True, (0, 0, 0))

            self.render_text_with_both("PLAY AGAIN",smaller_font , smaller_text_x+175,smaller_text_y , (255,255,255), 
                                       (105,105,105),Gx ,Gy ,click ,border_width= 4)
            
        if self.state == self.MENU:
            screen.blit(self.startImg , self.startRect)

            title_font = pygame.font.Font("assets/Daydream.ttf", 60)
            title_text = title_font.render("eppy milo", True, (0, 0, 0))
            self.render_text_with_border("eppy milo",title_font, self.width//2 - title_text.get_width()//2+250 ,80 , color = (255,255,255), border_color=(0,0,0),border_width = 4)

            smaller_font = pygame.font.Font("assets/Daydream.ttf", 50)
            smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))
            smaller_text_x = self.width // 2 - smaller_text.get_width() // 2
            smaller_text_y = self.height // 2 - 50

            if (smaller_text_x <= Gx <= smaller_text_x + smaller_text.get_width() and
                smaller_text_y <= Gy <= smaller_text_y + smaller_text.get_height()):
                smaller_text = smaller_font.render("PLAY", True, (140, 140, 139))
                if click:
                    pygame.mixer.music.play(-1)
                    self.state = self.PLAYING
            else:
                smaller_text = smaller_font.render("PLAY", True, (0, 0, 0))

            self.render_text_with_both("PLAY",smaller_font , smaller_text_x+100,smaller_text_y , 
                                       (255,255,255), (105,105,105),Gx ,Gy ,click ,border_width= 4)









