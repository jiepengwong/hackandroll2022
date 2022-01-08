
from pymongo import MongoClient

client = MongoClient("mongodb+srv://jiepeng:jiepeng@nodejstutoriallearning.xssjk.mongodb.net/hackandroll?retryWrites=true&w=majority")

db = client.get_database("hackandroll")

records = db.student_records


print(records.count_documents({}))