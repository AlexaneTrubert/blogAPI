from datetime import datetime
from classes.Database import Database

class Commentaire:

    def __init__(self, id, article_id, name, comment, ts):
        self.id = id
        self.article_id = article_id
        self.name = name
        self.comment = comment
        self.ts = ts

    def is_valid(self):
        if self.comment == None:
            return {"error": "Le commentaire ne peut pas être null"}

        if len(self.comment) < 3:
            return {"error": "Le commentaire est trop court"}

        return True

    def insert(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            Database.commit_bd(
                "INSERT INTO comments(article_id, comment, ts) VALUES (?, ?, ?)",
                (self.article_id, self.comment, formatted_date)
            )
            return True
        except:
            return {"error": "Une erreur est survenue"}

    def to_json(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "name": self.name,
            "comment": self.comment,
            "ts": self.ts
        }
