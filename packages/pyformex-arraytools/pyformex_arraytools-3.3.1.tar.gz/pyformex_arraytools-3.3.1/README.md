# pyFormex Array Tools

This package contains a collection of numerical utilities and array tools
from the [pyFormex project](https://pyformex.org).
During two decades of pyFormex development, some tools were created that may
be interesting for a wider community. So we decided to publish these tools
separately to make them easier to install for those not needing the whole
pyFormex framework.

## Requirements

  While these functions were historically developed for pyFormex,
  the only requirement to use this package is NumPy.
  It can be used outside of pyFormex without changes.

## Available modules

  * arraytools: A wide collection of numerical utilities and array tools.
	Most of the include funsctions are related to processing arrays.
	Some are similar to existing NumPy functions, others offer some extended
	functionality. Still others give array solutions to unique problems.
    See the [documentation](https://www.nongnu.org/pyformex/doc-3.0/ref/arraytools.html#module-path).

  * varray: Defines the Varray class: a variable width 2D integer array.
    Varray provides an efficient way to store large 2D tables of integer
    values when the rows of the table may have different length.
    [documentation](https://www.nongnu.org/pyformex/doc-3.0/ref/varray.html#module-path)

## Version

  The first two components of the pyFormex Tools version are always the same as
  the corresponding pyFormex release version. A third component may be added
  to tag subsequent versions of this package.


## License

  pyFormex is licensed under the
  [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html)
  or later (GPLv3+) and so are these tools.
