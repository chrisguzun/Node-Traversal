# Node-Traversal

An interactive graph editor and visualizer built with Python and Pygame. Create nodes, connect them with weighted edges, and run Dijkstra's shortest-path algorithm in real time.

## Features

- Add, remove, and connect nodes interactively
- Weighted directed edges
- Dijkstra's shortest-path visualization
- Save and load graphs from `.pkl` files
- Mouse-drag pan and scroll-to-zoom

## Requirements

- Python 3.8+
- pygame

## Installation

```bash
git clone https://github.com/chrisguzun/Node-Traversal.git
cd Node-Traversal
pip install -r requirements.txt
```

## Usage

```bash
python nodeTraversal.py
```

### Controls

| Input | Action |
|---|---|
| `N` | Add a new node at the mouse cursor |
| Left-click a node | Select it |
| Left-click a second node | Connect selected → clicked (weight 1) |
| Right-click a node | Set as **start** node |
| Middle-click a node | Set as **end** node |
| `P` | Run Dijkstra's algorithm (shortest path shown in pink) |
| `Backspace` | Delete selected node |
| `R` | Add 10 random nodes |
| `C` | Clear the graph |
| `S` | Save graph (prompts for filename) |
| `M` | Open load menu |
| Scroll | Zoom in / out |
| Click + drag | Pan the view |
