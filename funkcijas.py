import sqlite3
def connect():
    database = sqlite3.connect("parfumi.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_brand(brand_name, country, founded_year):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO Brands (BrandName, Country, FoundedYear) VALUES (?,?,?)",
                       (brand_name, country, founded_year))
        database.commit()
        brand_id = cursor.lastrowid
    finally:
        database.close()
    return brand_id


def add_perfume(brand_id, perfume_name, price):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO Perfumes (BrandID, PerfumeName, Price) VALUES (?,?,?)",
                       (brand_id, perfume_name, price))
        database.commit()
        perfume_id = cursor.lastrowid
    finally:
        database.close()
    return perfume_id


def add_wear(perfume_id, wear_date, occasion):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO WearLog (PerfumeID, WearDate, Occasion) VALUES (?,?,?)",
                       (perfume_id, wear_date, occasion))
        database.commit()
        wear_id = cursor.lastrowid
    finally:
        database.close()
    return wear_id


def add_rating(perfume_id, scent, longevity, projection, overall, review):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO Ratings (PerfumeID, ScentScore, LongevityScore, ProjectionScore, OverallScore, Review) VALUES (?,?,?,?,?,?)",
                       (perfume_id, scent, longevity, projection, overall, review))
        database.commit()
        rating_id = cursor.lastrowid
    finally:
        database.close()
    return rating_id


def add_note(note_name, note_category):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO FragranceNotes (NoteName, NoteCategory) VALUES (?,?)",
                       (note_name, note_category))
        database.commit()
        note_id = cursor.lastrowid
    finally:
        database.close()
    return note_id


def add_perfume_note(perfume_id, note_id):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO PerfumeNotes (PerfumeID, NoteID) VALUES (?,?)",
                       (perfume_id, note_id))
        database.commit()
    finally:
        database.close()


def add_perfume_season(perfume_id, season_id):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO PerfumeSeasons (PerfumeID, SeasonID) VALUES (?,?)",
                       (perfume_id, season_id))
        database.commit()
    finally:
        database.close()



def get_brand():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT BrandID, BrandName, Country, FoundedYear FROM Brands ORDER BY BrandID")
        brands = cursor.fetchall()
    finally:
        database.close()
    return brands


def get_perfume():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT Perfumes.PerfumeID, Perfumes.PerfumeName, Brands.BrandName, Perfumes.Price FROM Perfumes JOIN Brands ON Perfumes.BrandID = Brands.BrandID ORDER BY Perfumes.PerfumeID")
        perfumes = cursor.fetchall()
    finally:
        database.close()
    return perfumes


def get_wear():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT WearLog.WearID, Perfumes.PerfumeName, WearLog.WearDate, WearLog.Occasion FROM WearLog JOIN Perfumes ON WearLog.PerfumeID = Perfumes.PerfumeID ORDER BY WearLog.WearID")
        wear = cursor.fetchall()
    finally:
        database.close()
    return wear


def get_note():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT NoteID, NoteName, NoteCategory FROM FragranceNotes ORDER BY NoteID")
        notes = cursor.fetchall()
    finally:
        database.close()
    return notes


def get_season():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT SeasonID, SeasonName FROM Seasons ORDER BY SeasonID")
        seasons = cursor.fetchall()
    finally:
        database.close()
    return seasons


def get_rating():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT Ratings.RatingID, Perfumes.PerfumeName, Ratings.ScentScore, Ratings.LongevityScore, Ratings.ProjectionScore, Ratings.OverallScore, Ratings.Review FROM Ratings JOIN Perfumes ON Ratings.PerfumeID = Perfumes.PerfumeID ORDER BY Ratings.RatingID")
        ratings = cursor.fetchall()
    finally:
        database.close()
    return ratings


def get_perfume_note():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT Perfumes.PerfumeName, FragranceNotes.NoteName FROM PerfumeNotes JOIN Perfumes ON PerfumeNotes.PerfumeID = Perfumes.PerfumeID JOIN FragranceNotes ON PerfumeNotes.NoteID = FragranceNotes.NoteID ORDER BY Perfumes.PerfumeID")
        links = cursor.fetchall()
    finally:
        database.close()
    return links


def get_perfume_season():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT Perfumes.PerfumeName, Seasons.SeasonName FROM PerfumeSeasons JOIN Perfumes ON PerfumeSeasons.PerfumeID = Perfumes.PerfumeID JOIN Seasons ON PerfumeSeasons.SeasonID = Seasons.SeasonID ORDER BY Perfumes.PerfumeID")
        links = cursor.fetchall()
    finally:
        database.close()
    return links

def delete_perfume_rows(cursor, perfume_id):
    total = 0
    cursor.execute("DELETE FROM WearLog WHERE PerfumeID = ?", (perfume_id,))
    total += cursor.rowcount
    cursor.execute("DELETE FROM Ratings WHERE PerfumeID = ?", (perfume_id,))
    total += cursor.rowcount
    cursor.execute("DELETE FROM PerfumeNotes WHERE PerfumeID = ?", (perfume_id,))
    total += cursor.rowcount
    cursor.execute("DELETE FROM PerfumeSeasons WHERE PerfumeID = ?", (perfume_id,))
    total += cursor.rowcount
    cursor.execute("DELETE FROM Perfumes WHERE PerfumeID = ?", (perfume_id,))
    total += cursor.rowcount
    return total


def delete_brand(*values):
    brand_id = int(values[0])
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT PerfumeID FROM Perfumes WHERE BrandID = ?", (brand_id,))
        perfumes = cursor.fetchall()
        total = 0
        for row in perfumes:
            total += delete_perfume_rows(cursor, row[0])
        cursor.execute("DELETE FROM Brands WHERE BrandID = ?", (brand_id,))
        total += cursor.rowcount
        database.commit()
    finally:
        database.close()
    return total


def delete_perfume(*values):
    perfume_id = int(values[0])
    database = connect()
    cursor = database.cursor()
    try:
        total = delete_perfume_rows(cursor, perfume_id)
        database.commit()
    finally:
        database.close()
    return total


def delete_wear(*values):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM WearLog WHERE WearID = ?", (int(values[0]),))
        database.commit()
        deleted = cursor.rowcount
    finally:
        database.close()
    return deleted


def delete_rating(*values):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM Ratings WHERE RatingID = ?", (int(values[0]),))
        database.commit()
        deleted = cursor.rowcount
    finally:
        database.close()
    return deleted


def delete_note(*values):
    note_id = int(values[0])
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM PerfumeNotes WHERE NoteID = ?", (note_id,))
        total = cursor.rowcount
        cursor.execute("DELETE FROM FragranceNotes WHERE NoteID = ?", (note_id,))
        total += cursor.rowcount
        database.commit()
    finally:
        database.close()
    return total


def delete_season(*values):
    season_id = int(values[0])
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM PerfumeSeasons WHERE SeasonID = ?", (season_id,))
        total = cursor.rowcount
        cursor.execute("DELETE FROM Seasons WHERE SeasonID = ?", (season_id,))
        total += cursor.rowcount
        database.commit()
    finally:
        database.close()
    return total


def delete_perfume_note(*values):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM PerfumeNotes WHERE PerfumeID = (SELECT PerfumeID FROM Perfumes WHERE PerfumeName = ?) AND NoteID = (SELECT NoteID FROM FragranceNotes WHERE NoteName = ?)",
                       (values[0], values[1]))
        database.commit()
        deleted = cursor.rowcount
    finally:
        database.close()
    return deleted


def delete_perfume_season(*values):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("DELETE FROM PerfumeSeasons WHERE PerfumeID = (SELECT PerfumeID FROM Perfumes WHERE PerfumeName = ?) AND SeasonID = (SELECT SeasonID FROM Seasons WHERE SeasonName = ?)",
                       (values[0], values[1]))
        database.commit()
        deleted = cursor.rowcount
    finally:
        database.close()
    return deleted


def search_all(teksts):
    database = connect()
    cursor = database.cursor()
    try:
        like = "%" + teksts + "%"
        results = []

        cursor.execute("SELECT BrandID, BrandName, Country, FoundedYear FROM Brands WHERE BrandName LIKE ? OR Country LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            results.append(("Brendi", row[0], str(row[1]) + " — " + str(row[2]) + ", " + str(row[3])))


        cursor.execute("SELECT Perfumes.PerfumeID, Perfumes.PerfumeName, Brands.BrandName, Perfumes.Price FROM Perfumes JOIN Brands ON Perfumes.BrandID = Brands.BrandID WHERE Perfumes.PerfumeName LIKE ? OR Brands.BrandName LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            results.append(("Parfīmi", row[0], str(row[1]) + " — " + str(row[2]) + ", " + str(row[3]) + " EUR"))

        cursor.execute("SELECT WearLog.WearID, Perfumes.PerfumeName, WearLog.WearDate, WearLog.Occasion FROM WearLog JOIN Perfumes ON WearLog.PerfumeID = Perfumes.PerfumeID WHERE Perfumes.PerfumeName LIKE ? OR WearLog.Occasion LIKE ? OR WearLog.WearDate LIKE ?",
                       (like, like, like))
        for row in cursor.fetchall():
            parts = str(row[2]).split("-")
            if len(parts) == 3:
                datums = parts[2] + "-" + parts[1] + "-" + parts[0]
            else:
                datums = str(row[2])
            results.append(("Žurnāls", row[0], str(row[1]) + " — " + datums + " (" + str(row[3]) + ")"))

        cursor.execute("SELECT Ratings.RatingID, Perfumes.PerfumeName, Ratings.OverallScore, Ratings.Review FROM Ratings JOIN Perfumes ON Ratings.PerfumeID = Perfumes.PerfumeID WHERE Perfumes.PerfumeName LIKE ? OR Ratings.Review LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            review = str(row[3])
            if review == "None":
                review = ""
            results.append(("Vērtējumi", row[0], str(row[1]) + " — kopā " + str(row[2]) + " (" + review + ")"))

        cursor.execute("SELECT NoteID, NoteName, NoteCategory FROM FragranceNotes WHERE NoteName LIKE ? OR NoteCategory LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            results.append(("Notas", row[0], str(row[1]) + " (" + str(row[2]) + ")"))

        cursor.execute("SELECT SeasonID, SeasonName FROM Seasons WHERE SeasonName LIKE ?", (like,))
        for row in cursor.fetchall():
            results.append(("Sezonas", row[0], str(row[1])))

        cursor.execute("SELECT Perfumes.PerfumeName, FragranceNotes.NoteName FROM PerfumeNotes JOIN Perfumes ON PerfumeNotes.PerfumeID = Perfumes.PerfumeID JOIN FragranceNotes ON PerfumeNotes.NoteID = FragranceNotes.NoteID WHERE Perfumes.PerfumeName LIKE ? OR FragranceNotes.NoteName LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            results.append(("Parfīmu notas", "", str(row[0]) + " + " + str(row[1])))


        cursor.execute("SELECT Perfumes.PerfumeName, Seasons.SeasonName FROM PerfumeSeasons JOIN Perfumes ON PerfumeSeasons.PerfumeID = Perfumes.PerfumeID JOIN Seasons ON PerfumeSeasons.SeasonID = Seasons.SeasonID WHERE Perfumes.PerfumeName LIKE ? OR Seasons.SeasonName LIKE ?",
                       (like, like))
        for row in cursor.fetchall():
            results.append(("Parfīmu sezonas", "", str(row[0]) + " + " + str(row[1])))

        return results
    finally:
        database.close()