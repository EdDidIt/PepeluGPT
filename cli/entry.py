#!/usr/bin/env python3
"""
CLI entry point for PepeluGPT — single-mode Q&A.
Main executable file for the PepeluGPT cybersecurity assistant.
"""

from cli.args import parse_args
from cli.runner import run_cli


def main():
    """Main entry point for PepeluGPT CLI."""
    args = parse_args()
    run_cli(args)


if __name__ == "__main__":
    main()
