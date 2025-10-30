import pygame

WIDTH, HEIGHT = 1000, 600

def run_drawing():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()

    # --- Colors and setup ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 105, 180), (0, 255, 255),
        (255, 165, 0), (255, 255, 255), (128, 128, 128)
    ]

    current_color = WHITE
    brush_size = 8
    drawing = False
    erasing = False
    current_tool = "brush"
    filled = False
    start_pos = None
    undo_stack, redo_stack = [], []

    palette_rects = [(pygame.Rect(10 + i * 40, 10, 30, 30), c) for i, c in enumerate(COLORS)]
    font = pygame.font.SysFont("Segoe UI", 18)
    tip = font.render(
        "Tools: D=Draw | E=Eraser | L=Line | R=Rect | O=Circle | B=Bucket | "
        "F=Fill Toggle | LMB=Draw | RMB=Erase | +/-=Brush Size | C=Clear | "
        "S=Save | ESC=Menu | Z=Undo | Y=Redo", True, (200, 200, 200)
    )

    canvas = pygame.Surface((WIDTH, HEIGHT - 60))
    canvas.fill(BLACK)

    def flood_fill(surf, pos, target_color, replacement_color):
        if target_color == replacement_color:
            return
        stack = [pos]
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= surf.get_width() or y < 0 or y >= surf.get_height():
                continue
            if surf.get_at((x, y))[:3] != target_color:
                continue
            surf.set_at((x, y), replacement_color)
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    running = True

    while running:
        screen.fill((40, 40, 40))
        screen.blit(canvas, (0, 60))

        # --- Draw color palette ---
        for rect, color in palette_rects:
            pygame.draw.rect(screen, color, rect)
            if color == current_color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    undo_stack.append(canvas.copy())
                    redo_stack.clear()
                    canvas.fill(BLACK)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    brush_size = min(brush_size + 2, 50)
                elif event.key == pygame.K_MINUS:
                    brush_size = max(2, brush_size - 2)
                elif event.key == pygame.K_s:
                    pygame.image.save(canvas, "my_drawing.png")
                    print("🖼️ Saved as my_drawing.png!")
                elif event.key == pygame.K_d:
                    current_tool = "brush"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"
                elif event.key == pygame.K_l:
                    current_tool = "line"
                elif event.key == pygame.K_r:
                    current_tool = "rect"
                elif event.key == pygame.K_o:
                    current_tool = "circle"
                elif event.key == pygame.K_f:
                    filled = not filled
                elif event.key == pygame.K_b:
                    current_tool = "bucket"
                elif event.key == pygame.K_z:
                    if undo_stack:
                        redo_stack.append(canvas.copy())
                        canvas.blit(undo_stack.pop(), (0, 0))
                elif event.key == pygame.K_y:
                    if redo_stack:
                        undo_stack.append(canvas.copy())
                        canvas.blit(redo_stack.pop(), (0, 0))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Color selection
                    for rect, color in palette_rects:
                        if rect.collidepoint(event.pos):
                            current_color = color
                            break
                    else:
                        if current_tool == "bucket":
                            x, y = event.pos
                            if y > 60:
                                undo_stack.append(canvas.copy())
                                redo_stack.clear()
                                target_color = canvas.get_at((x, y - 60))[:3]
                                flood_fill(canvas, (x, y - 60), target_color, current_color)
                        else:
                            drawing = True
                            erasing = False
                            start_pos = event.pos
                            undo_stack.append(canvas.copy())
                            redo_stack.clear()
                elif event.button == 3:
                    erasing = True
                    drawing = False
                    undo_stack.append(canvas.copy())
                    redo_stack.clear()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos
                    if current_tool == "line":
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
                    elif current_tool == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        rect.normalize()
                        if filled:
                            pygame.draw.rect(canvas, current_color, rect)
                        else:
                            pygame.draw.rect(canvas, current_color, rect, brush_size)
                    elif current_tool == "circle":
                        radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                        if filled:
                            pygame.draw.circle(canvas, current_color, start_pos, radius)
                        else:
                            pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                    drawing = False
                    erasing = False
                    start_pos = None
                elif event.button == 3:
                    erasing = False

        mx, my = pygame.mouse.get_pos()

        # --- Cursor visibility control ---
        if my > 60:  # On canvas
            pygame.mouse.set_visible(False)
        else:        # On palette/UI
            pygame.mouse.set_visible(True)

        # --- Drawing logic ---
        if my > 60:
            if drawing:
                if current_tool == "brush":
                    pygame.draw.circle(canvas, current_color, (mx, my - 60), brush_size)
                elif current_tool == "eraser":
                    pygame.draw.circle(canvas, BLACK, (mx, my - 60), brush_size + 2)
            elif erasing:
                pygame.draw.circle(canvas, BLACK, (mx, my - 60), brush_size + 2)

        # --- Shape preview ---
        if drawing and start_pos and current_tool in ("line", "rect", "circle"):
            overlay = canvas.copy()
            end_pos = pygame.mouse.get_pos()
            if current_tool == "line":
                pygame.draw.line(overlay, current_color, start_pos, end_pos, brush_size)
            elif current_tool == "rect":
                rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                rect.normalize()
                if filled:
                    pygame.draw.rect(overlay, current_color, rect)
                else:
                    pygame.draw.rect(overlay, current_color, rect, brush_size)
            elif current_tool == "circle":
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                if filled:
                    pygame.draw.circle(overlay, current_color, start_pos, radius)
                else:
                    pygame.draw.circle(overlay, current_color, start_pos, radius, brush_size)
            screen.blit(overlay, (0, 60))

        # --- UI Info ---
        screen.blit(tip, (10, HEIGHT - 30))
        brush_label = font.render(
            f"Brush Size: {brush_size} | Tool: {current_tool.capitalize()} | Filled: {filled}",
            True, (230, 230, 230)
        )
        screen.blit(brush_label, (WIDTH - 350, 15))

        # --- Custom cursor preview ---
        if my > 60:
            if current_tool in ("brush", "eraser"):
                color = (255, 255, 255) if current_tool == "eraser" else current_color
                pygame.draw.circle(screen, color, (mx, my), brush_size, 1)
            elif current_tool in ("line", "rect", "circle"):
                pygame.draw.line(screen, (255, 255, 255), (mx - 5, my), (mx + 5, my), 2)
                pygame.draw.line(screen, (255, 255, 255), (mx, my - 5), (mx, my + 5), 2)

        pygame.display.flip()
        clock.tick(60)

    return
