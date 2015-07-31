from RankingFunctions import *

# Run these to create the .txt files. Then put them wherever ResultsFolder in RankingSettings is pointed, as necessary. 

WriteTxtFromChallonge('http://challonge.com/apex2014meleesinglestop8', 'Apex 2014')
WriteTxtFromChallonge('http://controlgaming.challonge.com/ROM7Singles', 'RoM 7')
WriteTxtFromChallonge('http://challonge.com/PH2_Singles', "Pat's House 2")
WriteTxtFromChallonge('http://supersweet.challonge.com/supersweetmeleesingles', 'Super SWEET')
WriteTxtFromChallonge('http://oxy.challonge.com/KoC4Singles', 'KoC 4')
WriteTxtFromChallonge('http://zenith.challonge.com/ZenithMeleeSingles', 'Zenith 2014')
WriteTxtFromChallonge('http://challonge.com/TippedOff10', 'Tipped Off 10')
WriteTxtFromChallonge('http://tbh4.challonge.com/meleesingles', 'TBH 4')
WriteTxtFromChallonge('http://dyfwi.challonge.com/dyftop32', 'DYFWI')
WriteTxtFromChallonge('http://challonge.com/forte2meleesingles', 'Forte 2')
WriteTxtFromChallonge('http://beastsmash.challonge.com/B5MSB', 'Beast V')
WriteTxtFromChallonge('http://paragon.challonge.com/orlando_2015_melee_singles', 'Paragon 2015')
WriteTxtFromChallonge('http://apex2015melee.challonge.com/singles', 'Apex 2015')
WriteTxtFromChallonge('http://challonge.com/INY2015Melee', 'INY')
WriteTxtFromChallonge('http://challonge.com/SandstormMeleeTop64', 'Sandstorm')

WriteTxtFromChallonge('http://tbh4.challonge.com/pmsingles', 'TBH 4 (PM)')

WriteTxtFromChallonge('http://beastsmash.challonge.com/B5S4SB', 'Beast V (Sm4sh)')



# Each ProcessRankings command should be run for results over a two month period of time.
# Make sure to process a Blank txt doc during each two month period (Jan-Feb, Mar-Apr, etc.)
# for which there are no results within a game after the initial processing of a game.

# 01-02/2014
ProcessRankings(['Apex 2014'], 'Melee')

# 03-04/2014
ProcessRankings(['RoM 7'], 'Melee')

# 05-06/2014
ProcessRankings(["Pat's House 2", 'Super SWEET'], 'Melee')

# 07-08/2014
ProcessRankings(['KoC 4', 'Zenith 2014'], 'Melee')

# 09-10/2014
ProcessRankings(['Tipped Off 10', 'TBH 4'], 'Melee')
ProcessRankings(['TBH 4 (PM)'], 'PM')

# 11-12/2014
ProcessRankings(['DYFWI', 'Forte 2'], 'Melee')
ProcessRankings(['Blank'], 'PM')

# 01-02/2015
ProcessRankings(['Beast V', 'Paragon 2015', 'Apex 2015'], 'Melee')
ProcessRankings(['Blank'], 'PM')
ProcessRankings(['Beast V (Sm4sh)'], 'Sm4sh')

# 03-04/2015
ProcessRankings(['INY', 'Sandstorm'], 'Melee')
ProcessRankings(['Blank'], 'PM')
ProcessRankings(['Blank'], 'Sm4sh')

##ShowAllRankings()


##UsefulFunctions()       # Run this to print all the useful functions as well as information about each.
##UsefulFunctionsListed() # Run this to print all the useful functions without the headers or additional information.
