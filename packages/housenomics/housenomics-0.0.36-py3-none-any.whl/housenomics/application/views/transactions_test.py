import pytest

from housenomics.application.views.transactions import ViewTransactions


class Database:
    def scalars(*_):
        return []


@pytest.mark.integration
def test_shown_no_transactions_on_empty_database():
    db = Database()

    transactions, total = ViewTransactions(db).data

    assert not transactions  # nosec
    assert not total  # nosec
