import chromadb
from chromadb.utils import embedding_functions
import csv

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="db/gaf_data")

# Load the embedding model
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = client.get_or_create_collection(name="gaf_reviews", embedding_function=sentence_transformer_ef)

# Create a new collection for contractor profiles
contractor_collection = client.get_or_create_collection(name="gaf_contractor_profiles", embedding_function=sentence_transformer_ef)

def ingest_contractor_profiles(file_path: str):
    '''
    Ingest contractor profiles from a CSV file and add them to ChromaDB.
    '''
    documents = []
    metadatas = []
    ids = []

    # Load data from the CSV file
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        cur_id = 1
        for row in reader:
            contractor_name = row.get("Contractor")
            # Filter out None keys from metadata
            metadata = {key: value for key, value in row.items() if key and key != "Contractor"}

            documents.append(contractor_name)
            metadatas.append(metadata)
            ids.append(str(cur_id))
            cur_id += 1

    # Add data to the contractor collection
    contractor_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )
    return documents

def ingest_reviews(file_path: str):
    '''
    Ingest reviews from a CSV file and add them to ChromaDB.
    '''

    documents = []
    metadatas = []
    ids = []

    # Load data from the CSV file
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        cur_id = 1
        for row in reader:
            contractor_name = row.get("Contractor")
            # Filter out None keys from metadata
            metadata = {key: value for key, value in row.items() if key and key != "Contractor"}

            documents.append(contractor_name)
            metadatas.append(metadata)
            ids.append(str(cur_id))
            cur_id += 1

    # Add data to ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

def query_contractor_profile_collection(query: str, top_k: int = 10):
    """Query ChromaDB for relevant contractor profiles."""
    print("[query_contractor_profile_collection] Querying profiles on ChromaDB...")
    results = contractor_collection.query(query_texts=query, n_results=top_k, include=["documents", "metadatas"])
    return results

def query_reviews_collection(query: str, top_k: int = 10):
    """Query ChromaDB for relevant customer reviews."""
    print("[query_reviews_collection] Querying reviews on ChromaDB...")
    results = collection.query(query_texts=query, n_results=top_k, include=["documents", "metadatas"])
    return results

def ingest_gaf_data():
    ingest_reviews("db/csv/reviews.csv")
    contractors = ingest_contractor_profiles("db/csv/contractor_info.csv")
    return contractors

# ingest_gaf_data()
# ingest_test3()

def ingest_test1():
    # ingest_part_information("PS11752778")
    while True:
        user_query = input("Enter: ('q' to quit): ")
        if user_query.lower() == 'q':
            break
        results = query_reviews_collection(user_query)
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"Result {i + 1}: {doc}")

def ingest_test2():
    ingest_reviews("db/csv/reviews.csv")
    while True:
        user_query = input("Enter: ('q' to quit): ")
        if user_query.lower() == 'q':
            break
        results = query_reviews_collection(user_query)
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"Result {i + 1}: {doc}")

def ingest_test3():
    ingest_contractor_profiles("db/csv/contractor_info.csv")
    while True:
        user_query = input("Enter: ('q' to quit): ")
        if user_query.lower() == 'q':
            break
        results = query_contractor_profile_collection(user_query)
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"Result {i + 1}: {meta}")
