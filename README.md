# smash_glicko2_ratings

## Python3 program for computing Glicko2 ratings of Super Smash Bros competitors

### Quick Setup

Run `python SmashRankingsCalculator.py` and watch the magic.

### How to use

When you download this repo, you'll see a file and two folders with the prefix "Melee". Depending on the game you're getting rankings for, this prefix could also be "SSB", "Brawl", "PM", or "Sm4sh".

`MeleeDates.txt`: A list of dates and tournaments.

    MeleeDates.txt

    2015-01-03
    Smash_The_Target
    SWEET_Prologue
    2015-01-10
    B.E.A.S.T_5
    2015-01-17
    Paragon_2015
    
`MeleeUrls/`: A folder containing text files with bracket urls corresponding to the above. Liquipedia and Challonge brackets are supported.

    Smash_The_Target.txt
    
    http://mh.challonge.com/stt1_pro


    SWEET_Prologue.txt
    
    http://wiki.teamliquid.net/smash/SWEET_Prologue&section=2
    http://wiki.teamliquid.net/smash/SWEET_Prologue/Singles_Top_32
    http://wiki.teamliquid.net/smash/SWEET_Prologue/Singles_Top_96_E
    http://wiki.teamliquid.net/smash/SWEET_Prologue/Singles_Top_96_F
    http://wiki.teamliquid.net/smash/SWEET_Prologue/Singles_Top_96_G
    http://wiki.teamliquid.net/smash/SWEET_Prologue/Singles_Top_96_H
    
    
    and so on...
    
`MeleeResults/`: A folder containing scraped matchups of the above tournaments.

    Smash_The_Target.txt
    
    Jj,0,Jjff,2
    Max,0,Tag,2
    Twin A,2,Cornholio69,0
    Fortefreak,2,Smurfyexe,0
    Corn,0,Capn Scfifty,2
    Wizard,2,Tinmo,1
    Glitch,2,6669,1
    Toro,2,Chroma,1
    Janet,0,Travist,2
    Turnipslip,0,Eastcoastjeff,2
    etc.
    
If you want to use this program for your own tournaments, replace the contents of `MeleeDates.txt` with your own tournaments the same way:

* tournaments in chronological order
* each tournament following the day it took place
* multiple tournaments in the same week not separated by a date

Then, create a file for each tournament in `MeleeUrls/`, matching the name written down in `MeleeDates.txt` with `.txt` added to the end of each, containing a list of the urls where brackets can be found for the tournament.

For other games, perform the same process: for Sm4sh, you would write `Sm4shDates.txt`, create files in `Sm4shUrls/`, and create an empty `Sm4shResults/` folder where the scraped results would be written to.

Then, uncomment the call to `scrape_all_tournaments()` in `SmashRankingsCalculator.py` and run the file with `python SmashRankingsCalculator.py`.
