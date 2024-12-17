import sys


class CLI:

    _last_message_was_vanishing = False

    def warning(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print(message, file=sys.stderr)
        CLI._last_message_was_vanishing = False

    def vanishing(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print(message, file=sys.stdout)
        CLI._last_message_was_vanishing = True

    def line_up() -> None:
        print("\033[A", end="", file=sys.stdout)

    def clear_line() -> None:
        print("\033[K", end="", file=sys.stdout)

    def out(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print(message, file=sys.stdout)
        CLI._last_message_was_vanishing = False
