# 🏀 3D Ball Roller Game

> **Built with:**  
> `PyOpenGL`, `GLUT`, `GLU`, `random`, `math`

A 3D obstacle-dodging game where you control a rolling ball through colorful challenges!

---

## 🎮 Features

### 🕹️ Core Gameplay
- **Ball Control**:
  - `←` `→` Arrow keys to move left/right between lanes
  - `SPACEBAR` to jump over obstacles
- **Objective**: Navigate through incoming balls while matching colors

### ⚡ Game Flow
- **Score System**:
  - `+1 point` when colliding with **orange balls** (matching color)
  - `Game Over` when hitting **blue/red balls** (wrong colors)
- **Progression**:
  - Complete levels by reaching the finish line
  - Increasing difficulty with each level

### 🎥 View Options
- **Camera Toggle** (`V` key):
  - **Third-person view** (default): Classic overhead perspective
  - **First-person view**: Immersive ball's-eye view

### ⏯️ Game Management
- `F1` - Start / Pause / Continue / Restart  
- `F2` - Pause the game  
- `ESC` - Exit game

### 🚀 Level System
- Progress through increasingly difficult levels
- New levels introduce faster obstacles and more complex patterns

---

## ✨ New Features

### 🧲 Power-ups
- **Magnet**: Automatically attracts same-colored balls (duration-limited)
- **Heart**: Grants extra life (up to 5 max)

### 💔 Lives System
- Player starts with 3 lives
- Wrong collisions reduce life
- Game ends when lives reach 0

### 🌗 Day/Night Mode
- Toggle day/night theme using `5` key
- Background and road visuals adapt dynamically

### 🔄 Wall Color Matching
- Periodic color walls require matching your ball’s color to pass
- Successful match changes the ball's color

### 💻 Cheat Mode (for fun/testing)
- Toggle with `C` key
- Enables invincibility and bonus scoring

### 🔃 Ball Rotation Animation
- Main ball rotates for visual feedback when moving/jumping

---

## 🛠️ How to Play
1. Use arrow keys to dodge incoming balls  
2. Jump (`SPACEBAR`) to avoid obstacles  
3. Match your ball's color to orange balls for points  
4. Avoid blue/red balls to survive  
5. Reach the finish line to level up!

---

## 📊 Scoring

| Action                  | Result           |
|-------------------------|------------------|
| Orange ball collision   | +1 point         |
| Blue/Red ball collision | Lose a life      |
| All lives lost          | Game Over        |
| Level completion        | Unlock next level |

> 💡 **Pro Tip**: Time your jumps carefully – you can leap over incoming balls and avoid death!
