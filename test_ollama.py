import requests

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"
MODEL_NAME = "phi4:latest"  # Change this to your preferred model

# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Respond concisely and clearly."
    }
]

def chat_with_ollama():
    print("Starting chat with Ollama (type 'exit' to end)")
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'exit':
                print("Exiting chat...")
                break

            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })

            # Create request payload
            payload = {
                "model": MODEL_NAME,
                "messages": conversation_history,
                "stream": False  # Set to True if you want streaming responses
            }

            # Send request to Ollama
            response = requests.post(
                OLLAMA_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()  # Raise exception for HTTP errors

            # Process response
            response_data = response.json()
            assistant_message = response_data['message']['content']
            
            # Add assistant response to history
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Print assistant response
            print(f"\nAssistant: {assistant_message}")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            break
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

if __name__ == "__main__":
    chat_with_ollama()