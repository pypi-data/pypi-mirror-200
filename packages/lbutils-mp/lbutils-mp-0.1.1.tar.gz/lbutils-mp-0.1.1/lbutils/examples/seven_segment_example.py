"""
Example of using the `lbutils.drivers.SegDisplay` driver for a seven-segment display, requiring seven GPIO pins.

Overview
--------

A complete example is available at [WokWi](https://wokwi.com/projects/360451068863047681), which is based on the same driver code.

In both cases a value is read from the Pico ADC on Pin 26 (i.e. `ADC0`), and converted in a value from `0` to `99`. The final output is the displayed using two seven-segment displays: each driven by the `lbutils.drivers.SegDisplay` class.

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

# Import required core libraries
try:
    import utime
    import hidden
except ImportError:
    print("Missing core libraries")

# Import required libraries from LBUtils
try:
    from lbutils.drivers import SegDisplay
except ImportError:
    print("Missing LBUtils seven segment driver")

# define GPIO pins to use, matching: 'A', 'B', 'C', 'D', 'E', 'F', and 'G'
# segments on the displays. Two lists are used, one for each segment.
seg_list1 = [2, 3, 4, 5, 6, 7, 8]
seg_list2 = [10, 11, 12, 13, 14, 15, 16]

# Create the seven-segment display objects, each attached to the relevant
# segment using the `SegDisplay` driver class
segDisp1 = SegDisplay(seg_list1)
segDisp2 = SegDisplay(seg_list2)

# Read the input value from ADC0 on GPIO Pin 26
adc = ADC(26)

# Set-up the main loop to read and display the input values
while True:
    adcval = adc.read_u16()
    temp = hidden.measureval(adcval)
    segDisp2.display(int(temp % 10))
    segDisp1.display(int((temp / 10) % 10))

    utime.sleep(1)
