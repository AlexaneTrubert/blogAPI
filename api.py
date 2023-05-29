from flask import Flask, request
from flask_cors import CORS
import time
from classes.Database import Database
from classes.Article import Article

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return "<h1>API d'un super blog (ou pas)</h1>"


@app.route("/articles", methods=['GET'])
def list():
    articles = Database.query_db('SELECT rowid, * FROM article')

    articleObjs = [Article(
        article['rowid'],
        article['title'],
        article['body'],
    ).to_json() for article in articles]

    return {
        "ts": int(round(time.time()*100)),
        "articles": articleObjs
    }

@app.route("/articles/id", methods=['GET'])
def get():
    id = request.args.get('id', None)
    article = Database.query_db('SELECT rowid, * FROM article WHERE rowid = ?', (id))

    if len(article) < 1:
        return {"error": "L'id n'existe pas"}
    article = article[0]

    articleObj = Article(
        article['rowid'],
        article['title'],
        article['body']
    )

    return {"success": True, "data": articleObj.to_json()}

@app.route("/post", methods=['POST'])
def add_article():
    title = request.form.get('title', None)
    body = request.form.get('body', None)

    article = Article(None, title, body)

    if not article.is_valid():
        return article.is_valid()
    
    if article.insert():
        return {"success": True}
    
    return {"error": "Une erreur est survenue"}

@app.errorhandler(404)
def not_found(error):
    return 'Error', 404
