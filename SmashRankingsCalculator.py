import argparse
from RankingFunctions import *
from ScrapingFunctions import *


def arg_parser(argv):
    """Process args passed in."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Computes Glicko2 ratings of Super Smash Bros competitors')
    parser.add_argument('--scrape', dest='scrape', action='store_true',
                        help='Set this flag if you have new tournaments to scrape')
    parser.set_defaults(scrape=False)
    parser.add_argument('--scrape_tournament', '--scrape-tournament', dest='tournaments', default=None,
                        help="Comma-separated list of tournaments to scrape, by filename.")
    parser.add_argument('--format', dest='output_format', default='human',
                        help="Format of output: 'human' (human-readable) or 'tab' (tab-separated). Default: human")
    parser.add_argument('--game', dest='game', default=None,
                        help="Select a single game to process: 'SSB', 'Melee', 'Brawl', 'PM', or 'Sm4sh'")
    parser.add_argument('--top_amount', '--top-amount', dest='top_amount', default=100,
                        help="The number of players to be displayed. Default value: 100")
    parser.add_argument('--sort', dest='sort', default='Low',
                        help="Rating sort: 'Middle', 'Low' (default), or 'Bottom'.")

    args = parser.parse_args(argv)
    return args


def display_game_rankings(game, output_format, top_amount, sort):
    """Display rankings for a single game as defined by format."""
    if output_format == "human":
        ShowRankings(game, TopAmount=top_amount, SortedBy=sort)
    elif output_format == "tab":
        ShowTabSepRankings(game, TopAmount=top_amount, SortedBy=sort)
    else:
        print("Format '" + output_format + "' not valid.")
        exit(1)


def main(args):
    """Process Glicko2 ratings."""
    scrape = args.scrape
    tournaments = args.tournaments
    output_format = args.output_format
    game = args.game
    top_amount = int(args.top_amount)
    sort = args.sort

    if scrape:
        scrape_all_tournaments()

    if tournaments:
        tournaments = tournaments.split(",")
        for tournament in tournaments:
            scrape_tournament_by_filename(tournament)

    # If a specific game is not set, process all games. Otherwise, process only that one game.
    if not game:
        process_all_games()
        ShowAllRankings(TopAmount=top_amount, SortedBy=sort)
    else:
        process_game_by_date(game)
        display_game_rankings(game, output_format, top_amount, sort)

    return 0


if __name__ == "__main__":
    parsed_args = arg_parser(sys.argv[1:])
    sys.exit(main(parsed_args))
