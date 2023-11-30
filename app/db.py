from dataclasses import dataclass
from enum import Enum
from operator import itemgetter
from typing import Callable
from typing import NamedTuple

import psycopg2
from faker import Faker
from psycopg2 import sql

fake = Faker()


def init_db(conn):
    with conn.cursor() as curs, open("init.sql") as file:
        curs.execute(file.read())
    conn.commit()


@dataclass(slots=True)
class SelectDescriptor:
    key: str
    table: str
    fake_factory: Callable


class Person(NamedTuple):
    firstname: int
    lastname: int
    surname: int
    city: int
    street: int
    building: str
    phone: str


class SelectDescriptorsEnum(Enum):
    firstnames = SelectDescriptor(key="firstname", table="Firstnames", fake_factory=fake.first_name)
    lastnames = SelectDescriptor(key="lastname", table="Lastnames", fake_factory=fake.last_name)
    surnames = SelectDescriptor(key="surname", table="Surnames", fake_factory=lambda: fake.passport_owner()[1])
    cities = SelectDescriptor(key="city", table="Cities", fake_factory=fake.city)
    streets = SelectDescriptor(key="street", table="Streets", fake_factory=fake.street_name)


def iter_datalist(conn, desc: SelectDescriptorsEnum, size: int = 50):
    with conn.cursor() as cursor:
        cursor.execute(sql.SQL(f"SELECT {desc.value.key} FROM {desc.value.table} ORDER BY RANDOM() LIMIT %s"), (size,))
        yield from map(itemgetter(0), cursor.fetchall())


def get_table_items(conn, page: int, search: str = '', page_size: int = 50):
    with conn.cursor() as cursor:
        cursor.execute("SELECT firstname, lastname, surname, Cities.city, Streets.street, building, phone, Persons.id "
                       "FROM Persons "
                       "JOIN Firstnames ON fname=Firstnames.id "
                       "JOIN Lastnames ON lname=Lastnames.id "
                       "JOIN Surnames ON sname=Surnames.id "
                       "JOIN Cities ON Persons.city=Cities.id "
                       "JOIN Streets ON Persons.street=Streets.id "
                       "WHERE (firstname || ' ' || lastname || ' ' || surname || ' ' || Cities.city || ' ' || Streets.street || ' ' || building || ' ' || phone) ~* %(search)s "
                       "LIMIT %(page_size)s OFFSET %(offset)s", {"search": search, "page_size": page_size, "offset": page_size * page})
        return cursor.fetchall()


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


def delete_person(conn, person_id) -> bool:
    with conn.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM Persons WHERE id=%s", (person_id,))
            conn.commit()
        except (BaseException, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
            return False
    return True
