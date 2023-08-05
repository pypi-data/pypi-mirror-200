# tsdb query string builder

```python
from tsdb.query import Query
from tsdb.query.filters import *

if __name__ == '__main__':
    print(Query('some.metrics').rate(True, 10, 20).aggr('max').filters({
        'a': 'b', 'c': 'd',
        'e': literal_or('f'),
        'g': regexp('.*', groupBy=False),
        'h': not_key(),
    }).m())
# max:rate{counter,10,20}:some.metrics{a=b,c=d,e=literal_or(f),h=not_key()}{g=regexp(.*)}
```
