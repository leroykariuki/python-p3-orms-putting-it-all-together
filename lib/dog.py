import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()
# ^^execute queries on database

# OBJECT is ROW, CLASS is TABLE
class Dog:
    # The __init__ method takes name and breed as arguments 
    # and saves them as instance attributes. 
    # It should also create an id instance attribute.
    def __init__(self, name, breed, id = None):
        self.id = id
        self.name = name
        self.breed = breed

    # Create a create_table() class method that will 
    # create the dogs table if it does not already exist. 
    # Table should have columns for an id, a name, a breed.
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
            )
        """
        CURSOR.execute(sql)

    # This class method drop_table() should drop(remove) 
    # the dogs table if it does exist
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        # CONN.commit() # makes changes/update database NECESSARY???

    # Create an instance method save() that 
    # saves a Dog object to your database.
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) 
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        # CONN.commit() NECESSARY???
        self.id = CURSOR.lastrowid 
        # sqlite3.Cursor object has lastrowid attribute 
        # self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        # ^THIS WORKS TOO

    # Create an class method create() that
    # creates a new row in the database and
    # returns a new instance of the Dog class.
    # (method to create dog object and save it (obj->row))
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    # Ultimately, the database is going to return an array 
    # representing a dog's data. We need to cast that data 
    # into the appropriate attributes of a dog. 
    # This method encapsulates that functionality. 
    # Methods like this, that return instances of the class,
    # are known as constructors, just like calling 
    # the class itself, except that they extend that 
    # functionality without overwriting __init__.
    # (method to create dog object from row values in the table(row->obj))
    @classmethod
    def new_from_db(cls, row):
        dog = cls(
            name = row[1],
            breed = row[2],
            id = row[0]
        )
        return dog

    #Class method get_all() should return a list of 
    #Dog instances for every record in the dogs table
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * 
            FROM dogs
        """
        # gets each row from query and creates dog object from row (returned)
        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]
#         print(CURSOR.execute(sql).fetchall()) #selects all rows that match query
#           => [(1, 'Princess', 'Lab'), (2, 'Pooh', 'Poodle')]
#         allRows = CURSOR.execute(sql).fetchall()
#         for row in allRows:
#             print(row.name) #gives error since it's tuple
#             print(row[1]) #prints out names 
# dog1=Dog('Princess', 'Lab', 1)
# dog2=Dog('Pooh', 'Poodle', 2)
# Dog.create_table()
# dog1.save()
# dog2.save()
# Dog.get_all()

    # search for dog in database, find that row, make and return dog obj
    # it's a classmethod bc it's referring to the entire table
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM dogs 
            WHERE name = ?
            """
        # selects single row that matches query
        row = CURSOR.execute(sql, (name,)).fetchone()
        # name, bc name is tuple 
        if not row:
            return None
        return Dog(
            name = row[1],
            breed= row[2],
            id = row[0],
        )

    # This class method takes in an ID, and should return 
    # a single Dog instance for the corresponding record 
    # in the dogs table with that same ID.
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM dogs 
            WHERE id = ?
            """
        # return CURSOR.execute(sql, (id,)).fetchone()
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            dog = Dog(
                name = row[1],
                breed= row[2],
                id = row[0],
            )
            return dog
        else:    
            return None
        
    # takes a name and a breed as arguments and creates a Dog instance 
    # matching that record if it does not exist. 
    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql="""
            SELECT * 
            FROM dogs
            WHERE (name, breed)=(?, ?)
            LIMIT 1
        """
        row = CURSOR.execute((sql), (name, breed)).fetchone()
        if not row:
            sql="""
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute((sql), (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )
        return Dog(
                name = row[1],
                breed= row[2],
                id = row[0],
        )
    
    def update(self):
        sql = """
            UPDATE dogs 
            SET name = ?,
                breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))