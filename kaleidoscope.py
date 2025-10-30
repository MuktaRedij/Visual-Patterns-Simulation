# kaleidoscope.py
import pygame
import moderngl
import numpy as np
import random
from pygame.locals import DOUBLEBUF, OPENGL

WIDTH, HEIGHT = 800, 600

def generate_palette():
    return [[random.random(), random.random(), random.random()] for _ in range(5)]

def run():
    # Save current display surface
    old_screen = pygame.display.get_surface()
    
    # Create new window for this module
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Kaleidoscope")
    clock = pygame.time.Clock()
    
    ctx = moderngl.create_context()

    vertex_shader = """
    #version 330
    in vec2 in_vert;
    void main() {
        gl_Position = vec4(in_vert, 0.0, 1.0);
    }
    """

    # 🌈 Enhanced fragment shader with multi-layer motion, rotation, and vivid blending
    fragment_shader = """
    #version 330
    uniform float time;
    uniform vec3 colors[5];
    out vec4 fragColor;

    float noise(vec2 p) {
        return fract(sin(dot(p, vec2(12.9898,78.233))) * 43758.5453);
    }

    vec3 palette(float t) {
        return mix(colors[int(mod(t*5.0,5.0))], colors[int(mod(t*5.0+1.0,5.0))], fract(t*5.0));
    }

    void main() {
        vec2 uv = gl_FragCoord.xy / vec2(800.0, 600.0);
        uv = uv * 2.0 - 1.0;
        uv.x *= 800.0/600.0; // keep proportions

        float r = length(uv);
        float a = atan(uv.y, uv.x);
        
        // 🌀 Add dynamic rotation and time warp
        a += sin(time * 0.5) * 0.5;
        r += 0.1 * sin(a * 6.0 + time * 0.8);

        // 🌸 Multi-layer symmetry blending
        float layers = 6.0;
        float sym = abs(sin(a * layers + time * 0.3));
        float pulse = sin(r * 15.0 - time * 1.2) * 0.5 + 0.5;

        // ✨ Depth modulation
        float depth = sin(r * 5.0 + sym * 3.0 + time * 0.5);

        // 🌈 Rich color mixing with palette function
        vec3 col = palette(pulse + depth * 0.3);
        col = mix(col, colors[int(mod(sym * 5.0, 5.0))], 0.4 + 0.3 * sin(time * 0.5));
        
        // 🪞 Mirror symmetry for kaleidoscope effect
        uv.x = abs(uv.x);
        uv.y = abs(uv.y);
        col *= (0.6 + 0.4 * sin(r * 6.0 + time));

        // 🌟 Add subtle glow
        float glow = exp(-r * 2.5) * 0.8;
        col += glow * vec3(0.8, 0.9, 1.0);

        fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
    }
    """

    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    vbo = ctx.buffer(np.array([-1,-1, 1,-1, -1,1, 1,1], dtype='f4'))
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

    palette = generate_palette()
    flat_colors = [v for c in palette for v in c]
    prog['colors'].write(np.array(flat_colors, dtype='f4').tobytes())

    time_val = 0.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                palette = generate_palette()
                flat_colors = [v for c in palette for v in c]
                prog['colors'].write(np.array(flat_colors, dtype='f4').tobytes())

        ctx.clear()
        time_val += 0.02
        prog['time'].value = time_val
        vao.render(moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        clock.tick(60)

    # Restore main menu window
    pygame.display.set_mode(old_screen.get_size(), pygame.RESIZABLE)
    pygame.display.set_caption("Visual Patterns Simulation")
    return
