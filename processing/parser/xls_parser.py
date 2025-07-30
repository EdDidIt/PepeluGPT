from typing import Dict, Any, List
import xlrd  # type: ignore

def parse(filepath: str) -> Dict[str, Any]:
    try:
        # Open the XLS workbook
        workbook = xlrd.open_workbook(filepath)
        content: str = ""
        
        # Process all worksheets
        for sheet_index in range(workbook.nsheets):
            sheet = workbook.sheet_by_index(sheet_index)
            sheet_name: str = sheet.name
            content += f"=== Sheet: {sheet_name} ===\n"
            
            # Extract data from all rows and columns
            for row_num in range(sheet.nrows):
                row_data: List[str] = []
                for col_num in range(sheet.ncols):
                    cell_value = sheet.cell_value(row_num, col_num)
                    if cell_value:  # Skip empty cells
                        row_data.append(str(cell_value))
                if row_data:  # Only add non-empty rows
                    content += "\t".join(row_data) + "\n"
            content += "\n"
        
        return {
            "status": "success",
            "filename": filepath,
            "content": content.strip(),
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "filename": filepath,
            "content": None,
            "error": str(e)
        }