from RankingFunctions import *
from ScrapingFunctions import *


if __name__ == "__main__":
    ##scrape_all_tournaments()
    ##scrape_tournament_by_filename("Apex_2015", "Melee")  # Use to scrape a single tournament for a single game

    process_all_games()  # Process all games' results
    ShowAllRankings()    # Display results for all games
    ##ShowTabSepRankings("Melee", TopAmount=64)  # Display results for a game in a format for pasting into a spreadsheet

    ##UsefulFunctions()       # Run this to print all the useful functions as well as information about each
    ##UsefulFunctionsListed() # Run this to print all the useful functions without the headers or additional information
