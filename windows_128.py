__author__ = 'Marco Fernandes'
__created__ = '2020/08/27'

from datetime import datetime, timezone


class Windows128bit(object):
    """
    Windows 128bit Hex to datetime obj:

    Example : The current time in Windows 128bit Hex (Big Endian) is D9070B00010002000600090013000000

    Epoch Date	N/A
    Unit	N/A
    Expression	Hex
    TimeZone	UTC

    This timestamp is expressed as a 128bit hex number which breaks down into several parts.
    First, it requires splitting into chunks of 2 bytes which must then be swapped and converted into decimal.

    values = D9070B00010002000600090013000000
    Split	    D907,	0B00,	0100,	0200,	0600,	0900,	1300,	0000
    Swapped	    07D9,	000B,	0010,	0002,	0006,	0009,	0013,	0000
    Converted	2009,	11,	    16,	    2,	    6,	    9,	    13,	    0,
    Assignment	Year,	Month,	DOW,	Day,	Hr,	    Min,	Sec,	MSec
    Note: DOW = Day of the Week
    """

    def __init__(self, tz: timezone = timezone.utc):
        self.tz = tz

    def swap(self, hex_val: str) -> str:
        values = self.split_bytes(hex_val)
        return ''.join(reversed(values))

    @staticmethod
    def split_bytes(line: str, n: int = 2) -> list:
        return [line[i:i + n] for i in range(0, len(line), n)]

    @staticmethod
    def hex_decimal(hex_val: str) -> hex:
        hex_int = int(hex_val, 16)
        return hex_int

    @staticmethod
    def assure_size(values: list) -> list:
        if len(values) < 8:
            values.extend([0] * (8 - len(values)))
        elif len(values) > 8:
            del values[8:]
        return values

    def get_date(self, values: list) -> datetime:
        dt_obj = datetime(*values[:2], *values[3:], tzinfo=self.tz)
        return dt_obj

    def get(self, hex_val: str):
        if hex_val[:2].lower() == '0x':
            hex_bytes = self.split_bytes(hex_val[2:], n=4)
        else:
            hex_bytes = self.split_bytes(hex_val, n=4)
        hex_swapped = [self.swap(h) for h in hex_bytes]
        values = [self.hex_decimal(h) for h in hex_swapped]
        values = self.assure_size(values)
        date = self.get_date(values)
        return date


if __name__ == '__main__':
    # Test Class Output
    hex_values = [
        "0xD9070B00010002000600090013000000",
        "0xD9070B000100020006000900130000000000",
        "0xD9070B0001000200060009001300",
        "D9070B0001000200060009001300"
    ]
    windows128bit = Windows128bit()
    for value in hex_values:
        output = windows128bit.get(value)
        print(output)
