__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import chromadb
from openai import OpenAI
import os



#chromdb client
client = chromadb.PersistentClient("./collection")

collection = client.get_or_create_collection(name="ITSMF_RAG",
                                             metadata={"hnsw:space": "cosine"})


#OpenAI Model
openai_client = OpenAI()


def run_rag_llm(query):

    rag_results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas"])

    print("rag_results", rag_results)


    search_results = []

    for res in rag_results["documents"]:
        for doc, meta in zip(res, rag_results["metadatas"][0]):
            # Format the document text and its metadata
            metadata_str = ", ".join(f"{key}: {value}" for key, value in meta.items())
            search_results.append(f"{doc}\nMetadata: {metadata_str}")
    search_text = "\n\n".join(search_results)


    print("search_text", search_text)


    prompt = f"""Your task is to answer the following user question using the supplied search results.
        User Question: {query}
        Search Results: {search_text}
        """




    response = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
           {"role": "system", "content": "You're a helpful assistant who looks up specific information about an organization called Information Technology Senior Management Forum (ITSMF) from user queries and search results about the organization. If you are not able to answer the question from the search results or your knowledge, say 'I'm sorry, I don't have access to that information. Make sure you give answers with good formatting, spacing, and the same font. You should use the search results to help answer the user's question."},
           {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content