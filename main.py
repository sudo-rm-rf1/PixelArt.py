import pygame
import sys


pygame.init()



SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600


CANVAS_MARGIN = 50

CANVAS_WIDTH = SCREEN_WIDTH - 200 

CANVAS_HEIGHT = SCREEN_HEIGHT - 2 * CANVAS_MARGIN


WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

GRAY = (200, 200, 200)

COLORS = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), WHITE]

current_color = BLACK


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("PixelArt.py")

GRID_SIZE = int(input("Enter the grid size: "))

SIZE = min(CANVAS_WIDTH, CANVAS_HEIGHT) // GRID_SIZE

font = pygame.font.Font(None, 24)



canvas = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]



history = []

redo_stack = []



input_active = False
input_text = ""



def draw_canvas(show_grid=True):

    """Draws the canvas with or without grid lines."""
    
    for y in range(len(canvas)):
        
        for x in range(len(canvas[y])):
            
            rect = pygame.Rect(

                CANVAS_MARGIN + x * SIZE,

                CANVAS_MARGIN + y * SIZE,

                SIZE, SIZE
            )

            pygame.draw.rect(screen, canvas[y][x], rect)

            if show_grid:

                pygame.draw.rect(screen, GRAY, rect, 1)



def draw_palette():
            
    """Draws the color palette on the right side."""
    
    palette_x_start = CANVAS_WIDTH + CANVAS_MARGIN
    palette_y_start = 10
    
    palette_rects = []
    
    for i, color in enumerate(COLORS):
        
        rect = pygame.Rect(palette_x_start + 10, palette_y_start + i * (SIZE + 5), SIZE, SIZE)
        
        pygame.draw.rect(screen, color, rect)
        
        palette_rects.append((rect, color))
        
    return palette_rects


def draw_text_field():
    
    """Draws the text input field for custom colors."""
    
    text_box = pygame.Rect(CANVAS_WIDTH + CANVAS_MARGIN + 10, SCREEN_HEIGHT - 50, 80, 30)
    
    pygame.draw.rect(screen, WHITE, text_box)
    
    pygame.draw.rect(screen, BLACK, text_box, 2)
    
    text_surface = font.render(input_text, True, BLACK)
    
    screen.blit(text_surface, (text_box.x + 5, text_box.y + 5))
    
    label_surface = font.render("RGB:", True, BLACK)
    
    screen.blit(label_surface, (text_box.x - 40, text_box.y + 5))
    
    return text_box


def save_canvas():
    
    """Saves the canvas as a PNG file."""
    
    surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    
    for y in range(len(canvas)):
        
        for x in range(len(canvas[y])):
            
            rect = pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE)
            
            pygame.draw.rect(surface, canvas[y][x], rect)
            
    pygame.image.save(surface, "pixel_art.png")
    
    print("Canvas saved as 'pixel_art.png'")
    


def load_canvas():
    
    """Loads an image file into the canvas."""
    
    global canvas
    try:
        
        loaded_image = pygame.image.load("pixel_art.png")
        
        loaded_image = pygame.transform.scale(loaded_image, (CANVAS_WIDTH, CANVAS_HEIGHT))
        
        for y in range(len(canvas)):
            
            for x in range(len(canvas[y])):
                
                color = loaded_image.get_at((x * SIZE + SIZE // 2, y * SIZE + SIZE // 2))
                
                canvas[y][x] = (color.r, color.g, color.b)
                
        print("Canvas loaded from 'pixel_art.png'")
        
    except FileNotFoundError:
        
        print("No saved file found to load.")
        


def undo():
    
    """Undoes the last action."""
    
    global canvas
    if history:
        
        redo_stack.append([row[:] for row in canvas])
        
        canvas = history.pop()
        


def redo():
    
    """Redoes the last undone action."""
    
    global canvas
    if redo_stack:
        
        history.append([row[:] for row in canvas])
        
        canvas = redo_stack.pop()
        


def parse_rgb(text):
    
    """Parses an RGB string (e.g., '255,0,128') into a tuple."""
    
    try:
        
        parts = text.split(",")
        
        if len(parts) == 3:
            
            r = int(parts[0].strip())
            
            g = int(parts[1].strip())
            
            b = int(parts[2].strip())
            
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                
                return (r, g, b)
            
    except ValueError:
        
        pass
    return None


running = True
show_grid = True
while running:
    
    screen.fill(WHITE)
    
    draw_canvas(show_grid)
    
    palette_rects = draw_palette()
    
    text_box = draw_text_field()
    


    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            running = False


        if pygame.mouse.get_pressed()[0]:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            


            if CANVAS_MARGIN <= mouse_x < CANVAS_MARGIN + CANVAS_WIDTH and CANVAS_MARGIN <= mouse_y < CANVAS_MARGIN + CANVAS_HEIGHT:
                
                grid_x = (mouse_x - CANVAS_MARGIN) // SIZE
                grid_y = (mouse_y - CANVAS_MARGIN) // SIZE
                if 0 <= grid_x < len(canvas[0]) and 0 <= grid_y < len(canvas):
                    
                    history.append([row[:] for row in canvas])
                    
                    redo_stack.clear()
                    
                    canvas[grid_y][grid_x] = current_color


            else:
                
                for rect, color in palette_rects:
                    
                    if rect.collidepoint((mouse_x, mouse_y)):
                        
                        current_color = color


            if text_box.collidepoint((mouse_x, mouse_y)):
                
                input_active = True
            else:
                
                input_active = False


        if event.type == pygame.KEYDOWN:
            
            if input_active:
                
                if event.key == pygame.K_RETURN:
                    
                    new_color = parse_rgb(input_text)
                    
                    if new_color:
                        
                        current_color = new_color
                        print(f"Selected color: {new_color}")
                        
                    else:
                        
                        print("Invalid color format. Use 'R,G,B'.")
                        
                    input_text = ""
                    
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    
                    input_text = input_text[:-1]
                    
                else:
                    
                    input_text += event.unicode
                    
            else:
                
                if event.key == pygame.K_s:
                    
                    save_canvas()
                    
                elif event.key == pygame.K_l:
                    
                    load_canvas()
                    
                elif event.key == pygame.K_u:
                    
                    undo()
                    
                elif event.key == pygame.K_r:
                    
                    redo()
                    
                elif event.key == pygame.K_c:
                    history.append([row[:] for row in canvas])
                    redo_stack.clear()
                    canvas = [[WHITE for _ in range(CANVAS_WIDTH // SIZE)] for _ in range(CANVAS_HEIGHT // SIZE)]
                elif event.key == pygame.K_g:
                    show_grid = not show_grid

    pygame.display.flip()

pygame.quit()
sys.exit()
