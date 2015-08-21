import datetime
import fileinput
import os
from ScrapingFunctions import safe_delete
"""
A utility class meant to make updating the tournament data easier.
"""

def get_date(line):
    """
    Convert the given string to a date, if possible, and return False if not possible
    """
    try:
        return datetime.datetime.strptime(line.strip(), '%Y-%m-%d')
    except:
        return False


def str_to_date(date):
    """
    Convert a string to a date, if necessary.
    """
    if type(date) == str:
        date = datetime.datetime.strptime(date.strip(), '%Y-%m-%d')
    return date


def get_saturday(date, weeks=0):
    """
    Get the Saturday in the same week as the given date
    :param date: a date, in either date form or string form (YY-mm-dd)
    :param next_week: int, the number of weeks to move forward (+) or backward (-)
    """
    date = str_to_date(date)
    saturday = 5 + 7 * weeks
    days_to_add = saturday - date.weekday()
    date += datetime.timedelta(days=days_to_add)
    return date


def get_next_saturday(date):
    return get_saturday(date, 1)


def get_prev_saturday(date):
    return get_saturday(date, -1)


def get_filename(name):
    """
    Takes the name of a tournament and points to its url file
    """
    ensure_dir("MeleeUrls/")
    name = name.strip()
    name = name.replace(":", "")
    if not name.startswith("MeleeUrls/"):
        name = "MeleeUrls/" + name
    if not name.endswith(".txt"):
        name += ".txt"
    return name


def ensure_dir(f):
    """
    Ensures a directory exists, and creates it if it doesn't
    """
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def add_tournaments(filename, date_filename):
    """
    Splits a list of dates, tournaments, and urls into a date-tournament list and a file for each tournament containing
    its urls.
    """
    safe_delete(date_filename)
    date = False
    tournament = False
    with open(filename, "r", encoding="ISO-8859-1") as file:
        for line in file:
            line = line.strip()
            # Ignore blank and commented lines (% is the comment marker as some tournaments may be hashtags)
            if line == "" or line.startswith("%"):
                pass
            # If the line is a date, write it and all other weeks after the previously written week to the date file
            elif get_date(line):
                new_date = get_saturday(get_date(line))
                # If date is not assigned, this is the first week
                # Set date to the previous week in order to start the loop
                # The date will move forward 1 week to new_date, printing the correct week to the date file
                if not date:
                    date = get_prev_saturday(new_date)
                with open(date_filename, "a", encoding="ISO-8859-1") as date_file:
                    while new_date > date:
                        date = get_next_saturday(date)
                        date_file.write(str(date).split(" ")[0] + "\n")
            # If the line is not a url, it is the tournament name. Write this to the date file
            elif not line.startswith("http"):
                tournament = line.strip()
                safe_delete(get_filename(tournament))
                with open(date_filename, "a", encoding="ISO-8859-1") as date_file:
                    date_file.write(line + "\n")
            # If the line is a url, write it to the tournament's url file.
            else:
                with open(get_filename(tournament), "a", encoding="ISO-8859-1") as tournament_file:
                    tournament_file.write(line + "\n")


def print_tournaments(filename):
    """
    Converts a date-tournament file back to a list file to ensure accuracy.
    Note that all dates in the new list will be Saturdays.
    """
    date = ""
    with open(filename, "r", encoding="ISO-8859-1") as file:
        for line in file:
            line = line.strip()
            if get_date(line):
                date = line
            else:
                print("\n" + date)
                print(line)
                with open(get_filename(line), "r", encoding="ISO-8859-1") as tournament_file:
                    for line in tournament_file:
                        print(line.strip())


if __name__ == "__main__":
    add_tournaments("MeleeTournaments.txt", "MeleeDates.txt")
    print_tournaments("MeleeDates.txt")