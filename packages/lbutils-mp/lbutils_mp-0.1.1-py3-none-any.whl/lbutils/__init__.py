"""Utilities and Drivers for MicroPython used at Leeds Beckett University

Background
----------

This library is designed to install all of the common drivers, library code, and helper code used within modules at Leeds Beckett University. It is principally targeted at MicroPython on the Pico H/W micro-controllers: but compatibility is also maintained with CPython 3.10 where possible (or relevant).

Examples for how to use the library can be found in the '`examples`' folder: or [in the documentation](https://dlove24.github.io/lbutils/lbutils/index.html). Otherwise the library is organised as follows

* **`drivers`**: Classes aimed at low-level support of I2C, SPI and other devices requiring board-level support.
* **`helpers`**: Functions and classes which help replace boiler-plate code for tasks such as setting up network access.
* **`pmod`**: Drivers and support for the [Digilent peripheral modules](https://digilent.com/reference/pmod/start).

Installation
------------

A package of this library is provided on PyPi as
[`lbutils`](https://pypi.org/project/lbutils/). This can be installed with the
normal Python tools, and should also install to boards running MicroPython
under [Thonny](https://thonny.org/).

For manual installation, everything under the `lbutils` directory should be copied
to the appropriate directory on the MicroPython board, usually `/lib`. The
library, or individual drivers, can then be imported as normal:
see the documentation for the
[examples](https://dlove24.github.io/urest/lbutils/examples/index.html) for more
detailed guidance on the use of the library. This code is also available in the
`lbutils/examples` folder, or as the library `lbutils.examples` when the package is
installed.

Notes
------

*   This library is principally a teaching library, so the
[Documentation](https://dlove24.github.io/urest/urest) should be at least as
important as the 'code'. Where possible all algorithms and implementation
techniques should also be explained as fully as possible, or at least linked to
reference standards/implementations

*   For consistency, all code should also be in the format standardised by the
[Black](https://github.com/psf/black) library. This makes it easier to
co-ordinate external code and documentation with the implementation documented
here.

Known Implementations
---------------------

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)

Licence
-------

This module, and all included code, is made available under the terms of the MIT
Licence

> Copyright 2022-2023, David Love

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
