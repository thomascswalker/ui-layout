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
    "background": Color(255, 255, 255),
    "border": Color(0, 0, 0),
    "text": Color(0, 0, 0),
}
DEPTH_COLORS: list[Color] = [
    Color(100, 150, 200),  # Light blue
    Color(150, 200, 100),  # Light green
    Color(200, 150, 100),  # Light orange
    Color(200, 100, 150),  # Light pink
    Color(150, 150, 200),  # Lavender
]

# Configuration
BORDER_WIDTH = 2
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
FONT_SIZE = 20
FONT: pygame.font.Font


def render(root: Element, title: str = "UI Layout Renderer") -> None:
    """
    Render a UI element tree to a window.

    Args:
        root: The root Element to render
        title: Window title
    """
    logger.debug("Initializing Pygame...")
    pygame.init()

    # Calculate window dimensions based on root element size
    window_width = MIN_WINDOW_WIDTH
    window_height = MIN_WINDOW_HEIGHT

    screen = pygame.display.set_mode((window_width, window_height), RESIZABLE)
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()
    global FONT
    FONT = pygame.font.Font(None, FONT_SIZE)

    logger.debug("Starting render loop...")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                screen = pygame.display.set_mode(
                    (window_width, window_height), RESIZABLE
                )

        # Draw background
        screen.fill(COLORS["background"])

        # Layout all elements
        layout(
            root,
            Rect(
                x=0,
                y=0,
                width=window_width,
                height=window_height,
            ),
        )

        # Draw all elements recursively
        draw_element(screen, root)

        pygame.display.flip()
        clock.tick(60)


def draw_element(screen: pygame.Surface, element: Element, level: int = 0) -> None:
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
        text_surface = FONT.render(element.id, True, COLORS["text"])
        text_rect = text_surface.get_rect()
        text_rect.topleft = (int(rect.x) + 5, int(rect.y) + 5)
        screen.blit(text_surface, text_rect)

    # Draw all children
    for child in element.children:
        draw_element(screen, child, level + 1)


def render_file(filename: str) -> None:
    """Render a UI layout from an XML file."""
    logger.debug(f"Loading {filename}")
    xml_path = Path(filename)
    if not xml_path.exists():
        raise FileNotFoundError("XML file not found")
    if not xml_path.is_file():
        raise ValueError("Provided path is not a file")
    with open(xml_path, "r") as f:
        xml_string = f.read()
    logger.debug("Parsing file...")
    root_element = Element.parse(xml_string)
    logger.debug("Rendering file...")
    render(root_element, xml_path.stem)
