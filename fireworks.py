# fireworks.py
import pygame
import random
import math

WIDTH, HEIGHT = 900, 600

# -----------------------------
#  PARTICLE CLASS
# -----------------------------
class Particle:
    def __init__(self, x, y, color, power):
        self.x = x
        self.y = y
        self.base_color = color
        self.color = color
        self.radius = random.randint(2, 4)
        self.life = 480  # ~5 seconds at 60fps
        self.age = 0
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.5, 6) * power
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.gravity = 0.07

    def update(self):
        # physics
        self.vx *= 0.99
        self.vy *= 0.99
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.age += 1

        # nonlinear fade curve
        fade_factor = 1 - (self.age / 480) ** 2.2
        self.life = max(0, 480 * fade_factor)

        # shrink radius for realism
        self.radius = max(1, self.radius - 0.01)

        # color shift toward white as it burns out
        r, g, b = self.base_color
        t = min(1.0, self.age / 480)
        self.color = (
            int(r + (255 - r) * t * 0.6),
            int(g + (255 - g) * t * 0.6),
            int(b + (255 - b) * t * 0.6),
        )

    def draw(self, screen):
        if self.life > 0:
            alpha = int(max(0, min(255, self.life)))
            surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(
                surface,
                (*self.color, alpha),
                (self.radius * 2, self.radius * 2),
                int(self.radius),
            )
            screen.blit(surface, (self.x - self.radius * 2, self.y - self.radius * 2))


# -----------------------------
#  ROCKET CLASS
# -----------------------------
class Rocket:
    def __init__(self, x, color, launch_sound=None):
        self.x = x
        self.y = HEIGHT
        self.vy = random.uniform(-8, -10)  # slower launch
        self.color = color
        self.exploded = False
        self.trail = []
        self.height_to_explode = random.randint(180, 280)
        if launch_sound:
            launch_sound.play()

    def update(self):
        if not self.exploded:
            self.trail.append((self.x, self.y))
            if len(self.trail) > 15:
                self.trail.pop(0)
            self.y += self.vy
            self.vy += 0.08
            if self.vy >= 0 or self.y < self.height_to_explode:
                self.exploded = True
        return self.exploded

    def draw(self, screen):
        for tx, ty in self.trail:
            pygame.draw.circle(screen, (255, 255, 255), (int(tx), int(ty)), 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)


# -----------------------------
#  FIREWORK CLASS
# -----------------------------
class Firework:
    def __init__(self, x, y, color, power=1.4, explode_sound=None):
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.exploded = False
        self.power = power
        self.explode_sound = explode_sound

    def explode(self):
        if not self.exploded:
            for _ in range(random.randint(130, 180)):
                self.particles.append(Particle(self.x, self.y, self.color, self.power))
            self.exploded = True
            if self.explode_sound:
                self.explode_sound.play()

    def update(self):
        if self.exploded:
            for p in self.particles[:]:
                p.update()
                if p.life <= 0:
                    self.particles.remove(p)

    def draw(self, screen):
        if self.exploded:
            for p in self.particles:
                p.draw(screen)


# -----------------------------
#  MAIN FUNCTION
# -----------------------------
def run_fireworks():
    pygame.init()
    pygame.mixer.init()

    # ✅ Save current display (main menu)
    old_screen = pygame.display.get_surface()
    old_size = old_screen.get_size() if old_screen else (900, 600)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fireworks")
    clock = pygame.time.Clock()

    # Sounds
    launch_sound = pygame.mixer.Sound("launch.mp3")
    explode_sound = pygame.mixer.Sound("explode.mp3")

    fireworks = []
    rockets = []
    colors = [
        (255, 120, 50),
        (255, 255, 120),
        (100, 255, 255),
        (255, 80, 200),
        (120, 200, 255),
        (255, 50, 100),
        (200, 255, 100),
    ]

    running = True
    while running:
        screen.fill((5, 5, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, _ = pygame.mouse.get_pos()
                rockets.append(Rocket(x, random.choice(colors), launch_sound))

        for r in rockets[:]:
            if r.update():
                rockets.remove(r)
                fw = Firework(r.x, r.y, r.color, random.uniform(1.3, 1.6), explode_sound)
                fw.explode()
                fireworks.append(fw)
            else:
                r.draw(screen)

        for fw in fireworks[:]:
            fw.update()
            fw.draw(screen)
            if fw.exploded and len(fw.particles) == 0:
                fireworks.remove(fw)

        # glow overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (20, 20, 40, 40), (0, 0, WIDTH, HEIGHT))
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    # ✅ Restore previous (menu) display
    pygame.display.set_mode(old_size, pygame.RESIZABLE)
    pygame.display.set_caption("Visual Patterns Simulation")
    return


# -----------------------------
#  RUN DIRECTLY
# -----------------------------
if __name__ == "__main__":
    run_fireworks()
