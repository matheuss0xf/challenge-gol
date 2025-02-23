from sqlalchemy import and_, asc, desc, or_

from app.database.connection import DBConnectionHandler
from app.models.flight import FlightModel


class FlightRepository:
    def get_flights(self, filters, sort):
        with DBConnectionHandler() as db:
            query = db.session.query(FlightModel)
            query = self._apply_filters(query, filters)
            query = self._apply_sort(query, sort)
            return query.all()

    @staticmethod
    def _apply_filters(query, filters):
        if 'market' in filters:
            query = query.filter(FlightModel.mercado == filters['market'])

        if 'start_year' in filters:
            start_year = filters['start_year']
            start_month = filters.get('start_month', 1)
            query = query.filter(
                or_(FlightModel.ano > start_year, and_(FlightModel.ano == start_year, FlightModel.mes >= start_month))
            )

        if 'end_year' in filters:
            end_year = filters['end_year']
            end_month = filters.get('end_month', 12)
            query = query.filter(
                or_(FlightModel.ano < end_year, and_(FlightModel.ano == end_year, FlightModel.mes <= end_month))
            )

        return query

    @staticmethod
    def _apply_sort(query, sort_params):
        field_mapping = {'year': 'ano', 'month': 'mes', 'market': 'mercado', 'rpk': 'rpk'}

        for field, direction in sort_params:
            mapped_field = field_mapping.get(field)
            if not mapped_field:
                raise ValueError(f'Campo inválido para ordenação: {field}')

            column = getattr(FlightModel, mapped_field)
            query = query.order_by(asc(column) if direction == 'asc' else desc(column))

        return query
