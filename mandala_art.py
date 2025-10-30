# mandala.py
import pygame
import moderngl
import numpy as np
import random
import time
from pygame.locals import DOUBLEBUF, OPENGL

WIDTH, HEIGHT = 800, 600

# ---------------- palette helpers ----------------
def hsv_to_rgb(h, s, v):
    """h:0..1, s:0..1, v:0..1 -> r,g,b 0..1"""
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    i %= 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return (r, g, b)

def generate_palette(n=6, style='vibrant'):
    """Return list of n RGB triplets (0..1). Style can bias saturation/value."""
    base = random.random()
    palette = []
    for i in range(n):
        h = (base + i * (0.61803398875)) % 1.0  # golden-ish spacing
        if style == 'pastel':
            s = random.uniform(0.25, 0.5)
            v = random.uniform(0.9, 1.0)
        elif style == 'cool':
            s = random.uniform(0.5, 0.85)
            v = random.uniform(0.7, 0.95)
            h = (h + 0.5) % 1.0
        else:  # vibrant
            s = random.uniform(0.65, 0.95)
            v = random.uniform(0.75, 1.0)
        palette.append(hsv_to_rgb(h, s, v))
    return palette

# ---------------- main run() ----------------
def run():
    # save old pygame surface so we can restore after exiting
    old_screen = pygame.display.get_surface()

    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Digital Mandala Studio")
    clock = pygame.time.Clock()

    ctx = moderngl.create_context()

    # Vertex shader (fullscreen quad)
    vertex_shader = """
    #version 330
    in vec2 in_vert;
    out vec2 v_uv;
    void main() {
        v_uv = in_vert * 0.5 + 0.5;
        gl_Position = vec4(in_vert, 0.0, 1.0);
    }
    """

    # Fragment shader - artistic digital mandala with modes, folding (symmetry), palette blending & glow
    fragment_shader = """
    #version 330
    uniform vec2 iResolution;
    uniform float iTime;
    uniform vec2 focal;    // pan (-1..1)
    uniform float zoom;
    uniform int folds;
    uniform int mode;
    uniform vec3 palette[6];

    in vec2 v_uv;
    out vec4 fragColor;

    // rotate matrix
    mat2 rot(float a){ float c=cos(a), s=sin(a); return mat2(c,-s,s,c); }

    // small hash / noise
    float hash21(vec2 p){
        p = fract(p * vec2(123.34, 456.21));
        p += dot(p, p + 23.45);
        return fract(p.x * p.y);
    }

    vec3 samplePalette(float t){
        t = fract(t);
        float idx = t * 6.0;
        int i = int(floor(idx));
        int j = (i + 1) % 6;
        float f = fract(idx);
        return mix(palette[i], palette[j], smoothstep(0.0, 1.0, f));
    }

    void main(){
        vec2 uv = (gl_FragCoord.xy / iResolution.xy) * 2.0 - 1.0;
        uv.x *= iResolution.x / iResolution.y;

        // apply pan/zoom
        vec2 p = (uv - focal) / zoom;

        float r = length(p);
        float a = atan(p.y, p.x);

        // fold angle into symmetric sector and mirror for kaleidoscope
        float F = max(1, folds);
        float sector = 2.0 * 3.141592653589793 / F;
        float aa = mod(a + 3.141592653589793, sector);
        aa = abs(aa - sector*0.5);

        float t = iTime * 0.9;

        vec3 color = vec3(0.0);
        float mask = 0.0;

        if(mode == 1){
            // petal/ripple mode: sharp petals with soft edges
            float petals = 6.0 + 6.0 * sin(t*0.25);
            float val = cos(aa * petals - r * 18.0 + sin(t*0.6)*2.0);
            mask = smoothstep(0.05, 0.65, val * (1.0 - r*0.7));
            color = samplePalette(0.12 + 0.8 * mask + 0.05 * sin(t + r*5.0));
        } else if(mode == 2){
            // layered rings with noise and angular modulation
            float rings = sin(r*14.0 - aa*8.0 + t*1.3);
            float n = hash21(p*6.0 + t*0.2);
            mask = smoothstep(-0.1, 0.8, rings + 0.25 * n - r*0.9);
            color = samplePalette(0.1 + 0.7*mask + 0.08*n);
        } else if(mode == 3){
            // swirl + fractal-ish layering
            vec2 q = p + 0.4 * vec2(cos(t*0.9), sin(t*0.9));
            float swirl = sin(6.0*aa + 10.0 * r + 0.9 * hash21(q*8.0 + t));
            mask = smoothstep(-0.2, 0.6, swirl - r*0.8);
            color = samplePalette(0.2 + 0.8 * mask);
            color += vec3(0.7,0.6,0.9) * exp(-r*4.0); // center glow
        } else {
            // star/spoke + subtle fractal sum
            float sum = 0.0;
            vec2 z = p * 1.3;
            for(int i=0;i<5;i++){
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + 0.2*vec2(cos(aa*(i+1.5)), sin(aa*(i+2.0)));
                sum += sin(length(z)*3.0 + t*0.6 + float(i));
            }
            mask = smoothstep(-1.0, 1.0, sum*0.35 - r*0.7);
            color = samplePalette(0.3 + 0.6*mask);
        }

        // combine base color and soft glow & bloom
        float vign = smoothstep(1.2, 0.15, r);
        vec3 grain = vec3(hash21(gl_FragCoord.xy * 0.012 + t*0.1) * 0.03);
        color = mix(vec3(0.015,0.01,0.04), color, vign);
        color += grain;

        float brightness = length(color);
        color += 0.28 * pow(max(0.0, brightness), 2.2) * vec3(1.0,0.9,1.0) * exp(-r*3.0);

        // subtle colored rim based on angle to emphasize symmetry lines
        color += 0.08 * samplePalette(fract((aa*5.0 + t*0.1)));

        fragColor = vec4(clamp(color, 0.0, 1.0), 1.0);
    }
    """

    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # full-screen quad
    vbo = ctx.buffer(np.array([-1.0, -1.0,  1.0, -1.0,  -1.0, 1.0,  1.0, 1.0], dtype='f4'))
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

    # initial uniform values
    prog['iResolution'].value = (float(WIDTH), float(HEIGHT))
    prog['iTime'].value = 0.0
    prog['focal'].value = (0.0, 0.0)
    prog['zoom'].value = 1.0
    prog['folds'].value = 12
    prog['mode'].value = 1

    # palette
    palette = generate_palette(6, style='vibrant')
    flat = [c for col in palette for c in col]
    prog['palette'].write(np.array(flat, dtype='f4').tobytes())

    # interactive state
    running = True
    start_time = time.time()
    animate = True
    anim_speed = 1.0
    folds = 12
    mode = 1
    zoom = 1.0
    focal = [0.0, 0.0]
    dragging = False
    last_mouse = (0, 0)
    fade = 0.0       # 0 = fully visible, 1 = fully faded (erase)
    fade_target = 0.0

    # small helper to write the palette to shader
    def upload_palette(new_palette):
        flatp = [c for col in new_palette for c in col]
        prog['palette'].write(np.array(flatp, dtype='f4').tobytes())

    # UI font (pygame)
    pygame.font.init()
    font = pygame.font.SysFont("Segoe UI", 16)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    animate = not animate
                elif event.key == pygame.K_UP:
                    anim_speed = min(4.0, anim_speed + 0.1)
                elif event.key == pygame.K_DOWN:
                    anim_speed = max(0.05, anim_speed - 0.1)
                elif event.key == pygame.K_LEFT:
                    folds = max(2, folds - 1); prog['folds'].value = folds
                elif event.key == pygame.K_RIGHT:
                    folds = min(64, folds + 1); prog['folds'].value = folds
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    mode = int(event.unicode); prog['mode'].value = mode
                elif event.key == pygame.K_r:
                    # randomize palette only
                    palette = generate_palette(6, style=random.choice(['vibrant','cool','pastel']))
                    upload_palette(palette)
                elif event.key == pygame.K_s:
                    # save a screenshot
                    px = ctx.fbo.read(components=3, alignment=1)
                    img = pygame.image.fromstring(px, (WIDTH, HEIGHT), 'RGB')
                    pygame.image.save(img, "mandala.png")
                    print("Saved mandala.png")
                elif event.key == pygame.K_e:
                    # start fade to erase
                    fade_target = 1.0
                elif event.key == pygame.K_d:
                    # resume drawing (cancel fade)
                    fade_target = 0.0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click: randomize pattern seed (palette + slight time nudge)
                    palette = generate_palette(6, style=random.choice(['vibrant','cool','pastel']))
                    upload_palette(palette)
                    # nudge time so visuals shift
                    start_time -= 0.2 * random.random()
                    # start dragging
                    dragging = True
                    last_mouse = event.pos
                elif event.button == 3:
                    # right click: reset focal/zoom
                    focal = [0.0, 0.0]
                    zoom = 1.0
                    prog['zoom'].value = zoom
                    prog['focal'].value = tuple(focal)
                elif event.button == 4:  # wheel up: zoom in towards mouse
                    mx, my = event.pos
                    ndc_x = (mx / WIDTH) * 2.0 - 1.0
                    ndc_y = (my / HEIGHT) * 2.0 - 1.0
                    ndc_x *= WIDTH / HEIGHT
                    focal[0] += ndc_x * 0.05 / zoom
                    focal[1] -= ndc_y * 0.05 / zoom
                    zoom *= 1.12
                    prog['zoom'].value = zoom
                    prog['focal'].value = tuple(focal)
                elif event.button == 5:  # wheel down: zoom out
                    mx, my = event.pos
                    ndc_x = (mx / WIDTH) * 2.0 - 1.0
                    ndc_y = (my / HEIGHT) * 2.0 - 1.0
                    ndc_x *= WIDTH / HEIGHT
                    focal[0] -= ndc_x * 0.04 / zoom
                    focal[1] += ndc_y * 0.04 / zoom
                    zoom /= 1.12
                    prog['zoom'].value = zoom
                    prog['focal'].value = tuple(focal)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    lx, ly = last_mouse
                    dx = (mx - lx) / float(WIDTH)
                    dy = (my - ly) / float(HEIGHT)
                    focal[0] -= dx * 2.0 / zoom * (WIDTH / HEIGHT)
                    focal[1] += dy * 2.0 / zoom
                    prog['focal'].value = tuple(focal)
                    last_mouse = event.pos

        # update time uniform
        now = time.time()
        elapsed = now - start_time
        prog['iTime'].value = elapsed * anim_speed if animate else 0.0

        # update uniforms
        prog['zoom'].value = zoom
        prog['focal'].value = tuple(focal)
        prog['folds'].value = folds
        prog['mode'].value = mode

        # fade smoothing (for erase/resume)
        fade += (fade_target - fade) * 0.06
        # if fade nearly 1, gradually darken the clear color
        clear_base = 0.02 * (1.0 - fade)
        ctx.clear(clear_base, 0.01 * (1.0 - fade), 0.04 * (1.0 - fade), 1.0)

        vao.render(moderngl.TRIANGLE_STRIP)

        # draw UI overlay using pygame (on top of GL)
        # get screen surface
        surf = pygame.display.get_surface()
        if surf:
            # simple UI box
            info = [
                f"Mode: {mode}  |  Folds: {folds}  |  Speed: {anim_speed:.2f}  |  Zoom: {zoom:.2f}",
                "LMB: new mandala / drag to pan  |  Wheel: zoom  |  R: palette  |  E: erase  |  D: resume",
                "1-4: modes  |  ←/→ folds  ↑/↓ speed  | S: save PNG  | Esc: exit"
            ]
            # semi-transparent rectangle
            ui_surf = pygame.Surface((WIDTH, 72), pygame.SRCALPHA)
            ui_surf.fill((10,10,12,100))
            surf.blit(ui_surf, (8, 8))
            # draw text lines
            y = 12
            for line in info:
                tx = font.render(line, True, (230, 230, 230))
                surf.blit(tx, (16, y))
                y += 22

        pygame.display.flip()
        clock.tick(60)

    # Restore previous surface (menu)
    if old_screen is not None:
        pygame.display.set_mode(old_screen.get_size(), pygame.RESIZABLE)
        pygame.display.set_caption("Visual Patterns Studio")
    return

# If run as main quickly demo:
if __name__ == "__main__":
    pygame.init()
    run()
