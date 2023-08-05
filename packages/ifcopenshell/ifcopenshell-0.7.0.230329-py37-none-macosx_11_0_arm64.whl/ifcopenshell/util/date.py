# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from re import findall
from dateutil import parser

try:
    import isodate
except:
    pass  # Duration parsing not supported


def timedelta2duration(timedelta):
    components = {
        "days": getattr(timedelta, "days", 0),
        "hours": 0,
        "minutes": 0,
        "seconds": getattr(timedelta, "seconds", 0),
    }
    if components["seconds"]:
        components["hours"], components["minutes"], components["seconds"] = [
            int(i) for i in str(datetime.timedelta(seconds=components["seconds"])).split(":")
        ]
    return isodate.Duration(**components)


def ifc2datetime(element):
    if isinstance(element, str) and "P" in element[0:2]:  # IfcDuration
        duration = isodate.parse_duration(element)
        if isinstance(duration, datetime.timedelta):
            return timedelta2duration(duration)
        return duration
    elif isinstance(element, str) and len(element) > 3 and element[2] == ":":  # IfcTime
        return datetime.time.fromisoformat(element)
    elif isinstance(element, str) and ":" in element:  # IfcDateTime
        return datetime.datetime.fromisoformat(element)
    elif isinstance(element, str):  # IfcDate
        return datetime.date.fromisoformat(element)
    elif isinstance(element, int):  # IfcTimeStamp
        return datetime.datetime.fromtimestamp(element)
    elif element.is_a("IfcDateAndTime"):
        return datetime.datetime(
            element.DateComponent.YearComponent,
            element.DateComponent.MonthComponent,
            element.DateComponent.DayComponent,
            element.TimeComponent.HourComponent,
            element.TimeComponent.MinuteComponent,
            int(element.TimeComponent.SecondComponent),
            # TODO: implement TimeComponent timezone
        )
    elif element.is_a("IfcCalendarDate"):
        return datetime.date(
            element.YearComponent,
            element.MonthComponent,
            element.DayComponent,
        )


def datetime2ifc(dt, ifc_type):
    if isinstance(dt, str):
        if ifc_type == "IfcDuration":
            return dt
        try:
            dt = datetime.datetime.fromisoformat(dt)
        except:
            dt = datetime.time.fromisoformat(dt)

    if ifc_type == "IfcDuration":
        return isodate.duration_isoformat(dt)
    elif ifc_type == "IfcTimeStamp":
        return int(dt.timestamp())
    elif ifc_type == "IfcDateTime":
        if isinstance(dt, datetime.datetime):
            return dt.isoformat()
        elif isinstance(dt, datetime.date):
            return datetime.datetime.combine(dt, datetime.datetime.min.time()).isoformat()
    elif ifc_type == "IfcDate":
        if isinstance(dt, datetime.datetime):
            return dt.date().isoformat()
        elif isinstance(dt, datetime.date):
            return dt.isoformat()
    elif ifc_type == "IfcTime":
        if isinstance(dt, datetime.datetime):
            return dt.time().isoformat()
        elif isinstance(dt, datetime.time):
            return dt.isoformat()
    elif ifc_type == "IfcCalendarDate":
        return {"DayComponent": dt.day, "MonthComponent": dt.month, "YearComponent": dt.year}
    elif ifc_type == "IfcLocalTime":
        # TODO implement timezones
        return {"HourComponent": dt.hour, "MinuteComponent": dt.minute, "SecondComponent": dt.second}

def string_to_date(string):
    if not string:
        return None
    try:
        return parser.isoparse(string)
    except:
        try:
            return parser.parse(string, dayfirst=True, fuzzy=True)
        except:
            return None

def string_to_duration(duration_string):
    # TODO support years, months, weeks aswell
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    match = findall(r"(\d+\.?\d*)d", duration_string)
    if match:
        days = float(match[0])
    match = findall(r"(\d+\.?\d*)h", duration_string)
    if match:
        hours = float(match[0])
    match = findall(r"(\d+\.?\d*)m", duration_string)
    if match:
        minutes = float(match[0])
    match = findall(r"(\d+\.?\d*)s", duration_string)
    if match:
        seconds = float(match[0])
    return isodate.duration_isoformat(datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))