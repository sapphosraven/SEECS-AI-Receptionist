import requests

# ngrok URL from the Kaggle notebook output
NGROK_URL = "https://b120-34-68-249-142.ngrok-free.app"  # Replace with your public ngrok URL

def query_server(query):
    """Send a query to the Flask server."""
    try:
        response = requests.post(
            f"{NGROK_URL}/infer",
            json={"query": query}
        )
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Error: {e}"

# Example query
query = "Who are you?"
response = query_server(query)
print(f"Query: {query}\nResponse: {response}")
