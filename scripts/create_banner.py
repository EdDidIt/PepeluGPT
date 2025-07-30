#!/usr/bin/env python3
"""
Create professional ASCII banners for PepeluGPT (Professional Edition)
"""

def create_ascii_banner():
    """
    Returns the full ASCII banner for the professional edition
    """
    banner = """<unchanged, as provided above>"""
    return banner

def create_simple_banner():
    """
    Returns a simplified banner for README or CLI output
    """
    banner = (
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "     PepeluGPT: Professional Cybersecurity Intelligence Platform\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "    Enterprise Security Intelligence Platform\n"
        "     Reliable, Professional, Secure\n"
        "═══════════════════════════════════════════════════════════════════════════════"
    )
    return banner

if __name__ == "__main__":
    print("🔵 Professional ASCII Banner:")
    print(create_ascii_banner())

    print("\n" + "="*80)
    print("\n🔵 Simple Banner:")
    print(create_simple_banner())