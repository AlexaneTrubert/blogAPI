import time
import re
from collections import Counter
from classes.Database import Database

class Article:

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

    def is_valid(self):
        if self.title == None:
            return {"error": "Le titre ne peut pas être null"}
        
        if len(self.title) < 3:
            return {"error": "Le titre est trop court"}
        
        if len(self.title) > 75:
            return {"error": "Le titre est trop long"}
        
        if self.body == None:
            return {"error": "Le corps de l'article ne peut pas être null"}
        
        if len(self.body) < 3:
            return {"error": "Le corps de l'article est trop court"}
        
        return True
    
    def insert(self):
        try:
            Database.commit_bd(
                "INSERT INTO article(title, body) VALUES (?, ?)",
                (self.title, self.body)
            )
            return True
        except:
            return {"error": "Une erreur est survenue"}
        
    def save(self):
        try:
            Database.commit_bd(
                "UPDATE article SET title = ?, body = ?",
                (self.title, self.bbody)
            )
            return True
        except:
            return {"error": "Une erreur est survenue"}
        
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }
    
    @staticmethod
    def findOneById(id):
        article = Database.query_db("SELECT rowid, * FROM article WHERE rowid = ?", (id,))

        if len(article) != 1:
            return {"error": "Cet article n'existe pas"}
        
        article = Article(
            article[0]['rowid'],
            article[0]['title'],
            article[0]['body'],
        )

        return article