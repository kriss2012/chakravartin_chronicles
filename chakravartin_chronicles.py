import pygame
import sys
import math
import random
import time

# --- Initialization ---
pygame.init()

# --- Screen Settings ---
BASE_WIDTH, BASE_HEIGHT = 1280, 720
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Chakravartin Chronicles")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 150, 0)
DARK_BLUE = (10, 20, 40)
TEJAS_COLOR = (0, 150, 255)
GRANDFATHER_COLOR = (200, 200, 150)
ARJUN_COLOR = (220, 50, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HAMPI_ROCK = (125, 115, 100)
HAMPI_SKY = (255, 220, 180)
WINDOW_BLUE = (20, 30, 60)
BUILDING_COLOR = (30, 40, 55)
LIGHT_YELLOW = (255, 255, 204)
MAHA_SKY = (20, 40, 80)
MAHA_WATER = (40, 80, 150)
MAHA_TEMPLE = (180, 170, 150)
CHID_TEMPLE = (150, 120, 80)
CHID_SKY = (10, 10, 20)
KAILASH_SKY = (150, 160, 180)
KAILASH_ROCK = (80, 90, 110)
SNOW = (240, 240, 240)


# --- Fonts ---
def get_font(size):
    try:
        return pygame.font.Font(None, size)
    except:
        return pygame.font.SysFont("sans", int(size * 0.8))

# --- Game Data (from script) ---
game_script = {
    "INTRO": {
      "text": "Tejas Shrivastava, CEO of a tech empire and a secret archaeologist, discovers an ancient manuscript... It speaks of the Chakravartin Seal, a divine artifact. When strange phenomena erupt at India's most sacred sites, Tejas realizes the Seal is awakening, and he must honor his grandfather's legacy to protect it from dark forces."
    },
    "PHASE_1": {
        "dialogue": [
            {"char": "Tejas", "line": "My grandfather's journal... it speaks of the Chakravartin Seal. The energy readings at Hampi are off the charts."},
            {"char": "Tejas", "line": "I need to decrypt his final notes. It seems they are protected by a riddle."},
            {"char": "Grandfather", "line": "Beta, some knowledge is too powerful for one lifetime. The Seal... it chooses its guardian."},
            {"char": "Tejas", "line": "The encryption is bypassed. His notes mention a rival... Arjun Malhotra."},
            {"char": "Arjun", "line": "So, the scholar's grandson plays with relics. You are out of your league, Shrivastava."},
            {"char": "Tejas", "line": "Arjun! He's already a step ahead. I need to know what he knows. Time for some corporate espionage."},
            {"char": "Tejas", "line": "Got it. His servers show the same energy anomalies. The location is confirmed: Hampi, Karnataka. My journey begins now."}
        ], "puzzle": {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "ECHO"}
    },
    "PHASE_2": {
         "dialogue": [
            {"char": "Tejas", "line": "I've arrived at Hampi. The archaeologists from UNESCO have vanished. The air feels... ancient."},
            {"char": "Tejas", "line": "The locals speak of 'Hanuman's awakening'. I must follow the ancient astronomical alignments through these boulders."}
         ]
    },
    "PHASE_3": {
        "dialogue": [
            {"char": "Tejas", "line": "Mahabalipuram... The second fragment is supposed to be in an underwater chamber beneath the Shore Temple."},
            {"char": "Tejas", "line": "Strange tidal patterns are reported. The Pallava King who built this temple created a sacred lock based on the ocean's rhythm."},
            {"char": "Grandfather", "line": "When the waters rise unnaturally, the serpent king shall test the worthy. Knowledge of the tides is key."},
            {"char": "Tejas", "line": "I need to activate the ancient mechanism in the correct sequence before the chamber floods."}
        ], "puzzle": {"prompt": "Activate the tidal keystones in the correct sequence.", "solution": ["Naga", "Fish", "Turtle", "Sun"]}
    },
    "PHASE_4": {
        "dialogue": [
            {"char": "Tejas", "line": "Chidambaram. The Nataraja Temple. The third fragment vibrates with the cosmic frequency of Shiva's dance."},
            {"char": "Arjun", "line": "You think a few parkour tricks will help you comprehend cosmic geometry? The Seal requires a king, not a technician."},
            {"char": "Tejas", "line": "It requires understanding, Arjun. Not brute force. In Shiva's dance lies the rhythm of the universe."}
        ], "puzzle": {"prompt": "Match the rhythm of the cosmic dance.", "solution": ["up", "down", "left", "right", "up", "right"]}
    },
    "PHASE_5": {
        "dialogue": [
            {"char": "Tejas", "line": "Mount Kailash. The final fragment. Grandfather always said this was the summit of not just the world, but of spirit."},
            {"char": "Grandfather", "line": "The mountain tests all who approach. It strips away ego, leaving only intention. Be pure of heart, beta."},
            {"char": "Tejan", "line": "I have to make it to the monastery at the peak. The weather is getting worse."}
        ], "puzzle": {"prompt": "Ascend the sacred mountain.", "height": 1000}
    },
    "PHASE_6": {
        "dialogue": [
            {"char": "Arjun", "line": "It is complete! The power to restore the glory of the kings is mine!"},
            {"char": "Tejas", "line": "This power is not for one man to wield, Arjun. It's for protecting dharma, not forcing it."},
            {"char": "Cosmic Voice", "line": "The Seal is a mirror. It offers what the heart desires. Choose wisely, Son of Bharata. What is your will?"}
        ], "choices": ["Become the Guardian.", "Destroy the Seal.", "Unify the People.", "Claim Absolute Power."]
    },
    "ENDINGS": {
        "Become the Guardian.": "Tejas accepts his role as protector. Using his vast resources, he establishes a secret organization to safeguard India's spiritual heritage, balancing the modern with the mystical.",
        "Destroy the Seal.": "Fearing its misuse, Tejas shatters the seal. The world is safe from its power, but also loses its divine protection. Mankind is left to forge its own destiny, for better or worse.",
        "Unify the People.": "Tejas uses the Seal's influence to inspire unity and peace. He becomes a reluctant spiritual leader, guiding the nation into a new golden age of conscious technology and shared dharma.",
        "Claim Absolute Power.": "The power was too tempting. Tejas becomes a tyrant, enforcing a strict and sterile order upon the world. He becomes the very thing he fought against, a new dark age under his 'perfect' rule."
    }
}


# --- Responsive UI Class ---
class UIManager:
    def __init__(self):
        self.update_scale()
    def update_scale(self):
        self.width, self.height = screen.get_size()
        self.scale_x = self.width / BASE_WIDTH
        self.scale_y = self.height / BASE_HEIGHT
        self.scale = min(self.scale_x, self.scale_y)
    def get_rect(self, x, y, w, h): return pygame.Rect(x * self.scale_x, y * self.scale_y, w * self.scale_x, h * self.scale_y)
    def get_font_size(self, size): return int(size * self.scale)
    def get_pos(self, x, y): return (x * self.scale_x, y * self.scale_y)

ui = UIManager()

# --- Player Class (Tejas) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 60]); self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.draw_character()
        self.velocity_y = 0; self.on_ground = True
        self.set_pos(350, BASE_HEIGHT - 105)
    def set_pos(self, x, y): self.rect.center = (x, y)
    def draw_character(self, color=TEJAS_COLOR):
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, color, (5, 0, 20, 20)) # Head
        pygame.draw.rect(self.image, color, (0, 22, 30, 38)) # Body
    def update(self, platforms=[]):
        if self.on_ground and "PLATFORMING" not in game.state: self.rect.y += int(math.sin(pygame.time.get_ticks()/200)*2)
        if not self.on_ground: self.velocity_y += 0.5
        self.rect.y += self.velocity_y
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and self.velocity_y >= 0:
                self.rect.bottom = p.rect.top; self.velocity_y = 0; self.on_ground = True; break
    def jump(self):
        if self.on_ground: self.velocity_y = -15; self.on_ground = False

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface([w, h]); self.image.fill(HAMPI_ROCK)
        self.rect = self.image.get_rect(); self.rect.topleft = (x, y)

# --- Text and UI Drawing Helper ---
def draw_text_anim(text, font, color, surface, rect, anim_progress):
    y = rect.top; lineSpacing = -2; font_height = font.get_linesize()
    text_to_show = text[:int(len(text) * anim_progress)]
    while text_to_show:
        i = 1
        if y + font_height > rect.bottom: break
        while font.size(text_to_show[:i])[0] < rect.width and i < len(text_to_show): i += 1
        if i < len(text_to_show): i = text_to_show.rfind(" ", 0, i) + 1
        if i == 0: i=1
        image = font.render(text_to_show[:i], True, color)
        surface.blit(image, (rect.left, y)); y += font_height + lineSpacing; text_to_show = text_to_show[i:]

# --- Main Game Class ---
class Game:
    def __init__(self):
        self.state = "TITLE"; self.clock = pygame.time.Clock()
        self.player = Player(); self.all_sprites = pygame.sprite.Group(self.player)
        self.dialogue_index = 0; self.anim_start_time = 0
        self.puzzle_input = ""; self.puzzle_message = ""
        self.phase_1_tasks = {"puzzle": False, "stealth": False}
        self.sequence_puzzle_state = []; self.puzzle_timer = 0
        self.rhythm_puzzle_state = []; self.rhythm_pulse_time = 0; self.current_rhythm_step = 0
        self.climb_height = 0; self.stamina = 100
        self.ending_choice = 0
        self.setup_all()

    def run(self):
        while True:
            self.handle_events(); self.update(); self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.VIDEORESIZE: ui.update_scale()
            if event.type != pygame.KEYDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN: self.handle_mouse_click(event)
                continue
            
            if self.state in ["TITLE", "INTRO", "ENDING"]:
                if event.key == pygame.K_RETURN: self.advance_gamestate()
            elif "DIALOGUE" in self.state:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]: self.advance_dialogue()
            elif self.state == "PHASE_1_PUZZLE": self.handle_puzzle1_input(event)
            elif self.state == "PHASE_2_PLATFORMING":
                if event.key == pygame.K_SPACE: self.player.jump()
            elif self.state == "PHASE_4_PUZZLE": self.handle_puzzle4_input(event)
            elif self.state == "PHASE_5_CLIMBING":
                if event.key == pygame.K_UP and self.stamina > 10:
                    self.climb_height += 5; self.stamina -= 5
            elif self.state == "PHASE_6_CHOICE":
                 if event.key == pygame.K_UP: self.ending_choice = (self.ending_choice - 1) % 4
                 if event.key == pygame.K_DOWN: self.ending_choice = (self.ending_choice + 1) % 4
                 if event.key == pygame.K_RETURN: self.state = "ENDING"
                 
    def handle_mouse_click(self, event):
        if self.state == "PHASE_3_PUZZLE":
            mouse_pos = pygame.mouse.get_pos()
            for i, btn in enumerate(self.tidal_buttons):
                scaled_btn = ui.get_rect(btn.x, btn.y, btn.w, btn.h)
                if scaled_btn.collidepoint(mouse_pos):
                    symbol = game_script["PHASE_3"]["puzzle"]["solution"][i] #This should be the symbol name
                    self.sequence_puzzle_state.append(symbol)
    
    def advance_gamestate(self):
        if self.state == "TITLE": self.state = "INTRO"
        elif self.state == "INTRO": self.state = "PHASE_1_DIALOGUE"; self.dialogue_index = 0
        elif self.state == "ENDING": self.state = "TITLE"; self.__init__() # Restart game
        self.anim_start_time = time.time()
        
    def advance_dialogue(self):
        current_phase_key = self.state.split('_')[0] + "_" + self.state.split('_')[1]
        if time.time() - self.anim_start_time < 1.0: self.anim_start_time = time.time() - 2.0; return
        self.dialogue_index += 1; self.anim_start_time = time.time()
        
        # State transitions
        if current_phase_key == "PHASE_1":
            if self.dialogue_index == 2 and not self.phase_1_tasks["puzzle"]: self.state = "PHASE_1_PUZZLE"
            elif self.dialogue_index == 6 and not self.phase_1_tasks["stealth"]: self.state = "PHASE_1_STEALTH"
            elif self.dialogue_index >= len(game_script["PHASE_1"]["dialogue"]): self.state = "PHASE_2_DIALOGUE"; self.dialogue_index = 0; self.player.set_pos(50, BASE_HEIGHT - 90)
        elif current_phase_key == "PHASE_2":
            if self.dialogue_index >= len(game_script["PHASE_2"]["dialogue"]): self.state = "PHASE_3_DIALOGUE"; self.dialogue_index = 0; self.player.set_pos(350, BASE_HEIGHT - 105)
        elif current_phase_key == "PHASE_3":
             if self.dialogue_index >= len(game_script["PHASE_3"]["dialogue"]): self.state = "PHASE_3_PUZZLE"; self.puzzle_timer = time.time() + 15
        elif current_phase_key == "PHASE_4":
            if self.dialogue_index >= len(game_script["PHASE_4"]["dialogue"]): self.state = "PHASE_4_PUZZLE"
        elif current_phase_key == "PHASE_5":
            if self.dialogue_index >= len(game_script["PHASE_5"]["dialogue"]): self.state = "PHASE_5_CLIMBING"
        elif current_phase_key == "PHASE_6":
             if self.dialogue_index >= len(game_script["PHASE_6"]["dialogue"]): self.state = "PHASE_6_CHOICE"

    def handle_puzzle1_input(self, event):
        if event.key == pygame.K_RETURN:
            if self.puzzle_input.upper() == game_script["PHASE_1"]["puzzle"]["answer"]: self.phase_1_tasks["puzzle"] = True; self.state = "PHASE_1_DIALOGUE"; self.puzzle_input = ""
            else: self.puzzle_message = "Incorrect."; self.puzzle_input = ""
        elif event.key == pygame.K_BACKSPACE: self.puzzle_input = self.puzzle_input[:-1]
        else:
            if len(self.puzzle_input) < 20: self.puzzle_input += event.unicode
            
    def handle_puzzle4_input(self, event):
        key_map = {pygame.K_UP: "up", pygame.K_DOWN: "down", pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}
        if event.key in key_map: self.rhythm_puzzle_state.append(key_map[event.key])

    def update(self):
        if self.state == "PHASE_1_STEALTH": self.update_stealth_game()
        elif self.state == "PHASE_2_PLATFORMING": self.update_platforming()
        elif self.state == "PHASE_3_PUZZLE": self.update_puzzle3()
        elif self.state == "PHASE_4_PUZZLE": self.update_puzzle4()
        elif self.state == "PHASE_5_CLIMBING": self.update_climbing()
        else: self.all_sprites.update()
    
    def update_platforming(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.player.rect.x -= 5
        if keys[pygame.K_RIGHT]: self.player.rect.x += 5
        self.all_sprites.update(self.platforms)
        if self.player.rect.x > BASE_WIDTH: self.state = "PHASE_3_DIALOGUE"; self.dialogue_index=0; self.player.set_pos(350, BASE_HEIGHT - 105) # Transition
            
    def update_puzzle3(self):
        solution = game_script["PHASE_3"]["puzzle"]["solution"]
        if self.sequence_puzzle_state == solution: self.state = "PHASE_4_DIALOGUE"; self.dialogue_index = 0
        elif len(self.sequence_puzzle_state) >= len(solution) or time.time() > self.puzzle_timer: self.sequence_puzzle_state = []; self.puzzle_timer = time.time() + 15
            
    def update_puzzle4(self):
        solution = game_script["PHASE_4"]["puzzle"]["solution"]
        if len(self.rhythm_puzzle_state) > len(solution): self.rhythm_puzzle_state = []
        if self.rhythm_puzzle_state == solution: self.state = "PHASE_5_DIALOGUE"; self.dialogue_index = 0
            
    def update_climbing(self):
        if self.stamina < 100: self.stamina += 0.5
        if self.climb_height >= game_script["PHASE_5"]["puzzle"]["height"]: self.state = "PHASE_6_DIALOGUE"; self.dialogue_index = 0

    def draw(self):
        screen.fill(BLACK)
        bg_map = {"PHASE_1": self.draw_office_bg, "PHASE_2": self.draw_hampi_bg, "PHASE_3": self.draw_maha_bg, "PHASE_4": self.draw_chid_bg, "PHASE_5": self.draw_kailash_bg, "PHASE_6": self.draw_final_bg}
        
        if self.state == "TITLE": self.draw_title_screen()
        elif self.state == "INTRO": self.draw_intro_screen()
        elif self.state == "ENDING": self.draw_ending_screen()
        else:
            phase_key = self.state.split('_')[0] + "_" + self.state.split('_')[1]
            if phase_key in bg_map: self.draw_scene(bg_map[phase_key])
        
        pygame.display.flip()

    def draw_scene(self, bg_func):
        bg_func()
        if "DIALOGUE" in self.state: self.all_sprites.draw(screen); self.draw_dialogue_box()
        elif self.state == "PHASE_1_PUZZLE": self.draw_puzzle1_screen()
        elif self.state == "PHASE_1_STEALTH": self.draw_stealth_game()
        elif self.state == "PHASE_2_PLATFORMING": self.platforms.draw(screen); self.all_sprites.draw(screen)
        elif self.state == "PHASE_3_PUZZLE": self.draw_puzzle3_screen()
        elif self.state == "PHASE_4_PUZZLE": self.draw_puzzle4_screen()
        elif self.state == "PHASE_5_CLIMBING": self.draw_climbing_screen()
        elif self.state == "PHASE_6_CHOICE": self.draw_choice_screen()
            
    def draw_title_screen(self):
        self.draw_office_bg()
        grad = self.create_gradient_surface((ui.width, ui.height), (0,0,0,220), (0,0,0,120)); screen.blit(grad, (0,0))
        font = get_font(ui.get_font_size(82)); title_surf = font.render("The Chakravartin Chronicles", True, ORANGE); screen.blit(title_surf, ui.get_pos(BASE_WIDTH/2 - title_surf.get_width()/2, 250))
        font = get_font(ui.get_font_size(40)); prompt_surf = font.render("Press Enter to Begin", True, WHITE); screen.blit(prompt_surf, ui.get_pos(BASE_WIDTH/2 - prompt_surf.get_width()/2, 400))
        
    def draw_dialogue_box(self):
        current_phase_key = self.state.split('_')[0] + "_" + self.state.split('_')[1]
        dialogue = game_script[current_phase_key]["dialogue"][self.dialogue_index]
        char, line = dialogue["char"], dialogue["line"]
        box_rect = ui.get_rect(70, 500, 1140, 200)
        grad = self.create_gradient_surface(box_rect.size, (20,20,30,220), (50,50,60,220)); screen.blit(grad, box_rect.topleft)
        pygame.draw.rect(screen, ORANGE, box_rect, 3, border_radius=10)
        if char in self.portraits:
            portrait = self.portraits[char]; portrait_rect = ui.get_rect(90, 520, 160, 160); screen.blit(portrait, portrait_rect)
        font = get_font(ui.get_font_size(38)); name_surf = font.render(f"{char}:", True, ORANGE); screen.blit(name_surf, ui.get_pos(280, 525))
        text_rect = ui.get_rect(280, 575, 880, 100)
        anim_progress = min(1.0, (time.time() - self.anim_start_time) / 1.0)
        draw_text_anim(line, font, TEXT_COLOR, screen, text_rect, anim_progress)

    def draw_puzzle4_screen(self):
        self.draw_puzzle_base("Task 4.1: Cosmic Dance", game_script["PHASE_4"]["puzzle"]["prompt"], is_input_box=False)
        solution = game_script["PHASE_4"]["puzzle"]["solution"]
        
        pulse_alpha = int((math.sin(time.time() * 4) + 1) / 2 * 255)
        pulse_color = (ORANGE[0], ORANGE[1], ORANGE[2], pulse_alpha)
        
        if time.time() > self.rhythm_pulse_time:
            self.rhythm_pulse_time = time.time() + 1.0
            self.current_rhythm_step = (self.current_rhythm_step + 1) % len(solution)

        for i, direction in enumerate(solution):
            x_offset = {"left": -60, "right": 60, "up": 0, "down": 0}[direction]
            y_offset = {"up": -60, "down": 60, "left": 0, "right": 0}[direction]
            pos = ui.get_pos(BASE_WIDTH/2 + x_offset*2, 350 + y_offset*2)
            
            color = GRAY
            if i < len(self.rhythm_puzzle_state) and self.rhythm_puzzle_state[i] == direction:
                color = GREEN
            elif i < len(self.rhythm_puzzle_state):
                color = RED

            if i == self.current_rhythm_step:
                # Draw the pulse using a temporary surface to support alpha
                pulse_surf = pygame.Surface((ui.get_font_size(100), ui.get_font_size(100)), pygame.SRCALPHA)
                pygame.draw.circle(pulse_surf, pulse_color, (ui.get_font_size(50), ui.get_font_size(50)), ui.get_font_size(50))
                screen.blit(pulse_surf, (pos[0] - ui.get_font_size(50), pos[1] - ui.get_font_size(50)))

            pygame.draw.circle(screen, color, pos, ui.get_font_size(40), 5)
            
    def draw_climbing_screen(self):
        self.draw_puzzle_base("Task 5.1: The Summit", game_script["PHASE_5"]["puzzle"]["prompt"], is_input_box=False)
        stamina_bar = ui.get_rect(50, 50, 400, 40)
        pygame.draw.rect(screen, DARK_GRAY, stamina_bar)
        pygame.draw.rect(screen, GREEN, (stamina_bar.x, stamina_bar.y, stamina_bar.w * (self.stamina / 100), stamina_bar.h))
        height_text = f"Altitude: {self.climb_height}m / {game_script['PHASE_5']['puzzle']['height']}m"
        font = get_font(ui.get_font_size(32)); screen.blit(font.render(height_text, True, WHITE), ui.get_pos(50, 100))
        
    def draw_choice_screen(self):
        self.draw_final_bg()
        choices = game_script["PHASE_6"]["choices"]
        for i, choice in enumerate(choices):
            color = ORANGE if i == self.ending_choice else WHITE
            font = get_font(ui.get_font_size(48)); text_surf = font.render(choice, True, color)
            screen.blit(text_surf, ui.get_pos(BASE_WIDTH/2 - text_surf.get_width()/2, 300 + i * 80))
            
    def draw_ending_screen(self):
        self.draw_final_bg()
        choice_text = game_script["PHASE_6"]["choices"][self.ending_choice]
        ending_text = game_script["ENDINGS"][choice_text]
        rect = ui.get_rect(100, 200, BASE_WIDTH-200, BASE_HEIGHT-300)
        draw_text_anim(ending_text, get_font(ui.get_font_size(42)), TEXT_COLOR, screen, rect, 1.0)
        prompt = get_font(ui.get_font_size(32)).render("Press Enter to play again.", True, ORANGE)
        screen.blit(prompt, ui.get_pos(BASE_WIDTH/2 - prompt.get_width()/2, 600))
        
    def setup_all(self):
        self.setup_stealth_game(); self.setup_platforming(); self.setup_visuals(); self.create_portraits()
    def setup_stealth_game(self): self.stealth_player = pygame.Rect(50, BASE_HEIGHT//2, 20, 20); self.guards = [pygame.Rect(300, 100, 25, 25), pygame.Rect(700, 500, 25, 25)]; self.guard_speed = [2, -2]; self.goal = pygame.Rect(BASE_WIDTH - 100, BASE_HEIGHT//2, 30, 30)
    def setup_platforming(self): self.platforms = pygame.sprite.Group(); self.platforms.add(Platform(0, BASE_HEIGHT - 40, BASE_WIDTH, 40)); self.platforms.add(Platform(300, BASE_HEIGHT - 150, 150, 40)); self.platforms.add(Platform(550, BASE_HEIGHT - 280, 150, 40)); self.platforms.add(Platform(800, BASE_HEIGHT - 400, 150, 40))
    def setup_visuals(self): self.building_lights = [pygame.Rect(random.randint(0, BASE_WIDTH), random.randint(100, BASE_HEIGHT - 300), 2, 2) for _ in range(100)]; self.tidal_buttons = [pygame.Rect(200 + i*220, 300, 150, 150) for i in range(4)]; self.tidal_symbols = {"Naga": self.create_symbol("Naga"), "Fish": self.create_symbol("Fish"), "Turtle": self.create_symbol("Turtle"), "Sun": self.create_symbol("Sun")}
    def create_portraits(self): self.portraits = {"Tejas": pygame.Surface((160,160)), "Grandfather": pygame.Surface((160,160)), "Arjun": pygame.Surface((160,160)), "Cosmic Voice": pygame.Surface((160,160))}; self.portraits["Tejas"].fill(TEJAS_COLOR); self.portraits["Grandfather"].fill(GRANDFATHER_COLOR); self.portraits["Arjun"].fill(ARJUN_COLOR); self.portraits["Cosmic Voice"].fill(BLACK)
    
    # --- Background Drawing Functions ---
    def draw_office_bg(self): screen.fill(DARK_GRAY); pygame.draw.rect(screen, WINDOW_BLUE, ui.get_rect(0, 0, BASE_WIDTH, BASE_HEIGHT - 75)); [pygame.draw.rect(screen, LIGHT_YELLOW, ui.get_rect(l.x, l.y, l.w, l.h)) for l in self.building_lights]; pygame.draw.rect(screen, BUILDING_COLOR, ui.get_rect(100, 300, 150, BASE_HEIGHT)); pygame.draw.rect(screen, DARK_GRAY, ui.get_rect(200, BASE_HEIGHT - 150, 400, 100)); pygame.draw.rect(screen, DARK_GRAY, ui.get_rect(0, BASE_HEIGHT-75, BASE_WIDTH, 75))
    def draw_hampi_bg(self): screen.fill(HAMPI_SKY)
    def draw_maha_bg(self): screen.fill(MAHA_SKY); pygame.draw.rect(screen, MAHA_WATER, ui.get_rect(0, 400, BASE_WIDTH, BASE_HEIGHT-400)); pygame.draw.rect(screen, MAHA_TEMPLE, ui.get_rect(500, 250, 280, 150))
    def draw_chid_bg(self): screen.fill(CHID_SKY); pygame.draw.rect(screen, CHID_TEMPLE, ui.get_rect(300, 200, 680, 400))
    def draw_kailash_bg(self): screen.fill(KAILASH_SKY); pygame.draw.polygon(screen, KAILASH_ROCK, [ui.get_pos(0,720), ui.get_pos(640, 100), ui.get_pos(1280, 720)]); pygame.draw.polygon(screen, SNOW, [ui.get_pos(440, 300), ui.get_pos(640, 100), ui.get_pos(840, 300)])
    def draw_final_bg(self): screen.fill(BLACK); [pygame.draw.circle(screen, (random.randint(50,150),random.randint(50,150),random.randint(150,255)), ui.get_pos(random.randint(0,1280), random.randint(0,720)), random.randint(1,3)) for _ in range(50)]
    
    # --- Puzzle Drawing and Asset Creation ---
    def draw_puzzle_base(self, title, prompt, user_input="", is_input_box=True):
        dim_surf = pygame.Surface(screen.get_size()); dim_surf.set_alpha(180); screen.blit(dim_surf, (0,0))
        font = get_font(ui.get_font_size(52)); screen.blit(font.render(title, True, ORANGE), ui.get_pos(BASE_WIDTH/2 - font.size(title)[0]/2, 150))
        font = get_font(ui.get_font_size(42)); screen.blit(font.render(prompt, True, WHITE), ui.get_pos(BASE_WIDTH/2 - font.size(prompt)[0]/2, 250))
        # Logic for different puzzle types
        if is_input_box: #Phase 1
            input_box = ui.get_rect(BASE_WIDTH/2 - 250, 400, 500, 60); pygame.draw.rect(screen, GRAY, input_box, 2, 5); screen.blit(get_font(ui.get_font_size(38)).render(user_input, True, WHITE), (input_box.x+15, input_box.y+15))
        elif self.state == "PHASE_3_PUZZLE":
             for i, btn_rect in enumerate(self.tidal_buttons):
                symbol_name = game_script["PHASE_3"]["puzzle"]["solution"][i]
                scaled_btn = ui.get_rect(btn_rect.x, btn_rect.y, btn_rect.w, btn_rect.h); pygame.draw.rect(screen, DARK_BLUE, scaled_btn, 0, 10); screen.blit(self.tidal_symbols[symbol_name], scaled_btn)
             time_left = self.puzzle_timer - time.time(); timer_text = f"Time Remaining: {max(0, int(time_left))}"; font = get_font(ui.get_font_size(38)); screen.blit(font.render(timer_text, True, RED if time_left < 5 else WHITE), ui.get_pos(BASE_WIDTH/2-font.size(timer_text)[0]/2, 550))
                
    def create_gradient_surface(self, size, start_color, end_color):
        surf = pygame.Surface(size, pygame.SRCALPHA);
        for y in range(size[1]):
            alpha = int(255 * (y / size[1]))
            color = [start_color[i] + (end_color[i] - start_color[i]) * alpha / 255 for i in range(3)]; color.append(start_color[3] + (end_color[3]-start_color[3]) * alpha / 255 if len(start_color) > 3 else 255)
            pygame.draw.line(surf, color, (0, y), (size[0], y))
        return surf
    def create_symbol(self, name):
        surf = pygame.Surface((150, 150), pygame.SRCALPHA)
        if name == "Naga": pygame.draw.circle(surf, ORANGE, (75,75), 50, 5)
        elif name == "Fish": pygame.draw.ellipse(surf, ORANGE, (25, 50, 100, 50), 5)
        elif name == "Turtle": pygame.draw.rect(surf, ORANGE, (25, 25, 100, 100), 5, 10)
        elif name == "Sun": pygame.draw.circle(surf, ORANGE, (75,75), 60); pygame.draw.circle(surf, DARK_BLUE, (75,75), 40)
        return surf
    def draw_intro_screen(self): screen.fill(BLACK); rect = ui.get_rect(100, 100, BASE_WIDTH-200, BASE_HEIGHT-200); draw_text_anim(game_script["INTRO"]["text"], get_font(ui.get_font_size(40)), TEXT_COLOR, screen, rect, 1.0); prompt = get_font(ui.get_font_size(32)).render("Press Enter to Continue...", True, ORANGE); screen.blit(prompt, ui.get_pos(BASE_WIDTH/2 - prompt.get_width()/2, 600))
    def draw_puzzle1_screen(self): self.draw_puzzle_base("Task 1.1: Digital Archaeology", game_script["PHASE_1"]["puzzle"]["question"], self.puzzle_input)
    def draw_puzzle3_screen(self): self.draw_puzzle_base("Task 3.1: Tidal Mechanics", game_script["PHASE_3"]["puzzle"]["prompt"], is_input_box=False)
    def update_stealth_game(self): keys = pygame.key.get_pressed(); self.stealth_player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3; self.stealth_player.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3; [setattr(g, 'y', g.y + s) or setattr(self, 'guard_speed', self.guard_speed[:i] + [-s] + self.guard_speed[i+1:]) for i, (g, s) in enumerate(zip(self.guards, self.guard_speed)) if g.top < 100 or g.bottom > BASE_HEIGHT - 100]; [self.stealth_player.topleft for g in self.guards if self.stealth_player.colliderect(g)]; self.phase_1_tasks["stealth"], self.state = (True, "PHASE_1_DIALOGUE") if self.stealth_player.colliderect(self.goal) else (self.phase_1_tasks["stealth"], self.state)
    def draw_stealth_game(self): screen.fill(BLACK); title_surf = get_font(ui.get_font_size(42)).render("Task 1.2: Corporate Espionage", True, ORANGE); screen.blit(title_surf, ui.get_pos(BASE_WIDTH/2-title_surf.get_width()/2, 50)); [pygame.draw.rect(screen, c, r) for c, r in [(TEJAS_COLOR, self.stealth_player), (GREEN, self.goal)] + [(RED, g) for g in self.guards]]


if __name__ == "__main__":
    game = Game()
    game.run()