import pytest

import utils


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeQuery:
    def __init__(self, client):
        self.client = client
        self.order_columns = []
        self.filters = []

    def select(self, select_query):
        self.select_query = select_query
        return self

    def eq(self, key, value):
        self.filters.append(("eq", key, value))
        return self

    def in_(self, key, value):
        self.filters.append(("in", key, list(value)))
        return self

    def order(self, column):
        self.order_columns.append(column)
        return self

    def range(self, start, end):
        self.start, self.end = start, end
        return self

    def execute(self):
        self.client.requests.append(self)
        if self.order_columns and self.client.fail_when_ordered:
            raise RuntimeError("column does not exist")
        return FakeResponse(self.client.rows[self.start:self.end + 1])


class FakeClient:
    def __init__(self, rows, fail_when_ordered=False):
        self.rows = rows
        self.fail_when_ordered = fail_when_ordered
        self.requests = []

    def table(self, name):
        return FakeQuery(self)


@pytest.fixture
def fake_client(mocker):
    def make(rows, **kwargs):
        client = FakeClient(rows, **kwargs)
        mocker.patch.object(utils, "get_supabase_client", return_value=client)
        return client
    return make


def test_fetches_all_pages_without_order_by_default(fake_client):
    rows = [{"id": i} for i in range(5)]
    client = fake_client(rows)

    result = utils.fetch_all_from_supabase("students", page_size=2)

    assert result == rows
    assert [(q.start, q.end) for q in client.requests] == [(0, 1), (2, 3), (4, 5)]
    assert all(q.order_columns == [] for q in client.requests)


def test_applies_order_to_every_page(fake_client):
    client = fake_client([{"id": i} for i in range(3)])

    utils.fetch_all_from_supabase("students", page_size=2, order_by=["a", '"b c"'])

    assert len(client.requests) == 2
    assert all(q.order_columns == ["a", '"b c"'] for q in client.requests)


def test_accepts_single_column_name(fake_client):
    client = fake_client([{"id": 1}])

    utils.fetch_all_from_supabase("students", order_by="id")

    assert client.requests[0].order_columns == ["id"]


def test_falls_back_to_unordered_when_ordered_query_fails(fake_client):
    rows = [{"id": i} for i in range(3)]
    client = fake_client(rows, fail_when_ordered=True)

    result = utils.fetch_all_from_supabase("students", page_size=2, order_by="id")

    assert result == rows
    assert client.requests[0].order_columns == ["id"]
    assert all(q.order_columns == [] for q in client.requests[1:])


def test_filters_are_passed_through(fake_client):
    client = fake_client([{"id": 1}])

    utils.fetch_all_from_supabase("students", filters={"курс": ["Курс 3", "Курс 4"], "уровень": "Бакалавриат"})

    assert client.requests[0].filters == [("in", "курс", ["Курс 3", "Курс 4"]), ("eq", "уровень", "Бакалавриат")]
