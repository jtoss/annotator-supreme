from annotator_supreme import app
from flask import g
import cassandra
from cassandra.cluster import Cluster

KEYSPACE = "annotator_supreme"

def get_db(config):
    """
    This functions connect to the Cassandra database and kept in the flask app
    """
    with app.app_context():
        db = getattr(g, '_database', None)
        if db is None:
            app.logger.info("database connection done again")
            
            cluster = Cluster()
            session = cluster.connect(KEYSPACE)
            db = g._database = session
        return db

class DatabaseController:
    
    def setup_database(self):
        cluster = Cluster()
        session = cluster.connect()

        # first create the database (aka keyspace)
        try:
            session.execute("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEYSPACE)
        except cassandra.AlreadyExists: 
            app.logger.info("Keyspace already exists.")

        # redefine session to use the keyspace
        session.set_keyspace(KEYSPACE)

        try:
            app.logger.info("\t- creating table dataset")
            session.execute("""
                CREATE TABLE datasets (
                    name text PRIMARY KEY,
                    tags list<text>
                )
                """)
        except cassandra.AlreadyExists: 
            app.logger.info("Table 'datasets' already exists.")


        app.logger.info("\t- creating type bbox")
        session.execute("""
            CREATE TYPE IF NOT EXISTS bbox ( 
                labels list<text>,
                top float,
                left float,
                bottom float,
                right float
            )
            """)

        try:
            app.logger.info("\t- creating table images")
            session.execute("""
                CREATE TABLE images (
                    id timeuuid,
                    dataset text,
                    name text,
                    img blob,
                    annotation map<text, frozen<list<bbox>>>,
                    PRIMARY KEY (id, dataset)
                )
                """)
        except cassandra.AlreadyExists: 
            app.logger.info("Table 'images' already exists.")