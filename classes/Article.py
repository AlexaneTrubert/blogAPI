from datetime import datetime
from classes.Database import Database

class Article:

    def __init__(self, id, title, description, createdDate, snaps, imageUrl, location):
        self.id = id
        self.title = title
        self.description = description
        self.createdDate = createdDate
        self.snaps = snaps
        self.imageUrl = imageUrl
        self.location = location

    def is_valid(self):
        if self.title == None:
            return {"error": "Le titre ne peut pas être null"}
        
        if len(self.title) < 3:
            return {"error": "Le titre est trop court"}
        
        if len(self.title) > 75:
            return {"error": "Le titre est trop long"}
        
        if self.description == None:
            return {"error": "Le corps de l'article ne peut pas être null"}
        
        if len(self.description) < 3:
            return {"error": "Le corps de l'article est trop court"}
        
        return True
    
    def insert(self):

        now = datetime.now()

        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            Database.commit_bd(
                "INSERT INTO article(title, description, createdDate, snaps, imageUrl, location) VALUES (?, ?, ?, 0, ?, ?)",
                (self.title, self.description, formatted_date, self.imageUrl, self.location)
            )
            return True
        except:
            return {"error": "Une erreur est survenue"}

    def update(self):
        try:
            Database.commit_bd(
                "UPDATE article SET title = ?, description = ?, imageUrl = ?, location = ?, snaps = ? WHERE rowid = ?",
                (self.title, self.description, self.imageUrl, self.location, self.snaps, self.id)
            )
            return True
        except:
            return {"error": "Une erreur est survenue"}
        
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "imageUrl": self.imageUrl,
            "createdDate": self.createdDate,
            "snaps": self.snaps,
            "location": self.location
        }

    def add_snap(self):
        self.snaps += 1
        return self.update()
    
    @staticmethod
    def findOneById(id):
        article = Database.query_db("SELECT rowid, * FROM article WHERE rowid = ?", (id,))

        if len(article) != 1:
            return {"error": "Cet article n'existe pas"}
        
        article = Article(
            article[0]['rowid'],
            article[0]['title'],
            article[0]['description'],
            article[0]['createdDate'],
            article[0]['snaps'],
            article[0]['imageUrl'],
            article[0]['location']
        )

        return article