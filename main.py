# main.py
import pygame
import sys
import time
import math
import kaleidoscope
import fractal
import mandala_art
import fireworks
import interactive_drawing

pygame.init()

# ---------- SETTINGS ----------
WIDTH, HEIGHT = 950, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Visual Patterns Simulation")

font_large = pygame.font.SysFont("Segoe UI", 40, bold=True)
font_small = pygame.font.SysFont("Segoe UI", 22)
clock = pygame.time.Clock()

# ---------- COLORS ----------
BG_COLOR = (20, 20, 20)
SIDEBAR_COLOR = (40, 40, 40)
ACCENT = (255, 165, 0)
HOVER_GLOW = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 140, 0)
BUTTON_HOVER = (255, 255, 255)

# ---------- BUTTON CLASS ----------
class Button:
    def __init__(self, text, y, action):
        self.text = text
        self.y = y
        self.action = action
        self.rect = pygame.Rect(-250, y, 220, 60)
        self.target_x = 40
        self.hovered = False
        self.base_color = pygame.Color(80, 60, 180)
        self.glow_alpha = 0

    def draw(self, surface):
        self.rect.x += (self.target_x - self.rect.x) * 0.2
        mouse = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse)
        target_alpha = 60 if self.hovered else 0
        self.glow_alpha += (target_alpha - self.glow_alpha) * 0.2
        pygame.draw.rect(surface, self.base_color, self.rect, border_radius=15)
        if self.glow_alpha > 0.5:
            glow = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*HOVER_GLOW, int(self.glow_alpha)), glow.get_rect(), border_radius=20)
            surface.blit(glow, (self.rect.x - 10, self.rect.y - 10))
        text_surf = font_small.render(self.text, True, TEXT_COLOR)
        surface.blit(text_surf, (self.rect.x + 25, self.rect.y + 18))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                self.action()

# ---------- SIDEBAR ----------
sidebar_width = 0
sidebar_target = 260
sidebar_open = True
animation_speed = 20

def toggle_sidebar():
    global sidebar_open
    sidebar_open = not sidebar_open

# ---------- MODULE ACTIONS ----------
def run_kaleidoscope(): kaleidoscope.run()
def run_fractal(): fractal.run()
def run_rangoli(): mandala_art.run()
def run_fireworks(): fireworks.run_fireworks()
def run_drawing(): interactive_drawing.run_drawing()

# ---------- BUTTON LIST ----------
buttons = [
    Button("Kaleidoscope", 150, run_kaleidoscope),
    Button("Fractal Generator", 230, run_fractal),
    Button("Mandala Art", 310, run_rangoli),
    Button("Fireworks", 390, run_fireworks),
    Button("Interactive Drawing", 470, run_drawing),
]

# ---------- MAIN MENU ----------
def menu():
    global sidebar_width, WIDTH, HEIGHT
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # <-- Fully quit program
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    toggle_sidebar()

        # Sidebar width animation
        if sidebar_open and sidebar_width < sidebar_target:
            sidebar_width += animation_speed
        elif not sidebar_open and sidebar_width > 0:
            sidebar_width -= animation_speed

        # Background
        screen.fill(BG_COLOR)

        # Sidebar
        if sidebar_width > 0:
            sidebar_surface = pygame.Surface((sidebar_width, HEIGHT))
            sidebar_surface.fill(SIDEBAR_COLOR)
            shadow = pygame.Surface((10, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0,0,0,60), shadow.get_rect())
            screen.blit(shadow, (sidebar_width-10,0))
            screen.blit(sidebar_surface, (0,0))
            title = font_large.render("Menu", True, ACCENT)
            screen.blit(title, (40, 60))
            for btn in buttons:
                btn.update(events)
                btn.draw(screen)

        # Center title
        t = time.time()
        glow_alpha = 60 + 30*math.sin(t*2)
        title_text = font_large.render("Visual Patterns Simulation", True, TEXT_COLOR)
        glow = pygame.Surface((title_text.get_width()+30, title_text.get_height()+30), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*ACCENT, int(glow_alpha)), glow.get_rect(), border_radius=15)
        title_x = WIDTH/2 - title_text.get_width()/2 + 100
        screen.blit(glow, (title_x-15,40))
        screen.blit(title_text, (title_x,50))

        # Footer tip
        tip = font_small.render("Press TAB to toggle sidebar", True, (200,200,200))
        screen.blit(tip, (WIDTH-tip.get_width()-20, HEIGHT-40))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    menu()
