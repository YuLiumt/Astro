import gzip
import bz2
import re
import os


class CactusScalar:
    _pat_fn = re.compile("^(\w+)((-(\w+))|(\[\d+\]))?\.(minimum|maximum|norm1|norm2|norm_inf|average)?\.asc(\.(gz|bz2))?$")
    _rtypes={'minimum':'min', 'maximum':'max', 'norm1':'norm1', 'norm2':'norm2', 'norm_inf':'infnorm', 'average':'average',None:'scalar'}
    _decompr = {None:open, 'gz':gzip.open, 'bz2':bz2.BZ2File}
    _pat_dc = re.compile("^# data columns: (.+)$")
    _pat_cf = re.compile("^# column format: (.+)$")
    _pat_col = re.compile("^(\d+):(\w+(\[\d+\])?)$")
    def __init__(self, path):
        self.path = str(path)
        self._vars = {}
        self.folder, fn = os.path.split(self.path)
        m = self._pat_fn.match(fn)
        if m is None:
            raise RuntimeError("CactusScalar: naming scheme not recognized for %s" % fn)
        vn1, _0, _1, vn2, vn3, rtyp, _2, self._compr = m.groups()
        if not rtyp in self._rtypes:
            raise RuntimeError("CactusScalar: reduction type %s not recognized" % rtyp)
        self.reduction_type = self._rtypes[rtyp]
        # if one_per_grp, we fetch varable name from file. otherwise from file name
        self._one_per_grp = (vn2 is not None)
        self._hdr_scanned = False
        if self._one_per_grp:
            self._scan_column_header()
        else:
            self._time_col = None
            vn4 = vn1 if (vn3 is None) else ("%s%s" % (vn1, vn3))
            self._vars = {vn4:None}
        

    def _scan_column_header(self):
        if self._hdr_scanned:
            return
        dcp = self._decompr[self._compr]
        with dcp(self.path) as f:
            hdr = [f.readline() for i in range(20)]
            if self.reduction_type == 'scalar': 
                m = self._pat_cf.match(hdr[9])
                if m is None: 
                    raise RuntimeError("CactusScalar: bad header (missing column format in line 10)")
                cols = [self._pat_col.match(col) for col in m.groups()[0].split()]
                if not all(cols):
                    raise RuntimeError("CactusScalarASCII: bad header")
                colsd = {vn:int(cn)-1 for cn, vn, vi in (c.groups() for c in cols)}
                tc = colsd.get('time', None)
                if tc is None:
                    raise RuntimeError("CactusScalarASCII: bad header (missing time column)")
                self._time_col = tc
                data_col = colsd.get('data', None)
                if data_col is None:
                    raise RuntimeError("CactusScalarASCII: bad header (missing data column)")
            else:
                self._time_col = 1
                data_col = 2

            if self._one_per_grp:
                if self.reduction_type == 'scalar': 
                    m = self._pat_dc.match(hdr[10])
                    if m is None: 
                        raise RuntimeError("CactusScalarASCII: bad header (missing data columns in line 11)")
                else:
                    m = self._pat_dc.match(hdr[6])
                    if m is None: 
                        raise RuntimeError("CactusScalarASCII: bad header (missing data columns in line 7)")
                cols = [self._pat_col.match(col) for col in m.groups()[0].split()]
                if not all(cols):
                    raise RuntimeError("CactusScalarASCII: bad header")
                colsd = {vn:int(cn)-1 for cn,vn,vi in (c.groups() for c in cols)}
                if len(colsd)<len(cols):
                    raise RuntimeError("CactusScalarASCII: bad header (duplicate variables)")
                self._vars.update(colsd)
            else:
                self._vars = {self._vars.keys()[0]:data_col}
        self._hdr_scanned = True

    def keys(self):
        return self._vars.keys()

class ScalarReader:
    """
    Helper class to read various types of scalar data. Not intended for direct use.
    """
    def __init__(self, simdir, kind):
        self.kind = str(kind)
        self._vars = {}
        for f in simdir.allfiles:
            try:
                fo = CactusScalar(f)
                if fo.reduction_type == kind:
                    for v in fo.keys():
                        self._vars.setdefault(v, {})[fo.folder] = 1
                    # print(f)
                    # print(fo.keys())
            except RuntimeError:
                pass

    def keys(self):
        return self._vars.keys()

    def __contains__(self, key):
        print(key)
        # return key in self._vars
    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def __str__(self):
        return "\nAvailable %s timeseries:\n%s" % (self.kind, self.keys())

class ScalarsDir:
    """
    This class provides acces to various types of scalar data in a given simulation directory.
    """
    def __init__(self, simdir):
        self.path     = simdir.path
        self.scalar   = ScalarReader(simdir, 'scalar')
        self.min      = ScalarReader(simdir, 'min')
        self.max      = ScalarReader(simdir, 'max')
        self.norm1    = ScalarReader(simdir, 'norm1')
        self.norm2    = ScalarReader(simdir, 'norm2')
        self.average  = ScalarReader(simdir, 'average')
        # self._infnorm = ScalarReader(simdir, 'infnorm')

    def __str__(self):
        return "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (self.path, self.scalar, self.min, self.max, self.norm1, self.norm2, self.average)