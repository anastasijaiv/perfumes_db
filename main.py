import sqlite3

# Pieslēgties pie DB
database = sqlite3.connect("parfumi.db")
cursor = database.cursor()

cursor.execute("PRAGMA foreign_keys = ON")


# Izveidot tabulu ar brendiem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Brands(
        BrandID INTEGER PRIMARY KEY,
        BrandName TEXT NOT NULL,
        Country TEXT,
        FoundedYear INTEGER
    )
""")


# Izveidot tabulu ar parfīmiem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Perfumes(
        PerfumeID INTEGER PRIMARY KEY,
        BrandID INTEGER NOT NULL,
        PerfumeName TEXT NOT NULL,
        Concentration TEXT,
        VolumeML INTEGER,
        ReleaseYear INTEGER,
        Price REAL,

        FOREIGN KEY (BrandID)
            REFERENCES Brands(BrandID)
    )
""")


# Izveidot tabulu ar notu sarakstu
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FragranceNotes(
        NoteID INTEGER PRIMARY KEY,
        NoteName TEXT NOT NULL,
        NoteCategory TEXT
    )
""")


# Izveidot saites tabulu parfīm un <-> notas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PerfumeNotes(
        PerfumeID INTEGER NOT NULL,
        NoteID INTEGER NOT NULL,

        PRIMARY KEY (PerfumeID, NoteID),

        FOREIGN KEY (PerfumeID)
            REFERENCES Perfumes(PerfumeID),

        FOREIGN KEY (NoteID)
            REFERENCES FragranceNotes(NoteID)
    )
""")


# Izveidot tabulu ar valkāšanu
cursor.execute("""
    CREATE TABLE IF NOT EXISTS WearLog(
        WearID INTEGER PRIMARY KEY,
        PerfumeID INTEGER NOT NULL,
        WearDate TEXT NOT NULL,
        Occasion TEXT,
        Weather TEXT,
        SprayCount INTEGER,

        FOREIGN KEY (PerfumeID)
            REFERENCES Perfumes(PerfumeID)
    )
""")


# Izveidot tabulu ar vērtējumiem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ratings(
        RatingID INTEGER PRIMARY KEY,
        PerfumeID INTEGER NOT NULL,
        ScentScore INTEGER,
        LongevityScore INTEGER,
        ProjectionScore INTEGER,
        OverallScore INTEGER,
        Review TEXT,

        FOREIGN KEY (PerfumeID)
            REFERENCES Perfumes(PerfumeID)
    )
""")


# Izveidot tabulu ar sezonām
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Seasons(
        SeasonID INTEGER PRIMARY KEY,
        SeasonName TEXT NOT NULL
    )
""")


# Izveidot saites tabulu parfīmi un sezonas 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PerfumeSeasons(
        PerfumeID INTEGER NOT NULL,
        SeasonID INTEGER NOT NULL,

        PRIMARY KEY (PerfumeID, SeasonID),

        FOREIGN KEY (PerfumeID)
            REFERENCES Perfumes(PerfumeID),

        FOREIGN KEY (SeasonID)
            REFERENCES Seasons(SeasonID)
    )
""")


# Ievietot datus brendu tabulā
cursor.execute("""
    INSERT OR IGNORE INTO Brands(BrandID, BrandName, Country, FoundedYear)
    VALUES(1, 'Afnan', 'UAE', 2007)
""")

cursor.execute("""
    INSERT OR IGNORE INTO Brands(BrandID, BrandName, Country, FoundedYear)
    VALUES(2, 'Lattafa', 'UAE', 2012)
""")

cursor.execute("""
    INSERT OR IGNORE INTO Brands(BrandID, BrandName, Country, FoundedYear)
    VALUES(3, 'Dior', 'France', 1946)
""")




# Ievietot datus parfīmu tabulā
cursor.execute("""
    INSERT OR IGNORE INTO Perfumes(PerfumeID, BrandID, PerfumeName, Concentration, VolumeML, ReleaseYear, Price)
    VALUES(1, 1, '9 PM', 'EDP', 100, 2020, 30.00)
""")

cursor.execute("""
    INSERT OR IGNORE INTO Perfumes(PerfumeID, BrandID, PerfumeName, Concentration, VolumeML, ReleaseYear, Price)
    VALUES(2, 2, 'Khamrah', 'EDP', 100, 2022, 35.00)
""")

cursor.execute("""
    INSERT OR IGNORE INTO Perfumes(PerfumeID, BrandID, PerfumeName, Concentration, VolumeML, ReleaseYear, Price)
    VALUES(3, 3, 'Sauvage', 'EDT', 100, 2015, 90.00)
""")




# Ievietot datus notu tabulā
cursor.execute("""
    INSERT OR IGNORE INTO FragranceNotes(NoteID, NoteName, NoteCategory)
    VALUES(1, 'Vanilla', 'Base')
""")

cursor.execute("""
    INSERT OR IGNORE INTO FragranceNotes(NoteID, NoteName, NoteCategory)
    VALUES(2, 'Bergamot', 'Top')
""")

cursor.execute("""
    INSERT OR IGNORE INTO FragranceNotes(NoteID, NoteName, NoteCategory)
    VALUES(3, 'Rose', 'Middle')
""")

cursor.execute("""
    INSERT OR IGNORE INTO FragranceNotes(NoteID, NoteName, NoteCategory)
    VALUES(4, 'Musk', 'Base')
""")

cursor.execute("""
    INSERT OR IGNORE INTO FragranceNotes(NoteID, NoteName, NoteCategory)
    VALUES(5, 'Cinnamon', 'Middle')
""")



# Ievietot datus saites tabulā parfīmi un notas
cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(1, 1)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(1, 2)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(1, 4)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(2, 1)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(2, 5)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(3, 2)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeNotes(PerfumeID, NoteID)
    VALUES(3, 4)
""")




# Ievietot datus sezonu tabulā
cursor.execute("""
    INSERT OR IGNORE INTO Seasons(SeasonID, SeasonName)
    VALUES(1, 'Spring')
""")

cursor.execute("""
    INSERT OR IGNORE INTO Seasons(SeasonID, SeasonName)
    VALUES(2, 'Summer')
""")

cursor.execute("""
    INSERT OR IGNORE INTO Seasons(SeasonID, SeasonName)
    VALUES(3, 'Autumn')
""")

cursor.execute("""
    INSERT OR IGNORE INTO Seasons(SeasonID, SeasonName)
    VALUES(4, 'Winter')
""")




# Ievietot datus saites tabulā parfīmi un sezonas
cursor.execute("""
    INSERT OR IGNORE INTO PerfumeSeasons(PerfumeID, SeasonID)
    VALUES(1, 3)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeSeasons(PerfumeID, SeasonID)
    VALUES(1, 4)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeSeasons(PerfumeID, SeasonID)
    VALUES(2, 3)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeSeasons(PerfumeID, SeasonID)
    VALUES(2, 4)
""")

cursor.execute("""
    INSERT OR IGNORE INTO PerfumeSeasons(PerfumeID, SeasonID)
    VALUES(3, 2)
""")



# Ievietot datus valkāšana
cursor.execute("""
    INSERT OR IGNORE INTO WearLog(WearID, PerfumeID, WearDate, Occasion, Weather, SprayCount)
    VALUES(1, 1, '2026-10-01', 'School', 'Cold', 3)
""")

cursor.execute("""
    INSERT OR IGNORE INTO WearLog(WearID, PerfumeID, WearDate, Occasion, Weather, SprayCount)
    VALUES(2, 2, '2026-10-05', 'Work', 'Rainy', 2)
""")

cursor.execute("""
    INSERT OR IGNORE INTO WearLog(WearID, PerfumeID, WearDate, Occasion, Weather, SprayCount)
    VALUES(3, 1, '2026-10-08', 'Everyday', 'Sunny', 4)
""")



# Ievietot datus vērtējumu tabulā
cursor.execute("""
    INSERT OR IGNORE INTO Ratings(RatingID, PerfumeID, ScentScore, LongevityScore, ProjectionScore, OverallScore, Review)
    VALUES(1, 1, 9, 8, 8, 9, 'Sweet and warm')
""")

cursor.execute("""
    INSERT OR IGNORE INTO Ratings(RatingID, PerfumeID, ScentScore, LongevityScore, ProjectionScore, OverallScore, Review)
    VALUES(2, 2, 10, 9, 8, 9, 'Very rich fragrance')
""")

cursor.execute("""
    INSERT OR IGNORE INTO Ratings(RatingID, PerfumeID, ScentScore, LongevityScore, ProjectionScore, OverallScore, Review)
    VALUES(3, 3, 8, 9, 9, 9, 'Fresh and strong')
""")


# Saņemt datus no brendu tabulas

cursor.execute("""
    SELECT *
    FROM Brands
""")

brands = cursor.fetchall()

print("\nBRENDI")

for brand in brands:
    print(brand)


# Savienot tabulas un saņemt valkāšanas žurnāla datus

cursor.execute("""
    SELECT
        Perfumes.PerfumeName,
        WearLog.WearDate,
        WearLog.Occasion,
        WearLog.SprayCount
    FROM Perfumes

    JOIN WearLog
        ON WearLog.PerfumeID = Perfumes.PerfumeID
""")

wear_log = cursor.fetchall()

print("\nVALKĀŠANAS ŽURNĀLS")

for wear in wear_log:
    perfume_name = wear[0]
    wear_date = wear[1]
    occasion = wear[2]
    spray_count = wear[3]

    print(perfume_name, wear_date, occasion, spray_count)


# Savienot tabulas un saņemt katra parfīma notas

cursor.execute("""
    SELECT
        Perfumes.PerfumeName,
        FragranceNotes.NoteName,
        FragranceNotes.NoteCategory
    FROM PerfumeNotes

    JOIN Perfumes
        ON PerfumeNotes.PerfumeID = Perfumes.PerfumeID

    JOIN FragranceNotes
        ON PerfumeNotes.NoteID = FragranceNotes.NoteID
""")

notes = cursor.fetchall()

print("\nPARFĪMU NOTAS")

for note in notes:
    print(note)

database.commit()
database.close()

print("\nDatubāze parfumi.db ir gatava!")