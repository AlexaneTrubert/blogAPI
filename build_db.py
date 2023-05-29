import sqlite3
con = sqlite3.connect("datas/blog.db")
cur = con.cursor()

cur.execute("CREATE TABLE article (title VARCHAR(75) NOT NULL, body TEXT NOT NULL)")

cur.execute("CREATE TABLE comments (article_id INT, name VARCHAR(16) NOT NULL, comment VARCHAR(255) NOT NULL, ts INT, CONSTRAINT `fk_article_id` FOREIGN KEY(`article_id`) REFERENCES `article`(`id`))")

cur.execute("CREATE TABLE users (username VARCHAR(30) NOT NULL, password VARCHAR(250) NOT NULL, jwt TEXT)")
