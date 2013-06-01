import logging
import sqlite3

class DB(object):
    """Set and get state for a given item"""
    def __init__(self):
        """Instantiates a database if none exists"""
        # instantiate logger
        self.log = logging.getLogger('bridgebeam')
        # open sqlite db (yes this is gross... it's hackday!)
        db_path='/opt/bridgebeam/bridgebeam.db'
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_schema()

    def _create_schema(self):
        """Create the schema for our sqlite3 db""" 
        self.cursor.execute("CREATE TABLE IF NOT EXISTS conferences (uuid text, name text, conference_sid text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS calls (sid text, phone_number text, conference_uuid text)")
        self.conn.commit()

    def get_conference_uuid(self, name):
        q = "SELECT uuid FROM conferences WHERE name=?"
        r = self.cursor.execute(q, (name,)).fetchone()
        try:
            conference_uuid = r[0]
        except TypeError as e:
            self.log.error(e)
            conference_uuid = None
        return conference_uuid

    def get_conference_name(self, uuid):
        self.log.info('looking up conference by uuid: {}'.format(uuid))
        q = "SELECT name FROM conferences WHERE uuid='{}'".format(uuid)
        self.log.info('query: {}'.format(q))
        r = self.cursor.execute(q).fetchone()
        try:
            conference_name = r[0]
        except TypeError as e:
            self.log.error(e)
            conference_name = None
        return conference_name

    def get_conferences(self):
        q = "SELECT name, phone_number FROM conferences, calls WHERE conferences.uuid = calls.conference_uuid"
        rows = self.cursor.execute(q).fetchall()
        conferences = {}
        for conference_name, phone_number in rows:
            if conference_name in conferences.keys():
                conferences[conference_name].append(phone_number)
            else:
                conferences[conference_name] = [phone_number,]
        return conferences
                

    def create_conference(self, uuid=None, name=None):
        if uuid and name:
            q = "INSERT INTO conferences (uuid, name) VALUES (?, ?)" 
            self.cursor.execute(q, (uuid, name))
            self.conn.commit()

    def add_to_conference(self, call_sid=None, conference_uuid=None, phone_number=None):
        if conference_uuid and call_sid and phone_number:
            q = "INSERT INTO calls (sid, phone_number, conference_uuid) VALUES (?, ?, ?)"
            self.cursor.execute(q, (call_sid, phone_number, conference_uuid))
            self.conn.commit()

    def remove_call(self, call_sid):
        if call_sid:
            q = "DELETE FROM calls WHERE sid='{}'".format(call_sid) 
            self.cursor.execute(q)
            self.conn.commit()
    def destroy(self):
        self.cursor.close()
