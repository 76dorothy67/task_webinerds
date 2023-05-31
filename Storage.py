import chromadb
from sentence_transformers import SentenceTransformer
from helpers import *


class Storage:

    def __init__(self, dir: str, collection_name: str = 'summaries'):
        self.client = chromadb.Client(chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=dir
        ))
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.collection_name = collection_name
        self._collection = None

    @property
    def all_documents(self):
        return self.collection.get(include=['documents'])['documents']

    def most_similar_to(self, text) -> str | None:
        d = self.collection.query(query_texts=[text], n_results=1)
        if not d or not 'documents' in d or not len(d['documents']) or not len(d['documents'][0]):
            return None
        return d['documents'][0][0]

    def save(self, text):
        self.collection.upsert(documents=[text], ids=[str(hash(text))])

    @property
    def collection(self) -> chromadb.api.models.Collection:
        if not self._collection:
            try:
                log(f'Loading collection {bold(self.collection_name)}')
                self._collection = self.client.get_collection(
                    self.collection_name,
                    self.embedding_model.encode
                )
            except ValueError:
                log(f'Creating collection {bold(self.collection_name)}')
                self._collection = self.client.create_collection(
                    self.collection_name,
                    None,
                    self.embedding_model.encode
                )
        return self._collection
