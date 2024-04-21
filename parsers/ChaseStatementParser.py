import dateparser

from parsers.StatementParser import StatementParser


class ChaseStatementParser(StatementParser):
    SOURCE = "Chase"
    CSV_FORMAT = ["Details", "Posting Date", "Description", "Amount", "Type", "Balance", "Check or Slip #", ""]
    CSV_CONVERSION = {
        "Posting Date": "Date",
        "Description": "Vendor",
        "Amount": "Amount",
        "Type": "Description"
    }

    def _filter_entries(self, statement: dict) -> dict:
        '''
        Remove rows with positive "Amount" and credit card payments
        '''
        non_debit_rows = [i for i, e in enumerate(statement["Amount"]) if not e.startswith('-')]

        cc_keywords = ["DISCOVER", "CAPITAL ONE"]
        cc_pmt_rows = []
        for i, entry in enumerate(statement["Vendor"]):
            for keyword in cc_keywords:
                if keyword in entry:
                    cc_pmt_rows.append(i)
                    break
        
        excluded_rows = sorted(set(non_debit_rows + cc_pmt_rows))

        for header in statement:
            column = statement[header]

            for r in reversed(excluded_rows):
                column.pop(r)
        
        return statement
    
    def _format_entries(self, statement: dict) -> dict:
        # standardize dates
        statement["Date"] = [ str(dateparser.parse(date).date()) for date in statement["Date"] ]

        # TODO is the $ necessary?
        statement["Amount"] = [ f'${amt.replace("-","")}' for amt in statement["Amount"] ]

        return statement
