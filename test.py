import requests
from concurrent.futures import ThreadPoolExecutor

def get_embedding(text):
    url = 'http://localhost:11434/api/embeddings'
    payload = {
        'model': 'nomic-embed-text',
        'prompt': text
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_chat_response(prompt):
    url = 'http://localhost:11434/api/chat'
    payload = {
        'model': 'llama3.2:1b',
        'prompt': prompt
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    text = "Your text here"
    prompt = "Hello, how can I assist you today?"

    with ThreadPoolExecutor(max_workers=2) as executor:
        embedding_future = executor.submit(get_embedding, text)
        chat_future = executor.submit(get_chat_response, prompt)

        embedding = embedding_future.result()
        chat_response = chat_future.result()

    print("Embedding:", embedding)
    print("Chat Response:", chat_response)

if __name__ == "__main__":
    main()
