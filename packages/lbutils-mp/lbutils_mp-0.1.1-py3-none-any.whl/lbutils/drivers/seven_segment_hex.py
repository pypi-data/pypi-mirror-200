"""
Simple hexadecimal driver for a seven-segment display, requiring seven GPIO pins.

Overview
--------

During initialisation the user must supply a list of exactly seven GPIO pins,
using the numeric pin identifier (e.g. 16 for GPIO Pin 16). Each entry in the
list corresponds to the segment 'a' (for the first entry) to 'g' (for the last
entry). Physically, each LED segment is also assumed to be laid out in the
standard pattern, shown below. Once the constructor has been called, no further
changes are possible: and the driver will also assume exclusive use of the
relevant GPIO pins.

     - A -
   |       |
   F       B
   | - G - |
   E       C
   |       |
     - D -

**Figure 1: Assumed Layout of the Seven Segment Display**

To display a character, the `display` method of the class is used: passing in an
integer in the range 0..F representing the number to show on the seven segment.
Not that by default the `display` method assumes that GPIO pins must be held
_low_ for the segment to display: i.e. the behaviour normally used by common
anode seven-segment displays. If you need the requested GPIO pin to be held
_high_ to display a segment, pass in `True` to the `inverted` parameter of the
`display` method.

.. Note: This driver will only display characters in the range '0' to 'F', and
will raise a `ValueError` exception if the requested character is not in an
appropriate range.

Examples
--------

* Examples Folder: `seven_segment_hex_example.py`
* [WokWi](https://wokwi.com/projects/360462223276690433)

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

* Raspberry Pi Pico H/W

Licence
-------

This module, and all included code, is made available under the terms of the MIT Licence

> Copyright (c) 2023 Roz Wyatt-Millington, David Love

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import MicroPython libraries for GPIO access if available
try:
    from machine import ADC
    from machine import Pin
except ImportError:
    print("Ignoring MicroPython includes")

# Import the Python type libraries if available
try:
    from typing import Union
except ImportError:
    print("The Python type library isn't present. Ignoring.")

##
## Constants
##

ASCII_UPPERCASE = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
""" Constant for the set of ASCII letters """
ASCII_DIGITS = set("0123456789")
""" Constant for the set of ASCII digits """
ASCII_HEX_DIGITS = set("0123456789ABCDEF")
""" Constant for the set of ASCII hexadecimal decimal digits,
including _only_ those which don't fit into `ASCII_DIGITS`"""
ASCII_HEX_EXTRA_DIGITS = set("ABCDEF")
""" Constant for the set of ASCII hexadecimal decimal digits,
including _only_ those which don't fit into `ASCII_DIGITS`"""

##
## Classes
##


class SegHexDisplay:
    char_list = [
        [False, False, False, False, False, False, True],
        [True, False, False, True, True, True, True],
        [False, False, True, False, False, True, False],
        [False, False, False, False, True, True, False],
        [True, False, False, True, True, False, False],
        [False, True, False, False, True, False, False],
        [False, True, False, False, False, False, False],
        [False, False, False, True, True, True, True],
        [False, False, False, False, False, False, False],
        [False, False, False, True, True, False, False],
        [False, False, False, True, False, False, False],
        [True, True, False, False, False, False, False],
        [False, True, True, False, False, False, True],
        [True, False, False, False, False, True, False],
        [False, True, True, False, False, False, False],
        [False, True, True, True, False, False, False],
    ]
    """
    Defines how characters are rendered, from zero ('0') in the first entry to
    nine ('9') as the last entry. Note that pins which are listed here as
    `False` will be _on_ using the default options to the `display` method.
    """

    def __init__(self, gpio_request: list):
        """
        Initialise a seven-segment display, using the user supplied
        list of GPIO pins in `gpio_request` as reference for pins to
        drive.

        This class also assume a common anode seven-segment display by default,
        and so will assume that pulling a GPIO pin _low_ will turn the relevant
        segment _on_. If you need to modify this behaviour, see the `inverted`
        parameter for the `display` method.

        .. Note::
            This list of entries in the `gpio_request` _must_ be exactly seven
            entries long, or the class will throw a `ValueError` in the constructor.

        Parameters
        ----------

        gpio_request: list
            The pin-ordered list of GPIO pins to use for the segment positions
            'a' (as the first entry in the list) to 'g' (as the last entry
            in the list).

            **NOTE**: The `SegDisplay` class will also attempt to create the
            underlying GPIO object for each of the entries in the list. If
            the GPIO pins need to be initialised first, this must be done
            _before_ calling this constructor.

        Raises
        ------

        * `ValueError` if the `gpio_request` is empty, or does not have exactly
          seven elements in the list.
        """
        self.pin_list = []

        if (gpio_request is None) or (not gpio_request):
            raise ValueError("The GPIO Request List is empty")
        elif len(gpio_request) != 7:
            raise ValueError("The GPIO Request List must be EXACTLY seven entries long")
        else:
            for segment in range(7):
                self.pin_list.append(Pin(gpio_request[segment], Pin.OUT))

    def display(self, character: Union[int, str], inverted: bool = False):
        """
        Display the given `character` on the seven-segment display,
        using the `char_list` as a guide for which pins to turn on or off. By default the
        `display` method will use the entries in the `char_list` directly: if you need to
        invert the 'normal' sense, set the `inverted` parameter to `True`.

        Parameters
        ----------

        character: int or str
            The value to be displayed on the seven segment display. The value must be
            either a `str` or an `int`, and will be interpreted as follows:

            `int`: The value must be between zero ('0') and sixteen decimal ('F'), and
            will be interpreted as a single, hexadecimal digit.

            `str`: The value will be interpreted directly as a hexadecimal digit, and
            must be in the range `[0..F]`.

            If the type does not conform to the above, then a `TypeError` will be raised.

        inverted: bool
            By default the `display` method assumes that pulling a GPIO pin _low_ will
            turn the relevant segment _on_; i.e. the typical behaviour for a common
            anode display. If the attached display needs to raise a GPIO pin _high_ to
            set the segment _on_ (i.e. the typical behaviour for a common cathode
            display), call the `display` method with `inverted` set to `True`.

        Raises
        ------

        * `IndexError` if the `character` is not in a range that can be displayed.
        * `TypeError` if the `character` is not either an `int` or a `str`
        """

        # Convert a decimal integer in the range [0..15], and then display
        if isinstance(character, int):

            # For a character in the valid range...
            if 0 <= character <= 15:

                if not inverted:
                    # ... if the request is to display in the non-inverted form, then
                    # select the row in `char_list` corresponding to the character to
                    # be displayed and then set in turn each of the GPIO pins corresponding
                    # to the segment values either high or low depending on the column
                    # value in `char_list` for that segment value
                    for pin in range(7):
                        self.pin_list[pin].value(self.char_list[character][pin])
                else:
                    # ... if the request is to display in the inverted form, then
                    # select the row in `char_list` corresponding to the character to
                    # be displayed and then set in turn each of the GPIO pins corresponding
                    # to the segment values either high or low depending on the _inverse_ of
                    # the column value in `char_list` for that segment value
                    for pin in range(7):
                        self.pin_list[pin].value(not self.char_list[character][pin])
            else:
                raise IndexError(
                    "The display character must be between zero ('0') and sixteen ('F')"
                )

        # Convert a string integer in the range [0..F], and then display
        elif isinstance(character, str):

            # Normalise the character by converting to upper case
            normalised_character = character.upper()

            # Check if this normalise character is a valid hexadecimal digit...
            if normalised_character in ASCII_HEX_DIGITS:

                # ... if so, convert the hexadecimal string to an integer, so we can use
                # this as the index for the character lookup
                char_list_index = int(normalised_character, 16)

                if not inverted:
                    # If the request is to display in the non-inverted form, then
                    # select the row in `char_list` corresponding to the `char_list_index` to
                    # be displayed and then set in turn each of the GPIO pins corresponding
                    # to the segment values either high or low depending on the column
                    # value in `char_list` for that segment value
                    for pin in range(7):
                        self.pin_list[pin].value(self.char_list[char_list_index][pin])

                else:
                    # If the request is to display in the inverted form, then
                    # select the row in `char_list` corresponding to the `char_list_index` to
                    # be displayed and then set in turn each of the GPIO pins corresponding
                    # to the segment values either high or low depending on the _inverse_ of
                    # the column value in `char_list` for that segment value
                    for pin in range(7):
                        self.pin_list[pin].value(
                            not self.char_list[char_list_index][pin]
                        )
            else:
                raise IndexError(
                    "The display character must be a string between '0' and 'F'"
                )

        # If we can't convert the input `character`, raise an exception
        else:
            raise TypeError(
                "The 'character' parameter must either be an integer\
                ('int') or a string ('str') type."
            )
