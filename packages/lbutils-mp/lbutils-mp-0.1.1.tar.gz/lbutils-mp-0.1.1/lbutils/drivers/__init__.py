"""
Drivers for low-level components, including those using the SPI or I2C busses

Overview
--------

This is mostly a collection of drivers, some third-party, which provide low-level access to devices. In most cases additional code will be required to _use_ these devices: the focus of the code in here is only on providing _access_ to those devices.

Examples for how to use the library can be found in the '`examples`' folder: or [in the documentation](https://dlove24.github.io/urest/lbutils/examples/index.html).

**NOTE:** The Digilent '`pmod`' devices are split into their own special section, and should be imported using the '`pmod`' libraries.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W

Licence
-------

This module, and all included code, is made available under the terms of the MIT Licence

> Copyright (c) 2023 David Love

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

### Expose the `drivers` module interface as a full package
from .seven_segment import SegDisplay
from .seven_segment_hex import SegHexDisplay
