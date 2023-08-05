from .components import *


class Query:
    def __init__(self, metric: str, debug=False) -> None:
        self._debug = debug
        self._components: dict[str, Component] = {
            'aggr': Aggregator('sum'),
            'rate': None,
            'metric': Metric(metric),
            'filters': Filters(),
        }

    def aggr(self, aggr) -> 'Query':
        self._components['aggr'] = Aggregator(aggr)
        return self

    def rate(self, counter=False, counterMax: int = None, resetValue: int = None, dropResets: bool = None) -> 'Query':
        '''
        :param ctr: 
        :param dropResets: Whether or not to simply drop rolled-over or reset data points.
        '''
        self._components['rate'] = RateOptions([counter, counterMax, resetValue, dropResets])
        return self

    def filters(self, filters: dict) -> 'Query':
        self._components['filters'].update(filters)
        return self

    def m(self):
        query = ''
        for c in ['aggr', 'rate', 'metric', 'filters']:
            if self._debug:
                print(c, self._components[c])
            if comp := self._components[c]:
                query += comp.m()

        return query
