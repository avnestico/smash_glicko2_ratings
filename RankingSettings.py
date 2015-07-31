##ResultsFolder = 'C:\\Users\\MasahiroSakurai\\Documents\\SmashStuff'      # Make sure to have double backslashes file paths.
    # ResultsFolder may be left undefined if result .txt files are in the same place as the Python code
DefaultTitleMin = 2
DefaultSort = 'Low'
DefaultSortTie = 'Middle'
DefaultLines = 2
RoundLen = 2             # How many Digits to round to in ranking displays
Rounding = '.' + str(RoundLen) + 'f'
DefaultRating = 1500
DefaultRD = 350
DefaultVol = 0.06


# Tags and names go here. There should only be one tag per real name.

TagDict = { \
    'MaNg0': 'Joseph Marquez', \
    'Armada': 'Adam Lindgren', \
    'PPMD': 'Kevin Nanney', \
    'Hungrybox': 'Juan Manuel Debiedma', \
    'Leffen': 'William Hjelte', \
    'Mew2King': 'Jason Zimmerman'\
    }


# Don't touch this.

NameDict = {}
for Tag in TagDict:
    NameDict[TagDict[Tag]] = Tag

    
# Any tags with numbers in them should go here, with the actual tag, then the tag with numbers written out.
# Note that tags of the form A1 or AA1 (that is, a capital letter followed by a number or two capital letters
# followed by a number) do not always process properly, and additional coding may be needing to avoid errors.

NumFixes = [ \
    ('AndrewAjt62', 'AndrewAjtsixtytwo'), \
    ('EMP P4K | Armada', 'Armada'), \
    ('P4K EMP Armada', 'Armada'), \
    ('P4K EMP | Armada', 'Armada'), \
    ('baka4moe', 'bakafourmoe'), \
    ('Carls492', 'Carlsfourninetwo'), \
    ('Gninja64', 'Gninjasixtyfour'), \
    ('482 | JSalt', 'foureighttwo | JSalt'), \
    ('f00', 'fzerozero'), \
    ('Jake13', 'Jakethirteen'), \
    ('j00t', 'jzerozerot'), \
    ('Kiw1', 'Kiwone'), \
    ('kukunok0', 'kukunokzero'), \
    ('C9|Mango', 'MaNgzero'), \
    ('C9 Mang0', 'MaNgzero'), \
    ('C9 MaNg0', 'MaNgzero'), \
    ('C9. Mango', 'MaNgzero'), \
    ('MaNg0', 'MaNgzero'), \
    ('PL MVG EMP Mew2King', 'MewtwoKing'), \
    ('PL MVG mew2king', 'MewtwoKing'), \
    ('EMP P4K | Mew2King', 'MewtwoKing'), \
    ('P4K | EMP |Mew2King', 'MewtwoKing'), \
    ('P4K EMP | Mew2King', 'MewtwoKing'), \
    ('P4K EMP Mew2King', 'MewtwoKing'), \
    ('P4K Mew2King', 'MewtwoKing'), \
    ('CT EMP|MewtwoKing', 'MewtwoKing'), \
    ('Mew2King', 'MewtwoKing'), \
    ('M2K', 'MewtwoKing'), \
    ('Poopmaister6000', 'Poopmaistersixthousand'), \
    ('SFS KoopaTroopa895', 'SFS KoopaTroopaeightninefive'), \
    ('[62Bit] Bladewise', '[sixtytwoBit] Bladewise'), \
    ('Smasher89', 'Smashereightynine'), \
    ('S2J', 'StwoJ'), \
    ('S0ft', 'Szeroft'), \
    ('LP.RaynEX', 'temprayn'), \
    ('RaynEX', 'temprayn'), \
    ('VO1D', 'VOoneD'), \
    ('X1', 'Xone'), \
    ('Cornholio69', 'Cornholiosixtynine'), \
    ('Ycz6', 'Yczsix'), \
    ('GamerGuitarist7', 'GamerGuitaristseven') \
    ]


# Typos, full last names, changed tags, names that have tags, extra spaces, etc., go here.

ReplacementList = [ \
    ('AG | Arc', 'Arc'), \
    ('[A]rmada', 'Armada'), \
    ('Alliance | Armada', 'Armada'), \
    ('EMP P4K | Armada', 'Armada'), \
    ('P4K EMP | Armada', 'Armada'), \
    ('P4K EMP Armada', 'Armada'), \
    ('MELEE HELL | Articanus', 'Articanus'), \
    ('Mortality_Axe', 'Axe'), \
    ('Mortality.Axe', 'Axe'), \
    ('MOR | Axe', 'Axe'), \
    ('SmashFactor | Aza', 'Aza'), \
    ('[62Bit] Bladewise', 'Bladewise'), \
    ('VS | Blea Gelo', 'Blea Gelo'), \
    ('VS I Blea Gelo', 'Blea Gelo'), \
    ('MGFC|Chain-Ace', 'Chain-Ace'), \
    ('CnB | Chandy', 'Chandy'), \
    ("Liquid' Chillindude", 'Chillindude'), \
    ('SS | Colbol', 'Colbol'), \
    ('CTRL|DJ Nintendo', 'DJ Nintendo'), \
    ('CTRL | DJ Nintendo', 'DJ Nintendo'), \
    ('XTR Eddy Mexico', 'Eddy Mexico'), \
    ('XTR I Eddy Mexico', 'Eddy Mexico'), \
    ('GK | EikelmannRUS', 'EikelmannRUS'), \
    ("SS | Flamin'Roy", "Flamin'Roy"), \
    ('SS | SDR | Flow', 'Flow'), \
    ('SS | Flow', 'Flow'), \
    ('SS | FullMetal', 'FullMetal'), \
    ('SS | Fullmetal', 'Fullmetal'), \
    ('EE Gahtzu', 'Gahtzu'), \
    ('GK Gahtzu', 'Gahtzu'), \
    ('GK | Gahtzu', 'Gahtzu'), \
    ('VGBC | GimR', 'GimR'), \
    ('GK | HarrietTheGuy', 'HarrietTheGuy'), \
    ('VGBC Hax', 'Hax'), \
    ('VGBC | Hax', 'Hax'), \
    ('FRQ | HugS', 'HugS'), \
    ('FRQ| HugS', 'HugS'), \
    ('Liquid`Hungrybox', 'Hungrybox'), \
    ('CT|Hungrybox', 'Hungrybox'), \
    ('Crs. Hungrybox', 'Hungrybox'), \
    ('CRS.Hungrybox', 'Hungrybox'), \
    ('Liquid` Hungrybox', 'Hungrybox'), \
    ('Liquid Hungrybox', 'Hungrybox'), \
    ('SmashFactor | Javi', 'Javi'), \
    ('MIOM | Juggleguy', 'Juggleguy'), \
    ('Liquid`KDJ', 'KDJ'), \
    ('SS | KeepSpeedN', 'KeepSpeedN'), \
    ('IPG | Kels', 'Kels'), \
    ('LiquidKen', 'Ken'), \
    ('Liquid Ken', 'Ken'), \
    ('EMG | KirbyKaze', 'KirbyKaze'), \
    ('SmashFactor | Lazh', 'Lazh'), \
    ('TSM|Leffen', 'Leffen'), \
    ('Huggies | Lucky', 'Lucky'), \
    ('LuCKy', 'Lucky'), \
    ('MVG Medz', 'Medz'), \
    ('MIOM I PewPewU', 'MIOM|PewPewU'), \
    ('C9|Mango', 'MaNg0'), \
    ('C9 MaNg0', 'MaNg0'), \
    ('C9 Mang0', 'MaNg0'), \
    ('C9. Mango', 'MaNg0'), \
    ('Mang0', 'MaNg0'), \
    ('Mango', 'MaNg0'), \
    ('SS | Merck', 'Merck'), \
    ('COG MVG mew2king', 'Mew2King'), \
    ('PL MVG mew2king', 'Mew2King'), \
    ('EMP P4K | Mew2King', 'Mew2King'), \
    ('PL MVG EMP Mew2King', 'Mew2King'), \
    ('P4K EMP Mew2King', 'Mew2King'), \
    ('P4K Mew2King', 'Mew2King'), \
    ('CT EMP|Mew2King', 'Mew2King'), \
    ('P4K | EMP |Mew2King', 'Mew2King'), \
    ('P4K EMP | Mew2King', 'Mew2King'), \
    ('M2K', 'Mew2King'), \
    ('GameGuys | Mojo', 'Mojo'), \
    ('HF Neon', 'Neon'), \
    ('SS | Nicaboy', 'Nicaboy'), \
    ('VS | NickRiddle', 'NickRiddle'), \
    ('Apex | Nintendude', 'Nintendude'), \
    ('WCS TGG | Oro?!', 'Oro'), \
    ('TRC | Owl', 'Owl'), \
    ('SS | PBJ', 'PB&J'), \
    ('EG I PPMD', 'PPMD'), \
    ('Dr. PP', 'PPMD'), \
    ('MIOM|PewPewU', 'PewPewU'), \
    ('VS | Plup', 'Plup'), \
    ('VS | Porkchops', 'Porkchops'), \
    ('VS Porkchops', 'Porkchops'), \
    ('vWs | Professor Pro', 'Professor Pro'), \
    ('GULL | Pink Fresh', 'Pink Fresh'), \
    ('ESI.GG | Prince Abu', 'Prince Abu'), \
    ('GK Reno', 'Reno'), \
    ('Apex | Ryobeat', 'Ryobeat'), \
    ('MIOM|Sfat', 'SFAT'), \
    ('MIOM | SFAT', 'SFAT'), \
    ('MIOM|SFAT', 'SFAT'), \
    ('MIOM | Scar', 'Scar'), \
    ('VS | Seibrik', 'Seibrik'), \
    ('MMG_Shroomed', 'Shroomed'), \
    ('GC | Silent Wolf', 'Silent Wolf'), \
    ('SS | SmashMac', 'SmashMac'), \
    ('SS | Soft', 'Soft'), \
    ('HV VS | Spider_Sense', 'Spider_Sense'), \
    ('EX | Star Lord', 'Star Lord'), \
    ('BERT I Swedish Delight', 'Swedish Delight'), \
    ('MIOM|Tafokints', 'Tafokints'), \
    ('MVG Tai', 'Tai'), \
    ('CTRL|The Moon', 'The Moon'), \
    ('CTRL | The Moon', 'The Moon'), \
    ('MIOM | Toph', 'Toph'), \
    ('SmashFactor | Twin', 'Twin'), \
    ('moe | Upke', 'Upke'), \
    ('SmashFactor | Valdo', 'Valdo'), \
    ('EMG | Weon-X', 'Weon-X'), \
    ('CT Wizzrobe', 'Wizzrobe'), \
    ('SS | CT | Wizzrobe', 'Wizzrobe'), \
    ('VS CT | Wizzrobe', 'Wizzrobe'), \
    ('COG | Wizzrobe', 'Wizzrobe'), \
    ('FX_DFW Wobbles', 'Wobbles'), \
    ('CT Zero', 'Zero'), \
    ('CT ZeRo', 'Zero'), \
    ('VGBC I aMSa', 'aMSa'), \
    ('VGBC|aMSa', 'aMSa'), \
    ('LP.raynEX', 'raynEX'), \
    ('EE | uuaa', 'uuaa')
    ]
