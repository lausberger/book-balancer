from parsers.StatementParser import StatementParser


class DiscoverStatementParser(StatementParser):
    SOURCE = "Discover"
    CSV_FORMAT = ["Trans. Date", "Post Date", "Description", "Amount", "Category"]
    CSV_CONVERSION = {
        "Post Date": "Date",
        "Description": "Vendor",
        "Category": "Description",
        "Amount": "Amount"
    }

    def _filter_entries(self, statement: dict) -> dict:
        '''
        Remove rows with a negative "Amount"
        '''
        non_debit_rows = [i for i, e in enumerate(statement["Amount"]) if e.startswith('-')]

        for header in statement:
            column = statement[header]

            for r in reversed(non_debit_rows):
                column.pop(r)
        
        return statement
