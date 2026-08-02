# Alien Invasion

A classic Space Invaders-style arcade game built with Python and Pygame. Defend your ship by shooting down waves of aliens before they reach the bottom of the screen.

<!-- Add your screenshots here -->
<!-- ![Gameplay](screenshots/gameplay.png) -->

## Features

- **Wave-based alien fleets** — aliens speed up as you clear each wave
- **Scoring system** — points increase per level with a persistent high score saved to `highscores.json`
- **Lives system** — 3 ships per game, displayed on the HUD
- **Level progression** — ship, bullet, and alien speeds scale with each wave cleared
- **Sound effects & music** — laser shots, explosions, and background music
- **Pause / Resume** — pause mid-game with `Esc`


## Controls

| Key | Action |
|---|---|
| `←` `→` | Move ship |
| `Space` | Fire bullet |
| `P` | Start game |
| `Esc` | Pause / Resume |
| `R` | Reset game |
| `Q` | Quit |

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/Ishaan16Gupta/Space-Invaders-Game.git
cd Space-Invaders-Game

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the Game

```bash
python alien_invasion.py
```

## Project Structure

```
.
├── alien_invasion.py    # Main game loop and event handling
├── settings.py          # Game configuration (speeds, colors, limits)
├── ship.py              # Player ship class
├── alien.py             # Alien sprite class
├── bullet.py            # Bullet sprite class
├── button.py            # UI button (Play / Resume)
├── scoreboard.py        # HUD — score, high score, level, lives
├── game_stats.py        # Tracks game state and stats
├── highscores.json      # Persistent high score storage
├── images/              # Sprite assets
├── Sounds/              # SFX and background music
└── requirements.txt
```

## Built With

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

## License

This project is open source and available for personal and educational use.
