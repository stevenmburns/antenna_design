from .. import AntennaBuilder
from types import MappingProxyType

class Builder(AntennaBuilder):
  original_params = MappingProxyType({
    'freq': 28.57,
    'base': 7,
    'halfdriver': (147.25 / 2 + 22 + 3/16)*0.0254,
    'aspect_ratio': (53 + 11/16) / 147.25,
    'tipspacer_factor': (4 + 1/16)/ (53 + 11/16),
    't0_factor': (22 + 3/16)/ (53 + 11/16)
  })

  default_params = MappingProxyType(
{'freq': 28.57, 'base': 7, 'halfdriver': 2.4597430629596713, 'aspect_ratio': 0.3646010186757216, 'tipspacer_factor': 0.07729647745945359, 't0_factor': 0.4078045966770739}
  )

  opt_params = MappingProxyType(
{'freq': 28.57, 'base': 7, 'halfdriver': 2.4454699666515394, 'aspect_ratio': 0.3646010186757216, 'tipspacer_factor': 0.047061074343758946, 't0_factor': 0.42268888502818136}
  )

  def build_wires(self):
    eps = 0.05
    base = self.base

    # short = aspect_ratio*long
    # halfdriver = long/2 + short*t0_factor
    # halfdriver = long/2 + aspect_ratio*long*t0_factor
    # 2*halfdriver = long + 2*aspect_ratio*long*t0_factor
    # 2*halfdriver = long*(1 + 2*aspect_ratio*t0_factor)
    # long = 2*halfdriver/(1 + 2*aspect_ratio*t0_factor)

    long = 2*self.halfdriver / (1 + 2*self.aspect_ratio*self.t0_factor)
    short = self.aspect_ratio * long

    tipspacer = short * self.tipspacer_factor
    t0 = short * self.t0_factor

    def build_path(lst, ns, ex):
      return ((a,b,ns,ex) for a,b in zip(lst[:-1], lst[1:]))
    def rx(p):
      return -p[0],  p[1], p[2]
    def ry(p):
      return  p[0], -p[1], p[2]

    """
    D----------C   B-----A
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    |                    S
    |                    |
    |                    T
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    |                    |
    E----------F   G-----H
	"""

    S = (short/2,       eps,    base) 
    A = (S[0],          long/2, base)
    B = (A[0]-t0,        A[1],   base)
    C = (B[0]-tipspacer, B[1],   base)
    D = rx(A)
    E, F, G, H, T = ry(D), ry(C), ry(B), ry(A), ry(S)

    n_seg0, n_seg1 = 21, 1
      
    tups = []
    tups.extend(build_path([S,A,B], n_seg0, None))
    tups.extend(build_path([C,D,E,F], n_seg0, None))
    tups.extend(build_path([G,H,T], n_seg0, None))
    tups.append((T, S, n_seg1, 1+0j))

    return tups
