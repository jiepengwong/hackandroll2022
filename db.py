
from pymongo import MongoClient

client = MongoClient("mongodb+srv://jiepeng:jiepeng@nodejstutoriallearning.xssjk.mongodb.net/hackandroll?retryWrites=true&w=majority")

db = client.get_database("hackandroll")

records = db.student_records

# Restart DB in a clean state
# records. delete_many({})


print(records.count_documents({}))