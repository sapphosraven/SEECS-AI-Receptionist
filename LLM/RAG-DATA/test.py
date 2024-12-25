from langgraph_adaptive_rag_final import run_ai_receptionist

def get_answer(question):
    print(f"Query received from local: {question}")
    response = run_ai_receptionist(question)
    return response

print(get_answer("how many computer labs are there in seecs?"))