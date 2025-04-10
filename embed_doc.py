import chromadb
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


client = chromadb.PersistentClient("./collection")

collection = client.get_or_create_collection(name="ITSMF_RAG",
                                             metadata={"hnsw:space": "cosine"})


text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", "? ", "! "],
    chunk_size=1500,
    chunk_overlap=200,
)

documents = []
metadatas = []
ids = []

folder_path = "./documents"
for file_name in os.listdir(folder_path):
        loader = PyPDFLoader(f"{folder_path}/{file_name}")
        chunks = loader.load_and_split(text_splitter)
        #iterate over every chunk
        for index, chunk in enumerate(chunks):
            #Append to metadata list with "title" and "index"
            metadatas.append({
                "document_title": file_name,
                "chunk_idx": index
            })
            #Append to ids each index
            ids.append(f"{file_name}_{index}")
            
            #Append to documents each chunk.page_content
            documents.append(chunk.page_content)



collection.add(documents=documents, metadatas=metadatas, ids=ids)

# Sample query run
results = collection.query(query_texts=["What is ITSMF?"], n_results=1)

print(results)
