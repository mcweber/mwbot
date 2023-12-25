# ____________________________________________________________________________
# Version 25.12.2023
# Author:  Martin Weber
# ____________________________________________________________________________

import pandas as pd
import numpy as np

import chromadb
import openai

# Constants ------------------------------------------------------------------
openai_client = openai.OpenAI()

# Functions reference --------------------------------------------------------

# def printTable(results)
# def init_vector_db()
# def search_vector_db(collection, query)
# def search_llm(question, history, systemPrompt = "", results = [])
# def update_history(history, question, answer)
# def compressPrompt(prompt)

# Functions ------------------------------------------------------------------
def printTable(results):
    # Erstellen Sie eine Tabelle
    table = PrettyTable()
    table.field_names = ["ID", "Artikel"]
    table.align["ID"] = "m"
    table.align["Artikel"] = "l"

    # Fügen Sie Zeilen hinzu
    max = len(results['ids'][0])
    for i in range(max):
        id = results['ids'][0][i]
        artikel = results['documents'][0][i][7:40]
        table.add_row([id, artikel])

    # Drucken Sie die Tabelle
    print(table)

def init_vector_db():
    print('Initializing vector DB...')
    # chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    client = chromadb.PersistentClient(path = "./db1/")
    collection = client.get_or_create_collection(
        name = "dvz_texte_chroma",
        #embedding_function = OpenaiEmbeddingFunction(),
        )
    return collection

def search_vector_db(collection, query):
    print('Searching VectorDB...')
    results = collection.query(query_texts=[query], n_results=10)
    return results

def search_llm(question, history = [], systemPrompt = "", results = []):
    # Transform results to LLM format
    init_prompt = [{"role": "system", "content": systemPrompt.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')}]
    if results:
        results_pool = "".join(results['documents'][0])
        results = [{"role": "system", "content": results_pool}]
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0,
        #Achtung: RAG umfasst nur die Ergebnisse der letzen Frage
        messages=init_prompt + results + history + [{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

def update_history(history, question, answer):
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})

def compressPrompt(prompt):
    prompt = prompt.replace('\n', ' ')
    prompt = prompt.replace('\t', ' ')
    prompt = prompt.replace('  ', ' ')
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60
        )
    return response.choices[0].text.strip()
  