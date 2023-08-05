from secenv.utils import escape


def test_escape_empty():
    assert escape("") == "''"


def test_escape_number():
    assert escape(69420) == "'69420'"


def test_escape_bool():
    assert escape(True) == "'True'"


def test_escape_str():
    assert escape("hello world") == "'hello world'"


def test_escape_dollar():
    assert escape("$str") == "'$str'"


def test_escape_single_quote():
    assert escape("st'r") == '"st\'r"'


def test_escape_double_quote():
    assert escape('st"r') == "'st\"r'"


def test_escape_both_quotes():
    assert escape("""s't"r""") == "'s'\"'\"'t\"r'"


def test_escape_single_quote_and_dollar():
    assert escape("s't$r") == '"s\'t\\$r"'


def test_escape_double_quote_and_dollar():
    assert escape('s"t$r') == "'s\"t$r'"


def test_escape_both_quotes_and_dollar():
    assert escape("""s't"r$""") == "'s'\"'\"'t\"r$'"
