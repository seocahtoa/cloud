from pymongo import MongoClient
#password = JsEKyQarr3HgptK1


from pymongo import MongoClient

uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/Users/sminsu/Downloads/X509-cert-2313919381921716032.pem')



db = client['bank']
collection_name = db["account"]
item_1 = {
"_id" : "U1IT00001",
"item_name" : "Blender",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 340,
"category" : "kitchen appliance"
}

item_2 = {
"_id" : "U1IT00002",
"item_name" : "Egg",
"category" : "food",
"quantity" : 12,
"price" : 36,
"item_description" : "brown country eggs"
}
collection_name.insert_many([item_1,item_2])


# print("Successfully Connected")
# c = {
#     'ID' : 'abc123',
#      'first_name' : 'Minsu',
#      'last_name' : 'Seo',
# }
# result=db.customer.insert_one(c)
client.close()

