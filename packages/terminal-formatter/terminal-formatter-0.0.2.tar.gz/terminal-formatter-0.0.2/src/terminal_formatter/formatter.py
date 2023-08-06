"""
Implements the formatting functionality.
Allows styling/formatting of text with custom functions and wrappers for pprintpp and colored.
"""
import shutil
import textwrap
import pprintpp as pprint  # type: ignore
import colored  # type: ignore

INDENT_SIZE = 4
HIGHLIGHT_COLOR = 'orange_1'
BOX_CHARACTER = '#'


def _terminal_width() -> int:
    """
    Get terminal width.
    :return: Width of the terminal
    """
    return shutil.get_terminal_size(fallback=(80, 50)).columns


def heading(text: str) -> str:
    """
    Formats headings, shortcut for box() inside highlight() function.
    :param text: Text to format
    :return: Formatted text
    """
    return highlight(box(text))


def highlight(text: str) -> str:
    """
    Highlight text by changing its color to HIGHLIGHT_COLOR
    :param text: Text to format
    :return: Formatted text
    """
    return colorize(text, HIGHLIGHT_COLOR)


def box(text: str) -> str:
    """
    Wraps text inside a box of BOX_CHARACTER characters to have it stand out of even large
    amounts of output.
    :param text: Text to format
    :return: Formatted text
    """
    filled = BOX_CHARACTER * _terminal_width()
    blank = BOX_CHARACTER + ' ' * (_terminal_width() - 2) + BOX_CHARACTER
    prefix = BOX_CHARACTER + ' ====> '
    suffix = ' ' + BOX_CHARACTER
    lines = _split(text, " ", _terminal_width() - len(prefix) - len(suffix))

    buffer = ['', filled, blank]
    for line in lines:
        buffer.append(prefix + line + ' ' * (_terminal_width() - len(prefix) - len(line) -
                                             len(suffix)) + suffix)
    buffer.append(blank)
    buffer.append(filled)
    buffer.append('')
    return '\n'.join(buffer)


def _split(text: str, sep: str, length: int) -> list[str]:
    """
    Split given text into smaller chunks inside given size limit.
    :param text: Text to split
    :param sep: Separator at which the text can be split
    :param length: Maximal length of split text lines
    :return: Split text lines
    """
    separated = []
    words = text.split(sep)
    counter = 0
    iterator = 0

    while len(words) > 0:
        if len(words[iterator]) > length:
            words[iterator] = words[iterator][:length - 5] + '...'
        while counter + len(words[iterator]) + 1 < length:
            counter += len(words[iterator]) + 1
            iterator += 1
            if iterator == len(words):
                break
        separated.append(sep.join(words[:iterator]))
        words = words[iterator:]
        iterator = 0
        counter = 0
    return separated


def _vsep() -> str:
    """
    Separator to visibly split text vertically.
    :return: Line of BOX_CHARACTER
    """
    return '\n' + BOX_CHARACTER * int(_terminal_width() / 2) + '\n\n'


def pretty(obj) -> str:
    """
    Prettyprint a data structure.
    :param obj: Data to print pretty
    :return: String of pretty data structure representation
    """
    return '\n' + pprint.pformat(obj, indent=INDENT_SIZE)


def indent(text: str, amount: int = 1, indent_character: str = ' ') -> str:
    """
    Indent text.
    :param text: Text to indent
    :param amount: Width of indent
    :param indent_character: Character to use for indent
    :return: Indented text
    """
    return textwrap.indent(text, amount * INDENT_SIZE * indent_character)


def colorize(text: str, color: str) -> str:
    """
    Colorized given text for colored terminal printing.
    :param text: Text to colorize
    :param color: Color to use, see https://pypi.org/project/colored/ for a list of color strings
    :return: Colorized text
    """
    return colored.stylize(text, colored.fg(color))


def colorize_bg(text: str, color: str) -> str:
    """
    Colorized given texts background for colored terminal printing.
    :param text: Text to colorize
    :param color: Color to use, see https://pypi.org/project/colored/ for a list of color strings
    :return: Text with colorized background
    """
    return colored.stylize(text, colored.bg(color))
