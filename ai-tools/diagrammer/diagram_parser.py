
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Box:
    id: str
    text: str
    size: Tuple[int, int]
    color: Tuple[int, int, int]
    description: str

@dataclass
class Arrow:
    start: str
    end: str
    color: Tuple[int, int, int]
    description: str

@dataclass
class Diagram:
    boxes: List[Box]
    arrows: List[Arrow]

def parse_diagram(filename: str) -> Diagram:
    boxes = []
    arrows = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('BOX'):
                parts = line.split('|')
                id = parts[1]
                text = parts[2]
                x1, y1 = map(int, parts[3].split(','))
                x2, y2 = map(int, parts[4].split(','))
                w, h = abs(x2 - x1), abs(y2 - y1)
                print(parts)
                r, g, b = map(int, parts[5].split(','))
                description = parts[6]
                boxes.append(Box(id, text, (w, h), (r, g, b), description))
            elif line.startswith('ARROW'):
                parts = line.split('|')
                start = parts[1]
                end = parts[2]
                r, g, b = map(int, parts[3].split(','))
                description = parts[4]
                arrows.append(Arrow(start, end, (r, g, b), description))

    return Diagram(boxes, arrows)
