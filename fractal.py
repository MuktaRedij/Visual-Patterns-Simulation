# fractal.py
import pygame
import moderngl
import numpy as np
import random
from pygame.locals import DOUBLEBUF, OPENGL

WIDTH, HEIGHT = 800, 600

def generate_palette():
    """Generate a random color palette."""
    return [[random.random(), random.random(), random.random()] for _ in range(5)]

def run():
    # Save current menu surface
    old_screen = pygame.display.get_surface()
    
    # Create a new window for fractal
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Fractal Generator")
    clock = pygame.time.Clock()
    
    ctx = moderngl.create_context()
    
    vertex_shader = """
    #version 330
    in vec2 in_vert;
    void main() { gl_Position = vec4(in_vert, 0.0, 1.0); }
    """
    
    fragment_shader = """
    #version 330
    uniform float time;
    uniform vec3 colors[5];
    out vec4 fragColor;
    void main() {
        vec2 uv = gl_FragCoord.xy / vec2(800,600);
        uv = uv * 2.0 - 1.0;
        uv.x *= 1.33;
        vec2 z = uv;
        int iterations = 0;
        const int maxIter = 50;
        for(int i=0;i<maxIter;i++){
            z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + uv;
            if(length(z) > 4.0) break;
            iterations++;
        }
        float t = float(iterations)/float(maxIter);
        vec3 color = mix(colors[0], colors[1], t);
        color = mix(color, colors[2], t*0.5);
        color += sin(time + t*10.0)*0.1;
        fragColor = vec4(clamp(color,0.0,1.0),1.0);
    }
    """
    
    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    vbo = ctx.buffer(np.array([-1,-1,1,-1,-1,1,1,1], dtype='f4'))
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
                # Regenerate palette on click
                palette = generate_palette()
                flat_colors = [v for c in palette for v in c]
                prog['colors'].write(np.array(flat_colors, dtype='f4').tobytes())
        
        ctx.clear()
        time_val += 0.02
        prog['time'].value = time_val
        vao.render(moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Restore main menu surface
    pygame.display.set_mode(old_screen.get_size(), pygame.RESIZABLE)
    pygame.display.set_caption("✨ Visual Patterns Studio ✨")
    return
