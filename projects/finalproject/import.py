import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    f = open("cities.csv")
    reader = csv.reader(f)

    for row in reader:

        db.execute("INSERT INTO cities (city, state, population, latitude, longitude) VALUES (:a, :b, :c, :d, :e)",
                    {"a": row[0], "b": row[1], "c": row[2], "d": row[3], "e": row[4]})
        print("Added cities successfully!")

    db.commit()

if __name__ == "__main__":
    main()
