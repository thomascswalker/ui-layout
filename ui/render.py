from copy import deepcopy
from pathlib import Path

import pygame
from pygame.color import Color
from pygame.locals import RESIZABLE
import logging

from ui.layout import layout
from ui.types import Element, Rect

logger = logging.getLogger(__name__)

COLORS: dict[str, Color] = {
    "background": Color.from_hex("#FFFFFF"),
    "border": Color.from_hex("#000000"),
    "text": Color.from_hex("#000000"),
}
DEPTH_COLORS: list[Color] = [
    Color.from_hex("#EF4444"),  # Red
    Color.from_hex("#F99B16"),  # Orange
    Color.from_hex("#EAAD08"),  # Yellow
    Color.from_hex("#22C55E"),  # Green
    Color.from_hex("#3B82F6"),  # Blue
]

# Configuration
BORDER_WIDTH = 2
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

FONT: pygame.font.Font
FONT_SIZE = 12
FONT_FAMILY = "monospace"


def render(root: Element, title: str) -> None:
    logger.debug("Initializing Pygame...")
    pygame.init()

    # Calculate window dimensions based on root element size
    window_width = MIN_WINDOW_WIDTH
    window_height = MIN_WINDOW_HEIGHT

    screen = pygame.display.set_mode((window_width, window_height), RESIZABLE)
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()
    global FONT
    FONT = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

    logger.debug("Starting render loop...")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                logger.debug("Exiting render loop...")
            if event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                screen = pygame.display.set_mode(
                    (window_width, window_height), RESIZABLE
                )
                logger.debug(f"Resized window to: {window_width}x{window_height}")

        # Draw background
        screen.fill(COLORS["background"])

        # Layout all elements
        available = Rect(x=0, y=0, width=window_width, height=window_height)
        layout(root, available)

        # Draw all elements recursively
        _render_element(screen, root)

        pygame.display.flip()
        clock.tick(60)
    logger.debug("Exiting...")


def _render_element(
    screen: pygame.Surface,
    element: Element,
    level: int = 0,
) -> None:
    rect = element.rect

    # Get the base color for this depth level and calculate a border color
    base_color = DEPTH_COLORS[level % len(DEPTH_COLORS)]
    border_color = deepcopy(base_color)
    border_color.r = max(0, border_color.r - 50)
    border_color.g = max(0, border_color.g - 50)
    border_color.b = max(0, border_color.b - 50)

    # Draw filled rectangle with main color
    pygame.draw.rect(
        screen,
        base_color,
        (rect.x, rect.y, rect.width, rect.height),
    )

    # Draw border with darker, more saturated color
    pygame.draw.rect(
        screen,
        border_color,
        (rect.x, rect.y, rect.width, rect.height),
        BORDER_WIDTH,
    )

    # Draw element ID as text (if large enough to fit text)
    if rect.width > 50 and rect.height > 30:
        pos_text = f"{int(element.rect.x)}x, {int(element.rect.y)}y"
        size_text = f"{int(element.rect.width)}w, {int(element.rect.height)}h"
        text_surface = FONT.render(
            f"{element.id}\n[{pos_text}], [{size_text}]",
            True,
            COLORS["text"],
        )
        text_rect = text_surface.get_rect()
        text_rect.topleft = (int(rect.x) + 5, int(rect.y) + 5)
        screen.blit(text_surface, text_rect)

    # Draw all children
    for child in element.children:
        _render_element(screen, child, level + 1)


def _find_file(filename: str) -> Path:
    path = Path(filename)
    if path.exists() and path.is_file():
        return path

    # Check in current directory
    current_dir_path = Path.cwd()
    pattern = f"**/{filename}"
    if not pattern.endswith(".html"):
        pattern += ".html"
    html_files = list(current_dir_path.glob(pattern))
    if html_files:
        return html_files[0]

    raise FileNotFoundError(
        f"File '{filename}' not found in current directory or provided path."
    )


def render_file(filename: str) -> None:
    html_path = _find_file(filename)
    logger.debug(f"Loading {filename} from {html_path}...")

    with open(html_path, "r") as f:
        xml_string = f.read()

    logger.debug("Parsing file...")
    root_element = Element.parse(xml_string)

    logger.debug("Rendering file...")
    render(root_element, html_path.stem)
