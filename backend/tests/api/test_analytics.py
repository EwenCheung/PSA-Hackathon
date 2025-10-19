from unittest.mock import MagicMock, patch

import pandas as pd
from pandas.errors import DatabaseError

from app.api.v1 import analytics


@patch("app.api.v1.analytics.sqlite3.connect")
@patch("app.api.v1.analytics.pd.read_sql_query")
def test_get_company_overview_handles_missing_table(mock_read_sql, mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read_sql.side_effect = DatabaseError("no such table: employee_insights")

    overview = analytics.get_company_overview()

    assert overview["total_employees"] == 0
    assert overview["roles_count"] == {}
    assert overview["top_skills"] == []
    mock_conn.close.assert_called_once()


@patch("app.api.v1.analytics.sqlite3.connect")
@patch("app.api.v1.analytics.pd.read_sql_query")
def test_get_employee_details_handles_missing_table(mock_read_sql, mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read_sql.side_effect = DatabaseError("no such table: employee_insights")

    employees = analytics.get_employee_details()

    assert employees == []
    mock_conn.close.assert_called_once()
