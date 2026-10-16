import sqlite3

def connect():
    database = sqlite3.connect("parfumi.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database

def add_brand(brand_name, country, founded_year):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO Brands (BrandName, Country, FoundedYear) VALUES (?,?,?)", (brand_name, country, founded_year))
    database.commit()
    brand_id = cursor.lastrowid
    database.close()
    return brand_id

def add_perfume(brand_id, perfume_name, price):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO Perfumes (BrandID, PerfumeName, Price) VALUES (?,?,?)", (brand_id, perfume_name, price))
    database.commit()
    perfume_id = cursor.lastrowid
    database.close()
    return perfume_id

def add_wear(perfume_id, wear_date, occasion):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO WearLog (PerfumeID, WearDate, Occasion) VALUES (?,?,?)", (perfume_id, wear_date, occasion))
    database.commit()
    wear_id = cursor.lastrowid
    database.close()
    return wear_id

def get_brand():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT BrandID, BrandName, Country, FoundedYear FROM Brands")
    brands = cursor.fetchall()
    database.close()
    return brands

def get_perfume():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
        SELECT
            Perfumes.PerfumeID,
            Perfumes.PerfumeName,
            Brands.BrandName,
            Perfumes.Price
        FROM Perfumes

        JOIN Brands
            ON Perfumes.BrandID = Brands.BrandID
        ORDER BY Perfumes.PerfumeID
    """)
    perfumes = cursor.fetchall()
    database.close()
    return perfumes

def get_wear():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
        SELECT
            WearLog.WearID,
            Perfumes.PerfumeName,
            WearLog.WearDate,
            WearLog.Occasion
        FROM WearLog

        JOIN Perfumes
            ON WearLog.PerfumeID = Perfumes.PerfumeID
        ORDER BY WearLog.WearID
    """)
    wear = cursor.fetchall()
    database.close()
    return wear