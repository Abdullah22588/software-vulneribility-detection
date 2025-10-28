# -----------------------------------------------
# File: utils/report_generator.py
# Purpose: Generate and save analysis report
# -----------------------------------------------

import os

def generate_report(results, output_path='results/report1.txt'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Open file with UTF-8 encoding to support emojis/symbols
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in results:
            f.write(f"{item}\n")

    print(f"\n📄 Report saved to {output_path}")
