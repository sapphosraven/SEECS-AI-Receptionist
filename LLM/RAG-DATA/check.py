import faiss
import torch

def check_faiss_gpu():
    if torch.cuda.is_available():
        res = faiss.StandardGpuResources()
        print(res)
        print("FAISS with GPU support is available.")
    else:
        print("GPU is not available.")

check_faiss_gpu()