# terminal formatter
The Terminal Formatter Library provides a few easy-to-use functions for formatting terminal-printed
text with custom functions and wrappers for pprintpp and colored. This library is mostly 
intended for personal use and might introduce breaking changes at any point.

With this library, you can:

* Highlight text
* Wrap text inside a box to have it stand out even in large amounts of output
* Pretty-print data structures
* Indent blocks of text
* Colorize text and backgrounds for colored terminal printing

## installation
The library can be installed with
```
pip install terminal-formatter
```
It then can be imported in your script with
```
import terminal-formatter
```


## available functions

`heading(text: str) -> str` - Formats headings, shortcut for box() inside highlight() function.

`highlight(text: str) -> str` - Highlight text by changing its color to `orange_1`.

`box(text: str) -> str` - Wraps text inside a box of `#` characters to have it stand out of even large amounts of output.

`pretty(obj) -> str` - Prettyprint a data structure - wraps pprintpp's `format` function.

`indent(text: str, amount: int = 1, indent_character: str = ' ') -> str` - Indent text by increments of four.

`colorize(text: str, color: str) -> str` - Colorize given text for colored terminal printing.

`colorize_bg(text: str, color: str) -> str` - Colorize given text's background for colored terminal printing.

## license

This library is licensed under the MIT License. See the LICENSE file for details.