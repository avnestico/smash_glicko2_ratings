import collections
import contextlib
import datetime
import json
import os
import re
from bs4 import BeautifulSoup
import requests
import sys
import RankingFunctions
from RankingSettings import *
from urllib.request import http


"""
Copyright (c) 2015 Andrew Nestico

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


def get_valid_games():
    return ["SSB", "Melee", "Brawl", "PM", "Sm4sh"]


def get_game_folders(game):
    valid_games = get_valid_games()
    if game in valid_games:
        date_file = game + "Dates.txt"      # List of tournaments, separated by date.
        url_folder = game + "Urls/"         # Location of folder containing tournaments and their corresponding urls.
                                            # Optionally, may be left blank (url_folder = "").
        result_folder = game + "Results/"   # Location of folder containing tournament results. Also may be left blank.
        ensure_dir_exists(result_folder)
        return date_file, url_folder, result_folder
    else:
        print('Error: game "' + game + '" is not a valid game name. Please submit one of ' + str(valid_games))
        sys.exit(1)


def strip_match(line):
    """Remove all the useless data from a line"""
    scores = re.findall('\|[rl]\d+m\d+p\d+score=', line)

    if len(scores) == 2:
        # normal match, need to check for non-number scores
        stripped_line = re.sub('\|[rl]\d+m\d+p1=(.*?) (?:\{\{advance|\|).*'
                               '[rl]\d+m\d+p1score=(.*?) \|.*'
                               '[rl]\d+m\d+p2=(.*?) (?:\{\{advance|\|).*'
                               '[rl]\d+m\d+p2score=(.*?)(?: .*|$)',
                               r'\1,\2,\3,\4', line)

    elif len(scores) == 4:
        # grand finals with a bracket reset - scores will always be numbers
        p1score = 0
        p2score = 0
        p1scores = re.findall('\|[rl]\d+m\d+p1score=\d', line)
        p2scores = re.findall('\|[rl]\d+m\d+p2score=\d', line)

        for score in p1scores:
            p1score += int(score[-1])

        for score in p2scores:
            p2score += int(score[-1])

        stripped_line = re.sub('\|[rl]\d+m\d+p1=(.*?) \|.* \|[rl]\d+m\d+p2=(.*?) \|.*', r'\1,' + str(p1score) + r',\2,'
                               + str(p2score), line)

    else:
        # line is either already formatted or does not contain match data
        stripped_line = line

    if stripped_line.count(",") == 3:
        return stripped_line


def normalize_name(line):
    """Convert the names in a match to a standarized format: Title case with no sponsors."""

    # Convert all names to titlecase
    line = line.title()

    # Remove pools
    line = remove_pools(line)

    # Remove usual sponsors
    line = line.split("|")[-1].strip()
    line = line.split(" I ")[-1].strip()

    # check if name contains an oddly formatted sponsor or otherwise needs to be changed
    for Replacement in ReplacementList:
        if line == Replacement[0].title():
            line = Replacement[1].title()

    return line


def remove_pools(string):
    # Things to remove:
    # Anything inside square brackets
    string = re.sub("\[.*\]", "", string).strip()
    # P2/2, (P2-2), etc.
    string = re.sub("\((?:P|)\d+(?:|(?:/:|-)\d+)\)", "", string).strip()
    # A2.2, B2.2, etc.
    string = re.sub("[A-Z]\d+\.\d", "", string).strip()
    # (Wave 2), (Wave2), etc.
    string = re.sub("\(Wave(?: |)\d\)", "", string).strip()
    # (S2 P2), etc.
    string = re.sub("\(S\d+ P\d+\)", "", string).strip()
    # (Setup), (Unpaid), etc.
    string = re.sub("\((?:Setup|Unpaid|Forfeit|Dq|Dnp)\)", "", string).strip()
    return string


def parse_match(line):
    """Given a string containing a match result, parse it"""
    # Convert things to pipes
    line = re.sub("{{!}}", "|", line)
    line = re.sub("&amp;#124;", "|", line)

    # Remove garbage
    line = re.sub(r"\|[lr]\dm\dp\dflag=.*?,", ",", line)

    # Remove html tags
    line = re.sub("&amp;", "&", line)
    line = re.sub("&lt;.*?&gt;", "", line)

    # Split into components for further processing
    line = line.split(",")
    line = [word.strip() for word in line]

    # Ignore games with byes or no results
    if "bye" in line[0].lower() or "bye" in line[2].lower():
        return ""
    if line[1] == "" and line[3] == "":
        return ""
    if "advance" in str(line[1]) or "advance" in str(line[3]):
        return ""
    if "DQ" in str(line[1]) or "DQ" in str(line[3]):
        return ""
    if line[0] == "" or line[2] == "":
        return ""
    if line[1] == "-1" or line[3] == "-1":
        return ""

    # Convert wins to 2-0's
    if "{{win}}" in line[1] or line[1] == "W":
        line[1], line[3] = "2", "0"
    if "{{win}}" in line[3] or line[3] == "W":
        line[1], line[3] = "0", "2"
    if line[1] == "1" and line[3] == "0":
        line[1] = "2"
    if line[3] == "1" and line[1] == "0":
        line[3] = "2"

    # Check if scores can be converted to numbers.
    # Discard matches containing invalid numbers (x < 0 or x > 6)
    # The few remaining errors (mostly blank spaces) can be converted to 0's
    try:
        num = int(line[1])
        if num < 0 or num > 6:
            return ""
    except ValueError:
        line[1] = "0"

    try:
        num = int(line[3])
        if num < 0 or num > 6:
            return ""
    except ValueError:
        line[3] = "0"

    if line[1] == "0" and line[3] == "0":
        return ""

    line[0] = normalize_name(line[0])
    line[2] = normalize_name(line[2])

    return ",".join(line)


def match_played(url, line):
    """Contains a list of matches that have results but were not played, and returns False if the given line contains
    one such match. Otherwise, returns True.
    If the match is on the unplayed list but has numerical scores assigned to it, assume it is a special case and was
    played.
    At this point in time, only Liquipedia brackets support being not played."""

    rounds_not_played = {
        "CEO_2015/Top_32": ["r1"],
        "Paragon_2015&section=2": ["r1", "l1", "r2"],
        "The_Big_House_4/Winners_Bracket": ["r1"],
        "WTFox/Singles_Bracket": ["r1"],
        "WTFox&section=T-1": ["l1", "r2", "r3"],  # Workaround because WF gets ignored by previous line
    }
    for key in rounds_not_played:
        for value in rounds_not_played[key]:
            if key in url and re.match(r"^\|" + value, line):
                return False
    return True


def match_has_scores(line):
    """Returns true if and only if a match has a numerical, non-negative score assigned to both players."""
    return re.search('[rl]\d+m\d+p1score=\d+', line) and re.search('[rl]\d+m\d+p2score=\d+', line)


def format_liquipedia_url(url):
    """Converts bracket url to source url, if necessary."""
    if not "&action=edit" in url:
        url = re.sub("(wiki\.teamliquid\.net/smash/)(.*)", r"\1index.php?title=\2&action=edit", url)
    return url


def write_txt_from_liquipedia(url, filename):
    """Returns match data from a Liquipedia link."""
    url = format_liquipedia_url(url)

    try:
        soup = BeautifulSoup(requests.get(url).content)
    except http.client.IncompleteRead as e:
        soup = BeautifulSoup(e.partial)

    match_data = str(soup.find("textarea"))

    matches = ""
    prev_line_start = "xxxx"
    for line in match_data.split("\n"):
        if re.match('^\|[rl]\d+m\d+', line):
            if line.startswith(prev_line_start):
                matches += " " + line
            else:
                matches += "\n" + line
                prev_line_start = re.sub('^(\|[rl]\d+m\d+).*', r'\1', line)

    parsed_matches = ""
    for line in matches.split("\n"):
        stripped_line = strip_match(line)
        if stripped_line is not None and match_played(url, line):
            parsed_match = parse_match(stripped_line)
            if parsed_match != "":
                parsed_matches += parsed_match + "\n"

    with open(filename, 'a', encoding="utf8") as file:
        file.write(parsed_matches)


def format_smashgg_url(url):
    """Converts bracket url to api url, if necessary."""
    if not "api.smash.gg" in url:
        url = "http://api.smash.gg/phase_group/" + url.split("/")[-1] + "?expand[0]=sets&expand[1]=entrants"
    return url


def parse_smashgg_set(set, entrant_dict):
    """Returns the winner and loser of a smash.gg set."""
    winnerId = set["winnerId"]
    entrant1Id = set["entrant1Id"]
    entrant1Score = set["entrant1Score"]
    entrant2Id = set["entrant2Id"]
    entrant2Score = set["entrant2Score"]

    if set["completedAt"]:
        entrant1Name = normalize_name(entrant_dict[entrant1Id])
        entrant2Name = normalize_name(entrant_dict[entrant2Id])

        if type(entrant1Score) is int and type(entrant2Score) is int:
            if entrant1Score > -1 and entrant2Score > -1:
                if entrant1Id == winnerId:
                    return(entrant1Name + "," + entrant2Name)
                else:
                    return(entrant2Name + "," + entrant1Name)
        else:
            if entrant1Id == winnerId:
                return(entrant1Name + "," + entrant2Name)
            else:
                return(entrant2Name + "," + entrant1Name)


def write_txt_from_smashgg(url, filename):
    """Writes smash.gg bracket data to a file."""
    url = format_smashgg_url(url)
    data = requests.get(url).json()

    entrants = data["entities"]["entrants"]
    entrant_dict = {}
    for entrant in entrants:
        entrant_dict[entrant["id"]] = entrant["name"]

    sets = data["entities"]["sets"]
    set_data = []
    grand_finals = []
    for set in sets:
        parsed_set = parse_smashgg_set(set, entrant_dict)
        if parsed_set:
            if set["isGF"]:
                grand_finals.append(parsed_set)
            else:
                set_data.append(parsed_set)
    set_data = set_data + grand_finals
    for line in set_data:
        print(line)


def safe_delete(filename):
    """Delete a file if it exists, and do nothing if it does not."""
    filename = add_txt(filename)
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


def check_if_date(line):
    """Returns true if a string is a valid date of the form YYYY-MM-DD."""
    try:
        datetime.datetime.strptime(line.strip(), '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_filename(folder, string):
    """Turn a string into a tournament's file name"""
    filename = add_txt(string)
    filename = re.sub(":", "", filename)
    filename = folder + filename
    return filename


def add_txt(string):
    """Ensures a filename ends in '.txt'."""
    if not string.endswith(".txt"):
        string += ".txt"
    return string


def ensure_dir_exists(folder):
    """Make sure a given directory exists."""
    directory = os.path.dirname(folder)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_tournaments(filename, url_folder):
    """Returns an ordered dict of tournaments where each tournament's value is a list of its bracket urls."""
    tournaments = collections.OrderedDict([])
    with open(filename, "r", encoding="ISO-8859-1") as file:
        for line in file:
            is_date = check_if_date(line)
            if not is_date:
                line = get_filename("", line.strip())
                tournaments[line] = get_tournament_urls(line, url_folder)
    return tournaments


def get_tournament_urls(filename, url_folder):
    """Reads a text file of urls and converts it to a list."""
    urls = []
    with open(get_filename(url_folder, filename), "r", encoding="ISO-8859-1") as file:
        for line in file:
            line = line.strip()
            urls.append(line)
    return urls


def scrape_tournament(filename, url_list):
    """Scrape all the urls in a file and write the corresponding tournament's matches to a text file."""
    for url in url_list:
        print(url)
        if "challonge" in url:
            RankingFunctions.WriteTxtFromChallonge(url, filename)
        elif "teamliquid" in url:
            write_txt_from_liquipedia(url, filename)
        elif "smash.gg" in url:
            write_txt_from_smashgg(url, filename)


def scrape_tournament_by_filename(tournament):
    """Scrapes a single tournament given only its file name."""
    for game in get_valid_games():
        scrape_tournament_by_game(game, tournament)


def scrape_tournament_by_game(game, tournament):
    date_file, url_folder, result_folder = get_game_folders(game)
    try:
        urls = get_tournament_urls(tournament, url_folder)
        tournament_filename = get_filename(result_folder, tournament)
        safe_delete(tournament_filename)
        scrape_tournament(tournament_filename, urls)
    except FileNotFoundError:
        print("No " + game + " data found for tournament '" + tournament + "'.")


def scrape_all_tournaments_for_game(game):
    """Scrape all match data and write to a set of files."""
    date_file, url_folder, result_folder = get_game_folders(game)
    tournaments = get_tournaments(date_file, url_folder)
    for tournament in tournaments:
        print(tournament)
        tournament_filename = get_filename(result_folder, tournament)
        safe_delete(tournament_filename)
        scrape_tournament(tournament_filename, tournaments[tournament])


def scrape_all_tournaments():
    for game in get_valid_games():
        try:
            print("Scraping " + game + " tournaments.")
            scrape_all_tournaments_for_game(game)
        except FileNotFoundError:
            print("No tournaments found for " + game)


def process_game_by_date(game):
    """Run Glicko2 ranking process for a single game in batches, with tournaments between dates processed in the same
    batch."""
    print("Processing " + game + "...")
    date_file, url_folder, result_folder = get_game_folders(game)
    tournaments = []
    with open(date_file, 'r', encoding="ISO-8859-1") as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            is_date = check_if_date(line)
            if not is_date:
                if not os.path.isfile(get_filename(result_folder, line)):
                    scrape_tournament_by_game(game, line)
                tournaments.append(get_filename(result_folder, line))
            else:
                print(line)
                RankingFunctions.ProcessRankings(tournaments, game)
                tournaments = []
    RankingFunctions.ProcessRankings(tournaments, game)


def process_all_games():
    """Run Glicko2 ranking process for all games"""
    for game in get_valid_games():
        try:
            process_game_by_date(game)
        except FileNotFoundError:
            print("Processing files not found for " + game)
