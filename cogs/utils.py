import re
time_parser = re.compile(r"(\d+)[dhmis]")

def time_converter(time):
    unit_value = {
        'd': 60 * 60 * 24,
        'h': 60 * 60,
        'm': 60,
        's': 1,
    }

    seconds = 0
    for number, unit in time_parser.findall(time):
        seconds = seconds + unit_value[unit] * int(number)
    return int(seconds)
