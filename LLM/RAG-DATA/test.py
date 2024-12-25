import time

init_time = time.time()
from langgraph_adaptive_rag import run_ai_receptionist

def measure_response_time(question: str, debug=False):
    """
    Measure the time taken for the LLM to respond to a query.

    Args:
        question (str): The user's question.
        debug (bool): Whether to enable debug information.

    Returns:
        tuple: (response, elapsed_time_in_seconds)
    """
    start_time = time.time()
    response = run_ai_receptionist(question, debug=debug)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return response, elapsed_time



questions = [
    "Who are you?",  # Simple direct question
    "Tell me about the computer science programs in SEECS",  # Complex question
    "What programs are offered in SEECS?",  # Similar but rephrased
    "What is the admission process at SEECS?"  # Question requiring procedural context
]

no_init_time = time.time()
print(f"Time taken to import the module: {no_init_time - init_time:.2f} seconds\n")

for question in questions:
    state = {
        "question": question,
        "max_retries": 3,
        "loop_step": 0,
        "documents": []
    }
    print(f"Question: {question}")
    response, elapsed_time = measure_response_time(question, debug=True)
    print(f"Response: {response}")
    print(f"Time taken: {elapsed_time:.2f} seconds\n")