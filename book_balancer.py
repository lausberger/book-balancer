from pathlib import Path

from StatementSummarizer import StatementSummarizer

from parsers.StatementParser import StatementParser
from parsers.DiscoverStatementParser import DiscoverStatementParser
from parsers.CapitalOneStatementParser import CapitalOneStatementParser
from parsers.HSBStatementParser import HSBStatementParser
from parsers.ChaseStatementParser import ChaseStatementParser


PARSER_MAPPING = {
    "hsb": HSBStatementParser,
    "chase": ChaseStatementParser,
    "capital_one": CapitalOneStatementParser,
    "discover": DiscoverStatementParser
}

OUTPUT_DIR = Path(__file__).parent / "out"
INPUT_DIR = Path(__file__).parent / "statements"
OVERWRITE = True
FORCE_PARSE = True


def summarize_statements():
    statements = {}

    for folder in INPUT_DIR.iterdir():
        if not folder.is_dir() or folder.stem not in PARSER_MAPPING:
            continue

        parser_class = PARSER_MAPPING[folder.stem]

        for file in folder.iterdir():
            if not file.is_file() or file.suffix.lower() != ".csv":
                continue

            if file.stem not in statements:
                statements[file.stem] = []
                
            parser: StatementParser = parser_class(file)
            statements[file.stem].append(parser.parse_csv(force=FORCE_PARSE))

    for month in statements:
        summarizer = StatementSummarizer(*statements[month])
        summarizer.write_to_csv(OUTPUT_DIR / f"{month}.csv", overwrite=OVERWRITE)


if __name__ == '__main__':
    summarize_statements()
