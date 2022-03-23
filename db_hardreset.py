import psycopg2

from config_db import host, user, password, db_name

try:
    # DB connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,

    )
    #sslmode = 'disable'
    # the cursor for performing database operations
    curs = connection.cursor()
    curs.execute(
        "SELECT version();"
    )
    print(f"Server version: {curs.fetchone()}")

    #Create magazines table
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
    pass

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        curs.close()
        connection.close()
        print("[INFO] PostgreSQL connection close.")
