# run_taxonomy.py

from src import taxonomy_service

def main():
    # 1. How many rows loaded?
    print("Rows in taxonomy:", len(taxonomy_service.unspsc_df))

    # 2. Show a few sample entries
    print("\nSample entries:")
    print(taxonomy_service.unspsc_df.head(3).to_string(index=False))

    # 3. Test ancestors for a top‑level code ('A')
    top_code = 'A'
    print(f"\nAncestors for top‑level code {top_code}:")
    print(taxonomy_service.unspsc_map.get(top_code))

    # 4. Test ancestors for a deeper code ('10101501')
    deep_code = '10101501'
    print(f"\nAncestors for deeper code {deep_code}:")
    print(taxonomy_service.unspsc_map.get(deep_code))

if __name__ == "__main__":
    main()
