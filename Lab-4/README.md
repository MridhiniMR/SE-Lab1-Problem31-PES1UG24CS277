# Lab 4 – Vibe Coding: Galaga

## Overview

This submission contains the modified Galaga game for Lab 4. The assignment involved fixing a bug in the existing code, implementing the required features, and recording gameplay before and after the modifications.

## Corrections and Implemented Features

### 1. Bézier Curve Correction
Fixed the cubic Bézier interpolation formula in `bezier()` by correcting the missing factor of `t` in the \(P_2\) terms for both the x and y coordinates.

### 2. Wave-Based Enemy Colours
Implemented wave-dependent enemy colour palettes using `WAVE_PALETTES` and `enemy_tint()`. Enemy colours change across waves while retaining the default colours where applicable.

### 3. Wave-Start Banner
Implemented a temporary banner displaying the current wave number whenever a new wave begins.

### 4. Shield Mechanic
Implemented one shield charge every third wave. The shield absorbs one hit without reducing the player's ships or lives.

## Requirements

- Python 3
- Pygame

## Installation and Execution

Install Pygame:

```bash
python -m pip install pygame
```

Navigate to the directory containing `game.py` and run:

```bash
python game.py
```

## Controls

- **Left Arrow:** Move left.
- **Right Arrow:** Move right.
- **Spacebar:** Shoot.
- **R:** Reset the game.

## Testing

The supporting test files are:

- `test_bezier.py` – Tests the Bézier curve correction.
- `test_tint.py` – Tests wave-dependent enemy colours.
- `test_shield.py` – Tests shield charge allocation across waves.

## AI-Assisted Development

- **AI Tool:** Claude
- **Claude Conversation:** https://claude.ai/share/42366f05-c59c-4e32-926c-151e69ebf0aa
- **Exported Chat History:** `claude_conversation.pdf`

## Submission Contents

The `Lab-4` folder contains the updated game source code, before-and-after gameplay recordings, and the exported AI conversation required for the assignment.
