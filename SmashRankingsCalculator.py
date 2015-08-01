from RankingFunctions import *
from ScrapingFunctions import *


if __name__ == "__main__":
    ##scrape_tournament_by_filename("Apex_2015", "Melee")  # Use to scrape a single tournament
    ##scrape_all_tournaments("Melee")                      # Use to scrape all tournaments for a game

    process_game_by_date("Melee")  # Process the results for a single game

    ShowRankings("Melee")     # Display results in a human-readable format
    ##ShowTabSepRankings("Melee", TopAmount=64)  # Display results for a game in a format for pasting into a spreadsheet
    ##ShowAllRankings()         # Display results for all games

    ##UsefulFunctions()       # Run this to print all the useful functions as well as information about each
    ##UsefulFunctionsListed() # Run this to print all the useful functions without the headers or additional information
