#! /usr/bin/env python3
# coding: utf-8
import curses

# function to deal properly with all kind of typed key
# get_wch() returns a str for standard keys;
# for functions keys, sometimes string names, sometimes escaped sequences,
# sometimes ordinal integers.
# stupid function that translates different possibilities into strings
# for the fun, it's terminal-dependant

# roughly tested with urvxt, screen, xterm terminals
# probably doesn't work with yours


def getkey(stdscr, debug=False):
    key = stdscr.get_wch()
    origkey = key
    if key == "":
        # half delay mode of 1/10s: no input key raises an error
        # assumption: no humain being type ESC + real keys so fast
        curses.halfdelay(1)
        try:
            # get the false keys and stack it
            while 1:
                key += str(stdscr.get_wch())
        except:
            # the bundle of special keys stopped:
            # back to normal mode
            curses.cbreak()
            origkey = key
            if key in ["[b", "[1;2B"]:
                key = "kDN"  # shift down
            elif key in ["[a", "[1;2A"]:
                key = "kUP"  # shift right
            elif key in ["[d", "[1;2D"]:
                key = "KEY_SLEFT"
            elif key in ["[c", "[1;2C"]:
                key = "KEY_SRIGHT"
            # non curses character: control+key
            elif key in ["Ob", "[1;5B"]:
                key = "KEY_CDOWN"
            elif key in ["Oa", "[1;5A"]:
                key = "KEY_CUP"
            elif key in ["Od", "[1;5D"]:
                key = "KEY_CLEFT"
            elif key in ["Oc", "[1;5C"]:
                key = "KEY_CRIGHT"
            elif key in ["OP"]:
                key = "KEY_F(1)"
            elif key in ["OQ"]:
                key = "KEY_F(2)"
            elif key in ["OR"]:
                key = "KEY_F(3)"
            elif key in ["OS"]:
                key = "KEY_F(4)"
            elif key in ["[1~", "OH", "[H"]:
                key = "KEY_HOME"
            elif key in ["[4~", "OF", "[F"]:
                key = "KEY_END"
            else:
                if not debug and len(key) > 1:
                    key = ""

    if type(key) == int:
        if key in [410]:
            key = "KEY_RESIZE"
        elif key in [258]:
            key = "KEY_DOWN"
        elif key in [259]:
            key = "KEY_UP"
        elif key in [260]:
            key = "KEY_LEFT"
        elif key in [261]:
            key = "KEY_RIGHT"
        elif key in [262, 362]:
            key = "KEY_HOME"
        elif key in [360, 385]:
            key = "KEY_END"
        elif key in [263]:
            key = "KEY_BACKSPACE"
        elif key in [265]:
            key = "KEY_F(1)"
        elif key in [266]:
            key = "KEY_F(2)"
        elif key in [267]:
            key = "KEY_F(3)"
        elif key in [268]:
            key = "KEY_F(4)"
        elif key in [269]:
            key = "KEY_F(5)"
        elif key in [270]:
            key = "KEY_F(6)"
        elif key in [271]:
            key = "KEY_F(7)"
        elif key in [272]:
            key = "KEY_F(8)"
        elif key in [273]:
            key = "KEY_F(9)"
        elif key in [274]:
            key = "KEY_F(10)"
        elif key in [275]:
            key = "KEY_F(11)"
        elif key in [276]:
            key = "KEY_F(12)"
        elif key in [330]:
            key = "KEY_DC"
        elif key in [331]:
            key = "KEY_IC"
        elif key in [338]:
            key = "KEY_NPAGE"
        elif key in [339]:
            key = "KEY_PPAGE"
        elif key in [353]:
            key = "KEY_BTAB"
        elif key in [513, 336]:
            key = "kDN"
        elif key in [529, 337]:
            key = "kUP"
        elif key in [393]:
            key = "KEY_SLEFT"
        elif key in [402]:
            key = "KEY_SRIGHT"
        # non curses character: control+key
        elif key in [514, 525]:
            key = "KEY_CDOWN"
        elif key in [530, 566]:
            key = "KEY_CUP"
        elif key in [523, 545]:
            key = "KEY_CLEFT"
        elif key in [528, 560]:
            key = "KEY_CRIGHT"
        elif key in [409]:
            key = "KEY_MOUSE"
        else:
            if not debug:
                key = ""
            else:
                key = str(key)
    return key

## comment previous line and uncomment the followings to use the standalone
#    if debug:
#        return key, origkey
#    else:
#        return key
#
## standalone function
## useful to complete the lists
##import curses
#def main(stdscr):
#    curses.noecho()
#    mmask = (curses.BUTTON1_PRESSED + curses.BUTTON1_RELEASED
#             + curses.BUTTON1_CLICKED + curses.BUTTON1_DOUBLE_CLICKED
#             + curses.BUTTON1_TRIPLE_CLICKED + curses.BUTTON_CTRL)
#    curses.mousemask(mmask)
#
#    ymax, xmax = stdscr.getmaxyx()
#    k = ""
#    i = 0
#    while k != "q":
#        k, ok = getkey(stdscr, debug=True)
#        stdscr.addstr(i%ymax, 0, "                       ")
#        stdscr.addstr(i%ymax, 0, str(k))
#        stdscr.addstr(i%ymax, 15, str(ok))
#        i += 1
#curses.wrapper(main)
