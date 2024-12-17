import sys


class CLI:

    _last_message_was_vanishing = False

    def warning(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print("\033[93m" + message + "\033[0m")
        CLI._last_message_was_vanishing = False

    def vanishing(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print("\033[90m" + message + "\033[0m")
        CLI._last_message_was_vanishing = True

    def line_up() -> None:
        print("\033[A", end="")

    def clear_line() -> None:
        print("\033[K", end="")

    def out(message: str) -> None:
        if CLI._last_message_was_vanishing:
            CLI.line_up()
            CLI.clear_line()
        print(message)
        CLI._last_message_was_vanishing = False
