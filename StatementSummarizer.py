import csv
from pathlib import Path


class StatementSummarizer:
    def __init__(self, *statements: dict):
        self.statement = self.__combine_statements(*statements)
    
    def __combine_statements(self, *statements: dict) -> dict:
        combined_statement = {}

        for d in statements:
            for key, value in d.items():
                combined_statement[key] = combined_statement.get(key, []) + value
        
        return combined_statement
    
    def _get_statement_rows(self, statement: dict) -> list:
        return list(zip(*statement.values()))
    
    def _get_summary(self, statement: dict) -> tuple[list]:
        summary_headers = ["Total"]

        total = sum([round(float(amt.replace('$', '')), 2) for amt in statement["Amount"]])
        total_amount = f'${total}'

        return summary_headers, [total_amount]

    def write_to_csv(self, output_file: Path, overwrite: bool = False):
        if not overwrite and output_file.exists():
            raise Exception(f"Output file {output_file} already exists. Aborting.")
        
        with open(output_file, 'w+') as csv_file:
            csv_writer = csv.writer(csv_file)

            summary = self._get_summary(self.statement)
            csv_writer.writerows(summary)

            headers = self.statement.keys()
            rows = self._get_statement_rows(self.statement)

            csv_writer.writerow(headers)
            csv_writer.writerows(rows)
