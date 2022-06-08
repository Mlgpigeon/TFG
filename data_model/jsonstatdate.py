import datetime



class JsonStatDate:
    """
    Class to represent a date in JSONStat format.
    """
    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return self.to_string()

    def to_string(self):
        """
        Return a string representation of the date.
        """
        if self.year is None:
            return ""
        else:
            if self.month is None:
                return str(self.year)
            else:
                if self.day is None:
                    return str(self.year) + "-" + str(self.month)
                else:
                    if self.hour is None:
                        return str(self.year) + "-" + str(self.month) + "-" + str(self.day)
                    else:
                        if self.minute is None:
                            return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " " + str(self.hour)
                        else:
                            if self.second is None:
                                return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " " + str(self.hour) + ":" + str(self.minute)
                            else:
                                return str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " " + str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)

    def to_datetime(self):
        """
        Return a datetime representation of the date.
        """
        if self.year is None:
            return None
        else:
            if self.month is None:
                return datetime.datetime(self.year, 1, 1)
            else:
                if self.day is None:
                    return datetime.datetime(self.year, self.month, 1)
                else:
                    if self.hour is None:
                        return datetime.datetime(self.year, self.month, self.day)
                    else:
                        if self.minute is None:
                            return datetime.datetime(self.year, self.month, self.day, self.hour)
                        else:
                            if self.second is None:
                                return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
                            else:
                                return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
