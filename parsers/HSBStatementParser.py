from parsers.StatementParser import StatementParser


class HSBStatementParser(StatementParser):
    SOURCE = "Home State Bank"
    CSV_FORMAT = ["Account", "ChkRef", "Debit", "Credit", "Balance", "Date", "Description"]
    CSV_CONVERSION = {
        "Date": "Date",
        "Description": "Vendor",
        "Debit": "Amount"
    }
