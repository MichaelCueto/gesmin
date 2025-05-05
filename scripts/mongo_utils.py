from pymongo import MongoClient, errors
import os

def connect_to_mongo():
    """Conecta a MongoDB local o usando MONGO_URI"""
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Prueba rápida de conexión
        print("✅ Conexión exitosa a MongoDB")
        return client["gesmin"], client  # Devuelvo también el objeto cliente para cerrarlo después
    except errors.ConnectionFailure as e:
        raise RuntimeError(f"❌ No se pudo conectar a MongoDB: {str(e)}")

def insert_json_in_collection(db, collection_name, json_data):
    """Inserta un JSON en la colección"""
    try:
        collection = db[collection_name]
        result = collection.insert_one(json_data)
        print(f"🗄️ Insertado en {collection_name} con ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        raise RuntimeError(f"❌ Error al insertar en MongoDB: {str(e)}")