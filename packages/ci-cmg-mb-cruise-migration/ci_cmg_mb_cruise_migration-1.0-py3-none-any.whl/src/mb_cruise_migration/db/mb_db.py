import oracledb

from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties


class MbDb(object):
    def __init__(self):
        config = MigrationProperties.mb_db_config
        self.connection = self.connection(config)
        self.cursor = self.connection.cursor()

    @staticmethod
    def connection(config):
        dsn_string = oracledb.makedsn(config.server, config.port, sid=config.sid, service_name=config.service)
        try:
            return oracledb.connect(
              user=config.user,
              password=config.password,
              dsn=dsn_string
            )
        except Exception as e:
            MigrationLog.log_exception(e)
            print("WARNING DB failed to connect. Script closing", e)
            raise e

    def query(self, command, data=None):
        if data:
            result = self.cursor.execute(command, data)
        else:
            result = self.cursor.execute(command)

        return result

    def fetch_one(self, command, data=None, row_factory=True):
        result = self.query(command, data=data)
        names = [c[0] for c in result.description]
        row = result.fetchone()
        if row_factory and row:
            return self.row_factory(names, row)[0]
        else:
            return row

    def fetch_all(self, command, data=None, row_factory=True):
        result = self.query(command, data=data)
        names = [c[0] for c in result.description]
        rows = result.fetchall()
        if row_factory and rows:
            return self.row_factory(names, rows)
        else:
            return rows

    def execute(self, command, data=None):
        self.cursor.execute(command, data)

    def update(self, command, data):
        self.cursor.execute(command, data)

    def insert(self, command, data):
        self.cursor.execute(command, data)

    def columns(self, command=None):
        if command:
            self.cursor.execute(command)
        names = [c[0] for c in self.cursor.description]
        return names

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def row_factory(names, data):
        #  Create list of dictionaries of query results with filed name as keys.
        row_list = []
        if not isinstance(data, list):
            data = [data]
        for row in data:
            row_dict = {}
            temp_map = zip(names, row)
            for item in temp_map:
                row_dict[item[0]] = item[1]
            row_list.append(row_dict)

        return row_list
