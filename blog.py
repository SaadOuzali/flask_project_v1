import mysql.connector
from mysql.connector import Error
from db import MysqlConnector
from helpers import db_config


class Blog:
    def __init__(self, id=None, title=None, content=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    
    @staticmethod
    def get_connection():
        return MysqlConnector(**db_config).connection()
    

    @staticmethod
    def get_all_blogs():
      conn = Blog.get_connection()
      cursor = conn.cursor(dictionary=True)  # returns rows as dicts

      cursor.execute("SELECT * FROM blog ORDER BY id DESC")
      blogs = cursor.fetchall()

      cursor.close()
      conn.close()

      return blogs
   
    
    # INSERT NEW BLOG
   
    def save(self):
        conn = Blog.get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO blog (title, content) VALUES (%s, %s)"
        cursor.execute(query, (self.title, self.content))
        conn.commit()

        self.id = cursor.lastrowid

        cursor.close()
        conn.close()
        return self.id

   
    # GET BLOG BY ID
   
    @staticmethod
    def get(blog_id):
        conn = Blog.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM blog WHERE id = %s", (blog_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        print(row)
        if row:
            return Blog(**row)
        return None

    
    # UPDATE BLOG
    @staticmethod
    def update(self):
        conn = Blog.get_connection()
        cursor = conn.cursor()

        query = "UPDATE blog SET title = %s, content = %s WHERE id = %s"
        cursor.execute(query, (self.title, self.content, self.id))
        conn.commit()

        cursor.close()
        conn.close()

   
    # DELETE BLOG
       
    @staticmethod
    def delete(self):
        conn = Blog.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM blog WHERE id = %s", (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
