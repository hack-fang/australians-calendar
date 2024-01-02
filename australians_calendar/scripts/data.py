# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime

import australians_calendar

constants_template = """# -*- coding: utf-8 -*-
# this file is generated by australians_calendar.scripts.generate_constants
from __future__ import absolute_import, unicode_literals

import datetime
from enum import Enum


class Holiday(Enum):
    def __new__(cls, english, chinese, days):
        obj = object.__new__(cls)
        obj._value_ = english

        obj.chinese = chinese
        obj.days = days
        return obj

    new_years_day = "New Year's Day", "元旦", 1
    australia_day = "Australia Day","澳大利亚国庆日",1
    good_friday = "Good Friday","耶稣受难日",1
    easter_saturday = "Easter Saturday","耶稣受难日翌日",1
    easter_sunday = "Easter Sunday","复活节星期日",1
    easter_monday = "Easter Monday","复活节星期一",1
    anzac_day = "Anzac Day","澳新军团日",1
    kings_birthday = "King's Birthday","国王诞辰日",1
    labour_day = "Labour Day","劳动节",1
    christmas_day = "Christmas Day","圣诞节",1
    boxing_day = "Boxing Day","节礼日",1
    

holidays = {}

workdays = {}

in_lieu_days = {}
"""


class Arrangement(object):
    WORKDAY = 1
    HOLIDAY = 2
    IN_LIEU = 3

    def __init__(self):
        self.holidays = {}
        self.workdays = {}
        self.in_lieu_days = {}

        self.year = None
        self.month = None
        self.day = None
        self.holiday = None
        self.day_type = None

        for method in dir(self):
            try:
                int(method[1:])
                getattr(self, method)()
            except ValueError:
                pass

    # fmt: off
    def _2024(self):
        """ https://holidays-calendar.net/calendar_zh_cn/japan_zh_cn.html
        1 月 1 日（周一）：元旦
        1 月 26 日（周五）：澳大利亚国庆日
        3 月 29 日（周五）：耶稣受难日
        3 月 30 日（周六）：复活节星期六
        3 月 31 日（周日）：复活节星期日
        4 月 1 日（周一）：复活节星期一
        4 月 25 日（周二）：澳新军团日
        6 月 10 日（周一）：国王诞辰日
        10 月 7 日（周一）：劳动节
        12 月 25 日（周三）：圣诞节
        12 月 26 日（周四）：节礼日
        """
        self.year_at(2024) \
            .new_year().rest(1, 1) \
            .australia_day().rest(1, 26) \
            .good_friday().rest(3, 29) \
            .easter_saturday().rest(3, 30) \
            .easter_sunday().rest(3,31) \
            .easter_monday().rest(4,1) \
            .anzac_day().rest(4,25) \
            .kings_birthday().rest(6,12) \
            .labour_day().rest(10,7) \
            .christmas_day().rest(12,25) \
            .boxing_day().rest(12,26)

    def _2023(self):
        """ https://www.australia.cn/zh-cn/facts-and-planning/when-to-go/australian-public-holidays.html
        1 月 1 日（周日）：元旦
        1 月 2 日（周一）：元旦传统假期
        1 月 26 日（周四）：澳大利亚国庆日
        4 月 7 日（周五）：耶稣受难日
        4 月 8 日（周六）：耶稣受难日翌日
        4 月 9 日（周日）：复活节星期日
        4 月 10 日（周一）：复活节星期一
        4 月 25 日（周二）：澳新军团日
        6 月 12 日（周一）：国王诞辰日 (新南威尔士)
        10 月 2 日（周一）：劳动节 (新南威尔士)
        12 月 25 日（周一）：圣诞节
        12 月 26 日（周二）：节礼日
        """
        self.year_at(2023) \
            .new_year().rest(1, 1).to(1, 2) \
            .australia_day().rest(1, 26) \
            .good_friday().rest(4, 7) \
            .easter_saturday().rest(4, 8) \
            .easter_sunday().rest(4,9) \
            .easter_monday().rest(4,10) \
            .anzac_day().rest(4,25) \
            .kings_birthday().rest(6,12)\
            .labour_day().rest(10,2) \
            .christmas_day().rest(12,25) \
            .boxing_day().rest(12,26)

    def year_at(self, number):
        self.year = number
        return self

    def new_year(self):
        """元旦 New Year's Day"""
        return self.mark(australians_calendar.Holiday.new_years_day)

    def australia_day(self):
        """澳大利亚国庆日 Australia Day"""
        return self.mark(australians_calendar.Holiday.australia_day)

    def good_friday(self):
        """耶稣受难日 Good Friday"""
        return self.mark(australians_calendar.Holiday.good_friday)

    def easter_saturday(self):
        """耶稣受难日翌日 Easter Saturday"""
        return self.mark(australians_calendar.Holiday.easter_saturday)

    def easter_sunday(self):
        """复活节星期日 Easter Sunday"""
        return self.mark(australians_calendar.Holiday.easter_sunday)

    def easter_monday(self):
        """复活节星期一 Easter Monday"""
        return self.mark(australians_calendar.Holiday.easter_monday)

    def anzac_day(self):
        """澳新军团日 Anzac Day"""
        return self.mark(australians_calendar.Holiday.anzac_day)

    def kings_birthday(self):
        """国王诞辰日  King's Birthday"""
        return self.mark(australians_calendar.Holiday.kings_birthday)

    def labour_day(self):
        """劳动节 Labour Day"""
        return self.mark(australians_calendar.Holiday.labour_day)

    def christmas_day(self):
        """圣诞节 Christmas Day"""
        return self.mark(australians_calendar.Holiday.christmas_day)

    def boxing_day(self):
        """节礼日 Boxing Day"""
        return self.mark(australians_calendar.Holiday.boxing_day)

    def mark(self, holiday):
        self.holiday = holiday
        return self

    def work(self, month, day):
        return self.save(month, day, self.WORKDAY)

    def rest(self, month, day):
        return self.save(month, day, self.HOLIDAY)

    def in_lieu(self, month, day):
        """调休 in lieu"""
        return self.save(month, day, self.IN_LIEU)

    def save(self, month, day, day_type):
        if not self.year:
            raise ValueError("should set year before saving holiday")
        if not self.holiday:
            raise ValueError("should set holiday before saving holiday")
        self.day_type = day_type
        self.days[datetime.date(year=self.year, month=month, day=day)] = self.holiday
        self.month = month
        self.day = day
        return self

    def to(self, month, day):
        if not (self.year and self.month and self.day):
            raise ValueError("should set year/month/day before saving holiday range")
        start_date = datetime.date(year=self.year, month=self.month, day=self.day)
        end_date = datetime.date(year=self.year, month=month, day=day)
        if end_date <= start_date:
            raise ValueError("end date should be after start date")
        for i in range((end_date - start_date).days):
            the_date = start_date + datetime.timedelta(days=i + 1)
            self.days[the_date] = self.holiday
        return self

    @property
    def days(self):
        mapping = {self.HOLIDAY: self.holidays, self.IN_LIEU: self.in_lieu_days, self.WORKDAY: self.workdays}
        return mapping[self.day_type]