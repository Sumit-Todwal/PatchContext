from models.embedding_model import get_embedding_model

embedding_model = get_embedding_model()

vector = embedding_model.embed_query(
    "How does FastAPI dependency injection work?"
)

print(len(vector))
print(vector[:10])