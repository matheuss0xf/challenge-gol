from app.repositories.flight import FlightRepository


class FlightService:
    def __init__(self):
        # TODO: Desacoplar a criação do repositório
        self.repo = FlightRepository()

    def search_flights(self, query_params):
        validated_params = self._validate_and_parse_params(query_params)
        flights = self.repo.get_flights(**validated_params)
        return [self._flight_to_dict(f) for f in flights]

    def _validate_and_parse_params(self, query_params):
        filters = {}

        if query_params['market']:
            filters['market'] = query_params['market'].strip().upper()

        if query_params['flight_date']:
            filters.update(self._parse_date_filter(query_params['flight_date']))

        sort = self._parse_sort(query_params['sort'])

        return {'filters': filters, 'sort': sort}

    def _parse_date_filter(self, flight_date_str):
        try:
            if not flight_date_str or flight_date_str.strip() == ';':
                return {}

            date_parts = flight_date_str.split(';', 1)
            start_str = date_parts[0].strip() if date_parts[0].strip() else None
            end_str = date_parts[1].strip() if len(date_parts) > 1 else None

            date_filters = {}
            if start_str:
                start_year, start_month = self._parse_single_date(start_str, is_end=False)
                date_filters.update({'start_year': start_year, 'start_month': start_month})

            if end_str:
                end_year, end_month = self._parse_single_date(end_str, is_end=True)
                date_filters.update({'end_year': end_year, 'end_month': end_month})

            if date_filters.get('start_year') and date_filters.get('end_year'):
                start_num = date_filters['start_year'] * 100 + date_filters.get('start_month', 1)
                end_num = date_filters['end_year'] * 100 + date_filters.get('end_month', 12)
                if start_num > end_num:
                    raise ValueError('Start date is greater than end date')

            return date_filters

        except ValueError as e:
            raise ValueError(f'Invalid date format: {str(e)}')

    @staticmethod
    def _parse_single_date(date_str, is_end=False):
        min_month = 1
        max_month = 12
        min_parts = 1
        max_parts = 3
        parts_for_month = 2
        parts = date_str.split('/')
        if len(parts) < min_parts or len(parts) > max_parts:
            raise ValueError('Format must be YYYY, YYYY/MM, or YYYY/MM/DD')

        try:
            year = int(parts[0])
            month = max_month if is_end else min_month

            if len(parts) >= parts_for_month:
                month = int(parts[1])
                if month < min_month or month > max_month:
                    raise ValueError(f'Month must be between {min_month}-{max_month}')

            return year, month
        except ValueError:
            raise ValueError('Date must contain valid numbers')

    @staticmethod
    def _parse_sort(sort_str):
        allowed_fields = {'year', 'month', 'market', 'rpk'}
        sort_params = []

        if not sort_str:
            return [('year', 'asc'), ('month', 'asc')]

        for part in sort_str.split(','):
            field, _, direction = part.partition(':')
            field = field.strip().lower()
            direction = direction.strip().lower()

            if field not in allowed_fields:
                raise ValueError(f'Invalid field for sorting: {field}')
            if direction not in {'asc', 'desc'}:
                raise ValueError(f'Invalid direction: {direction}')

            sort_params.append((field, direction))

        return sort_params or [('year', 'asc'), ('month', 'asc')]

    @staticmethod
    def _flight_to_dict(flight):
        return {'mercado': flight.mercado, 'ano': flight.ano, 'mes': flight.mes, 'rpk': flight.rpk}
