import yaml
from fuzzywuzzy import fuzz
from src.taxonomy_service import unspsc_map

rules = yaml.safe_load(open('data/rules.yaml'))

def apply_rules(desc: str, thresh: int=90) -> dict:
    """
    Returns hierarchy + confidence=1.0 if a keyword fuzzy-matches description.
    """
    for kw, code in rules.items():
        if fuzz.partial_ratio(kw.lower(), desc) >= thresh:
            info = unspsc_map[code].copy()
            info.update({'confidence':1.0,'matched_rule':kw})
            return info
    return None