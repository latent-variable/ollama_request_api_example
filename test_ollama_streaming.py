from requests.exceptions import ChunkedEncodingError
import requests
import json

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"
MODEL_NAME = "phi4:latest"

conversation_history = [
    {
        "role": "system",
        "content": "You're a technical AI assistant. Keep responses concise but precise."
    }
]

def chat_stream():
    print("Chat with Phi-4 (type 'exit' to quit)")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ('exit', 'quit'):
                print("Ending session...")
                break

            conversation_history.append({"role": "user", "content": user_input})

            payload = {
                "model": MODEL_NAME,
                "messages": conversation_history,
                "stream": True
            }

            with requests.post(
                OLLAMA_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                stream=True
            ) as response:
                response.raise_for_status()
                
                full_response = []
                print("Assistant: ", end='', flush=True)
                
                for chunk in response.iter_lines():
                    if chunk:
                        try:
                            json_chunk = json.loads(chunk.decode('utf-8'))
                            if 'message' in json_chunk and 'content' in json_chunk['message']:
                                token = json_chunk['message']['content']
                                print(token, end='', flush=True)
                                full_response.append(token)
                        except json.JSONDecodeError:
                            continue

                # Add the complete response to history
                if full_response:
                    conversation_history.append({
                        "role": "assistant",
                        "content": "".join(full_response)
                    })
                print()  # New line after stream

        except ChunkedEncodingError:
            print("\n\nConnection error - try again")
            continue
        except KeyboardInterrupt:
            print("\nSession ended by user")
            break

if __name__ == "__main__":
    chat_stream()