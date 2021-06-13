from flask import Flask, render_template, request #Flaskの操作に必要なモジュールをインポート
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String #DBのテーブルの型をインポート
import os

#Flaskの立ち上げ
app = Flask(__name__,static_folder='app/static', template_folder='app/templates')
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.sqlite' # DBへのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#SQLAlchemyでデータベース定義
db = SQLAlchemy(app)


#SQLiteのDBテーブル情報
class FLASKDB(db.Model):
    __tablename__ = 'flask_table'

    ID = db.Column(Integer, primary_key=True)
    YOURNAME = db.Column(String(32))

#DBの作成
db.create_all()


#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")
def top():
    return render_template("top.html")


#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/topics", methods = ['POST', 'GET'])
def topic():
    if request.method == 'POST':
        yourname = request.form['yourname']
        flask = FLASKDB(YOURNAME=yourname)
        db.session.add(flask)
        db.session.commit()
        db.session.close()
        FLASKDB_infos = db.session.query(FLASKDB.ID, FLASKDB.YOURNAME).all()
        return render_template('topics.html', FLASKDB_infos=FLASKDB_infos)
    else:
        FLASKDB_infos = db.session.query(FLASKDB.ID, FLASKDB.YOURNAME).all()
        return render_template('topics.html', FLASKDB_infos=FLASKDB_infos)


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/detail")
def detail():
    return render_template('detail.html')


#おまじない
if __name__ == "__main__":
    port = int(os.getenv("PORT"))

    app.run(host="0.0.0.0", port=port, threaded=True)
