#! /usr/bin/env python3
# coding: utf-8
import caldav
import datetime
import icalendar
from . import calendar, getkey
from urllib import request


class Cdav:
    def __init__(self, caldav_dict, screen, conf):
        self._list = caldav_dict
        self._conf = conf
        self._icals = []        # list of Icalendar, for each caldav
                                # proper url if webcal; None if offline
        self._iscaldav = []     # list of True/False
        self._tags = []         # associated tags
        self._cal = []          # single list of all events in Agenda class
        self._cals = []         # list of event lists, by caldav
        self._screen = screen   # to give feedbacks in UI
        self._ymax, self._xmax = self._screen.getmaxyx()
        self.initialize()       # get cals and associated tags
        self.sync()             # update and redefine _events

    @property
    def icals(self):
        return self._icals

    @property
    def events(self):
        return self._cal.events

    def resize(self):
        self._ymax, self._xmax = self._screen.getmaxyx()

    def initialize(self):
        for cdav_idx, cdav in enumerate(self._list):
            self.initialize_single(cdav, cdav_idx)

    def initialize_single(self, cdav, cdav_idx):
        try:
            if "@" in cdav["url"]:  # there is a password in the url
                head_user_password, tail = cdav["url"].split("@")
                head, user_password = head_user_password.split("://")
                user = user_password.split(":")[0]
                url = head+"://"+user+":"+"*****"+"@"+tail
            else:
                url = cdav["url"]
            msg = _("Loading caldav ")+str(cdav_idx+1)+_(": ")+url
            self.inform(msg)

            if cdav["url"][:4] == "http":  # caldav
                flag = True  # it's a proper caldav
                client = self.get_client(cdav)
                principal = self.get_principal(client)
                self.add_calendar(principal)
            if cdav["url"][:6] == "webcal":  # webcal
                flag = False  # it's a webcal
                if cdav["url"][:7] == "webcals":  # webcal
                    urlh = "https" + cdav["url"][7:]
                else:
                    urlh = "http" + cdav["url"][6:]
                cal = read_webcal_url(urlh)
                self._icals.append(urlh)
            self._iscaldav.append(flag)
        except:
            self.resize()  # if screen sized changed during loading
            err = _("Error: can't contact caldav ")+cdav["url"]
            if calendar.load_local_caldav(cdav["url"], cdav["username"],
                                          self._conf._datapath, check=True):
                err += _(" -- using offline copy")
            err += _(" -- press any key to continue")
            self.inform(err)
            # append None to keep same size as _list
            self._icals.append(None)
            self._iscaldav.append(False)
            # pause; resize if necessary
            if getkey.getkey(self._screen) == "KEY_RESIZE":
                self.draw_conf_screen()
        self.add_tag(cdav)

    def get_client(self, cdav):
        if len(cdav["username"]) != 0:
            client = caldav.DAVClient(cdav["url"],
                                      username=cdav["username"],
                                      password=cdav["password"])
        else:
            client = caldav.DAVClient(cdav["url"])
        return client

    def get_principal(self, client):
        return client.principal()

    def add_calendar(self, principal):
        if len(principal.calendars()) == 0:
            cal = principal.make_calendar()
            # useful for my poor test of python-radicale
        else:
            # TODO: when several calendars, what to do?
            cal = principal.calendars()[0]
        self._icals.append(cal)

    def add_tag(self, cdav):
        if cdav:
            self._tags.append(cdav["tag"])
        else:
            self._tags.append(None)

    def sync(self):
        # extracts all the events of the the ICalendar
        # set all events in a single culendar/Agenda class
        self.inform(_("Synchronising caldavs…"))
        # resets the differents cals
        self._cals = []
        for ind, cal in enumerate(self._icals):
            tmpcal = calendar.Agenda()
            if self._iscaldav[ind]:
                ical = cal.events()
                for e in ical:  # a list of ical events, each one in a calendar
                    agenda = icalendar.Calendar()
                    agenda = agenda.from_ical(e.data)
                    agendacul = calendar.Agenda2Cul(agenda, [],
                                                    self._tags[ind],
                                                    cal)
                    ecul = agendacul.events[0]  # a single event
                    ecul.url = e.canonical_url
                    ecul.colour = self._list[ind]["colour"]
                    tmpcal.add_event(ecul)
            else:
                try:
                    # if unreachable, cal was None and thus, error
                    cal = read_webcal_url(cal)
                except:
                    pass
                # reached and a webcal
                if cal and cal[:15] == "BEGIN:VCALENDAR":
                    # in a webcal, _icals is url
                    # in a webcal, we get everything.
                    ical = icalendar.Calendar.from_ical(cal)
                    agendacul = calendar.Agenda2Cul(ical, [],
                                                    self._tags[ind],
                                                    "webcal")
                    for e in agendacul.events:
                        e.colour = self._list[ind]["colour"]
                        tmpcal.add_event(e)
                else:  # unreachable, use offline copy if any
                    url = self._list[ind]["url"]
                    username = self._list[ind]["username"]
                    tmpcal = calendar.load_local_caldav(url, username,
                                                        self._conf._datapath)
                    if cal:  # we got something, but not a wecal
                        warn = _("Warning: contacting ")
                        if len(url) > 20:
                            warn += url[:20] + "[…]"
                        else:
                            warn += url
                        warn += _(" gave a ")
                        warn += cal[:23]
                        warn += _(" -- using offline copy")
                        warn += _(" -- press any key to continue")
                        self.inform(warn)
                        if getkey.getkey(self._screen) == "KEY_RESIZE":
                            self.draw_conf_screen()
            if tmpcal:  # avoid None from loading offline apts
                tmpcal.sort()  # sort for better offline text copy
                self._cals.append(tmpcal)
        self._cal = calendar.Agenda()
        for cal in self._cals:
            for e in cal.events:
                self._cal.add_event(e)

        calendar.save_caldav(self._conf, self)  # local save

    def inform(self, msg):
        # clear footer
        self._screen.hline(self._ymax-1, 0, " ", self._xmax)
        self._screen.addstr(self._ymax-1, 0, msg[0:self._xmax-1])
        self._screen.refresh()

    def del_caldav(self, list_idx):
        # _list already removed in confscreen
        # clean what is required:
        # from highest position to lowest to pop easily
        list_idx.sort(reverse=True)
        for idx in list_idx:
            del_tag = self._tags.pop(idx)
            self._icals.pop(idx)
            self._iscaldav.pop(idx)

    def update(self, oldconf):
        list_idx = []
        for idx, conf in enumerate(oldconf):
            if conf not in self._list:
                list_idx.append(idx)
        if list_idx:
            self.del_caldav(list_idx)
        idx = 0
        for conf in self._list:
            if conf not in oldconf:
                self.initialize_single(conf, idx)
                idx += 1
        self.sync()


def del_event(event):
    event.caldav.event_by_url(event.url).delete()


def add_event(event, cdav):
    event.caldav = cdav
    ical = icalendar.Calendar()
    icalevent = calendar.event2icalevent(event)
    # caldav reguires a UID
    icalevent.add("uid", hash(datetime.datetime.now()))
    ical.add_component(icalevent)
    tmpevent = cdav.add_event(ical.to_ical().decode())
    event.url = tmpevent.canonical_url


def read_webcal_url(url):
    if "@" not in url:  # no password
        return request.urlopen(url).read().decode()
    else:
        # keep between http[s] *://* user:pwd *@* url
        user_and_password = url.split("@")[0].split("://")[1]
        user = user_and_password.split(":")[0]
        # if there are ":" in the password, join them again
        password = ":".join(user_and_password.split(":")[1:])
        # remove login and password from url
        url_clean = "".join(url.split(user+":"+password+"@"))

        # create a password manager and an opener
        pwd_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        pwd_mgr.add_password(None, url_clean, user, password)
        handler = request.HTTPBasicAuthHandler(pwd_mgr)
        opener = request.build_opener(handler)

        # finally read and decode the data
        return opener.open(url_clean).read().decode()
