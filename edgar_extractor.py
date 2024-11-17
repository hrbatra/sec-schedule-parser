"""
Edgar Schedule of Investments Extractor
-------------------------------------
Downloads and processes Schedule of Investments from SEC EDGAR filings.
"""

import os
import csv
import shutil
from edgar import Company, set_identity

class ScheduleOfInvestmentsExtractor:
    def __init__(self, email: str, output_dir: str = "output"):
        self.email = email
        set_identity(email)
        self.output_dir = output_dir
        
    def _download_filing(self, ticker: str, form_type: str, latest_n: int = 1):
        filings = Company(ticker).get_filings(form=form_type).latest(latest_n)
        return [filings] if latest_n == 1 else filings
    
    def _get_sections(self, filing_text: str) -> list[str]:
        split_text = filing_text.split("Consolidated Schedule of Investments")
        
        if len(split_text) == 1:
            return []
        
        sections = ["Consolidated Schedule of Investments" + section for section in split_text[1:]]
        max_lines = max(len(section.splitlines()) for section in sections[:-1])
        sections = [section for section in sections if len(section.splitlines()) <= 1.5 * max_lines]
        
        return sections
    
    def _parse_sections(self, sections: list[str], output_path: str) -> None:
        all_rows = []
        seen_rows = set()
        
        for section in sections:
            lines = [line.strip() for line in section.splitlines() if line.strip().startswith('|')]
            for line in lines:
                cols = [col.strip() for col in line.split('|')[1:-1]]
                if cols:
                    row_str = ','.join(cols)
                    if row_str not in seen_rows:
                        seen_rows.add(row_str)
                        all_rows.append(cols)
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(all_rows)
    
    def process_companies(self, schema: dict, output_dir: str = None) -> None:
        """
        Process companies according to schema.
        
        Args:
            schema (dict): Dictionary specifying companies and filings to process
                Format: {
                    "TICKER": {"10-Q": n_quarters, "10-K": n_years},
                    ...
                }
            output_dir (str, optional): Override default output directory
        """
        output_dir = output_dir or self.output_dir
        
        for ticker, forms in schema.items():
            print(f"Processing {ticker}...")
            for form_type, latest_n in forms.items():
                if latest_n == 0:
                    continue
                    
                print(f"  Downloading {latest_n} {form_type} filing(s)...")
                filings = self._download_filing(ticker, form_type, latest_n)
                
                for filing in filings:
                    filing_dict = filing.to_dict()
                    company_name = filing_dict['company'].replace(' ', '_').replace(',', '').replace('.', '')
                    
                    base_dir = f"{output_dir}/{company_name}"
                    os.makedirs(base_dir, exist_ok=True)
                    
                    sections = self._get_sections(filing.markdown())
                    if sections:
                        output_path = os.path.join(base_dir, f"{ticker}_{form_type}_{filing_dict['filing_date']}.csv")
                        self._parse_sections(sections, output_path)
                        print(f"    Saved {os.path.basename(output_path)}")
                    
        shutil.make_archive(self.output_dir, 'zip', self.output_dir)
        print(f"\nResults saved to {self.output_dir}.zip")

# Example usage if run as a script
if __name__ == "__main__":
    USER_EMAIL = "your.email@domain.com"  # Replace with your email
    
    # Default schema - modify as needed
    SCHEMA = {
        "GSBD": {"10-Q": 4, "10-K": 1},
        "OBDC": {"10-Q": 4, "10-K": 1},
        "BBDC": {"10-Q": 4, "10-K": 1},
        "BCSF": {"10-Q": 4, "10-K": 1}
    }
    
    extractor = ScheduleOfInvestmentsExtractor(USER_EMAIL)
    extractor.process_companies(SCHEMA)