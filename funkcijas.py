import sqlite3


def connect():
    database = sqlite3.connect("parfumi.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_brand(brand_name, country, founded_year):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO Brands (BrandName, Country, FoundedYear) VALUES (?,?,?)",
                   (brand_name, country, founded_year))
    database.commit()
    brand_id = cursor.lastrowid
    database.close()
    return brand_id


def add_perfume(brand_id, perfume_name, price):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO Perfumes (BrandID, PerfumeName, Price) VALUES (?,?,?)",
                   (brand_id, perfume_name, price))
    database.commit()
    perfume_id = cursor.lastrowid
    database.close()
    return perfume_id


def add_wear(perfume_id, wear_date, occasion):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO WearLog (PerfumeID, WearDate, Occasion) VALUES (?,?,?)",
                   (perfume_id, wear_date, occasion))
    database.commit()
    wear_id = cursor.lastrowid
    database.close()
    return wear_id


def add_rating(perfume_id, scent, longevity, projection, overall, review):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO Ratings (PerfumeID, ScentScore, LongevityScore, ProjectionScore, OverallScore, Review) VALUES (?,?,?,?,?,?)",
                   (perfume_id, scent, longevity, projection, overall, review))
    database.commit()
    rating_id = cursor.lastrowid
    database.close()
    return rating_id


def add_note(note_name, note_category):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO FragranceNotes (NoteName, NoteCategory) VALUES (?,?)",
                   (note_name, note_category))
    database.commit()
    note_id = cursor.lastrowid
    database.close()
    return note_id


def add_perfume_note(perfume_id, note_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT OR IGNORE INTO PerfumeNotes (PerfumeID, NoteID) VALUES (?,?)",
                   (perfume_id, note_id))
    database.commit()
    database.close()


def add_perfume_season(perfume_id, season_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT OR IGNORE INTO PerfumeSeasons (PerfumeID, SeasonID) VALUES (?,?)",
                   (perfume_id, season_id))
    database.commit()
    database.close()


def get_brand():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT BrandID, BrandName, Country, FoundedYear FROM Brands ORDER BY BrandID")
    brands = cursor.fetchall()
    database.close()
    return brands


def get_perfume():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT Perfumes.PerfumeID, Perfumes.PerfumeName, Brands.BrandName, Perfumes.Price FROM Perfumes JOIN Brands ON Perfumes.BrandID = Brands.BrandID ORDER BY Perfumes.PerfumeID")
    perfumes = cursor.fetchall()
    database.close()
    return perfumes


def get_wear():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT WearLog.WearID, Perfumes.PerfumeName, WearLog.WearDate, WearLog.Occasion FROM WearLog JOIN Perfumes ON WearLog.PerfumeID = Perfumes.PerfumeID ORDER BY WearLog.WearID")
    wear = cursor.fetchall()
    database.close()
    return wear


def get_note():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT NoteID, NoteName, NoteCategory FROM FragranceNotes ORDER BY NoteID")
    notes = cursor.fetchall()
    database.close()
    return notes


def get_season():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT SeasonID, SeasonName FROM Seasons ORDER BY SeasonID")
    seasons = cursor.fetchall()
    database.close()
    return seasons


def get_rating():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT Ratings.RatingID, Perfumes.PerfumeName, Ratings.ScentScore, Ratings.LongevityScore, Ratings.ProjectionScore, Ratings.OverallScore, Ratings.Review FROM Ratings JOIN Perfumes ON Ratings.PerfumeID = Perfumes.PerfumeID ORDER BY Ratings.RatingID")
    ratings = cursor.fetchall()
    database.close()
    return ratings


def get_perfume_note():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT Perfumes.PerfumeName, FragranceNotes.NoteName FROM PerfumeNotes JOIN Perfumes ON PerfumeNotes.PerfumeID = Perfumes.PerfumeID JOIN FragranceNotes ON PerfumeNotes.NoteID = FragranceNotes.NoteID ORDER BY Perfumes.PerfumeID")
    links = cursor.fetchall()
    database.close()
    return links


def get_perfume_season():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT Perfumes.PerfumeName, Seasons.SeasonName FROM PerfumeSeasons JOIN Perfumes ON PerfumeSeasons.PerfumeID = Perfumes.PerfumeID JOIN Seasons ON PerfumeSeasons.SeasonID = Seasons.SeasonID ORDER BY Perfumes.PerfumeID")
    links = cursor.fetchall()
    database.close()
    return links