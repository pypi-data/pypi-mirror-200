#! /usr/bin/env python3
# coding: utf-8
import curses
import datetime
import icalendar
import sys
from .cul import config, culendar, calendar, helpscr, confscr, culdav, getkey
from .cul import mouse


def main(stdscr):
    # configialize ncurses and get conf
    conf = config.Config()

    # the current day
    day = datetime.date.today()
    if (day.isoweekday() in [6, 7]) & (conf.WE == 0):
        # if we are during an unshown day, go to the next Monday
        while day.isoweekday() in [6, 7]:
            day = datetime.date.fromordinal(day.toordinal() + 1)

    # get data and todo and caldavs urls
    cal, todo = calendar.load(conf.datafile, conf.todofile)
    cdav = culdav.Cdav(conf.caldav, stdscr, conf)

    # include first drawing
    cul = culendar.Culendar(stdscr, conf, day, cal, cdav, todo)

    # main loop
    key = ""
    while not(key in conf.keys['quit']):
        key = getkey.getkey(cul.screen, conf.debug)

        if key == 'KEY_RESIZE':
            cul.update()

        # repeat action at least 1, or the entered count value
        repetitions = max(1, cul.count)
        # changing day or week or year
        if key in conf.keys['prevday']:
            cul.addday(-repetitions)
        if key in conf.keys['nextday']:
            cul.addday(+repetitions)
        if key in conf.keys['nextweek']:
            cul.addday(+7*repetitions)
        if key in conf.keys['prevweek']:
            cul.addday(-7*repetitions)
        if key in conf.keys['nextmonth']:
            cul.addmonth(+repetitions)
        if key in conf.keys['prevmonth']:
            cul.addmonth(-repetitions)
        if key in conf.keys['nextyear']:
            cul.addyear(+repetitions)
        if key in conf.keys['prevyear']:
            cul.addyear(-repetitions)
        if key in conf.keys['today']:
            cul.changeday(day=datetime.date.today())
        if key in conf.keys['setday']:
            cul.changeday()
        if key in conf.keys['startweek']:
            cul.addday(-cul.day.isoweekday()+1)
        if key in conf.keys['endweek']:
            cul.addday(-cul.day.isoweekday()+cul.daynb)

        # change highlighted event of current day
        if key in conf.keys['nextevent']:
            cul.sameday()
            cul.changehl(+repetitions)
            cul.draw_hl()
        if key in conf.keys['prevevent']:
            cul.sameday()
            cul.changehl(-repetitions)
            cul.draw_hl()

        # delete, edit, add (highlighted) event (if existing)
        if key in conf.keys['delevent']:
            cul.del_event()
        if key in conf.keys['editevent']:
            cul.edit_event()
        if key in conf.keys['addevent']:
            cul.add_event()
        if key in conf.keys['tagevent']:
            cul.tag_event()
        if key in conf.keys['copyevent']:
            cul.copy_event(repetitions)
        if key in conf.keys['minusshifthour']:
            cul.shift_event(-repetitions)
        if key in conf.keys['minusshiftday']:
            cul.shift_event(-repetitions*24)
        if key in conf.keys['shifthour']:
            cul.shift_event(+repetitions)
        if key in conf.keys['shiftday']:
            cul.shift_event(+repetitions*24)

        # toggle week-end display
        if key in conf.keys['toggleWE']:
            cul.toggle_WE()

        # toggle Todo bar focus (appear/disappear)
        if key in conf.keys['toggletodo']:
            cul.toggle_TODO()

        if key in conf.keys['redraw']:
            cul.clear_cal()
            cul.draw_cal()
        if key in conf.keys['sync']:
            cul.sync_caldav()

        if key in conf.keys['help']:
            H = helpscr.Help(cul.screen, cul.conf)
            H.help_screen()
            # redraw, works even in case of KEY_RESIZE inside help
            cul.update()
        if key in conf.keys['save']:
            cul.inform(_("Saving configuration and calendar…"))
            conf.save()
            cul.save()
            cul.inform(_("Configuration and calendar saved!"))
        if key in conf.keys['setconfig']:
            C = confscr.Conf(cul.screen, cul.conf, cul.caldav)
            # real copy to keep a backup
            old_caldav_conf = [conf for conf in cul.conf._caldav]
            # conf_screen returns a possibly modified conf
            cul.conf = C.conf_screen()
            if old_caldav_conf != cul.conf._caldav:
                cul.caldav.update(old_caldav_conf)
            # redraw, works even in case of KEY_RESIZE inside help
            cul.update()
        if key in conf.keys['import']:
            cul.importcal()
        if key in conf.keys['export']:
            cul.exportcal()
        if key == "KEY_MOUSE":
            mouse.clicked(cul)

        # define the buffer and the repetition of actions
        try:  # is the key an integer?
            # type 1 then 2, get 12
            cul.count = cul.count*10 + int(key)
        except:  # not a number, back to zero
            cul.count = 0

    # autosave on quit
    if conf.autosave:
        cul.save()
        conf.save()


# here starts culendar!
def run():
    # TODO: parse arguments
    curses.wrapper(main)


if __name__ == "__main__":
    run()
