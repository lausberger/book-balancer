import csv
import dateparser
from pathlib import Path


class StatementParser:
    STANDARD_FORMAT = ["Date", "Vendor", "Amount", "Description", "Source"]
    REQUIRED_ATTRIBUTES = ["CSV_CONVERSION", "CSV_FORMAT", "SOURCE"]

    def __init__(self, csv_file_path: Path):
        # python classes are kinda dumb. defining the interface here
        for attr in self.REQUIRED_ATTRIBUTES:
            if not hasattr(self, attr):
                raise Exception(f"Object of type {type(self)} has no attribute {attr}")

        if not csv_file_path.exists():
            raise Exception(f"Invalid file path: {csv_file_path}")
        
        self.csv_file_path = csv_file_path

    def __raise_continue_prompt(self):
        while True:
            answer = input("Continue parsing? (y/n) ")

            if 'y' in answer.lower():
                return
            elif 'n' in answer.lower():
                print("Aborting...")
                exit()
            else:
                print("Invalid response")
                pass

    def parse_csv(self, force: bool = False) -> list:
        with open(self.csv_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
        
            headers = next(csv_reader)

            if headers != self.CSV_FORMAT and not force:
                print(f"Unrecognized header format: {headers}")
                self.__raise_continue_prompt()

            csv_columns = {header: [] for header in self.CSV_FORMAT}

            self.num_rows = 0
            for row in csv_reader:
                if not row: # last row is empty
                    break
                for i, cell in enumerate(row):
                    csv_columns[self.CSV_FORMAT[i]].append(cell)
                self.num_rows += 1

        statement = { header: [''] * self.num_rows for header in self.STANDARD_FORMAT }
        statement["Source"] = [self.SOURCE] * self.num_rows

        # omit headers that do not correspond to the standard format
        for header in csv_columns:
            if header in self.CSV_CONVERSION:
                true_header = self.CSV_CONVERSION[header]

                statement[true_header] = csv_columns[header]
        
        statement = self._filter_entries(statement)
        statement = self._format_entries(statement)

        return statement

    def _filter_entries(self, statement: dict) -> dict:
        '''
        Remove rows with an empty "Amount"
        '''
        non_debit_rows = [i for i, e in enumerate(statement["Amount"]) if not e]

        for header in statement:
            column = statement[header]

            for r in reversed(non_debit_rows):
                column.pop(r)
        
        return statement

    def _format_entries(self, statement: dict) -> dict:
        # standardize dates
        statement["Date"] = [ str(dateparser.parse(date).date()) for date in statement["Date"] ]

        # TODO is the $ necessary?
        statement["Amount"] = [ f'${amt}' for amt in statement["Amount"] ]

        return statement
