import sqlalchemy

db = sqlalchemy.create_engine("postgresql+psycopg2://cocollector:12345678@192.168.137.196:8080/CocoExamen")
db.connect()
print(db)
