import sqlite3
from contextlib import contextmanager
from sqlite3 import Error
import time

class Database:
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance

    def create_table(self):
        with self.connect() as cursor:
            try:
                cursor.execute('CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, instructions TEXT, code TEXT, result TEXT, timestamp INTEGER)')
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Erstellen der Tabelle: {e}")

    @contextmanager
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            yield self.cursor
        except Error as e:
            print(f"Fehler bei der Verbindung zur Datenbank: {e}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def validate_entry(self, instructions, code, result):
        if not instructions or not code or not result:
            print("Ungültige Eingabe: Alle Felder müssen ausgefüllt sein.")
            return False

        # Weitere Validierungen können hier hinzugefügt werden.

        return True

    def create_entry(self, instructions, code, result,*args, **kwargs):
        if not self.validate_entry(instructions, code, result):
            return

        timestamp = int(time.time())

        with self.connect() as cursor:
            try:
                cursor.execute('INSERT INTO entries (instructions, code, result, timestamp) VALUES (?, ?, ?, ?)',
                                 (instructions, code, result, timestamp))
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Erstellen des Eintrags: {e}")

    def get_entries(self):
        with self.connect() as cursor:
            try:
                cursor.execute('SELECT * FROM entries')
                return cursor.fetchall()
            except Error as e:
                print(f"Fehler beim Abrufen der Einträge: {e}")
                return []

    def delete_entry(self, entry_id):
        with self.connect() as cursor:
            try:
                cursor.execute('DELETE FROM entries WHERE id=?', (entry_id,))
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Löschen des Eintrags: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
