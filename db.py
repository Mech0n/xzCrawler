from os.path import exists
from sqlite3 import Connection


class db:
    def __init__(self):
        self.database_path = "database.db"
        if exists(self.database_path):
            self.conn = Connection(self.database_path, check_same_thread=False)
        else:
            self.conn = Connection(self.database_path, check_same_thread=False)
            self.__create_schema()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def __create_schema(self):
        schema = """create table main (
            id int primary key,
            title text unique not null,
            indexed bool not null
        );"""
        try:
            cur = self.conn.cursor()
            cur.execute(schema)
        finally:
            cur.close()

    def add(self, values: tuple):
        """values : ('id', 'title', 'indexed')"""
        try:
            cur = self.conn.cursor()
            cur.execute("insert into main values (?, ?, ?)", values)
            self.conn.commit()
        finally:
            cur.close()

    def delete(self, values: tuple):
        """values : ('id',)"""
        try:
            cur = self.conn.cursor()
            cur.execute("delete from main where id=?", values)
            self.conn.commit()
        finally:
            cur.close()

    def indexed(self, values: tuple):
        """values : ('indexed', 'id')"""
        try:
            cur = self.conn.cursor()
            cur.execute("update main set indexed=? where id=?", values)
            self.conn.commit()
        finally:
            cur.close()

    def update_title(self, values: tuple):
        """values : ('title', 'id')"""
        try:
            cur = self.conn.cursor()
            cur.execute("update main set title=? where id=?", values)
            self.conn.commit()
        finally:
            cur.close()

    def query(self, values):
        """
        values : ('id',)
        return [{'id': 1, 'title': 'www.balala.com', 'indexed': 1}]
        """
        try:
            cur = self.conn.cursor()
            query_res = cur.execute("select * from main where id=?", values)
            self.conn.commit()
        except Exception as e:
            print(f"db.query : {e}")
            res = []
            return res
        else:
            res = []
            for cow in query_res:
                element = {}
                element["id"] = cow[0]
                element["title"] = cow[1]
                element["indexed"] = cow[2]
                res.append(element)
            cur.close()
            return res

    def query_all_new_content(self):
        """
        values : ('id',)
        return [{'id': 1, 'title': 'www.balala.com', 'indexed': 1}]
        """
        try:
            cur = self.conn.cursor()
            query_res = cur.execute("select * from main where indexed=?", (False,))
            self.conn.commit()
        except Exception as e:
            print(f"db.query : {e}")
            res = []
            return res
        else:
            res = []
            for cow in query_res:
                element = {}
                element["id"] = cow[0]
                element["title"] = cow[1]
                element["indexed"] = cow[2]
                res.append(element)
            cur.close()
            return res


if __name__ == "__main__":
    database = db()
    # add
    # database.add((1, 'www.balala.com', 1))
    # database.add((12, 'www.balalaa.com', 1))
    # indexed
    # database.indexed((False, 1))
    # delete
    # database.delete((400,))
    # database.update_title(('asdasdas', 400))
    # query
    print(database.query_all())
