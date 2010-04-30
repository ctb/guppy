class BinCount(object):
    def __init__(self):
        self.data = []

    def add(self, d):
        self.data.append(float(d))

    def extend(self, dl):
        self.data.extend(dl)

    def bin(self, binsize, min_=None, max_=None):
        if min_ is None:
            min_ = min(self.data)
        if max_ is None:
            max_ = max(self.data)

        binsize = float(binsize)
        min_ = float(min_)
        max_ = float(max_)

        n_bins = int((max_ - min_) / binsize) + 1
        bins = [0] * n_bins

        calc_bin = lambda d: int((d - min_) / binsize)

        for d in self.data:
            bins[calc_bin(d)] += 1

        return _BinnedData(bins, min_, max_, binsize)

class _BinnedData(object):
    def __init__(self, bins, min_, max_, binsize):
        self.bins = bins
        self.min = min_
        self.max = max_
        self.binsize = binsize

    def values(self, center=True):
        total = sum(self.bins)
        for i, n in enumerate(self.bins):
            center_val = i * self.binsize + self.min
            if center:
                center_val += (self.binsize / 2.)

            yield center_val, n, n / float(total)

    def write(self, fp, **kw):
        cum = 0
        cumfrac = 0.0
        for center, count, frac in self.values(**kw):
            cum += count
            cumfrac += frac
            fp.write('%f %d %f %d %f\n' % (center, count, frac, cum, cumfrac))
