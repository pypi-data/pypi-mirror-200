from . import filters


class Component:
    def m(self):
        raise NotImplementedError()


class Aggregator(Component, str):
    def __new__(cls, val):
        if val not in ["min", "sum", "max", "avg", "dev"]:
            raise ValueError('invalid aggregator')
        return str.__new__(cls, val)

    def m(self):
        return self + ':'


class RateOptions(Component):
    def __init__(self, v):
        self.counter, self.counterMax, self.resetValue, self.dropResets = v
        if self.dropResets and not self.counter:
            raise ValueError('invalid rate params')

    def m(self):
        if not self.counter and not self.dropResets:
            return 'rate:'
        ar = ['counter' if not self.dropResets else 'dropcounter']
        if self.counterMax:
            ar.append(str(self.counterMax))
        if self.resetValue:
            if len(ar) == 1:
                ar.append('')
            ar.append(str(self.resetValue))
        return f'''rate{{{",".join(ar)}}}:'''


class Metric(Component, str):
    def m(self):
        return self


class Filters(Component, dict):
    def m(self):
        if not self:
            return ''
        is_group_by = lambda v: (v.group_by if isinstance(v, filters._filter) else True)
        # grouped filters
        gf = {k: v for k, v in self.items() if is_group_by(v)}
        # non-grouped filters
        ngf = {k: v for k, v in self.items() if not is_group_by(v)}
        fmt = lambda v: '{{{}}}'.format(','.join(
            f'{k}={v.m() if isinstance(v, filters._filter) else v}' for k, v in v.items()
        ))
        if ngf:
            return fmt(gf) + fmt(ngf)
        else:
            return fmt(gf)
