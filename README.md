# ✨ Visual Patterns Studio 🎨
*A Creative Interactive Application for Drawing, Fractals, and Kaleidoscopic Visuals*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5-green.svg)](https://www.pygame.org/)
[![ModernGL](https://img.shields.io/badge/Renderer-ModernGL-orange.svg)](http://moderngl.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

**Visual Patterns Studio** is a creative graphics project built using **Python**, **Pygame**, and **ModernGL**.
It offers an **interactive drawing canvas**, a **fractal generator**, and a **kaleidoscope visualizer** —
all wrapped in an intuitive menu system.

This project is perfect for exploring **computer graphics concepts**, **OpenGL shaders**, and **creative visual art** in programming!

---

## 🚀 Features

### 🖌️ **Interactive Drawing Board**
- Paint using different tools — **Brush**, **Line**, **Rectangle**, **Circle**, and **Bucket Fill**
- Adjustable brush size and eraser
- **Undo / Redo** functionality
- Color palette selection
- Custom brush cursor preview
- Save your art instantly as `.png`

### 🌌 **Fractal Generator**
- **GPU-accelerated** fractal rendering using **ModernGL**
- Dynamic coloring and continuous zoom
- Interactive zoom and pan controls
- Real-time animation and color palette regeneration

### 🌈 **Kaleidoscope Visualizer**
- **Symmetrical animated visuals**
- Beautiful color transitions and mirror effects
- Live color regeneration with one click
- Mesmerizing motion blending using **OpenGL shaders**
  
### 🌀 **Mandala (Rangoli) Art Module**
- **Real-Time GPU Rendering** for intricate mandala patterns  
- Dynamic **color palette generation** (vibrant, cool, pastel modes)
- **Shader-based glow and bloom effects** for a luminous aesthetic  

### 🎆 **Fireworks Simulation**
- **Particle-based fireworks physics** using Pygame  
- Realistic **gravity, drag, and fading** effects  
- Each rocket spawns 130–180 glowing particles  
- **Mouse-click to launch** rockets dynamically  
- **Randomized explosion colors** for every launch
- Integrated **sound effects**
---

## 🧠 Concepts Used

* **Pygame:** Window management, input handling, and 2D drawing
* **ModernGL:** GPU rendering using **OpenGL shaders**
* **Fragment Shaders:** Color blending, motion effects, and procedural patterns
* **Interactive Graphics:** Mouse & keyboard event handling
* **Procedural Art:** Random color palettes and geometry-based visuals
* **Data Structures:** Undo/Redo stack management
* **Mathematical Concepts:**
    * Mandelbrot fractal formula: $z = z^n + c$
    * Polar coordinates & trigonometric symmetry
    * Smooth color interpolation

---

## 🕹️ Controls

### 🎨 Drawing Mode
| Action | Key / Mouse |
|:---|:---|
| Draw | **Left Click** |
| Erase | **Right Click** |
| Change Brush Size | **+** / **-** |
| Switch Tool | **D**, **E**, **L**, **R**, **O**, **B** |
| Toggle Fill | **F** |
| Undo / Redo | **Z** / **Y** |
| Clear Canvas | **C** |
| Save Image | **S** |
| Back to Menu | **ESC** |

### 🌌 Fractal Mode
| Action | Key / Mouse |
|:---|:---|
| Zoom In / Out | **Mouse Wheel** |
| Pan | **Drag Left Click** |
| Regenerate Colors | **Left Click** |
| Adjust Power | **↑** / **↓** |
| Reset View | **R** |
| Exit | **ESC** |

### 🌈 Kaleidoscope Mode
| Action | Key / Mouse |
|:---|:---|
| Regenerate Colors | **Left Click** |
| Exit | **ESC** |

## 🎆 Fireworks Mode 

| **Control** | **Action** |
|--------------|------------|
| 🖱️ **Left Mouse Click** | Launch a rocket at the clicked position |
| ⌨️ **ESC Key** | Exit Fireworks mode / Return to main menu |
| ⌨️ **Q Key (optional addition)** | Could be added as a quit shortcut |
| 💥 **Automatic Explosion** | Rockets automatically explode mid-air |
| 🌈 **Colors** | Randomly chosen from a predefined palette |
| 🔊 **Sounds** | Launch and explosion effects via `launch.mp3` and `explode.mp3` |

### 🌀 Mandala (Rangoli) Art Module Controls (matches your `rangoli.py`)

| **Control** | **Action** |
|--------------|------------|
| 🖱️ **Left Mouse Click** | Generate a new mandala (randomize palette and pattern) |
| 🖱️ **Left Mouse Drag** | Pan the view |
| 🖱️ **Right Mouse Click** | Reset zoom and pan (center view) |
| 🖱️ **Mouse Wheel Up / Down** | Zoom in / out towards the mouse pointer |
| ⌨️ **Arrow Keys ← / →** | Decrease / Increase number of symmetry folds |
| ⌨️ **Arrow Keys ↑ / ↓** | Increase / Decrease animation speed |
| ⌨️ **1–4 Keys** | Switch between visual modes (pattern types) |
| ⌨️ **R Key** | Randomize color palette (vibrant, cool, or pastel) |
| ⌨️ **S Key** | Save current mandala as `mandala.png` |
| ⌨️ **E Key** | Gradually erase / fade out the pattern |
| ⌨️ **D Key** | Resume drawing after fade |
| ⌨️ **Spacebar** | Pause or resume animation |
| ⌨️ **ESC Key** | Exit Mandala module / return to main menu |

---

## ⚙️ Installation

### 🪄 Step 1: Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)<your-username>/Visual-Patterns-Studio.git
cd Visual-Patterns-Studio
```
### 🪄 Step 2: Install Dependencies
Ensure you have **Python 3.8+** installed, then install the required libraries:

```bash
pip install pygame moderngl numpy
```
###🪄 Step 3: Run the Application
```bash
python main.py
```
---
⭐ Enjoy creating beautiful patterns and exploring the magic of graphics!

---
### License
This project is licensed under the MIT License – feel free to use and modify it for educational or creative purposes.

