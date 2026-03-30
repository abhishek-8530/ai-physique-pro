import numpy as np

# ---------------- FAISS SETUP ----------------
try:
    import faiss
    use_faiss = True
except:
    print("⚠️ FAISS not installed, using numpy fallback")
    use_faiss = False


# ---------------- LOAD EMBEDDINGS ----------------
try:
    embeddings = np.load("models/embeddings.npy").astype("float32")
    print("✅ Embeddings loaded:", embeddings.shape)
except:
    print("⚠️ embeddings.npy not found, using random embeddings")
    embeddings = np.random.rand(10, 512).astype("float32")


# ---------------- NORMALIZATION (VERY IMPORTANT) ----------------
def normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / (norms + 1e-10)


embeddings = normalize(embeddings)


# ---------------- FAISS INDEX ----------------
if use_faiss:
    dim = embeddings.shape[1]

    # Use Inner Product (better for similarity)
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)


# ---------------- SEARCH FUNCTION ----------------
def search(query_embedding, top_k=3):

    query_embedding = np.array([query_embedding]).astype("float32")
    query_embedding = normalize(query_embedding)

    if use_faiss:
        scores, indices = index.search(query_embedding, top_k)
        return indices[0].tolist()

    else:
        # Cosine similarity using numpy
        similarities = np.dot(embeddings, query_embedding.T).flatten()
        return np.argsort(-similarities)[:top_k].tolist()