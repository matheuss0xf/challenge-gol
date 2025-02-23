from unittest.mock import MagicMock, patch

import pytest

from app.repositories.flight import FlightRepository
from app.services.flight import FlightService


@pytest.fixture
def mock_flight_repo():
    return MagicMock(FlightRepository)


@patch('app.services.flight.FlightRepository')
def test_search_flights(repo_fake, mock_flight_repo):
    mock_flight_repo.get_flights.return_value = [
        MagicMock(mercado='SBARSBBR', ano=2022, mes=5, rpk=4237760.0),
    ]
    repo_fake.return_value = mock_flight_repo

    service = FlightService()
    query_params = {'market': 'SBARSBBR', 'flight_date': '2022/05;2022/06', 'sort': 'year:asc,month:desc'}
    result = service.search_flights(query_params)

    assert len(result) == 1
    assert result[0]['mercado'] == 'SBARSBBR'
    mock_flight_repo.get_flights.assert_called_once_with(
        filters={'market': 'SBARSBBR', 'start_year': 2022, 'start_month': 5, 'end_year': 2022, 'end_month': 6},
        sort=[('year', 'asc'), ('month', 'desc')],
    )


def test_validate_and_parse_params():
    service = FlightService()
    query_params = {'market': 'SBARSBBR', 'flight_date': '2022/05;2022/06', 'sort': 'year:asc,month:desc'}
    result = service._validate_and_parse_params(query_params)

    assert result['filters'] == {
        'market': 'SBARSBBR',
        'start_year': 2022,
        'start_month': 5,
        'end_year': 2022,
        'end_month': 6,
    }
    assert result['sort'] == [('year', 'asc'), ('month', 'desc')]


def test_parse_date_filter_invalid():
    service = FlightService()
    with pytest.raises(ValueError, match='Invalid date format: Date must contain valid numbers'):
        service._parse_date_filter('2022/05;2023/13')  # Mês inválido


def test_parse_sort_invalid_field():
    service = FlightService()
    with pytest.raises(ValueError, match='Invalid field for sorting: invalid_field'):
        service._parse_sort('invalid_field:asc')


def test_parse_sort_invalid_direction():
    service = FlightService()
    with pytest.raises(ValueError, match='Invalid direction: invalid'):
        service._parse_sort('year:invalid')


def test_parse_single_date_invalid_format():
    service = FlightService()
    with pytest.raises(ValueError, match='Date must contain valid numbers'):
        service._parse_single_date('2022/25/12', is_end=False)
