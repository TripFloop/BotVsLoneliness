import sqlite3
import typing


class Database:

    def __init__(self, path_to_db='main.db'):
        self.path_do_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_do_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        try:
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        except sqlite3.OperationalError:
            sql = self.create_tables()
            connection.commit(sql)
        connection.close()
        return data

    def get_all_voice_messages(self, owner: str):
        sql = f"""
         SELECT 
             * 
         FROM
             voice_messages_from_{owner}
         """
        return self.execute(sql, fetchall=True)

    def add_voice_message(self, owner: str, file_id: str, comment: str = None):
        sql = f"""
         INSERT 
         INTO 
             voice_messages_from_{owner}
             (file_id, comment) 
         VALUES
             (?, ?)
         """
        self.execute(sql, parameters=(file_id, comment), commit=True)

    def delete_voice_message(self, voice_message_id: int, owner: str):
        sql = f"""
        DELETE FROM
            voice_messages_from_{owner}
        WHERE
            voice_message_id={voice_message_id}
        """
        self.execute(sql, commit=True)

    def get_voice_message(self, voice_message_id: int, owner: str):
        sql = f"""
        SELECT
            file_id, comment
        FROM
            voice_messages_from_{owner}
        WHERE
            voice_message_id = {voice_message_id}
        """
        data = self.execute(sql, fetchone=True)
        file_id, comment = data
        return file_id, comment

    def add_text(self, text: str, owner: str, iserotic: bool):
        sql = f"""
        INSERT 
        INTO
            texts_to_pic_from_{owner}
            (text, iserotic)         
        VALUES
            (?, ?)
        """
        self.execute(sql, parameters=(text, iserotic), commit=True)

    def get_rand_text(self, from_name: str, iserotic: bool):
        if iserotic is True:
            iserotic = 1
        else:
            iserotic = 0
        sql = f"""
        SELECT
            text           
        FROM
            Texts_to_pic           
        WHERE
            from_name = {from_name}               
            AND iserotic = {iserotic}         
        ORDER   BY
            RANDOM()         LIMIT 1
        """
        return self.execute(sql, fetchone=True)

    def add_pic(self, owner: str, file_id: str, iserotic: bool = False):
        if iserotic is True:
            iserotic = 1
        else:
            iserotic = 0
        sql = """
          INSERT 
          INTO 
            pics
                (owner, file_id, iserotic) 
            VALUES 
                (?, ?, ?)
          """
        self.execute(sql, parameters=(owner, file_id, iserotic), commit=True)

    def get_rand_pic(self, owner: str, iserotic: bool):
        string_from_db = self.execute(
            sql=f"""
        SELECT 
            *
        FROM 
            pics
        WHERE 
            owner = {owner}
            AND iserotic = {iserotic}
        ORDER BY 
            RANDOM()
        LIMIT 1
            """,
            fetchone=True)
        return string_from_db[0][3]

    def delete_text(self, text_id: int, owner: str):
        sql = f"""
           DELETE
           FROM texts_to_pic_from_{owner}
           WHERE text_id = {text_id}
           """
        self.execute(sql, commit=True)

    def delete_film(self, film_id: int):
        sql = f"""
           DELETE
           FROM films
           WHERE film_id = {film_id}
           """
        self.execute(sql, commit=True)

    def add_film(self, film_name: str, comment: str = None):
        sql = f"""
           INSERT
           INTO
               films
               (film_name, comment)
           VALUES
               (?, ?)
           """
        self.execute(sql, parameters=(film_name, comment), commit=True)

    def get_all_text(self, owner: str):
        return self.execute(sql=f"SELECT * FROM texts_to_pic_from_{owner}", fetchall=True)

    def get_all_films(self):
        return self.execute(sql=f"SELECT * FROM films", fetchall=True)

    def get_all_music(self):
        return self.execute(sql=f"SELECT * FROM music", fetchall=True)

    def get_all_pics(self, owner: str):
        return self.execute(sql=f"SELECT * FROM pics WHERE owner={owner}", fetchall=True)

    def get_text(self, owner: str, text_id: int):
        text = self.execute(sql=f"SELECT text FROM texts_to_pic_from_{owner} WHERE text_id = {text_id}", fetchone=True)
        return str(text[0])

    def get_slice_of_texts(self, owner: str, page: int = 1):
        offset = 10 * (page - 1)
        sql = f"""
        SELECT
            *
        FROM
            texts_to_pic_from_{owner}
        LIMIT
            10
        OFFSET 
            {offset}
        """
        # logging.info(sql)
        data = self.execute(sql, fetchall=True)
        # pprint(data)
        return data

    def get_slice_of_voice_messages(self, owner: str, page: int = 1):
        offset = 10 * (page - 1)
        sql = f"""
        SELECT
            *
        FROM
            voice_messages_from_{owner}
        LIMIT
            10
        OFFSET 
            {offset}
        """
        return self.execute(sql, fetchall=True)

    def get_slice_of_films(self, page: int = 1):
        offset = 10 * (page - 1)
        sql = f"""
        SELECT
            *
        FROM
            films
        LIMIT
            10
        OFFSET 
            {offset}
        """
        return self.execute(sql, fetchall=True)

    def count_number_of_rows_in_table(self, what_table: str, owner: str = None):
        table = ""
        if what_table == "texts_to_pic":
            if owner == "leila":
                table = what_table + "_from_" + owner
            elif owner == "sasha":
                table = what_table + "_from_" + owner
        elif what_table == "voice_messages":
            if owner == "leila":
                table = what_table + "_from_" + owner
            elif owner == "sasha":
                table = what_table + "_from_" + owner
        elif what_table == "pics":
            table = what_table
        elif what_table == "music":
            table = what_table
        elif what_table == "films":
            table = what_table

        sql = f"""
        SELECT
            COUNT(*)
        FROM
            {table}
        """

        if what_table == "pics":
            sql = f"""
            SELECT
                COUNT(owner)
            FROM
                pics
            WHERE
                owner = '{owner}'
                """
        return self.execute(sql=sql, fetchone=True)

    def get_rand_voice_message(self, owner: str):
        sql = f"""
        SELECT
            file_id
        FROM
            voice_messages_from_{owner}
        ORDER BY 
            RANDOM()
        LIMIT 1
        """
        data = self.execute(sql=sql, fetchone=True)
        return data

    def add_music(self, music_mood_type: str, file_id: str, music_name: str, duration: int):
        sql = f"""
        INSERT INTO
            music
                (file_id, music_name, duration, music_mood_type)
            VALUES
                (?,?,?,?)
        """
        self.execute(sql, parameters=(file_id, music_name, duration, music_mood_type), commit=True)

    def get_pic(self, owner: str, page: int = 1):
        offset = page - 1
        sql = f"""
        SELECT
            pic_id, file_id, iserotic
        FROM
            pics
        WHERE
            owner = '{owner}'
        LIMIT 1
        OFFSET {offset}
        """
        data = self.execute(sql, fetchone=True)
        if data is None:
            return None
        return data[0], data[1], data[2]

    def set_cooldown(self, owner: str, time_trigger: typing.Union[int, float]):
        data_sql = f"""
        SELECT
            *
        FROM
            is_got
        WHERE who = "{owner}"
        """
        data = self.execute(data_sql, fetchone=True)
        if data is None:
            sql = f"""
            INSERT
            INTO
                is_got
                (who, time_trigger)
                VALUES
                (?, ?)
            """
            self.execute(sql, parameters=(owner, time_trigger), commit=True)
        else:
            sql = f"""
            UPDATE is_got
            SET time_trigger = {time_trigger}
            WHERE who = "{owner}"
            """
            self.execute(sql, commit=True)

    def check_voice_avaliable(self,
                              owner: str,
                              time_trigger: typing.Union[int, float],
                              cooldown: typing.Union[int, float] = 3600) -> bool:
        time_from_db = int(self.execute(f"SELECT time_trigger FROM is_got WHERE who = '{owner}'", fetchone=True)[0])
        delta = time_trigger - time_from_db
        if delta >= cooldown:
            return True
        else:
            return False

    def return_delta(self,
                     owner: str,
                     time_trigger: typing.Union[int, float]
                     ) -> typing.Union[int, float]:
        time_from_db = int(self.execute(f"SELECT time_trigger FROM is_got WHERE who = '{owner}'", fetchone=True)[0])
        return time_trigger - time_from_db

    def delete_pic(self,
                   pic_id: int):
        self.execute(f"DELETE FROM pics WHERE pic_id = {pic_id}", commit=True)

    def get_slice_of_music_by_mood(self, mood: str, page: int = 1):
        offset = 10 * (page - 1)
        sql = f"""
        SELECT
            *
        FROM
            music
        WHERE
            music_mood_type = "{mood}"
        LIMIT
            10
        OFFSET 
            {offset}
        """
        # logging.info(sql)
        data = self.execute(sql, fetchall=True)
        # pprint(data)
        return data

    def get_music(self, music_id: str):
        sql = f"""
        SELECT
            file_id, duration
        FROM
            music
        WHERE
            music_id = "{music_id}"
        """
        file_id, duration = self.execute(sql, fetchone=True)
        return file_id, duration

    def get_film(self, film_id: int):
        sql = f"""
        SELECT
            film_name, comment
        FROM
            films
        WHERE
            film_id = "{film_id}"
        """
        film_name, comment = self.execute(sql, fetchone=True)
        return film_name, comment

    def delete_music(self, music_id):
        sql = f"""
        DELETE FROM
            music
        WHERE
            music_id = "{music_id}"
        """
        self.execute(sql, commit=True)
        
    def create_tables(self):
        sql =        """CREATE TABLE "films" (
                        "film_id"	INTEGER NOT NULL UNIQUE,
                        "film_name"	TEXT NOT NULL,
                        "comment"	TEXT,
                        PRIMARY KEY("film_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "is_got" (
                        "who"	TEXT NOT NULL UNIQUE,
                        "time_trigger"	INTEGER
                        );
                        CREATE TABLE "music" (
                        "music_id"	INTEGER NOT NULL UNIQUE,
                        "music_mood_type"	TEXT NOT NULL,
                        "file_id"	INTEGER NOT NULL UNIQUE,
                        "music_name"	TEXT NOT NULL,
                        "duration"	TEXT NOT NULL,
                        PRIMARY KEY("music_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "pics" (
                        "pic_id"	INTEGER NOT NULL UNIQUE,
                        "owner"	TEXT NOT NULL,
                        "iserotic"	INTEGER NOT NULL,
                        "file_id"	TEXT NOT NULL UNIQUE,
                        PRIMARY KEY("pic_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "texts_to_pic_from_leila" (
                        "text_id"	INTEGER NOT NULL UNIQUE,
                        "text"	TEXT NOT NULL UNIQUE,
                        "iserotic"	INTEGER NOT NULL,
                        PRIMARY KEY("text_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "texts_to_pic_from_sasha" (
                        "text_id"	INTEGER NOT NULL UNIQUE,
                        "text"	TEXT NOT NULL UNIQUE,
                        "iserotic"	INTEGER NOT NULL,
                        PRIMARY KEY("text_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "voice_messages_from_leila" (
                        "voice_message_id"	INTEGER NOT NULL UNIQUE,
                        "file_id"	TEXT NOT NULL UNIQUE,
                        "comment"	TEXT,
                        PRIMARY KEY("voice_message_id" AUTOINCREMENT)
                        );
                        CREATE TABLE "voice_messages_from_sasha" (
                        "voice_message_id"	INTEGER NOT NULL,
                        "file_id"	TEXT NOT NULL UNIQUE,
                        "comment"	TEXT NOT NULL,
                        PRIMARY KEY("voice_message_id" AUTOINCREMENT)
                        )
                        """
        return sql

