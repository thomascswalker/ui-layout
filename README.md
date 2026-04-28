# UI Layout

## Overview

Algorithms for laying out GUI elements, written in Python for simplicity. 

![Example Image](images/example.png)

## Usage

1. `uv venv`
2. Activate the virtual environment:
    - Windows: `.venv\scripts\activate`
    - Linux: `source .venv/bin/activate`
3. `uv sync`

> [!TIP]
> If you want to run linting or tests, use `uv sync --all-extras`.

At this point you can run the simple CLI renderer.

4. `uv run layout <name>`

> [!NOTE]
> `uv run layout basic`

> [!TIP]
> Example .html files can be found in `tests/fixtures/`.

## AI Usage

Used Copilot to generate/maintain tests as well as the win32/x11 abstractions (as these were 
not the focus of the project).
