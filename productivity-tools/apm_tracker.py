import threading
from pynput import mouse, keyboard
import pystray
from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk
import time
import argparse
from collections import deque

# Global variables
action_times = deque()
apm = 0
running = True
icon = None
graph_icon = None
period_start_time = None
  # Efficient fixed-size history

# Parse command-line arguments
parser = argparse.ArgumentParser(description="APM Monitor - Track actions per minute")
parser.add_argument("-constant", action="store_true", help="Constant/rolling window mode")
parser.add_argument("-report-card", action="store_true", help="Report-card mode (default)")
parser.add_argument("-period", type=float, default=60, help="Period in seconds (default=60s)")
args = parser.parse_args()

# Determine mode: default to "report-card" if neither or both flags are specified
mode = "report-card" if (args.constant and not args.report_card) else "constant"
period = args.period
apm_history = deque(maxlen=int(period*100)) # max 100 aps (doubt but whatever)

# Input handlers
def on_action(*args):
    action_times.append(time.time())

def on_click(x, y, button, pressed):
    if pressed:
        action_times.append(time.time())

# APM calculation
def calculate_apm():
    global action_times, apm, period_start_time, apm_history
    period_start_time = time.time() if mode == "report-card" else None
    while running:
        current_time = time.time()
        if mode == "constant":
            # Remove old actions in bulk
            while action_times and current_time - action_times[0] > period:
                action_times.popleft()
            apm = int(len(action_times) * 60 / period) if action_times else 0
            apm_history.append(apm)
            update_tray_icons()
            time.sleep(0.5)
        else:  # report-card
            if current_time - period_start_time >= period:
                apm = int(len(action_times) * 60 / (current_time - period_start_time)) if action_times else 0
                apm_history.append(apm)
                update_tray_icons()
                action_times.clear()
                period_start_time = current_time
            time.sleep(0.1)

# Create text icon
def create_text_icon(apm_value):
    img = Image.new('RGB', (128, 64), color=(46, 46, 46))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 40)
        d.text((10, 12), str(apm_value), fill=(255, 255, 255), font=font)
    except Exception as e:
        print(e)
        d.text((10, 25), str(apm_value), fill=(255, 255, 255), fontsize=40)  # Fallback
    return img

# Create simplified graph icon
def create_graph_icon():
    img = Image.new('RGB', (128, 64), color=(46, 46, 46))
    d = ImageDraw.Draw(img)
    if not apm_history:
        return img
    
    max_apm = max(apm_history) or 1
    width, height = 128, 64
    points = []
    history_len = len(apm_history)
    
    # Pre-calculate points
    for i, value in enumerate(apm_history):
        x = i * (width - 1) // (history_len - 1) if history_len > 1 else width // 2
        y = height - 1 - int((value / max_apm) * (height - 1))
        points.append((x, y))
    
    # Draw line
    if len(points) > 1:
        d.line(points, fill=(53, 168, 84), width=7)
    else:
        d.point(points[0], fill=(53, 168, 84))
    
    return img

# Update tray icons
def update_tray_icons():
    if icon:
        icon.icon = create_text_icon(apm)
    if graph_icon:
        graph_icon.icon = create_graph_icon()

# Quit handler
def quit_app(icon_arg, item):
    global running, icon, graph_icon
    running = False
    if icon:
        icon.stop()
    if graph_icon:
        graph_icon.stop()
    root.quit()

# Setup tray icons
def setup_tray():
    global icon, graph_icon
    menu = pystray.Menu(pystray.MenuItem("Quit", quit_app))
    icon = pystray.Icon("APM", create_text_icon(0), "APM Monitor", menu)
    graph_icon = pystray.Icon("APM Graph", create_graph_icon(), "APM History")
    
    threading.Thread(target=icon.run, daemon=True).start()
    threading.Thread(target=graph_icon.run, daemon=True).start()

# Main
if __name__ == "__main__":
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_release=on_action)
    mouse_listener.start()
    keyboard_listener.start()

    apm_thread = threading.Thread(target=calculate_apm, daemon=True)
    apm_thread.start()

    root = Tk()
    root.withdraw()
    setup_tray()
    root.mainloop()
