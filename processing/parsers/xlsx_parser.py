import pandas as pd
from typing import Any, Dict, List


class XLSXParser:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def parse(self, filepath: str) -> List[str]:
        # Read all sheets
        df_dict = pd.read_excel(filepath, sheet_name=None)  # type: ignore

        data: List[str] = []
        for sheet_name, df in df_dict.items():
            data.append(f"Sheet: {sheet_name}")  # type: ignore

            # Special handling for acronym files (likely 2-column format)
            if df.shape[1] >= 2 and "acronym" in filepath.lower():
                # Assume first column is acronym, second is definition
                for _, row in df.iterrows():
                    acronym = str(row.iloc[0]).strip()
                    definition = str(row.iloc[1]).strip()
                    if (
                        acronym
                        and definition
                        and acronym != "nan"
                        and definition != "nan"
                    ):
                        data.append(f"{acronym} - {definition}")  # type: ignore
            else:
                # Default behavior: flatten all data
                for _, row in df.iterrows():
                    row_data = [str(cell) for cell in row if str(cell) != "nan"]
                    if row_data:
                        data.append(" | ".join(row_data))  # type: ignore

        return data
