#!/usr/bin/env python3
"""
Parse ALL cybersecurity documents and prepare them for vector embedding
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Set
import nltk  # type: ignore
from pathlib import Path
from datetime import datetime

# Type aliases for better readability
ParseResult = Dict[str, Any]
EnvConfig = Dict[str, Any]
FilePath = str
SummaryData = Dict[str, Any]

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')  # type: ignore
    nltk.data.find('tokenizers/punkt_tab')  # type: ignore
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt')  # type: ignore
    nltk.download('punkt_tab')  # type: ignore

# Add current directory to path for module imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from processing.router import parse_files

def get_all_cyber_documents() -> List[FilePath]:
    """Get list of ALL files in cyber_documents folder"""
    cyber_docs_path = Path("cyber_documents")
    if not cyber_docs_path.exists():
        print("🔴 cyber_documents folder not found!")
        return []
    
    supported_extensions: Set[str] = {'.pdf', '.docx', '.html', '.xml', '.pptx', '.txt', '.xls', '.xlsx'}
    files: List[FilePath] = []
    
    for file_path in cyber_docs_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files.append(str(file_path.absolute()))
    
    return sorted(files)

def main() -> Optional[List[ParseResult]]:
    print("� PepeluGPT Full Document Parser")
    print("=" * 60)
    
    # Configuration for parsing
    env_config: EnvConfig = {
        "lowercase": False,  # Keep original case for cybersecurity terms
        "strip_html": True,
        "summary_threshold": 5000,  # Summarize files longer than 5000 chars
        "max_retries": 2
    }
    
    # Get ALL cybersecurity documents
    cyber_files: List[FilePath] = get_all_cyber_documents()
    
    if not cyber_files:
        print("🔴 No supported files found in cyber_documents folder")
        return None
    
    print(f"📁 Found {len(cyber_files)} files to parse:")
    for i, file_path in enumerate(cyber_files, 1):
        print(f"  {i:2d}. {os.path.basename(file_path)}")
    
    print(f"\n� Starting full parsing process...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse ALL files
    results: List[Optional[ParseResult]] = parse_files(cyber_files, env_config)
    
    # Analyze results - filter out None values
    successful: List[ParseResult] = [r for r in results if r is not None and r['status'] == 'success']
    failed: List[ParseResult] = [r for r in results if r is not None and r['status'] == 'error']
    
    print(f"\n� Final Parsing Results:")
    print(f"  🟢 Successful: {len(successful)}")
    print(f"  🔴 Failed: {len(failed)}")
    print(f"  � Success Rate: {len(successful)/len(results)*100:.1f}%")
    
    # Calculate total content
    total_chars: int = sum(len(r.get('content', '')) for r in successful)
    total_tokens: int = sum(len(r.get('tokenized_content', [])) for r in successful)
    
    print(f"\n📄 Content Statistics:")
    print(f"  Total Characters: {total_chars:,}")
    print(f"  🔤 Total Tokens: {total_tokens:,}")
    print(f"  Avg chars per doc: {total_chars//len(successful) if successful else 0:,}")
    
    # Show failed files if any
    if failed:
        print(f"\n🔴 Failed Files:")
        for r in failed:
            filename: str = os.path.basename(r['filename'])
            error: str = r.get('error', 'Unknown error')[:100]
            print(f"  • {filename}: {error}")
    
    # Show top 10 largest documents
    successful.sort(key=lambda x: len(x.get('content', '')), reverse=True)
    print(f"\n📚 Top 10 Largest Documents:")
    for i, r in enumerate(successful[:10], 1):
        filename: str = os.path.basename(r['filename'])
        chars: int = len(r.get('content', ''))
        language: str = r.get('language', 'unknown')
        print(f"  {i:2d}. {filename:<40} {chars:>8,} chars ({language})")
    
    # Save all results
    output_file: str = "parsed_cyber_documents.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full results saved to: {output_file}")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Prepare summary for next step
    summary: SummaryData = {
        "total_files": len(cyber_files),
        "successful_files": len(successful),
        "failed_files": len(failed),
        "total_characters": total_chars,
        "total_tokens": total_tokens,
        "largest_documents": [
            {
                "filename": os.path.basename(r['filename']),
                "characters": len(r.get('content', '')),
                "language": r.get('language', 'unknown')
            } for r in successful[:10]
        ]
    }
    
    with open("parsing_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🔵 Ready for Step 2: Vector Database Setup!")
    return successful

if __name__ == "__main__":
    main()
