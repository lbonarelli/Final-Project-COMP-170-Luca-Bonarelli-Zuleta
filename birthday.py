from datetime import datetime  # to pull today's date


class Birthday:

    # Static data: number of days in each month (Feb = 28, no leap years)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, month, day):
        """Validates month and day; defaults to January 1 if invalid."""
        if 1 <= month <= 12:
            self.__month = month
        else:
            self.__month = 1

        if 1 <= day <= Birthday.days_in_month[self.__month - 1]:
            self.__day = day
        else:
            self.__day = 1

    def set_day(self, day):
        """Updates day if valid for the stored month."""
        if 1 <= day <= Birthday.days_in_month[self.__month - 1]:
            self.__day = day

    def get_month(self):
        """Accessor for month"""
        return self.__month

    def get_day(self):
        """Accessor for day"""
        return self.__day

    def days_until(self):
        """Returns number of days until this birthday from today."""
        today = datetime.today()
        today_day = self.day_in_year(today.month, today.day)
        birthday_day = self.day_in_year(self.__month, self.__day)
        if birthday_day >= today_day:
            return birthday_day - today_day
        else:
            return 365 - today_day + birthday_day

    def day_in_year(self, month, day):
        """Returns the day number (1-365) for a given month/day."""
        return sum(Birthday.days_in_month[:month - 1]) + day

    def __str__(self):
        """String representation"""
        return f"[ {self.get_month()}/{self.get_day()} ]"


# Demo/Test Code
if __name__ == "__main__":
    demo = Birthday(6, 29)
    print(demo.day_in_year(6, 29))  # Expected: 180
    print(demo.day_in_year(4, 29))  # Expected: 119
    print(f"Days until next birthday: {demo.days_until()}")

