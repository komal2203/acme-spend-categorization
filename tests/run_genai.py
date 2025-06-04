from src.genai_inference import classify_with_ai
from src.retrieval import shortlist

desc = "Ergonomic mesh office chair"
supp = "FurnitureCo"
top_k = shortlist(desc, k=5)

result = classify_with_ai(desc, supp, top_k)
print(result)
