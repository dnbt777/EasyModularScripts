
import pygame
from diagram_parser import Diagram, Box, Arrow
import math

def calculate_layout(diagram: Diagram, screen_width: int, screen_height: int):
    # Calculate total area needed for boxes
    total_area = sum(box.size[0] * box.size[1] for box in diagram.boxes)
    
    # Calculate the number of rows and columns
    aspect_ratio = screen_width / screen_height
    num_boxes = len(diagram.boxes)
    num_cols = math.ceil(math.sqrt(num_boxes * aspect_ratio))
    num_rows = math.ceil(num_boxes / num_cols)
    
    # Calculate cell size
    cell_width = screen_width // num_cols
    cell_height = screen_height // num_rows
    
    # Position boxes
    positions = {}
    for i, box in enumerate(diagram.boxes):
        row = i // num_cols
        col = i % num_cols
        x = col * cell_width + (cell_width - box.size[0]) // 2
        y = row * cell_height + (cell_height - box.size[1]) // 2
        positions[box.id] = [x, y]
    
    return positions

def word_wrap(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def check_box_collisions(positions, box_sizes):
    colliding = False
    for id1, pos1 in positions.items():
        for id2, pos2 in positions.items():
            if id1 != id2:
                x1, y1 = pos1
                x2, y2 = pos2
                w1, h1 = box_sizes[id1]
                w2, h2 = box_sizes[id2]
                if (x1 < x2 + w2 and x1 + w1 > x2 and
                    y1 < y2 + h2 and y1 + h1 > y2):
                    colliding = True
                    break
        if colliding:
            break
    return colliding

def render_diagram(screen: pygame.Surface, diagram: Diagram, offset: tuple, zoom: float):
    screen_width, screen_height = screen.get_size()
    positions = calculate_layout(diagram, screen_width, screen_height)
    box_sizes = {box.id: box.size for box in diagram.boxes}
    
    # Handle box dragging
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    
    if mouse_buttons[2] and keys[pygame.K_LSHIFT]:  # Right mouse button and left shift  # Right mouse button and left shift
        for box in diagram.boxes:
            x, y = positions[box.id]
            width, height = box.size
            box_rect = pygame.Rect((x + offset[0]) * zoom, (y + offset[1]) * zoom, width * zoom, height * zoom)
            if box_rect.collidepoint(mouse_pos):
                dx, dy = pygame.mouse.get_rel()
                positions[box.id][0] += dx / zoom
                positions[box.id][1] += dy / zoom
                positions[box.id][1] += dy / zoom
                break
    
    # Check for collisions and print status
    colliding = check_box_collisions(positions, box_sizes)
    print(f"Boxes colliding: {'Yes' if colliding else 'No'}")
    
    # Set background color to dark
    screen.fill((30, 30, 30))  # Dark background color
    
    for box in diagram.boxes:
        x, y = positions[box.id]
        x = (x + offset[0]) * zoom
        y = (y + offset[1]) * zoom
        width = box.size[0] * zoom
        height = box.size[1] * zoom
        
        pygame.draw.rect(screen, box.color, (x, y, width, height))
        font = pygame.font.Font(None, int(24 * zoom))
        
        # Word wrap the box text
        wrapped_text = word_wrap(box.text, font, width - 10)
        line_height = font.get_linesize()
        total_text_height = line_height * len(wrapped_text)
        
        text_y = y + (height - total_text_height) // 2
        for line in wrapped_text:
            text = font.render(line, True, (255, 255, 255))  # White text color
            text_rect = text.get_rect(center=(x + width // 2, text_y + line_height // 2))
            screen.blit(text, text_rect)
            text_y += line_height
        
        # Render description
        if box.description:
            desc_font = pygame.font.Font(None, int(18 * zoom))
            desc_lines = word_wrap(box.description, desc_font, width - 10)
            for i, line in enumerate(desc_lines):
                desc_text = desc_font.render(line, True, (255, 255, 255))  # White text color
                desc_rect = desc_text.get_rect(topleft=(x + 5, y + height + 5 + i * 20 * zoom))
                screen.blit(desc_text, desc_rect)

    for arrow in diagram.arrows:
        start_pos = positions[arrow.start]
        end_pos = positions[arrow.end]
        start_x = (start_pos[0] + offset[0]) * zoom
        start_y = (start_pos[1] + offset[1]) * zoom
        end_x = (end_pos[0] + offset[0]) * zoom
        end_y = (end_pos[1] + offset[1]) * zoom
        
        pygame.draw.line(screen, arrow.color, (start_x, start_y), (end_x, end_y), max(1, int(2 * zoom)))
        
        # Draw arrow head
        angle = pygame.math.Vector2(end_x - start_x, end_y - start_y).angle_to((1, 0))
        arrow_head = pygame.math.Vector2(10 * zoom, 0).rotate(angle)
        pygame.draw.polygon(screen, arrow.color, [
            (end_x, end_y),
            (end_x - arrow_head.x - arrow_head.y * 0.5, end_y - arrow_head.y + arrow_head.x * 0.5),
            (end_x - arrow_head.x + arrow_head.y * 0.5, end_y - arrow_head.y - arrow_head.x * 0.5),
        ])
        
        # Render arrow description
        if arrow.description:
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            desc_font = pygame.font.Font(None, int(18 * zoom))
            
            # Calculate arrow length and max box width
            arrow_length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            max_box_width = min(arrow_length * 0.25, 200 * zoom)  # 25% of arrow length or 200 pixels, whichever is smaller
            
            # Word wrap the arrow description
            wrapped_desc = word_wrap(arrow.description, desc_font, max_box_width)
            
            # Calculate box dimensions
            line_height = desc_font.get_linesize()
            box_width = max(desc_font.size(line)[0] for line in wrapped_desc)
            box_height = line_height * len(wrapped_desc)
            
            # Create an invisible box for the arrow description
            padding = 5 * zoom
            box_rect = pygame.Rect(mid_x - box_width // 2 - padding, mid_y - box_height // 2 - padding,
                                   box_width + 2 * padding, box_height + 2 * padding)
            pygame.draw.rect(screen, (30, 30, 30), box_rect)  # Dark background for description
            pygame.draw.rect(screen, arrow.color, box_rect, 1)  # Border
            
            # Render wrapped text
            for i, line in enumerate(wrapped_desc):
                desc_text = desc_font.render(line, True, arrow.color)
                desc_rect = desc_text.get_rect(center=(mid_x, mid_y - (box_height // 2) + (i + 0.5) * line_height))
                screen.blit(desc_text, desc_rect)
    return diagram

def get_diagram_size(diagram: Diagram):
    max_x = max(box.size[0] for box in diagram.boxes)
    max_y = max(box.size[1] for box in diagram.boxes)
    return (max_x * len(diagram.boxes), max_y * len(diagram.boxes))
