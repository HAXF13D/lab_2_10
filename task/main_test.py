#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import main
from datetime import datetime
import sqlite3
import os
from random import choice, randint
from string import ascii_lowercase, digits, ascii_uppercase


class TrainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("Настройка класса")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("Снос класса")

    def setUp(self):
        """Set up for test"""
        print("Настройка для [" + self.shortDescription() + "]")
        print("Создание тестовой базы данных...")

    def tearDown(self):
        """Tear down for test"""
        print("Снос для [" + self.shortDescription() + "]")
        os.remove('test.db')
        print("Тестовая база данных была удалена")

    def test_select_all(self):
        """The whole selection test"""
        con = sqlite3.connect('test.db')
        cur = con.cursor()

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS types(
                type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                train_type TEXT NOT NULL
            )
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS departures(
                departure_id INTEGER PRIMARY KEY AUTOINCREMENT,
                train_number INTEGER NOT NULL,
                destination TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                time DATE,
                FOREIGN KEY(type_id) REFERENCES types(type_id)
            )
            '''
        )
        db_list = []
        num_of_records = randint(2, 10)

        print(f"Количество записей: {num_of_records}")

        for _ in range(num_of_records):
            train_types = ('Cargo', 'Passenger', 'Construction')
            ##################################################################
            letters = ascii_lowercase
            length = randint(1, 15)

            destination = ''.join(choice(letters) for i in range(length))

            number = randint(1, 100)

            train_type = choice(train_types)

            time = ''.join(str(randint(10, 23)) +
                           ":" + str(randint(10, 59)))

            ans = {
                'destination': destination,
                'number': number,
                'train_type': train_type,
                'time': datetime.strptime(time, '%H:%M'),
            }

            print(ans)
            db_list.append(ans)

            cursor = con.cursor()

            cursor.execute(
                """
                SELECT type_id FROM types WHERE train_type = ?
                """,
                (train_type,)
            )
            row = cursor.fetchone()

            if row is None:
                cursor.execute(
                    """
                    INSERT INTO types (train_type) VALUES (?)
                    """,
                    (train_type,)
                )
                type_id = cursor.lastrowid
            else:
                type_id = row[0]

            cursor.execute(
                """
                INSERT INTO departures (train_number, destination, type_id, time)
                VALUES (?, ?, ?, ?)
                """,
                (number, destination, type_id, time)
            )

            con.commit()

        self.assertListEqual(main.select_all('test.db'), db_list)
        con.close()

    def test_select_by_type(self):
        """Selection test"""
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS types(
                type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                train_type TEXT NOT NULL
            )
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS departures(
                departure_id INTEGER PRIMARY KEY AUTOINCREMENT,
                train_number INTEGER NOT NULL,
                destination TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                time DATE,
                FOREIGN KEY(type_id) REFERENCES types(type_id)
            )
            '''
        )

        train_types = ('Cargo', 'Passenger', 'Construction')
        ##################################################################
        letters = ascii_lowercase
        length = randint(1, 15)

        destination = ''.join(choice(letters) for i in range(length))

        number = randint(1, 100)

        train_type = choice(train_types)

        time = ''.join(str(randint(10, 23)) +
                       ":" + str(randint(10, 59)))

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT type_id FROM types WHERE train_type = ?
            """,
            (train_type,)
        )
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                """
                INSERT INTO types (train_type) VALUES (?)
                """,
                (train_type,)
            )
            type_id = cursor.lastrowid
        else:
            type_id = row[0]

        cursor.execute(
            """
            INSERT INTO departures (train_number, destination, type_id, time)
            VALUES (?, ?, ?, ?)
            """,
            (number, destination, type_id, time)
        )
        conn.commit()

        ans = [
            {
                'destination': destination,
                'number': number,
                'train_type': train_type,
                'time': datetime.strptime(time, '%H:%M'),
            }
        ]
        print(ans)
        test_data = 'select ' + ''.join(str(time))
        self.assertListEqual(
            main.select(test_data, 'test.db'), ans
        )
        conn.close()
