__author__ = 'Marco Fernandes'
__created__ = '2020/08/27'

from datetime import datetime, timezone


class UnixEpoch(object):
    """
    Convert hex to decimal and then get the unix epoch time stamp
    This class accounts for both hex with and without milliseconds

    Epoch Date: 1st January 1970
    Unit:       Seconds
    Expression: Decimal
    TimeZone:   UTC

    Example : The current time in UNIX TimeStamp is 5F476E77.
    steps to take:
    value       5F476E77
    decimal     1598516855
    datetime    2020-08-27 08:27:35+00:00
    """

    def __init__(self, tz: timezone = timezone.utc):
        self.tz = tz
        self.unix_y2k = datetime(year=2038, month=1, day=19, hour=3, minute=14, second=7).timestamp()

    def get_date(self, epoch_time: int) -> datetime:
        return datetime.fromtimestamp(epoch_time, tz=self.tz)

    @staticmethod
    def convert(value: str, n: int = 16) -> int:
        return int(value, n)

    def probably_milliseconds(self, seconds: int) -> bool:
        return True if seconds > self.unix_y2k else False

    @staticmethod
    def get_seconds(milli: int) -> float:
        return float('.'.join([str(i) for i in divmod(milli, 1000)]))

    @staticmethod
    def split_bytes(line: str, n: int = 2) -> list:
        return [line[i:i + n] for i in range(0, len(line), n)]

    def reverse(self, value: str) -> str:
        return ''.join(reversed(self.split_bytes(value)))

    def get(self, value: str, endian: str = 'big') -> datetime:
        if value[:2].lower() == '0x':
            value = value[2:]
        if endian.lower() == 'little':
            value = self.reverse(value)
        value = self.convert(value)
        if self.probably_milliseconds(value):
            value = self.get_seconds(value)
        value = self.get_date(value)
        return value


if __name__ == '__main__':
    # Test Class output
    big_endians = ['5F476E77', '0x5F476E77', '000001743068BF46', '1743078961F']
    little_endians = ['776E475F', '0x776E475F', '46BF683074010000', '1F9678307401']
    unix_epoch = UnixEpoch()
    for en in big_endians:
        print(unix_epoch.get(en, endian='big'))
    for en in little_endians:
        print(unix_epoch.get(en, endian='little'))
