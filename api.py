from flask import Flask, request
from flask_cors import CORS
import time
from classes.Database import Database
from classes.Article import Article
from classes.Commentaire import Commentaire

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return "<h1>API d'un super blog (ou pas)</h1>"


# On s'occupe des articles / facesnaps
@app.route("/facesnaps", methods=['GET'])
def list():
    articles = Database.query_db('SELECT rowid, * FROM article')

    articleObjs = [Article(
        article['rowid'],
        article['title'],
        article['description'],
        article['createdDate'],
        article['snaps'],
        article['imageUrl'],
        article['location']
    ).to_json() for article in articles]

    return {
        "facesnaps": articleObjs,
        "ts": int(round(time.time()*100))
    }

@app.route("/facesnaps/<id>", methods=['GET'])
def get(id):
    article = Database.query_db('SELECT rowid, * FROM article WHERE rowid = ?', (id))
    commentaires = Database.query_db('SELECT rowid, * FROM comments WHERE article_id = ?', (id))

    if len(article) < 1:
        return {"error": "L'id n'existe pas"}

    article = article[0]
    commentaires = commentaires[0]

    articleObj = Article(
        article['rowid'],
        article['title'],
        article['description'],
        article['createdDate'],
        article['snaps'],
        article['imageUrl'],
        article['location'],
    )

    commentairesObjs = Commentaire(
        commentaires['rowid'],
        commentaires['article_id'],
        commentaires['name'],
        commentaires['comment'],
        commentaires['ts'],
    )

    return {"success": True, "facesnap": articleObj.to_json(), "comment": commentairesObjs.to_json()}

@app.route("/facesnaps", methods=['POST'])
def add_article():
    title = request.form.get('title', None)
    description = request.form.get('description', None)
    createdDate = time.strftime('%Y-%m-%d %H:%M:%S')
    snaps = 0
    imageUrl = request.form.get('imageUrl', None)
    location = request.form.get('location', None)

    article = Article(None, title, description, createdDate, snaps, imageUrl, location)

    if not article.is_valid():
        return article.is_valid()
    
    if article.insert():
        return {"success": True}
    
    return {"error": "Une erreur est survenue"}

@app.route("/facesnaps/<id>/snaps", methods=["PUT"])
def add_snap(id):

    article = Article.findOneById(id)

    if not isinstance(article, Article):
        return {"error": "Cet article n'existe pas"}

    result = article.add_snap()
    if not result == True:
        return result

    return {"success": True}

@app.route("/facesnaps/<id>/snaps", methods=["DELETE"])
def remove_snap(id):

    article = Article.findOneById(id)

    if not isinstance(article, Article):
        return {"error": "Cet article n'existe pas"}

    result = article.remove_snap()
    if not result == True:
        return result

    return {"success": True}


# On s'occupe des commentaires
@app.route("/commentaires/<id>", methods=['GET'])
def listCommentaires(id):
    commentaires = Database.query_db('SELECT rowid, * FROM comments WHERE article_id = ?', (id))

    commentairesObjs = [Commentaire(
        commentaire['rowid'],
        commentaire['article_id'],
        commentaire['name'],
        commentaire['comment'],
        commentaire['ts']
        ).to_json() for commentaire in commentaires]

    return {
        "commentaires": commentairesObjs,
        "ts": int(round(time.time()*100))
        }

@app.route("/commentaires/<id>", methods=['POST'])
def add_commentaire(id):
    comment = request.form.get('comment', None)
    article_id = id

    commentaire = Commentaire(None, article_id, comment, None)

    if not commentaire.is_valid():
        return commentaire.is_valid()

    if commentaire.insert():
        return {"success": True}

@app.errorhandler(404)
def not_found(error):
    return 'Error', 404
