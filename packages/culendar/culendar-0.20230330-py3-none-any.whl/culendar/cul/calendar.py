#! /usr/bin/env python3
# coding: utf-8
import icalendar
import datetime
from os import path, rename


########################################################################
# Event class
########################################################################

class Event:
    def __init__(self, date, duration, summary, place="", tag=0,
                 url=None, caldav=None, colour=None):
        self._date = date          # datetime.datetime()
        self._duration = duration  # seconds
        self._summary = summary.strip()   # text
        self._place = place.strip()       # text
        self._tag = tag
        self._colour = colour  # default colour is tag; useful for caldav
        self._samehour = 0     # number of simultaneous events
        self._hlines = None    # horizontal lines of event
        self._vlines = None    # vertical lines of event
        # CalDAV
        self._url = url
        self._caldav = caldav

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, d):
        self._date = d

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, d):
        self._duration = d

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, s):
        self._summary = s

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, p):
        self._place = p

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, t):
        self._tag = t

    @property
    def samehour(self):
        return self._samehour

    @samehour.setter
    def samehour(self, samehour):
        self._samehour = samehour

    @property
    def hlines(self):
        return self._hlines

    @hlines.setter
    def hlines(self, hlines):
        self._hlines = hlines

    @property
    def vlines(self):
        return self._vlines

    @vlines.setter
    def vlines(self, vlines):
        self._vlines = vlines

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def caldav(self):
        return self._caldav

    @caldav.setter
    def caldav(self, caldav):
        self._caldav = caldav

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    def compute_vlines(self, cul):
        start_hour = int(self.date.strftime('%H'))
        start_min = int(self.date.strftime('%M'))
        end_time = start_hour*3600 + start_min*60 + self.duration
        # if starting hour doesn't fit, make it fit
        if start_hour < cul.hmin:
            start_hour = cul.hmin
            start_min = 0
        if start_hour >= cul.hmax:
            start_hour = cul.hmax
            start_min = 0
        if end_time < start_hour*3600:
            end_time = start_hour*3600

        # don't overflow
        end_time = min(cul.hmax*3600, end_time)
        end_hour = end_time//3600
        end_min = (end_time - end_hour*3600)//60

        # time to lines
        # select the lines
        startline = start_hour - cul.hmin
        endline = end_hour - cul.hmin
        shline = cul.lines[1][startline] + 1  # 1st line after hour line
        ehline = cul.lines[1][endline] + 1    # same as start hour

        # lines to range of line
        if cul.hour_size == 1:
            # small terminals: starts on line event
            shline = shline-1
            ehline = ehline-1
            pass
        else:  # tall terminal, work between lines, deal with minutes
            minute_size = round(60 / (cul.hour_size-1))
            if cul.hour_size > 2:
                # change start line only for wide hours
                shline += start_min // minute_size
            if end_min == 0:
                ehline -= 1  # stops before hour line
            else:
                ehline += end_min // minute_size

            # special case out of schedule
            if start_hour == cul.hmax:
                shline -= 1
        # failproof
        if ehline <= shline:
            ehline = shline+1

        # finally define the range
        self.vlines = range(shline, ehline)

    def compute_hlines(self, cul, col, width, maxevents, table):
        start_vline = table[self.vlines[0]]
        e_width = width//maxevents
        left = 0
        while sum(start_vline[left:(left+e_width)]) != 0:
            left += 1  # width//maxevents

        # have we gone too far?
            if left+e_width > len(start_vline):
                # reduce event width
                e_width = len(start_vline)-left

        # first column picked from lines
        for v in self.vlines:
            for i in range(e_width):
                table[v][left+i] = 1

        # first column: right of vertical day line + offset of multievent
        first_col = cul.lines[0][col] + 1 + left

        # finally define the range
        self.hlines = range(first_col, first_col + e_width)

        # too many events or too small terminal
        if len(self.hlines) < 1:
            self.hlines = (cul.lines[0][col]+1, width)


########################################################################
# Agenda class
########################################################################

class Agenda:
    def __init__(self):
        self._events = []

    def add_event(self, e):
        self._events.append(e)

    def del_event(self, e):
        self._events.remove(e)

    @property
    def events(self):
        return self._events

    # sort by date and time
    def sort(self):
        maxdate = datetime.date(9999, 12, 31)
        self._events = sorted(self._events,
                              key=lambda e: e.date if e.date else maxdate)


########################################################################
# other related functions
########################################################################

def extract_day(cal, caldav, day):
    # create a list of subcals for each day of the week
    calday = Agenda()

    for e in cal.events + caldav.calweek.events:
        # if the right day, add the event
        if e.date.toordinal() == day.toordinal():
            calday.add_event(e)

    calday.sort()
    return(calday)


def extract_week(cal, caldav, day, cul, autosync=1):
    # create a list of subcals for each day of the week
    calweek = []
    for i in range(7):
        calweek.append(Agenda())

    # selects the events in caldavs, if required
    if autosync:
        caldav.sync()

    # first day of the current week; +1 for starting on monday in ordinal
    firstday = day.toordinal() - day.isoweekday() + 1

    for e in cal.events + caldav.events:
        diffday = e.date.toordinal() - firstday
        # if in the right week, we have
        if 0 <= diffday <= 6:
            calweek[diffday].add_event(e)

    for iday in range(cul.daynb):  # for all printed days
        calweek[iday].sort()
        for e in calweek[iday].events:
            # compute each vertical position for events
            e.compute_vlines(cul)

        # initialize no event on all lines
        nbevent = [0 for h in range(cul.ymax)]
        for e in calweek[iday].events:
            for i in e.vlines:
                nbevent[i] += 1
        maxevent = max(nbevent)

        # if last idayumn, the day size is not cul.day_size
        if iday == cul.daynb-1:
            width = cul.lines[0][-1] - cul.lines[0][-2] - 1
        else:
            width = cul.day_size - 1
        # day_size - 1: doesn't include vertical separating lines

        # table of position of events on day
        table = [[0 for d in range(width)] for y in range(cul.ymax)]
        for e in calweek[iday].events:
            maxevent = max([nbevent[i] for i in e.vlines])
            e.compute_hlines(cul, iday, width, maxevent, table)

    return calweek


def import_ical(filename, categories, default_tag=0):
    with open(filename, "r") as f:
        ical = icalendar.Calendar.from_ical(f.read())
    return Agenda2Cul(ical, categories, default_tag)


def Agenda2Cul(agenda, categories, default_tag, caldav=None):
    cal = Agenda()
    for ie in agenda.walk('vevent'):
        sdate = ie['dtstart'].dt
        try:  # is there an end date?
            edate = ie['dtend'].dt
            # if so, compute duration
            dur = (edate - sdate).seconds
        except:
            try:  # there is thus a duration
                dur = ie['duration'].dt.seconds
            except:  # no end date, no duration… Are you kidding me?
                dur = 0  # it exists, that's all
        try:  # is there a summary?
            summ = ie['summary'].lstrip().replace('\n', "-")
        except:  # if none, NULL summary
            summ = " "
        try:  # is there a location?
            place = ie['location'].lstrip().replace('\n', "-")
        except:  # if none, NULL summary
            place = ""
        try:  # is there a category?
            cat = ie['category']
            tag = default_tag
            if type(cat) == list:  # several categories in a single event
                for c in cat:
                    for t in range(1, 8):
                        if c.lstrip() in categories[t]:
                            # if category exists, tag it
                            tag = t
            else:  # single category
                for t in range(1, 8):
                    if cat.lstrip() in categories[t]:
                        # if category exists, tag it
                        tag = t
        except:  # no category
            tag = default_tag
        # special case for events without hour:
        # set 1st hour to 0:00 and duration to 24h
        if type(sdate) == datetime.date:
            sdate = datetime.datetime.combine(sdate, datetime.time(0))
            dur = 24*60*60
        # check the potential timezone and put to local
        if sdate.tzinfo:
            sdate = sdate.astimezone()
            sdate = sdate.replace(tzinfo=None)
        if caldav:
            e = Event(sdate, dur, summ, place, tag, caldav=caldav)
        else:
            e = Event(sdate, dur, summ, place, tag)
        cal.add_event(e)
    return cal


def event2icalevent(e, categories=None):
    ie = icalendar.Event()
    ie.add('dtstart', e.date)
    ie.add('duration', datetime.timedelta(seconds=e.duration))
    ie.add('summary', e.summary)
    if e.place:
        ie.add('location', e.place)
    if e.tag and type(e.tag) == int:
        if len(categories[e.tag]) > 1:
            ie.add('category', categories[e.tag][1])
        else:
            ie.add('category', e.tag)
    if e.url:
        ie.add('url', e.url)
    return ie


def export_ical(cal, filename, categories):
    ical = icalendar.Calendar()
    ical.add('prodid', '-//From Culendar')
    ical.add('version', '2.0')

    for e in cal.events:
        ie = event2icalevent(e, categories)
        ical.add_component(ie)

    with open(filename, "wb") as f:
        f.write(ical.to_ical())


def import_calcurse(filename, t=0):
    cal = Agenda()
    with open(filename) as f:
        for line in f:
            smon = int(line[0:2])
            sday = int(line[3:5])
            syea = int(line[6:10])
            shou = int(line[13:15])
            smin = int(line[16:18])
            emon = int(line[22:24])
            eday = int(line[25:27])
            eyea = int(line[28:32])
            ehou = int(line[35:37])
            emin = int(line[38:40])
            summ = line[42:-1]  # strips final \n
            sdate = datetime.datetime(syea, smon, sday, shou, smin)
            edate = datetime.datetime(eyea, emon, eday, ehou, emin)
            e = Event(sdate, (edate-sdate).seconds, summ, tag=t)
            cal.add_event(e)
    return cal


def export_calcurse(cal, filename):
    lines = ""
    for e in cal.events:
        line = str(e.date.strftime('%m/%d/%Y @ %H:%M'))
        line += " -> "
        enddate = e.date + datetime.timedelta(seconds=e.duration)
        line += str(enddate.strftime('%m/%d/%Y @ %H:%M'))
        line += " |"
        line += e.summary
        if e.place:
            line += "@"
            line += e.place
        line += "\n"
        lines += line
    with open(filename, "w") as f:
        f.write(lines)


def load(filename, todofilename):
    return load_apts(filename), load_todo(todofilename)


def load_apts(filename, caldav=None):
    cal = Agenda()
    with open(filename) as f:
        for line in f:
            syea = int(line[0:4])
            smon = int(line[5:7])
            sday = int(line[8:10])
            shou = int(line[13:15])
            smin = int(line[16:18])
            eyea = int(line[22:26])
            emon = int(line[27:29])
            eday = int(line[30:32])
            ehou = int(line[35:37])
            emin = int(line[38:40])
            rema = line[42:-1]  # strips final \n
            # search for a tag
            try:
                if "|" in rema:
                    tag = int(rema[rema.find("|")+1:])
                    rema = rema[:rema.find("|")]
                else:
                    tag = 0
            except:
                tag = 0
            # search for a location delimiter
            if "@" in rema:
                summ = rema[:rema.find("@")]
                place = rema[rema.find("@")+1:]
            else:
                summ = rema
                place = ""
            sdate = datetime.datetime(syea, smon, sday, shou, smin)
            edate = datetime.datetime(eyea, emon, eday, ehou, emin)
            e = Event(sdate, (edate-sdate).seconds, summ, place, tag,
                      caldav=caldav)
            cal.add_event(e)
    cal.sort()
    return cal


def load_todo(todofilename):
    # Todo list: ugly hack, use Agenda
    # Todo item: Event with no duration and optional date
    todo = Agenda()
    with open(todofilename) as f:
        for line in f:
            try:  # if there is a date
                syea = int(line[0:4])
                smon = int(line[5:7])
                sday = int(line[8:10])
                sdate = datetime.date(syea, smon, sday)
                rema = line[14:-1]  # strips final \n
            except:
                rema = line[:-1]  # strips final \n
                sdate = None
            try:
                # if no |, empty tag and rema doesn't change
                tag = int(rema[rema.find("|")+1:])
                summ = rema[:rema.find("|")]
            except:
                tag = 0
                summ = rema
            e = Event(sdate, None, summary=summ, tag=tag)
            todo.add_event(e)
    todo.sort()
    return todo


def cal2txt(cal, colour=None):
    lines = ""
    for e in cal.events:
        line = str(e.date.strftime('%Y/%m/%d @ %H:%M'))
        line += " -> "
        enddate = e.date + datetime.timedelta(seconds=e.duration)
        line += str(enddate.strftime('%Y/%m/%d @ %H:%M'))
        line += " |"
        line += e.summary
        if e.place:
            line += "@"
            line += e.place
        if colour:
            line += "|"
            line += str(colour)
        elif e.tag:
            line += "|"
            line += str(e.tag)
        line += "\n"
        lines += line
    return lines


def todo2txt(todo):
    lines = ""
    for e in todo.events:
        if e.date:
            line = str(e.date.strftime('%Y/%m/%d'))
            line += " -> "
        else:
            line = ""
        line += e.summary
        if e.tag:
            line += "|"
            line += str(e.tag)
        line += "\n"
        lines += line
    return lines


def save(cal, todo, conf, caldav=None):
    # main Agenda
    # backup current one
    if path.exists(conf.datafile):
        rename(conf.datafile, conf.datafile+'.old')
    with open(conf.datafile, "w") as f:
        f.write(cal2txt(cal))

    # Todo file
    # backup current one
    if path.exists(conf.todofile):
        rename(conf.todofile, conf.todofile+'.old')

    with open(conf.todofile, "w") as f:
        f.write(todo2txt(todo))

    if caldav:
        save_caldav(conf, caldav)


def save_caldav(conf, caldav):
    # Caldav local saves - no backup, it's online
    for cdav_idx, cdav in enumerate(caldav._list):
        if caldav._icals[cdav_idx]:  # is there anything to save
            url = cdav["url"]
            suffix = url.replace("/", "-") + cdav["username"]
            fname = "apts." + suffix
            with open(conf._datapath+"/"+fname, "w") as f:
                f.write(cal2txt(caldav._cals[cdav_idx], cdav["colour"]))


def load_local_caldav(url, username, fpath, check=False):
    suffix = url.replace("/", "-") + username
    filename = fpath + "/" + "apts." + suffix
    if path.exists(filename):
        if check:  # just check existence
            return True
        else:
            return load_apts(filename, caldav="webcal")
    else:  # no local copy exists
        return None
