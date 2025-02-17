import logging
import os
from typing import List, Dict, Optional, Any
import spacy
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
import openai

# Load spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

class MilvusManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MilvusManager, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, host: str = "localhost", port: str = "19530", openai_api_key: str = None, **kwargs):
        """Initialization logic for MilvusManager to make it a Singleton."""
        # Check if openai_api_key is passed or exists in the environment
        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise ValueError("OpenAI API key is not provided and is missing from the environment variables.")

        openai.api_key = openai_api_key

        # Connect to Milvus
        try:
            connections.connect("default", host=host, port=port)
            logging.info(f"Successfully connected to Milvus at {host}:{port}")
        except Exception as e:
            logging.error(f"Failed to connect to Milvus at {host}:{port} - {e}")
            raise

    def create_index(self, collection_name: str, field_name: str = "embedding", index_type: str = "IVF_FLAT", metric_type: str = "L2", nlist: int = 100, **kwargs):
        """Creates an index for the collection on the embedding field if it doesn't already exist."""
        collection = Collection(collection_name)

        # Check if index already exists to avoid duplicate creation
        existing_indexes = collection.indexes
        if existing_indexes:
            logging.info(f"Index already exists for collection: {collection_name}")
            return  # Skip index creation

        index_params = {
            "index_type": index_type,
            "metric_type": metric_type,
            "params": {"nlist": nlist}
        }

        collection.create_index(field_name=field_name, index_params=index_params)
        logging.info(f"Index created for collection: {collection_name}")

    def create_collection(self, collection_name: str, dim: int = 1536, fields: Optional[List[Dict[str, Any]]] = None, **kwargs):
        """Creates a new collection if it doesn't exist."""
        if utility.has_collection(collection_name):
            return

        # Default fields for collection if not provided
        fields = fields or [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255),
            FieldSchema(name="keywords", dtype=DataType.VARCHAR, max_length=255),
            FieldSchema(name="text_content", dtype=DataType.VARCHAR, max_length=10000)
        ]

        schema = CollectionSchema(fields, description=f"Collection for {collection_name}")
        Collection(name=collection_name, schema=schema)

    def create_embedding(self, text: str, model: str = "text-embedding-ada-002", **kwargs) -> List[float]:
        """Generates an embedding for the given text."""
        response = openai.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    def extract_keywords(self, text: str) -> List[str]:
        """Extracts keywords from the text using SpaCy."""
        doc = nlp(text)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
        return keywords[:10]  # Limit to top 10 keywords

    def insert_document(self, collection_name: str, texts: List[str], file_names: Optional[List[str]] = None, keywords: Optional[List[List[str]]] = None, **kwargs):
        """Inserts multiple documents with embeddings into a specific collection."""
        self.create_collection(collection_name, **kwargs)
        collection = Collection(collection_name)

        # Generate embeddings for all texts
        embeddings = [self.create_embedding(text, **kwargs) for text in texts]
        
        # Handle file names
        file_names = file_names or [""] * len(texts)
        
        # Handle keywords - if not provided, extract them from texts
        if keywords is None:
            keywords = [self.extract_keywords(text) for text in texts]

        # Convert keywords list of lists into strings
        keyword_strings = [', '.join(keyword_list) for keyword_list in keywords]

        # Verify all lists have the same length
        if not all(len(lst) == len(texts) for lst in [embeddings, file_names, keyword_strings]):
            raise ValueError("Field data sizes do not align. Please ensure all fields have the same number of elements.")

        # Prepare data to insert
        insert_data = [
            embeddings,      # List of embeddings
            file_names,      # List of file names
            keyword_strings, # List of keywords as strings
            texts           # List of text content (full text)
        ]
        
        collection.insert(insert_data)

        # Create index after inserting the documents
        self.create_index(collection_name, **kwargs)

    def search_similar(self, query: str, top_k: int = 5, collection_name: Optional[str] = None, filters: Optional[Dict[str, Any]] = None, **kwargs) -> List[Dict]:
        """Searches for similar documents in a specific collection with optional filters."""
        query_embedding = self.create_embedding(query, **kwargs)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        collections_to_search = [collection_name] if collection_name else utility.list_collections()
        results = []

        for col_name in collections_to_search:
            collection = Collection(col_name)
            collection.load()

            # Build the expression string properly
            expr = None
            if filters:
                expr_parts = []
                if "file" in filters and isinstance(filters["file"], list):
                    # Handle file name filter
                    file_conditions = [f'file_name == "{fname}"' for fname in filters["file"]]
                    if file_conditions:
                        expr_parts.append(f"({' or '.join(file_conditions)})")
                
                if "keywords" in filters and isinstance(filters["keywords"], list):
                    # Handle keywords filter using LIKE operator for partial matches
                    keyword_conditions = [f'keywords like "%{kw}%"' for kw in filters["keywords"]]
                    if keyword_conditions:
                        expr_parts.append(f"({' or '.join(keyword_conditions)})")
                
                # Combine all conditions with AND
                if expr_parts:
                    expr = " and ".join(expr_parts)

            try:
                search_result = collection.search(
                    data=[query_embedding],
                    anns_field="embedding",
                    param=search_params,
                    limit=top_k,
                    expr=expr
                )

                # Fetch text content and other metadata
                if search_result[0]:
                    ids = [str(result.id) for result in search_result[0]]
                    id_expr = f"id in [{','.join(ids)}]"
                    query_results = collection.query(
                        expr=id_expr,
                        output_fields=["file_name", "keywords", "text_content"]
                    )

                    for result, doc in zip(search_result[0], query_results):
                        results.append({
                            "collection": col_name,
                            "id": result.id,
                            "distance": result.distance,
                            "file_name": doc.get("file_name", ""),
                            "keywords": doc.get("keywords", ""),
                            "text_content": doc.get("text_content", "")
                        })

            except Exception as e:
                logging.error(f"Error searching collection {col_name}: {str(e)}")
                continue

        return sorted(results, key=lambda x: x["distance"])    

    def delete_document(self, collection_name: str, doc_id: int, **kwargs):
        """Deletes a document by ID in a specific collection."""
        if utility.has_collection(collection_name):
            collection = Collection(collection_name)
            collection.delete(f"id in [{doc_id}]")

    def update_document(self, collection_name: str, doc_id: int, new_text: str, new_file_name: Optional[str] = None, new_keywords: Optional[List[str]] = None, **kwargs):
        """Updates a document embedding in a specific collection."""
        new_embedding = self.create_embedding(new_text, **kwargs)
        collection = Collection(collection_name)
        
        update_data = {"embedding": new_embedding, "text_content": new_text}
        
        if new_file_name:
            update_data["file_name"] = new_file_name
        
        if new_keywords:
            update_data["keywords"] = ', '.join(new_keywords)
        elif new_text:  # If no keywords provided but text is updated, extract new keywords
            update_data["keywords"] = ', '.join(self.extract_keywords(new_text))

        collection.update(expr=f"id in [{doc_id}]", data=update_data)

    def drop_collection(self, collection_name: str, **kwargs):
        """Drops a specific collection."""
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

# # Example usage
# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
    
#     # Initialize the manager
#     milvus = MilvusManager(
#         host="172.52.20.37", 
#         port="19530", 
#         openai_api_key=os.getenv("OPENAI_KEY")
#     )
    
#     # Example documents
#     texts = [
#         "What is machine learning?",
#         "Introduction to blockchain."
#     ]
#     file_names = [
#         "ml_intro.pdf",
#         "blockchain_intro.pdf"
#     ]
    
#     # Insert documents with automatic keyword extraction
#     try:
#         # milvus.insert_document(
#         #     collection_name="sample_collection",
#         #     texts=texts,
#         #     file_names=file_names
#         # )
#         # print("Documents inserted successfully!")
        
#         # Search example
#         results = milvus.search_similar(
#             "what is machine learning?",
#             filters={
#                 "keywords":["machine"],
#                 # "file": ["blockchain_intro.pdf"]
#             }
#         )
#         print("Search results:", results)
        
#     except Exception as e:
#         print(f"An error occurred: {e}")