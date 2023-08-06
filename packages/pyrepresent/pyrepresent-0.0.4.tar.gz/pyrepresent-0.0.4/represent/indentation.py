# indentation.py

from typing import Optional

__all__ = [
    "indent"
]

def indent(source: str, *, indentation: Optional[int] = 4) -> str:
    """
    Indents a string of object structures.

    :param indentation: The amount of spaces to indent according to.
    :param source: The source string.

    :return: The indented model structure.
    """

    if indentation is None:
        indentation = 4

    elif not indentation:
        return source
    # end if

    tab = " " * indentation

    openers = ["{", "[", "("]
    closers = ["}", "]", ")"]

    left = 0

    output = ""
    quotes = []
    quote_open = False
    exclude = 0

    for char in source:
        if exclude:
            exclude -= 1

            continue
        # end if

        if char in ("'", '"'):
            if not quotes or char != quotes[-1]:
                quotes.append(char)

                quote_open = True

            else:
                quotes.pop(-1)

                quote_open = False
            # end if

        elif not quote_open:
            if char in openers:
                left += 1

                output += char
                output += "\n" + tab * left

            elif char in closers:
                left -= 1

                output += "\n" + tab * left
                output += char

            elif char == ",":
                exclude += 1

                output += char[0]
                output += "\n" + tab * left

            else:
                output += char
            # end if

        else:
            output += char
        # end if
    # end for

    return output
# end indent