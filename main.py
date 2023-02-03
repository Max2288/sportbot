# This is a sample Python script.
import datetime
import logging
import random
import psycopg2
from db_exceptions import UserException, PlaceException, TrainingException, DnevnikException

DATABASE = "sportbot_db"
USER = "sportbot_user"
PASSWORD = "user"
HOST = "127.0.0.1"
PORT = "5432"


def init_database():
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(open("init.sql", "r").read())


def create_place(name: str):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO tgbot_place(name) VALUES (%s)",
                    (name,))
        logging.info(f"place created ")


def get_place(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        if id:
            cur.execute(f"SELECT * FROM tgbot_place WHERE id = {id}")
            return cur.fetchone()[1]
        else:
            return None


def create_training(name: str, lvl: int, gender: str, type: str,
                    description: str, muscle_group: str, places_id: list):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO tgbot_training(name, lvl,gender,type,description,muscle_group) "
                    f"VALUES (%s, %s,%s, %s,%s, %s) RETURNING id;",
                    (name, lvl, gender, type, description, muscle_group))
        training_id = cur.fetchone()[0]
        logging.info(f"training with id =  {training_id} created ")
        for place_id in places_id:
            cur.execute(f"SELECT id FROM tgbot_place WHERE id = {place_id}")
            if cur.fetchone() is None:
                raise ValueError(f"Place with id = {place_id} not found")
            else:
                cur.execute(f"INSERT INTO tgbot_training_places(place_id,training_id) VALUES (%s, %s)",
                            (place_id, training_id))


def set_dnevnik(date, user_id, trainings_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO tgbot_dnevnik(date, user_id) "
                    f"VALUES (%s, %s) RETURNING id;", (date, user_id))
        dnevnik_id = cur.fetchone()[0]
        logging.info(f"dnevnik with id =  {dnevnik_id} created ")
        for training_id in trainings_id:
            cur.execute(f"SELECT id FROM tgbot_training WHERE id = {training_id}")
            if cur.fetchone() is None:
                raise ValueError(f"training with id = {training_id} not found")
            else:
                cur.execute(f"INSERT INTO tgbot_dnevnik_trainings(dnevnik_id,training_id) VALUES (%s, %s)",
                            (dnevnik_id, training_id))


def create_user(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:

            cur.execute(f"INSERT INTO tgbot_user (id, name) VALUES (%s, %s)", (user_id, user_name))
            logging.info(f"User with id = {user_id} successfully registered")
        else:
            logging.info(f"User with id = {user_id} already registered")


def get_user_info(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute(f"select  name, age, height, weight, gender, lvl, "
                        f"training_goal, place_id from tgbot_user where id = {user_id}")
            user = cur.fetchone()
            return {
                "name": user[0],
                "age": user[1],
                "height": user[2],
                "weight": user[3],
                "gender": user[4],
                "lvl": user[5],
                "training_goal": user[6],
                "place_id": user[7],
            }

def get_trainings_id(muscle_group: str, count=1, user_id=None):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"select place_id from tgbot_user where id = {user_id}")

        user_place = cur.fetchone()[0]
        if user_place is None:
            user_place = "place_id"

        cur.execute(f"select id from tgbot_dnevnik where user_id = {user_id} order by date DESC")
        user_dnevnik = cur.fetchone()
        if user_dnevnik:
            user_dnevnik = user_dnevnik[0]
        else:
            user_dnevnik = 'null'

        cur.execute(f"select id from tgbot_training where muscle_group = '{muscle_group}' \
                    and id in (select training_id from tgbot_training_places where place_id =  {user_place}) "
                    f"and id not in (select training_id from tgbot_dnevnik_trainings where dnevnik_id = {user_dnevnik} )")

        trainings_all = [el[0] for el in cur.fetchall()]
        random.shuffle(trainings_all)
        return trainings_all[:count]

def get_trainings(ids):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        trainings = []
        for id in ids:
            cur.execute(f"SELECT name, description FROM tgbot_training WHERE id = {id}")
            row = cur.fetchone()
            trainings.append("<a href='{}'>{}</a>".format(row[1], row[0]))
        return trainings


def set_user_name(user_id, name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute(f"update tgbot_user set name = %s where id = %s", (name, user_id))
            logging.info(f"User with id = {user_id} updated")


def set_user_age(user_id, age: int):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set age = %s where id = %s", (age, user_id))
            logging.info(f"User with id = {user_id} updated")

def set_user_height(user_id, height: int):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set height = %s where id = %s", (height, user_id))
            logging.info(f"User with id = {user_id} updated")

def set_user_lvl(user_id, lvl: int):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set lvl = %s where id = %s", (lvl, user_id))
            logging.info(f"User with id = {user_id} updated")


def set_user_gender(user_id, gender: str):
    if gender == "Мужской":
        gender = 'M'
    else:
        gender = 'F'
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set gender = %s where id = %s", (gender, user_id))
            logging.info(f"User with id = {user_id} updated")


def set_user_training_task(user_id, training_goal: str):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set training_goal = %s where id = %s", (training_goal, user_id))
            logging.info(f"User with id = {user_id} updated")


def set_user_weight(user_id, weight: float):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute("update tgbot_user set weight = %s where id = %s", (weight, user_id))
            logging.info(f"User with id = {user_id} updated")


def set_user_place(user_id, place_id: id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        else:
            cur.execute(f"SELECT * FROM tgbot_place WHERE id = {place_id}")
            if cur.fetchone() is None:
                raise PlaceException(f"place with id = {place_id} not found")
            else:
                cur.execute(f"update tgbot_user set place_id = {place_id} where id = {user_id}")
                logging.info(f"User with id = {user_id} updated")


def create_dnevnik(user_id: int):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()
        cur.execute("INSERT INTO tgbot_dnevnik (date, user_id) VALUES (%s, %s) returning id", (datetime.datetime.now(), user_id))
        dnevnik_id = cur.fetchone()[0]

        return dnevnik_id
def add_training_to_dnevnik(dnevnik_id, training_id, start_time):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_training WHERE id = {training_id}")
        if cur.fetchone() is None:
            raise TrainingException()
        cur.execute(f"SELECT * FROM tgbot_dnevnik WHERE id = {dnevnik_id}")
        if cur.fetchone() is None:
            raise DnevnikException()
        cur.execute(f"INSERT INTO tgbot_dnevnik_trainings (dnevnik_id, training_id, start_training) VALUES (%s, %s, %s) returning id", (dnevnik_id, training_id, start_time))
        id = cur.fetchone()[0]

        return id


def get_user_dnevniks(user_id, count=7):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_user WHERE id = {user_id}")
        if cur.fetchone() is None:
            raise UserException()

        cur.execute(f"select id from tgbot_dnevnik where user_id = {user_id} order by date DESC limit {count}")
        dnevniks = [el[0] for el in cur.fetchall()]

        return dnevniks

def get_trainings_name_in_dnevnik(dnevnik_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM tgbot_dnevnik WHERE id = {dnevnik_id}")
        if cur.fetchone() is None:
            raise DnevnikException()
        cur.execute(f"select training_id from tgbot_dnevnik_trainings WHERE dnevnik_id = {dnevnik_id} ORDER BY start_training")
        ids = cur.fetchall()
        nm = []
        for id in ids:
            cur.execute(f"SELECT name from tgbot_training WHERE id = {id[0]}")
            nm.append(cur.fetchall())
        names = [el[0][0] for el in nm]
        return names

def get_dnevnik_date(dnevnik_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM tgbot_dnevnik WHERE id = {dnevnik_id}")
        if cur.fetchone() is None:
            raise DnevnikException()
        cur.execute(f"SELECT date FROM tgbot_dnevnik WHERE id = {dnevnik_id}")
        return cur.fetchone()[0]

def set_training_end_time(dnevnik_id, training_id, end_time):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tgbot_training WHERE id = {training_id}")
        if cur.fetchone() is None:
            raise TrainingException()
        cur.execute(f"SELECT * FROM tgbot_dnevnik WHERE id = {dnevnik_id}")
        if cur.fetchone() is None:
            raise DnevnikException()
        cur.execute("UPDATE tgbot_dnevnik_trainings SET end_training = (%s) WHERE dnevnik_id = (%s) and training_id = (%s)", (end_time, dnevnik_id, training_id, ))