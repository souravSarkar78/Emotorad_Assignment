from db_connection import conn

cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Contact;')

# create contact table
cursor.execute("""create table Contact (
                id SERIAL primary key,
                phoneNumber VARCHAR,
                email varchar,
                linkedId INT,
                linkedPrecedence varchar(10) check (linkedPrecedence in ('secondary', 'primary')),
                createdAt TIMESTAMP with time zone default current_timestamp,
                updatedAt TIMESTAMP with time zone default current_timestamp,
                deletedAt TIMESTAMP with time zone
                );""")


conn.commit()

print("Succesfull!")

cursor.close()
conn.close()