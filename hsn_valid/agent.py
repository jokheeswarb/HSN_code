import pandas as pd
from typing import List
from google.adk.agents import LlmAgent

HSN_MASTER_FILE_PATH = r"C:\\Users\\venka\\HSN\\excel.csv"

try:
    
    hsn_df = pd.read_csv(HSN_MASTER_FILE_PATH)
    hsn_df.columns = hsn_df.columns.str.strip() 

    if "HSNCode" not in hsn_df.columns or "Description" not in hsn_df.columns:
        raise KeyError(f"Missing required columns. Found columns: {hsn_df.columns.tolist()}")

    hsn_df["HSNCode"] = hsn_df["HSNCode"].astype(str).str.strip()
    hsn_dict = dict(zip(hsn_df["HSNCode"], hsn_df["Description"]))

except Exception as e:
    raise RuntimeError(f"Failed to load HSN data: {e}")


def validate_hsn_codes(codes: List[str]) -> dict:
    results = []
    for code in codes:
        code = code.strip()
        if code in hsn_dict:
            results.append({
                "hsn_code": code,
                "valid": True,
                "description": hsn_dict[code]
            })
        else:
            results.append({
                "hsn_code": code,
                "valid": False,
                "error": "Invalid or unknown HSN code"
            })

    return {
        "status": "success",
        "validation_results": results
    }

root_agent = LlmAgent(
    name="hsn_validation_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to validate HSN (Harmonized System of Nomenclature) codes used for classifying traded products."
    ),
    instruction=(
        "You are a helpful agent who validates HSN codes against a master dataset. "
        "Return the description if the code is valid or an error message if invalid."
    ),
    tools=[validate_hsn_codes],
)
