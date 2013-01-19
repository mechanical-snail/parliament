Script to generate a pretty parliament seat allocation diagram.

Original version written by [David Richfield (“Slashme”)](https://en.wikipedia.org/wiki/User:Slashme). Obtained from his website at http://drichfld.freeshell.org/arch.py (live version: http://drichfld.freeshell.org/perlcgi/arch.cgi).

Info: https://en.wikipedia.org/wiki/User_talk:Slashme/parliament.py

License: GPLv3

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
> 
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
> 
> For the text of the GNU General Public License, please see http://www.gnu.org/licenses/.


Example usage
----

    import parliament as P
    P.display(P.render_svg([
        ['I-D', 2],
        ['D', 51],
        ['R', 47],
    ]))
