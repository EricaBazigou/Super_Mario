import pygame      # Εισαγωγή της βιβλιοθήκης Pygame
import random      # Εισαγωγή της βιβλιοθήκης random για τυχαίες τιμές
import os          # Εισαγωγή της βιβλιοθήκης os για διαχείριση διαδρομών (paths)

# --- 1. Αρχικοποίηση Pygame και Ρυθμίσεις ---
pygame.init()      # Αρχικοποίηση όλων των modules του Pygame

# Σταθερές Οθόνης
SCREEN_WIDTH = 800         # Ορισμός του πλάτους της οθόνης σε pixels
SCREEN_HEIGHT = 600        # Ορισμός του ύψους της οθόνης σε pixels
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Δημιουργία του παραθύρου/οθόνης
pygame.display.set_caption("Super Mario 2D Game") # Ορισμός του τίτλου του παραθύρου

# Χρώματα
BLACK = (0, 0, 0)          # Μαύρο χρώμα (RGB)
WHITE = (255, 255, 255)    # Άσπρο χρώμα (RGB)
RED_PLACEHOLDER = (200, 50, 50) # Κόκκινο για χρήση ως placeholder

# Ρυθμός Καρέ (FPS)
FPS = 60                   # Ορισμός του ρυθμού ανανέωσης (Frames Per Second)
clock = pygame.time.Clock() # Δημιουργία αντικειμένου Clock για τον έλεγχο του FPS

# Σταθερές Παιχνιδιού (Αυξημένη Δυσκολία)
PLAYER_SPEED = 7           # Ταχύτητα κάθετης κίνησης του Mario
OBSTACLE_BASE_SPEED = 7    # Βασική ταχύτητα κίνησης των εμποδίων
STAR_BONUS = 5             # Πόντοι που δίνει το κανονικό αστέρι
MIN_SPAWN_INTERVAL = 400   # Ελάχιστος χρόνος (ms) μεταξύ δημιουργίας αντικειμένων
MAX_SPAWN_INTERVAL = 1000  # Μέγιστος χρόνος (ms) μεταξύ δημιουργίας αντικειμένων

SUPER_STAR_SIZE = (60, 60) # Μέγεθος του Super Star
SUPER_STAR_BONUS = STAR_BONUS * 2 # Πόντοι που δίνει το Super Star

# --- 2. Φόρτωση Γραφικών (Εικόνες) ---

# Απόλυτη διαδρομή προς τον φάκελο assets
ASSET_DIR = r'C:\Users\erica\Desktop\Super_Mario\assets' 

# Διαστάσεις Sprite 
MARIO_SIZE = (50, 75)      # Μέγεθος sprite του Mario
ENEMY_SIZE = (55, 55)      # Μέγεθος sprite των εχθρών
STAR_SIZE = (40, 40)       # Μέγεθος sprite του αστεριού

# Μεταβλητές για τις εικόνες
PLAYER_IMAGE = None
BACKGROUND_IMAGE = None
ENEMY_IMAGES = []
STAR_IMAGE = None
SUPER_STAR_IMAGE = None 
MUSIC_LOADED = False       # Έλεγχος αν η μουσική φορτώθηκε επιτυχώς

try:
    # 2.1. Φόρτωση Παίκτη και Φόντου
    # Φόρτωση εικόνας Mario, μετατροπή με διαφάνεια (convert_alpha)
    PLAYER_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, 'mario.png')).convert_alpha()
    PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, MARIO_SIZE) # Αλλαγή μεγέθους
    
    # Φόρτωση εικόνας φόντου (convert)
    BACKGROUND_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, 'background.png')).convert()
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Αλλαγή μεγέθους στο μέγεθος οθόνης

    # 2.2. Φόρτωση Εμποδίων (5 εχθροί)
    enemy_files = ['goomba.png', 'koopa.png', 'plant.png', 'buzzy_beetle.png', 'hammer_bro.png']
    for filename in enemy_files: # Επανάληψη για κάθε αρχείο εχθρού
        img = pygame.image.load(os.path.join(ASSET_DIR, filename)).convert_alpha()
        img = pygame.transform.scale(img, ENEMY_SIZE)
        ENEMY_IMAGES.append(img) # Προσθήκη της εικόνας στη λίστα

    # 2.3. Φόρτωση Power-up
    STAR_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, 'star.png')).convert_alpha()
    STAR_IMAGE = pygame.transform.scale(STAR_IMAGE, STAR_SIZE)
    
    SUPER_STAR_IMAGE = pygame.image.load(os.path.join(ASSET_DIR, 'super_star.png')).convert_alpha()
    SUPER_STAR_IMAGE = pygame.transform.scale(SUPER_STAR_IMAGE, SUPER_STAR_SIZE)
    
    # ******************************************************
    # [ΦΟΡΤΩΣΗ ΤΟΥ MP3]
    # ******************************************************
    pygame.mixer.init()         # Αρχικοποίηση του mixer (για ήχο)
    
    MUSIC_FILE = 'mario_theme.mp3' 
    pygame.mixer.music.load(os.path.join(ASSET_DIR, MUSIC_FILE)) # Φόρτωση του αρχείου μουσικής
    
    MUSIC_LOADED = True         # Επιτυχής φόρτωση, ορίζουμε τη σημαία σε True
    print(f"Το αρχείο μουσικής {MUSIC_FILE} φορτώθηκε επιτυχώς.") # Εκτύπωση επιβεβαίωσης


except pygame.error as e: # Εάν αποτύχει οποιαδήποτε φόρτωση (εικόνας/ήχου)
    print(f"Σφάλμα φόρτωσης γραφικών ή μουσικής. Χρησιμοποιούνται placeholders. Error: {e}")
    # ... (placeholders για εικόνες - Δημιουργία απλών επιφανειών αν αποτύχει η φόρτωση)
    PLAYER_IMAGE = pygame.Surface(MARIO_SIZE); PLAYER_IMAGE.fill(BLACK)
    for i in range(5): 
        placeholder = pygame.Surface(ENEMY_SIZE); placeholder.fill(RED_PLACEHOLDER)
        ENEMY_IMAGES.append(placeholder)
        
    STAR_IMAGE = pygame.Surface(STAR_SIZE); STAR_IMAGE.fill((255, 255, 0))
    SUPER_STAR_IMAGE = pygame.Surface(SUPER_STAR_SIZE); SUPER_STAR_IMAGE.fill((255, 165, 0))
    BACKGROUND_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); BACKGROUND_IMAGE.fill(WHITE)
    
# Φόρτωση Γραμματοσειράς
font_score = pygame.font.Font(None, 40)    # Γραμματοσειρά για το σκορ
font_message = pygame.font.Font(None, 74)  # Γραμματοσειρά για μηνύματα (π.χ. Game Over)

# --- 3. Κλάσεις (Player, Obstacle, Star) ---
class Player(pygame.sprite.Sprite): # Κλάση για τον παίκτη, κληρονομεί από Pygame Sprite
    def __init__(self):
        super().__init__()          # Καλεί τον constructor της Sprite
        self.image = PLAYER_IMAGE   # Ορίζει την εικόνα
        self.rect = self.image.get_rect() # Παίρνει το ορθογώνιο περίγραμμα (για συγκρούσεις/θέση)
        self.rect.x = 50            # Αρχική θέση X
        self.rect.y = SCREEN_HEIGHT // 2 - self.rect.height // 2 # Αρχική θέση Y (κέντρο)
        self.vel_y = 0              # Κάθετη ταχύτητα (αρχικά 0)
    
    def update(self):
        self.rect.y += self.vel_y   # Μετακινεί τον παίκτη κάθετα
        
        # Περιορισμός εντός οθόνης (Πάνω όριο)
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0 
        # Περιορισμός εντός οθόνης (Κάτω όριο)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0 

    def move_up(self):
        self.vel_y = -PLAYER_SPEED  # Κινείται προς τα πάνω (αρνητική ταχύτητα)
        
    def move_down(self):
        self.vel_y = PLAYER_SPEED   # Κινείται προς τα κάτω (θετική ταχύτητα)
        
    def stop_vertical(self):
        self.vel_y = 0              # Σταματάει την κάθετη κίνηση
        
class Obstacle(pygame.sprite.Sprite): # Κλάση για τα εμπόδια
    def __init__(self, speed):
        super().__init__()
        self.image = random.choice(ENEMY_IMAGES) # Επιλογή τυχαίου εχθρού
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH          # Ξεκινάει εκτός οθόνης (δεξιά)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height) # Τυχαία θέση Y
        self.speed = speed                  # Ορίζει την ταχύτητα

    def update(self):
        self.rect.x -= self.speed           # Κινείται προς τα αριστερά (μείωση X)
        
        # Εάν το εμπόδιο βγει από την αριστερή πλευρά της οθόνης
        if self.rect.right < 0:
            self.kill()                     # Καταστρέφει το sprite (αφαίρεση από τα groups)
            global score
            score += 1                      # Αυξάνει το σκορ (για επιτυχή αποφυγή)

class Star(pygame.sprite.Sprite): # Κλάση για τα αστέρια (power-ups)
    def __init__(self, speed, type='normal'):
        super().__init__()
        self.type = type
        if type == 'super':
            self.image = SUPER_STAR_IMAGE
            self.points = SUPER_STAR_BONUS
        else:
            self.image = STAR_IMAGE
            self.points = STAR_BONUS
            
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH 
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed           # Κινείται προς τα αριστερά
        
        if self.rect.right < 0:
            self.kill()                     # Καταστρέφει το sprite αν βγει εκτός

# --- 6. Συναρτήσεις Διαχείρισης Παιχνιδιού ---

def draw_score():
    score_text = font_score.render(f"Σκορ: {score}", True, BLACK) # Δημιουργία κειμένου σκορ
    SCREEN.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10)) # Σχεδίαση στην πάνω δεξιά γωνία

def reset_game():
    """Επαναφέρει την κατάσταση του παιχνιδιού στις αρχικές τιμές."""
    global game_over, score, last_spawn_time, player
    global MUSIC_LOADED # Χρειαζόμαστε πρόσβαση στη σημαία φόρτωσης μουσικής
    
    game_over = False
    score = 0
    
    all_sprites.empty()       # Καθαρισμός όλων των sprites
    obstacles_group.empty()
    stars_group.empty() 
    
    player = Player()
    all_sprites.add(player)   # Δημιουργία και προσθήκη νέου παίκτη
    
    last_spawn_time = pygame.time.get_ticks()
    
    # ΞΑΝΑΞΕΚΙΝΗΣΗ ΜΟΥΣΙΚΗΣ ΣΤΟ RESET ΜΟΝΟ ΑΝ ΕΧΕΙ ΦΟΡΤΩΘΕΙ
    if MUSIC_LOADED:
        pygame.mixer.music.play(-1) # Ξαναρχίζει να παίζει σε λούπα


def spawn_entity():
    choice = random.random() # Τυχαία τιμή από 0 έως 1
    
    if choice < 0.8: # 80% πιθανότητα
        new_obstacle = Obstacle(OBSTACLE_BASE_SPEED)
        all_sprites.add(new_obstacle)
        obstacles_group.add(new_obstacle)
        
    elif choice < 0.95: # 15% πιθανότητα (μεταξύ 0.8 και 0.95)
        new_star = Star(OBSTACLE_BASE_SPEED, type='normal')
        all_sprites.add(new_star)
        stars_group.add(new_star)
        
    else: # 5% πιθανότητα (μεταξύ 0.95 και 1)
        new_super_star = Star(OBSTACLE_BASE_SPEED, type='super')
        all_sprites.add(new_super_star)
        stars_group.add(new_super_star)

# --- 7. Κύριες Μεταβλητές Παιχνιδιού και Groups ---
all_sprites = pygame.sprite.Group()   # Ομάδα για όλα τα sprites (για εύκολο draw/update)
obstacles_group = pygame.sprite.Group() # Ομάδα μόνο για τα εμπόδια (για συγκρούσεις)
stars_group = pygame.sprite.Group()     # Ομάδα μόνο για τα αστέρια (για συγκρούσεις)

game_over = False                     # Κατάσταση παιχνιδιού
score = 0                             # Αρχικό σκορ
last_spawn_time = pygame.time.get_ticks() # Χρόνος της τελευταίας δημιουργίας αντικειμένου
SPAWN_INTERVAL = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL) # Τυχαίο διάστημα δημιουργίας

player = Player()                     # Δημιουργία αντικειμένου παίκτη
all_sprites.add(player)               # Προσθήκη του παίκτη στην ομάδα

# ΕΝΑΡΞΗ ΜΟΥΣΙΚΗΣ ΣΤΗΝ ΑΡΧΗ ΤΟΥ ΠΑΙΧΝΙΔΙΟΥ ΜΟΝΟ ΑΝ ΕΧΕΙ ΦΟΡΤΩΘΕΙ
if MUSIC_LOADED: # Ελέγχει αν η MUSIC_LOADED είναι True (αν η φόρτωση ήταν επιτυχής)
    try:
        pygame.mixer.music.play(-1)     # Παίζει συνεχώς (-1 για λούπα)
        pygame.mixer.music.set_volume(0.5) # Ρυθμίζει την ένταση στο 50%
    except pygame.error:
        print("Η μουσική δεν μπόρεσε να ξεκινήσει.")


# --- 8. Ο Κύκλος του Παιχνιδιού (Game Loop) ---
running = True # Μεταβλητή για τον έλεγχο του βρόχου
while running: # Κύριος βρόχος του παιχνιδιού
    clock.tick(FPS) # Περιορίζει τον βρόχο να τρέχει στο μέγιστο FPS

    # --- Διαχείριση Συμβάντων (Events) ---
    for event in pygame.event.get(): # Λαμβάνει όλα τα συμβάντα
        if event.type == pygame.QUIT:
            running = False # Έξοδος από τον βρόχο αν κλείσει το παράθυρο
        
        if not game_over: # Χειρισμός κίνησης μόνο αν το παιχνίδι τρέχει
            if event.type == pygame.KEYDOWN: # Όταν πατηθεί ένα πλήκτρο
                if event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()
            
            if event.type == pygame.KEYUP: # Όταν αφεθεί ένα πλήκτρο
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.stop_vertical() # Σταματάει την κίνηση
        else: # Αν το παιχνίδι έχει τελειώσει (Game Over)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game() # Επανεκκίνηση με το πλήκτρο SPACE

    # --- 9. Λογική Παιχνιδιού (Update) ---
    if not game_over: # Εκτέλεση λογικής μόνο αν το παιχνίδι τρέχει
        
        all_sprites.update() # Καλεί τη μέθοδο update() για όλα τα sprites
        
        # Λογική Δημιουργίας (Spawn Logic)
        now = pygame.time.get_ticks() # Τρέχων χρόνος
        if now - last_spawn_time > SPAWN_INTERVAL: # Αν πέρασε αρκετός χρόνος
            spawn_entity() # Δημιουργία νέου αντικειμένου
            last_spawn_time = now
            SPAWN_INTERVAL = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL) # Ορισμός νέου διαστήματος
            
        # Έλεγχος Συγκρούσεων
        
        # α) Σύγκρουση με Εμπόδιο (Game Over)
        # Ελέγχει σύγκρουση παίκτη με οποιοδήποτε εμπόδιο (δεν καταστρέφει το εμπόδιο: False)
        if pygame.sprite.spritecollide(player, obstacles_group, False): 
            if not game_over:
                # ΣΤΑΜΑΤΗΜΑ ΜΟΥΣΙΚΗΣ ΜΟΝΟ ΑΝ ΕΧΕΙ ΦΟΡΤΩΘΕΙ
                if MUSIC_LOADED:
                    pygame.mixer.music.stop() # Σταματάει τη μουσική
            game_over = True # Ορίζει την κατάσταση σε Game Over
            
        # β) Συλλογή Αστεριού (Points)
        # Ελέγχει σύγκρουση παίκτη με αστέρια (καταστρέφει το αστέρι: True)
        stars_collected = pygame.sprite.spritecollide(player, stars_group, True) 
        if stars_collected:
            for star in stars_collected:
                score += star.points # Προσθήκη πόντων
        

    # --- 10. Σχεδίαση (Draw) ---
    
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0)) # Σχεδίαση του φόντου
    
    all_sprites.draw(SCREEN) # Σχεδίαση όλων των sprites στην οθόνη
    
    draw_score() # Σχεδίαση του σκορ
    
    # Εμφάνιση μηνύματος Game Over
    if game_over:
        message = font_message.render("GAME OVER", True, BLACK)
        restart_message = font_score.render("Πατήστε SPACE για επανεκκίνηση", True, BLACK)
        
        # Υπολογισμός κεντρικής θέσης
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        restart_rect = restart_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        SCREEN.blit(message, message_rect)
        SCREEN.blit(restart_message, restart_rect)

    # Τελική ενημέρωση της οθόνης
    pygame.display.flip() # Εμφανίζει στην οθόνη ό,τι σχεδιάστηκε

# --- 11. Τερματισμός Pygame ---
pygame.quit() # Τερματίζει σωστά το Pygame (απελευθέρωση πόρων)