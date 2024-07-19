import sys
import os
import glob
import re
from aiqs import ModelInterface
from diagram_renderer import render_diagram, get_diagram_size
from diagram_parser import Diagram, Box, Arrow, parse_diagram
from system_prompts import DEFAULT_PROMPT
import pygame
import time

def gather_files(pattern):
    return glob.glob(pattern, recursive=True)

def read_file_contents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def format_files_for_ai(files):
    formatted_content = '<project files>\n'
    for file in files:
        content = read_file_contents(file)
        formatted_content += f'<file path="{file}">{content}</file>\n'
    formatted_content += '</project files>'
    return formatted_content

def read_system_instructions():
    return DEFAULT_PROMPT

def generate_diagram(project_files, system_instructions, model_interface, generations=1):
    prompt = f"{system_instructions}\n\n{project_files}"
    
    for _ in range(generations):
        response, _ = model_interface.send_to_ai(prompt, model="bedrock-sonnet", max_tokens=4000)
        diagram_match = re.search(r'<diagram>(.*?)</diagram>', response, re.DOTALL)
        
        if diagram_match:
            return diagram_match.group(1).strip()
    
    raise ValueError("No diagram found in the AI response after all generations.")

def save_diagram(diagram, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(diagram)

def display_diagram(diagram_path):
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Interactive Diagram Renderer")

    # Parse the diagram file
    diagram = parse_diagram(diagram_path)

    # Get the diagram size
    diagram_width, diagram_height = get_diagram_size(diagram)

    # Initialize variables for panning and zooming
    offset_x, offset_y = 0, 0
    zoom = 1.0
    dragging = False
    last_mouse_pos = (0, 0)

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Mouse wheel up
                    zoom *= 1.1
                elif event.button == 5:  # Mouse wheel down
                    zoom /= 1.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                    offset_x += dx / zoom
                    offset_y += dy / zoom
                    last_mouse_pos = event.pos
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Render the diagram
        render_diagram(screen, diagram, (offset_x, offset_y), zoom)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

def main():
    if len(sys.argv) == 1:
        default_diagram_path = "diagrams/output.sdiag"
        display_diagram(default_diagram_path)
    elif len(sys.argv) < 2:
        print("Usage: python diagram_generator.py [file glob matching pattern] [number of generations=1]")
        sys.exit(1)

    file_pattern = sys.argv[1]
    generations = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    files = gather_files(file_pattern)
    if not files:
        print(f"No files found matching the pattern: {file_pattern}")
        sys.exit(1)

    project_files = format_files_for_ai(files)
    system_instructions = read_system_instructions()

    model_interface = ModelInterface()

    try:
        diagram = generate_diagram(project_files, system_instructions, model_interface, generations)
        output_path = os.path.join("diagrams", "output.sdiag")
        save_diagram(diagram, output_path)
        display_diagram(output_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise error
        sys.exit(1)

if __name__ == "__main__":
    main()
