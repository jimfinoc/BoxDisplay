import sys
import subprocess
import commands

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186

def printColor(text, colour=WHITE):
    has_colours = True
    if not hasattr(sys.stdout, "isatty"):
        has_colours = False
    if not sys.stdout.isatty():
        has_colours = False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        has_colours = ( curses.tigetnum("colors") > 2 )
    except:
        # guess false in case of error
        has_colours = False
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m\n"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)