import pandas as pd
import json, time
from pathlib import Path

CSV   = Path('data/unspsc_full.csv')
CACHE = Path('data/unspsc_cache.json')
META  = CACHE.with_suffix('.meta')
TTL   = 24*3600  # 1 day

def fetch_unspsc():
    try:
        meta = json.loads(open(META).read())
        if time.time() - meta['fetched_at'] < TTL:
            df = pd.read_json(CACHE, orient='records')
            df = df.rename(columns={
                'Key':'key',
                'Parent key':'parent',
                'Code':'code',
                'Title':'title'
            })
            return df
    except:
        pass
    df = pd.read_csv(CSV, dtype=str, encoding='utf-8-sig')
    df = df.rename(columns={
        'Key':'key',
        'Parent key':'parent',
        'Code':'code',
        'Title':'title'
    })
    df.to_json(CACHE, orient='records')
    with open(META, 'w') as f:
        json.dump({'fetched_at': time.time()}, f)
    return df

# Load the taxonomy
unspsc_df = fetch_unspsc()
print("unspsc_df columns:", unspsc_df.columns)

# 1) Map by key so we can follow parents
# key_map = {r['key']: r for _, r in unspsc_df.iterrows()}

key_map = {r['key']: r for _, r in unspsc_df.iterrows()}
row_map = {r['code']: r for _, r in unspsc_df.iterrows()}


# 2) A helper to walk up the tree via key
def get_ancestors_by_key(start_key):
    path = [start_key]
    cur = key_map.get(start_key)
    while cur is not None and pd.notna(cur['parent']):
        parent_key = cur['parent']
        cur = key_map.get(parent_key)
        if cur is None:
            break
        path.append(cur['key'])
    return list(reversed(path))  # from root-key → leaf-key

# 3) Build final map keyed by the UNSPSC code
unspsc_map = {}
for _, row in unspsc_df.iterrows():
    code     = row['code']
    node_key = row['key']

    # get ancestor keys and map them to codes
    ancestor_keys  = get_ancestors_by_key(node_key)
    ancestor_codes = [key_map[k]['code'] for k in ancestor_keys if k in key_map]

    # pad/truncate to 4 codes
    if len(ancestor_codes) < 4:
        ancestor_codes = [None]*(4-len(ancestor_codes)) + ancestor_codes
    else:
        ancestor_codes = ancestor_codes[-4:]
    seg_c, fam_c, cls_c, com_c = ancestor_codes

    # now fetch titles from row_map (code → row), not key_map
    unspsc_map[code] = {
        'segment_code':   seg_c,
        'segment_title':  row_map.get(seg_c,{}).get('title'),
        'family_code':    fam_c,
        'family_title':   row_map.get(fam_c,{}).get('title'),
        'class_code':     cls_c,
        'class_title':    row_map.get(cls_c,{}).get('title'),
        'commodity_code': com_c,
        'commodity_title':row_map.get(com_c,{}).get('title'),
    }
    
    # Simplified map for dropdown
    unspsc_dropdown_map = {code: details['commodity_title'] for code, details in unspsc_map.items()}



# 4) Add a text column for search/display
unspsc_df['text'] = unspsc_df.apply(
    lambda r: f"{r['code']} – {r['title'].lower()}", axis=1
)
