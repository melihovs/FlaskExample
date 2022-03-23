from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
from config_db import host, user, password, db_name

app = Flask(__name__)
app.secret_key = "melihov-sergey-secret-key"


def db_connect():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )


# **************************************
# **           Home Page              **
# **************************************
@app.route("/")
def index():
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = "SELECT * FROM article_types"
    cur.execute(s)  # Execute the SQL
    list_article_types = cur.fetchall()

    s = "SELECT * FROM author"
    cur.execute(s)  # Execute the SQL
    list_author = cur.fetchall()

    s = "SELECT * FROM magazines"
    cur.execute(s)  # Execute the SQL
    list_magazines = cur.fetchall()

    s = "SELECT * FROM articles"
    cur.execute(s)  # Execute the SQL
    list_articles = cur.fetchall()

    cur.close()
    db_connect().close()

    return render_template('index.html', list_article_types=list_article_types, list_author=list_author,
                           list_magazines=list_magazines, list_articles=list_articles)


# **************************************
# ** working with Article Types Table **
# **************************************
@app.route("/article_types")
def article_types():
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = "SELECT * FROM article_types  ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_article_types = cur.fetchall()

    cur.close()
    db_connect().close()
    return render_template('article_types.html', list_article_types=list_article_types)


@app.route('/add_article_type', methods=['POST'])
def add_article_type():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        arttype = request.form['arttype']
        print(arttype)
        cur.execute("INSERT INTO article_types (type) VALUES (%s)", (arttype,))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('article_types'))


@app.route('/edit_article_type/<id>', methods=['POST', 'GET'])
def edit_article_type(id):
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM article_types WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    db_connect().close()
    print(data)
    return render_template('edit_article_type.html', article_data=data[0])


@app.route('/update_article_type/<id>', methods=['POST'])
def update_article_type(id):
    if request.method == 'POST':
        arttype = request.form['arttype']
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE article_types SET type = %s WHERE id = %s", (arttype, id))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('article_types'))


@app.route('/delete_article_type/<id>', methods=['POST', 'GET'])
def delete_article_type(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM article_types WHERE id = %s", (id,))
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('article_types'))


# **************************************
# **   working with Articles Table    **
# **************************************
@app.route("/articles")
def articles():
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = "SELECT * FROM article_types ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_article_types = cur.fetchall()

    s = "SELECT * FROM author ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_author = cur.fetchall()

    s = "SELECT * FROM magazines ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_magazines = cur.fetchall()

    s = "SELECT * FROM articles ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_articles = cur.fetchall()

    cur.close()
    db_connect().close()

    return render_template('articles.html', list_article_types=list_article_types, list_author=list_author,
                           list_magazines=list_magazines, list_articles=list_articles)


@app.route('/add_article', methods=['POST'])
def add_article():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        magazine_id = request.form['magazine-id']
        arttype_id = request.form['arttype-id']
        author_id = request.form['author-id']
        cur.execute("INSERT INTO articles (magazines_id, article_type_id, author_id) VALUES (%s,%s,%s)", (magazine_id,
                                                                                                          arttype_id,
                                                                                                          author_id))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('articles'))


@app.route('/edit_article/<id>', methods=['POST', 'GET'])
def edit_article(id):
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM articles WHERE id = %s', (id,))
    data = cur.fetchall()

    s = "SELECT * FROM article_types ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_article_types = cur.fetchall()

    s = "SELECT * FROM author ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_author = cur.fetchall()

    s = "SELECT * FROM magazines ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_magazines = cur.fetchall()

    s = "SELECT * FROM articles ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_articles = cur.fetchall()

    cur.close()
    db_connect().close()
    return render_template('edit_article.html', article_data=data[0], list_article_types=list_article_types,
                           list_author=list_author, list_magazines=list_magazines, list_articles=list_articles)


@app.route('/update_article/<id>', methods=['POST'])
def update_article(id):
    if request.method == 'POST':
        magazine_id = request.form['magazine-id']
        arttype_id = request.form['arttype-id']
        author_id = request.form['author-id']

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE articles SET magazines_id = %s, article_type_id = %s, author_id = %s WHERE id = %s",
                    (magazine_id, arttype_id, author_id, id))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('articles'))


@app.route('/delete_article/<id>', methods=['POST', 'GET'])
def delete_article(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM articles WHERE id = %s", (id,))
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('articles'))


# **************************************
# **   working with Author Table      **
# **************************************
@app.route("/authors")
def authors():
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = "SELECT * FROM author  ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_authors = cur.fetchall()

    cur.close()
    db_connect().close()
    return render_template('authors.html', list_authors=list_authors)


@app.route('/add_author', methods=['POST'])
def add_author():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        author = request.form['author']
        cur.execute("INSERT INTO author (author) VALUES (%s)", (author,))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('authors'))


@app.route('/edit_author/<id>', methods=['POST', 'GET'])
def edit_author(id):
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM author WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    db_connect().close()
    return render_template('edit_author.html', author_data=data[0])


@app.route('/update_author/<id>', methods=['POST'])
def update_author(id):
    if request.method == 'POST':
        author = request.form['author']
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE author SET author = %s WHERE id = %s", (author, id))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('authors'))


@app.route('/delete_author/<id>', methods=['POST', 'GET'])
def delete_author(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM author WHERE id = %s", (id,))
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('authors'))


# **************************************
# **   working with Magazine Table    **
# **************************************
@app.route("/magazines")
def magazines():
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    s = "SELECT * FROM magazines  ORDER BY id"
    cur.execute(s)  # Execute the SQL
    list_magazines = cur.fetchall()

    cur.close()
    db_connect().close()
    return render_template('magazines.html', list_magazines=list_magazines)


@app.route('/add_magazine', methods=['POST'])
def add_magazine():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        magazine = request.form['magazine']
        cur.execute("INSERT INTO magazines (name) VALUES (%s)", (magazine,))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('magazines'))


@app.route('/edit_magazine/<id>', methods=['POST', 'GET'])
def edit_magazine(id):
    cur = db_connect().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM magazines WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    db_connect().close()
    return render_template('edit_magazine.html', magazine_data=data[0])


@app.route('/update_magazine/<id>', methods=['POST'])
def update_magazine(id):
    if request.method == 'POST':
        magazine = request.form['magazine']
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE magazines SET name = %s WHERE id = %s", (magazine, id))
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('magazines'))


@app.route('/delete_magazine/<id>', methods=['POST', 'GET'])
def delete_magazine(id):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM magazines WHERE id = %s", (id,))
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('magazines'))


@app.route("/hello")
def test():
    #return "<h1>Hello EPAM1</h1>"
    return render_template('hello.html')


@app.route('/reset_to_default', methods=['POST', 'GET'])
def reset_to_default():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    # the cursor for performing database operations
    curs = connection.cursor()
    curs.execute(
        "SELECT version();"
    )
    print(f"Server version: {curs.fetchone()}")

    # Create magazines table
    curs.execute(
        """
        DROP TABLE IF EXISTS magazines, article_types, author, Articles;
        CREATE TABLE magazines(
             id serial PRIMARY KEY,
             name varchar(50) NOT NULL);
        ALTER SEQUENCE magazines_id_seq RESTART WITH 4;  
        """
    )
    connection.commit()
    print("[INFO] Table magazines create")

    # Create values from file
    with open('file.csv', 'r', encoding="utf-8") as f:
        next(f)
        curs.copy_from(f, 'magazines', sep=',')
    connection.commit()
    print("[INFO] Values insert in table magazines from file")

    # Create default tables, values an relations
    curs.execute(
        """
        CREATE TABLE article_types(
             id serial PRIMARY KEY,
             type varchar(50) NOT NULL);
        INSERT INTO article_types (type)
            VALUES
                ('News'),
                ('Tech'),
                ('Enternament');

        CREATE TABLE author(
             id serial PRIMARY KEY,
             author varchar(50) NOT NULL);
        INSERT INTO author (author)
            VALUES
                ('Chappie'),
                ('Wall-e'),
                ('Atom'),
                ('T1000');
        CREATE TABLE Articles(
            id serial PRIMARY KEY,
            magazines_id INTEGER REFERENCES magazines(id) ON DELETE CASCADE,
            article_type_id INTEGER REFERENCES article_types(id) ON DELETE CASCADE,
            author_id INTEGER REFERENCES author(id) ON DELETE CASCADE);

        INSERT INTO Articles (magazines_id, article_type_id, author_id)
            VALUES
                (1, 2, 3),
                (3, 3, 2),
                (2, 2, 4),
                (1, 1, 1);
        """
    )
    connection.commit()
    print("[INFO] Tables created")
    curs.close()
    connection.close()
    print("[INFO] PostgreSQL connection close.")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")
