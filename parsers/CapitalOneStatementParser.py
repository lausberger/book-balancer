from parsers.StatementParser import StatementParser


class CapitalOneStatementParser(StatementParser):
    SOURCE = "Capital One"
    CSV_FORMAT = ["Transaction Date", "Posted Date", "Card No.", "Description",	"Category",	"Debit", "Credit"]
    CSV_CONVERSION = {
        "Posted Date": "Date", 
        "Description": "Vendor", 
        "Category": "Description", 
        "Debit": "Amount"
    }
