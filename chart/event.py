# -*- coding: utf-8 -*-

import datetime

class DateTime:
    """Date and time of the event used for chart calculation."""

    # Calendar type.
    GREGORIAN = 0
    JULIAN = 1
    # times
    ZONE = 0
    GREENWICH = 1
    LOCALMEAN = 2
    LOCALAPPARENT = 3
    HOURSPERDAY = 24.0

    # zt is zonetime, zh is zonehour, zm is zoneminute, full means to
    # calculate everything e.g. FixedStars, MidPoints, ...
    def __init__(
            self, year, month, day, hour, minute, second, bc, cal, zone_time,
            plus, zone_hour, zone_minute, daylightsaving, place, full=True):
        self.year = year
        self.month = month
        self.day = day
        self.origyear = year
        self.origmonth = month
        self.origday = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.bc = bc
        self.cal = cal
        self.zt = zone_time
        self.plus = plus
        self.zh = zone_hour
        self.zm = zone_minute
        self.daylightsaving = daylightsaving
        self.ph = None

        # Represent date / time as datetime object.
        timezone = self.create_timezone(zone_hour, zone_minute)
        self.date = self.create_datetime(
            year, month, day, hour, minute, second, timezone, daylightsaving)
        self.jd = self.convert_to_julian(self.date)

        if full:
            self.calcPHs(place)


    def create_datetime(
            self, year: int, month: int, day: int, hour: int, minute: int,
            second: int, timezone: datetime.timezone, daylightsaving: bool):
        """
        Create a datetime object.

        :param year: Date year.
        :type year: int
        :param month: Date month.
        :type month: int
        :param day: Date day.
        :type day: int
        :param hour: Time hour.
        :type hour: int
        :param minute: Time minutes.
        :type minute: int
        :param second: Time seconds.
        :type second: int
        :param timezone: Timezone of the time, will transform to UTC.
        :type timezone: datetime.timezone
        :param daylightsaving: Flag to indicate time has daylight saving.
        :type daylightsaving: bool
        """

        date = datetime.datetime(
            year, month, day, hour, minute, second, 0, timezone)

        # Apply daylight balance when applies.
        if daylightsaving:
            date = date + datetime.timedelta(hours=-1)

        return date


    def create_timezone(self, zone_hour: int, zone_minute: int):
        """
        Create datetime timezone object.

        :param zone_hour: Timezone hour.
        :type zone_hour: int
        :param zone_minute: Timezone minute.
        :type zone_minute: int
        :return: Datetime timezone object.
        :rtype: datetime.timezone
        """

        timezone_hours = zone_hour + (zone_minute / 60)
        timezone_delta = datetime.timedelta(hours=timezone_hours)
        timezone = datetime.timezone(timezone_delta)
        return timezone

    def convert_to_julian(self, date: datetime):
        """
        Convert date from Gregorian to Julian calendar.

        :param date: Date represented as datetime object.
        :type date: datetime
        :param daylightsaving: Flag if hour needs day light saving adjust.
        :rtype: int
        """

        # Transform to UTC timezone.
        date = date.astimezone(pytz.timezone('UTC'))
        # Aggregate hours, mins, secs as required by swisseph.
        aggregate_time = date.hour + (date.minute/60.0) + (date.second/3600.0)
        self.time = aggregate_time
        # Set calendar type to use based on time options.
        calflag = astrology.SE_GREG_CAL

        # Convert date to Julian Day.
        julian_date = swisseph.julday(
            date.year,
            date.month,
            date.day,
            aggregate_time,
            calflag)

        return julian_date


    def calcPHs(self, place):
        # Planetary day/hour calculation
        self.weekday = self.date.weekday()
        lon = place.deglon+place.minlon/60.0
        if not place.east:
            lon *= -1
        lat = place.deglat+place.minlat/60.0
        if not place.north:
            lat *= -1

        self.ph = hours.PlanetaryHours(
            lon, lat, place.altitude, self.weekday, self.jd)


