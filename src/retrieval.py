from sentence_transformers import SentenceTransformer, util
import numpy as np
from src.taxonomy_service import unspsc_df

_model = SentenceTransformer('all-MiniLM-L6-v2')
_embs  = _model.encode(unspsc_df['text'].tolist(), convert_to_tensor=True)

def shortlist(desc: str, k: int=10):
    q_emb = _model.encode([desc], convert_to_tensor=True)
    sims = util.cos_sim(q_emb, _embs)[0].cpu().numpy()
    idx  = np.argsort(sims)[-k:][::-1]
    return unspsc_df.iloc[idx].assign(score=sims[idx])