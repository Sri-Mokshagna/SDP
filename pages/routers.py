class MongoDBRouter:
    def db_for_read(self, model, **hints):
        # Return the database name for read operations
        return 'mongodb'

    def db_for_write(self, model, **hints):
        # Return the database name for write operations
        return 'mongodb'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both objects are in the MongoDB database
        if obj1._state.db == 'mongodb' and obj2._state.db == 'mongodb':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only allow migrations for the 'pages' app to the MongoDB database
        if app_label == 'pages':
            return db == 'mongodb'
        return None
