import pandas as pd

def detect_dataset_type(file_path):
    try:
        # Load the file into a DataFrame
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Normalize column names
        columns = set(col.strip().lower() for col in df.columns)

        # Define keyword sets
        sales_keywords = {"date", "product", "revenue", "sales", "region", "amount"}
        hr_keywords = {"employee", "department", "salary", "designation", "join", "name"}
        marketing_keywords = {"campaign", "click", "leads", "conversion", "budget"}

        # Match scoring
        sales_matches = len(columns & sales_keywords)
        hr_matches = len(columns & hr_keywords)
        marketing_matches = len(columns & marketing_keywords)

        # Decide type based on most keyword matches
        if sales_matches >= max(hr_matches, marketing_matches) and sales_matches >= 2:
            return "sales"
        elif hr_matches >= max(sales_matches, marketing_matches) and hr_matches >= 2:
            return "hr"
        elif marketing_matches >= 2:
            return "marketing"
        else:
            return "general"

    except Exception as e:
        print(f"[Detector Error] Failed to detect dataset type: {e}")
        return "general"
