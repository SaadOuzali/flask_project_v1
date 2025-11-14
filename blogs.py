from mysql.connector import Error
from db import MysqlConnector
from helpers import db_config,db_config_env
from translate import Translator
from gtts import gTTS


class Blog:
    def __init__(
        self, id=None, title=None, content=None, created_at=None, updated_at=None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_connection():
        """Get a new DB connection."""
        return MysqlConnector(**db_config_env).connection()

    # GET ALL BLOGS
    @staticmethod
    def get_all_blogs():
        conn = None
        cursor = None
        try:
            conn = Blog.get_connection()
            cursor = conn.cursor(dictionary=True)  # returns rows as dicts

            cursor.execute("SELECT * FROM blog ORDER BY id DESC")
            blogs = cursor.fetchall()

            return blogs

        except Error as e:
            print("DB Error in get_all_blogs:", e)
            raise Error(str(e))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # INSERT NEW BLOG
    def save(self):
        conn = None
        cursor = None
        try:
            conn = Blog.get_connection()
            cursor = conn.cursor()

            query = "INSERT INTO blog (title, content) VALUES (%s, %s)"
            cursor.execute(query, (self.title, self.content))
            conn.commit()

            self.id = cursor.lastrowid
            return self.id

        except Error as e:
            print("DB Error in save:", e)
            if conn is not None:
                conn.rollback()
                raise Error(str(e))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # GET BLOG BY ID

    def get_by_Id(self):
        print("ana bdit")
        if self.id is None:
            print("Cannot translate blog without id")
            return False

        conn = None
        cursor = None
        try:
            conn = Blog.get_connection()
            cursor = conn.cursor(dictionary=True)
            print("dwzha")
            cursor.execute("SELECT * FROM blog WHERE id = %s", (self.id,))
            row = cursor.fetchone()
            print(f"my row is : {row}")

            if row:
                return Blog(**row), True
            return None, False

        except Error as e:

            print("DB Error in get:", e)
            raise Error(str(e))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # UPDATE BLOG
    def update(self):
        if self.id is None:
            print("Cannot update blog without id")
            return False
        conn = None
        cursor = None
        try:
            conn = Blog.get_connection()
            cursor = conn.cursor()

            query = "UPDATE blog SET title = %s, content = %s WHERE id = %s"
            cursor.execute(query, (self.title, self.content, self.id))
            conn.commit()

            return cursor.rowcount > 0  # True if something was updated

        except Error as e:
            print("DB Error in update:", e)
            if conn is not None:
                conn.rollback()
            raise Error(str(e))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # DELETE BLOG
    def delete(self):
        if self.id is None:
            print("⚠ Cannot delete blog without id")
            return False

        conn = None
        cursor = None
        try:
            conn = Blog.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM blog WHERE id = %s", (self.id,))
            conn.commit()

            return cursor.rowcount > 0  # True if a row was deleted

        except Error as e:
            print("DB Error in delete:", e)
            if conn is not None:
                conn.rollback()
                raise Error(str(e))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # translate blog
    def translate(self, source_lang="en", target_lang="fr"):

        try:

            translator = Translator(from_lang=source_lang, to_lang=target_lang)
            translated_text = translator.translate(self.content)
            return translated_text

        except Exception as e:
            raise Exception(str(e))
            


    def translate_and_generate_audio(self, source_lang, target_lang):

        try:

            translated_text = self.translate(
                source_lang=source_lang, target_lang=target_lang
            )
            
            if translated_text:
                tts = gTTS(text=translated_text, lang=target_lang, slow=False)
                audio_file = f"blog_{self.id}.mp3"
                tts.save(audio_file)
                return translated_text

        except Exception as e:
            raise Exception(str(e))
            
