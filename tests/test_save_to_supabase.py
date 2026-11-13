import pandas as pd
import pytest

import constants
from logic import external_assessment

EMAIL, DISCIPLINE, GRADE = constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE


class FakePeresdachi:
    """Таблица с уникальностью по (email, дисциплина): как Postgres, отклоняет весь запрос с дубликатом."""

    def __init__(self, existing_emails=(), error=None):
        self.emails = set(existing_emails)
        self.error = error
        self.requests = []

    def table(self, name):
        assert name == constants.DB_TABLE_PERESDACHI
        return self

    def insert(self, records):
        self.pending = records
        return self

    def execute(self):
        self.requests.append(len(self.pending))
        if self.error:
            raise RuntimeError(self.error)
        emails = [record[EMAIL] for record in self.pending]
        if len(set(emails)) < len(emails) or self.emails & set(emails):
            raise RuntimeError('duplicate key value violates unique constraint "peresdachi_unique"')
        self.emails.update(emails)


def records(emails):
    return pd.DataFrame({
        EMAIL: emails,
        DISCIPLINE: constants.DISCIPLINE_FINAL,
        GRADE: "8",
        "Оценка за проект": 8.0,  # колонки вне схемы peresdachi не отправляются
    })


@pytest.fixture
def table(mocker):
    def make(**kwargs):
        fake = FakePeresdachi(**kwargs)
        mocker.patch.object(external_assessment, "get_supabase_client", return_value=fake)
        return fake
    return make


def test_saves_everything_in_one_request_when_there_are_no_duplicates(table):
    fake = table()

    success, message = external_assessment.save_to_supabase(records(["a@edu.hse.ru", "b@edu.hse.ru"]))

    assert (success, message) == (True, "Данные успешно сохранены.")
    assert fake.requests == [2]
    assert fake.emails == {"a@edu.hse.ru", "b@edu.hse.ru"}
    assert "Оценка за проект" not in fake.pending[0]


def test_duplicates_are_skipped_and_the_rest_is_really_saved(table):
    emails = [f"s{i}@edu.hse.ru" for i in range(8)]
    fake = table(existing_emails=["s2@edu.hse.ru", "s7@edu.hse.ru"])

    success, message = external_assessment.save_to_supabase(records(emails))

    assert success
    assert message == "Сохранено 6, пропущено дубликатов 2. Всего записей"
    assert fake.emails == set(emails)


def test_other_errors_are_reported_as_failure(table):
    table(error="permission denied for table peresdachi")

    success, message = external_assessment.save_to_supabase(records(["a@edu.hse.ru"]))

    assert not success
    assert "permission denied" in message


def test_empty_frame_is_not_saved(table):
    fake = table()

    success, _ = external_assessment.save_to_supabase(pd.DataFrame())

    assert not success
    assert fake.requests == []
