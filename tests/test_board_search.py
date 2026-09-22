"""Unit tests for crew.board.search_tickets."""
from crew.board import search_tickets


def _ticket(number: int, title: str, body: str = "", plan: str = "alpha") -> dict:
    return {"number": number, "title": title, "body": body, "plan": plan}


def test_empty_query_returns_nothing():
    tickets = [_ticket(1, "Hello world")]
    assert search_tickets(tickets, "") == []
    assert search_tickets(tickets, "   ") == []


def test_single_token_matches_title():
    tickets = [_ticket(1, "Add login flow"), _ticket(2, "Fix logout bug")]
    assert search_tickets(tickets, "login") == [tickets[0]]


def test_single_token_matches_body():
    tickets = [
        _ticket(1, "Refactor", body="the login flow needs work"),
        _ticket(2, "Refactor", body="unrelated content"),
    ]
    assert search_tickets(tickets, "login") == [tickets[0]]


def test_multi_token_requires_all_tokens_present():
    tickets = [
        _ticket(1, "Add login flow", body="supports oauth and saml"),
        _ticket(2, "Add login flow", body="only oauth"),
        _ticket(3, "Add signup", body="oauth and saml"),
    ]
    result = search_tickets(tickets, "oauth saml")
    assert result == [tickets[0]]


def test_case_insensitive():
    tickets = [_ticket(1, "Add LOGIN Flow")]
    assert search_tickets(tickets, "login") == tickets
    assert search_tickets(tickets, "LOGIN") == tickets


def test_punctuation_in_query_does_not_block_match():
    tickets = [_ticket(1, "Fix login, please!")]
    assert search_tickets(tickets, "login, please!") == tickets


def test_no_match_returns_empty():
    tickets = [_ticket(1, "Add login flow")]
    assert search_tickets(tickets, "logout") == []


def test_token_in_middle_of_word_does_not_block():
    """Tokens are substring matches, so 'log' matches 'login' intentionally."""
    tickets = [_ticket(1, "Add login flow")]
    assert search_tickets(tickets, "log") == tickets
