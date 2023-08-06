import pymongo
from bson.objectid import ObjectId
import pandas as pd
from beartype import beartype
from gridfs import GridFS
from typing import Optional, Union

# clientAddress       = "mongodb://localhost:27017/"
# databaseName        = "mydatabase"
# collectionEquipment = "equipment"
# collectionMaterial  = "material"
# collectionProcessData = "process_data"

class client:
    @beartype
    def __init__(self, clientAddress:str):
        self.clientAddress = clientAddress

    def get_client(self):
        myclient = pymongo.MongoClient(self.clientAddress)
        return myclient

    def all_database_names(self):
        myclient = self.get_client()
        return myclient.list_database_names()


class database(client):
    @beartype
    def __init__(self, clientAddress:str, databaseName:str):
        super().__init__(clientAddress)
        self.clientAddress = clientAddress
        self.databaseName = databaseName
    
    def get_database(self):
        myclient = self.get_client()
        mydb     = myclient[self.databaseName]
        return mydb

    def all_collection_names(self):
        mydb = self.get_database()
        return mydb.list_collection_names()

    @beartype
    def get_file(self, id:str):
        mydb  = self.get_database()
        fs    = GridFS(mydb)
        return fs.get(ObjectId(id)).read()

    @beartype
    def delete_file(self, id:str):
        mydb  = self.get_database()
        fs    = GridFS(mydb)
        fs.delete(ObjectId(id))
        return True


class collection(database):

    @beartype
    def __init__(self, clientAddress:str, databaseName:str, collectionName:str):
        super().__init__(clientAddress, databaseName)
        self.collectionName = collectionName
    
    def get_collection(self):
        mydb  = self.get_database()
        mycol =  mydb[self.collectionName]
        return mycol
    
    @beartype
    def insert(self, insert_dict:dict):
        mycol = self.get_collection()
        x = mycol.insert_one(insert_dict)
        return str(x.inserted_id)

    def get_all_documents(self, query_condition:Optional[dict]=None):
        mycol = self.get_collection()
        if query_condition == None:
            find_info = mycol.find()
        else:
            find_info = mycol.find(query_condition)
        all   = []
        for x in find_info:
            all.append(x)
        return all

    @beartype
    def query(self, query_condition:dict):
        mycol = self.get_collection()
        mydoc = mycol.find(query_condition)
        all   = []
        for x in mydoc:
            all.append(x)
        return all

    @beartype
    def delete(self, id:str):
        mycol = self.get_collection()
        mycol.delete_one({"_id": ObjectId(id)})
        return True

    @beartype
    def update(self, update_condition:dict, id:str):
        mycol = self.get_collection()
        myquery = { "_id": ObjectId(id)}
        newvalues = { "$set": update_condition }
        mycol.update_one(myquery, newvalues)
        return True
    
    @beartype
    def insert_file(self, filecontent:bytes, filename:str, filetype:str):
        mydb  = self.get_database()
        mycol = self.get_collection()
        fs    = GridFS(mydb)
        fsid  = fs.put(filecontent, filename=filename)
        filedict = {"_id": ObjectId(fsid), "filetype":filetype}
        self.insert(filedict)
        return True



# ------------------ collections -------------------------
@beartype
def insert_doc(clientAddress:str, databaseName:str, collectionName:str, insert_dict:dict):
    mycol = collection(clientAddress, databaseName, collectionName)
    info  = mycol.insert(insert_dict)
    return info

@beartype
def delete_doc(clientAddress:str, databaseName:str, collectionName:str, id:str):
    mycol       = collection(clientAddress, databaseName, collectionName)
    info        = mycol.delete(id=id)
    return info

@beartype
def get_one_doc(clientAddress:str, databaseName:str, collectionName:str, id:str):
    mycol       = collection(clientAddress, databaseName, collectionName)
    query_condition = {"_id": ObjectId(id)}
    info        = mycol.query(query_condition)
    return info

@beartype
def get_all_doc(clientAddress:str, databaseName:str, collectionName:str, query_condition:Optional[dict]=None):
    mycol       = collection(clientAddress, databaseName, collectionName)
    return mycol.get_all_documents(query_condition)

@beartype
def update_doc(clientAddress:str, databaseName:str, collectionName:str, update_condition:dict, id:str):
    mycol       = collection(clientAddress, databaseName, collectionName)
    info = mycol.update(update_condition, id)
    return info


# @beartype
# def get_all_doc(clientAddress:str, databaseName:str, collectionName:str):
#     mycol       = collection(clientAddress, databaseName, collectionName)
#     df          = mycol.get_all_documents()
#     return df

# ------------------ files ---------------------

@beartype
def insert_one_file(clientAddress:str, databaseName:str, collectionName:str,
                filecontent:bytes, filename:str, filetype:str):
    mycol   = collection(clientAddress, databaseName, collectionName)
    info    = mycol.insert_file(filecontent, filename, filetype)
    return info

@beartype
def get_one_file(clientAddress:str, databaseName:str, id:str):
    mydb       = database(clientAddress, databaseName)
    output_data = mydb.get_file(id)
    return output_data

@beartype
def delete_one_file(clientAddress:str, databaseName:str, collectionName:str, id:str):
    # delete doc from file_management
    mycol      = collection(clientAddress, databaseName, collectionName)
    mycol.delete(id)
    # delete file from fs.files and fs.chunks
    mydb       = database(clientAddress, databaseName)
    mydb.delete_file(id)
    return True
    



# file_location = "IMG_0317.JPG"
# filename      = "IMG_0317.JPG"
# file_data = open(file_location, "rb")
# data = file_data.read()
# print(delete_file(id="63cbca98774f1eab47dce160"))
# output_data = get_file(id="63cbca98774f1eab47dce160")
# output = open("/Users/mklu/myCodes/models/mongodb/download/img.JPG", "wb")
# output.write(output_data)
# output.close()
# print(insert_file(data, filename))

# print(update_document(collectionEquipment, {"geometry": {"bottom diameter": 0.14, "top diameter": 0.295, "height": 0.548}}, "63cb2b25ffba3ca8d046bee9" ))

'''
newFBG              = { "name": "GPCG2-3L", "geometry": {"bottom diameter": 0.10, "top diameter": 0.295, "height": 0.548} }
insert_document(collectionEquipment, newFBG)
'''
