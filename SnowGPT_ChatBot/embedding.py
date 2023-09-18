from sentence_transformers import SentenceTransformer

# Load a pre-trained model (you can use different models)
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Your sentence
sentence = "Machine learning is a subfield of artificial intelligence."

# Get the sentence embedding
embedding = model.encode(sentence)

# The 'embedding' variable now contains the sentence embedding as a NumPy array
print(embedding)
