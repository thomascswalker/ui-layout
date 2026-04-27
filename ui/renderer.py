import sys


class Renderer:
    def __init__(self) -> None:
        match sys.platform:
            case "win32":
                self._init_win()
            case _:
                raise OSError(f"Unsupported OS: {sys.platform}")

    def _init_win(self) -> None:
        return


if __name__ == "__main__":
    print(sys.platform)
