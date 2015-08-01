import argparse
from RankingFunctions import *
from ScrapingFunctions import *


def arg_parser(argv):
    """Process args passed in."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Computes Glicko2 ratings of Super Smash Bros competitors')
    parser.add_argument('--print_functions', dest='print_functions', default=None,
                        help='Display information on useful functions (all) or just a list of useful functions (list)')
    parser.add_argument('--scrape', dest='scrape', action='store_true',
                        help='Set this flag if you have new tournaments to scrape')
    parser.set_defaults(scrape=False)
    parser.add_argument('--scrape_tournament', dest='tournament', default=None,
                        help="Scrape the data for all games in a single tournament. Arg is tournament's filename.")
    parser.add_argument('--format', dest='output_format', default='human',
                        help="Format of output: 'human' (human-readable) or 'tab' (tab-separated)")
    parser.add_argument('--game', dest='game', default=None,
                        help="Select a single game to process: 'SSB', 'Melee', 'Brawl', 'PM', or 'Sm4sh'")
    parser.add_argument('--top_amount', dest='top_amount', default=100,
                        help="The number of players to be displayed. Set to 100 by default.")

    args = parser.parse_args(argv)
    return args


def display_game_rankings(game, output_format, top_amount):
    """Display rankings for a single game as defined by format."""
    if output_format == "human":
        ShowRankings(game, TopAmount=top_amount)
    elif output_format == "tab":
        ShowTabSepRankings(game, TopAmount=top_amount)
    else:
        print("Format '" + output_format + "' not valid.")
        exit(1)


def main(args):
    """Process Glicko2 ratings."""
    print_functions = args.print_functions
    scrape = args.scrape
    tournament = args.tournament
    output_format = args.output_format
    game = args.game
    top_amount = int(args.top_amount)

    if print_functions:
        if print_functions == "all":
            UsefulFunctions()        # Run this to print all the useful functions as well as information about each
        elif print_functions == "list":
            UsefulFunctionsListed()  # Run this to list all useful functions without headers or additional information
        return 0

    if scrape:
        scrape_all_tournaments()

    if tournament:
        scrape_tournament_by_filename(tournament)

    # If a specific game is not set, process all games. Otherwise, process only that one game.
    if not game:
        process_all_games()
        ShowAllRankings(TopAmount=top_amount)
    else:
        process_game_by_date(game)
        display_game_rankings(game, output_format, top_amount)

    return 0


if __name__ == "__main__":
    parsed_args = arg_parser(sys.argv[1:])
    sys.exit(main(parsed_args))
