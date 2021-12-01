from pymongo import  MongoClient
import gridfs


"""
https://www.youtube.com/watch?v=KSB5g8qt9io
"""

def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        return conn.grid_file
    except Exception as e:
        raise Exception(e)


db = mongo_conn()
file_name = "test_blog.odt"
file_location = "/opt/core/Letters/resources/test/" + file_name

with open(file_location, "rb") as br:
    file_data = br.read()

fs = gridfs.GridFS(db)

fs.put(file_data, filename=file_name)

print("upload completed")


data = db.fs.files.find_one({"filename": file_name})
print(data)
