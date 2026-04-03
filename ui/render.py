import pygame
from ui.types import Element


# Colors for visualization
COLORS = {
    "background": (240, 240, 240),
    "border": (0, 0, 0),
    "text": (50, 50, 50),
}

# Configuration
BORDER_WIDTH = 2
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
FONT_SIZE = 12


def render(root: Element, title: str = "UI Layout Renderer") -> None:
    """
    Render a UI element tree to a window.

    Args:
        root: The root Element to render
        title: Window title
    """
    pygame.init()
    try:
        # Calculate window dimensions based on root element size
        window_width = max(int(root.rect.width) + 40, MIN_WINDOW_WIDTH)
        window_height = max(int(root.rect.height) + 40, MIN_WINDOW_HEIGHT)

        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(title)

        clock = pygame.time.Clock()
        font = pygame.font.Font(None, FONT_SIZE)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw background
            screen.fill(COLORS["background"])

            # Draw all elements recursively
            _draw_element(screen, root, font)

            pygame.display.flip()
            clock.tick(60)

    finally:
        pygame.quit()


def _draw_element(
    screen: pygame.Surface, element: Element, font: pygame.font.Font, level: int = 0
) -> None:
    """
    Recursively draw an element and all its children.

    Args:
        screen: Pygame surface to draw on
        element: Element to draw
        font: Font for rendering element IDs
        level: Depth level in the tree (for visual distinction)
    """
    rect = element.rect
    color = _get_color_for_level(level)
    border_color = _get_border_color(color)

    # Draw filled rectangle with main color
    pygame.draw.rect(
        screen,
        color,
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
        text_surface = font.render(element.id, True, COLORS["text"])
        text_rect = text_surface.get_rect()
        text_rect.topleft = (int(rect.x) + 5, int(rect.y) + 5)
        screen.blit(text_surface, text_rect)

    # Draw all children
    for child in element.children:
        _draw_element(screen, child, font, level + 1)


def _get_color_for_level(level: int) -> tuple[int, int, int]:
    """
    Get a color based on tree depth to visually distinguish elements.

    Args:
        level: Depth level in the element tree

    Returns:
        RGB color tuple
    """
    colors = [
        (100, 150, 200),  # Light blue
        (150, 200, 100),  # Light green
        (200, 150, 100),  # Light orange
        (200, 100, 150),  # Light pink
        (150, 150, 200),  # Lavender
    ]
    return colors[level % len(colors)]


def _get_border_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Create a darker, more saturated version of the given color for borders.

    Args:
        color: RGB color tuple

    Returns:
        Darker, more saturated RGB color tuple
    """
    r, g, b = color

    # Darken the color by reducing brightness
    darken_factor = 0.6
    r = int(r * darken_factor)
    g = int(g * darken_factor)
    b = int(b * darken_factor)

    # Increase saturation by finding the max component and boosting it
    max_val = max(r, g, b)
    saturation_boost = 1.3

    if max_val > 0:
        if r == max_val:
            r = min(255, int(r * saturation_boost))
        elif g == max_val:
            g = min(255, int(g * saturation_boost))
        elif b == max_val:
            b = min(255, int(b * saturation_boost))

    return (r, g, b)
