from sentence_transformers import SentenceTransformer

# Load a multilingual model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_embedding(text: str) -> list:
    """
    Converts input text to a 384-dimensional vector using a multilingual model.
    """
    return model.encode(text).tolist()
