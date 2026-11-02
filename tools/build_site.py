"""Regenerates the whole TemplivoX site. Usage: python3 build_site.py [output_folder]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import files, pages as S
root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files.build_files(root)
S.build_site(root)
print("Built site in", root)
