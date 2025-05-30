### 3.9 `src/09_manual_review.py`
import streamlit as st
import pandas as pd
from src.taxonomy_service import unspsc_map

st.set_page_config(page_title='Manual Review')
st.title('🛠️ Low-Confidence Manual Review')

df = pd.read_csv('data/manual_review.csv')
for i,row in df.iterrows():
    st.markdown(f"**Invoice {row['invoice_id']}** — {row['description']}")
    opts=[f"{c} – {unspsc_map[c]['commodity_title']}" for c in unspsc_map]
    sel = st.selectbox('Correct code:', opts, key=i)
    if st.button('Save & Next', key=f'btn{i}'):
        code = sel.split(' – ')[0]
        df.at[i,'commodity_code'] = code
        df.at[i,'confidence']    = 1.0
        df.to_csv('data/manual_review.csv',index=False)
        st.success('Saved! Refresh to continue.')
        st.stop()

