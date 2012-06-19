Script to generate a pretty parliament seat allocation diagram.

Original version from http://drichfld.freeshell.org/arch.py (live version: http://drichfld.freeshell.org/perlcgi/arch.cgi)

Info: https://en.wikipedia.org/wiki/User_talk:Slashme/parliament.py

License: GPLv3

Example usage
----

    import parliament as P
    P.display(P.render_svg([
        ['I-D', 2],
        ['D', 51],
        ['R', 47],
    ]))
