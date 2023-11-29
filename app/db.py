from enum import Enum
from dataclasses import dataclass, asdict
from typing import NamedTuple
import psycopg2
from psycopg2 import sql
from operator import itemgetter


def init_db(conn):
    with conn.cursor() as curs, open("init.sql") as file:
        curs.execute(file.read())
    conn.commit()


@dataclass(slots=True)
class SelectDescriptor:
    key: str
    table: str


class Person(NamedTuple):
    firstname: int
    lastname: int
    surname: int
    city: int
    street: int
    building: str
    phone: str


class SelectDescriptorsEnum(Enum):
    firstnames = SelectDescriptor(key="firstname", table="Firstnames")
    lastnames = SelectDescriptor(key="lastname", table="Lastnames")
    surnames = SelectDescriptor(key="surname", table="Surnames")
    cities = SelectDescriptor(key="city", table="Cities")
    street = SelectDescriptor(key="street", table="Streets")


def get_list(conn, t: SelectDescriptorsEnum):
    with conn.cursor() as cursor:
        cursor.execute(sql.SQL(f"SELECT %(key)s FROM {t.value.table} ORDER BY %(key)s"), asdict(t.value))
        return cursor.fetch_all()


def replace_vals_by_ids(cursor, values):
    for desc in SelectDescriptorsEnum:
        val = desc.value
        if val.key not in values:
            continue
        cursor.execute(
            sql.SQL(f"SELECT id FROM {val.table} WHERE {val.key} = %s LIMIT 1"),
            (values[val.key],))
        if item_id := cursor.fetchone():
            values[val.key] = item_id
            continue
        cursor.execute(
            sql.SQL(f"INSERT INTO {val.table}({val.key}) VALUES (%s) RETURNING id"),
            (values[val.key],))
        values[val.key] = cursor.fetchone()


def add_person(conn, values) -> bool:
    with conn.cursor() as cursor:
        try:
            replace_vals_by_ids(cursor, values)
            cursor.execute(
                "INSERT INTO Persons(fname, lname, sname, city, street, building, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                itemgetter('firstname', 'lastname', 'surname', 'city', 'street', 'building', 'phone')(values)
            )
            conn.commit()
        except (BaseException, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
            return False
    return True
