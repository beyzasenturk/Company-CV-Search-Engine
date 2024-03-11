from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient, TEXT
from pymongo.operations import IndexModel
import json
import re


# MongoDB bağlantısı
client = MongoClient("mongodb://myuser:mymongodbUser01!@my-mongodb:27017/")
db = client["company"]
collection = db["resume"]

'''
db.resume.createIndex({
    Category: 'text',
    Resume: 'text',
  },
  {
    default_language: 'english',
    weights: {
      Category: 2,
      Resume: 1
    },
    name: 'custom_text_index',
    background: true,
    analyzer: 'lucene.whitespace',
    search_analyzer: 'lucene.standard'
  })
'''

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_special_characters(text):
    # Sadece harfleri ve boşlukları koru, diğer karakterleri temizle
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    return cleaned_text

@app.get("/search/{search_text}")
def read_root(search_text):
    # Arama metnini temizle
    cleaned_search_text = clean_special_characters(search_text)

    result = collection.find({"$text": {"$search": f"{cleaned_search_text}"}})

    result_list = []
    for news in result:
        news["_id"] = None
        result_list.append(news)

    return result_list

# POST metodunu işleyen basit bir endpoint
#@app.post("/search")
# def create_item(body:dict):
#     print(body)
#     return {"message": body["search_text"]}



