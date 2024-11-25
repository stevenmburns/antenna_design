from .. import AntennaBuilder
import math
from types import MappingProxyType


class Builder(AntennaBuilder):
  default_params = MappingProxyType({
    'freq': 28.57,
    'base': 7,
    #'halfdriver': 2.6416,
    'halfdriver': 2.841,
    'tipspacer_factor': 0.1900,
    't0_factor': 0.1171
  })

  opt_params = MappingProxyType({'freq': 28.57, 'base': 7, 'halfdriver': 2.782539354535098, 'tipspacer_factor': 0.20803460322922357, 't0_factor': 0.07058920808116927})

  def build_wires(self):
    eps = 0.05

    #2*radius = self.halfdriver + t0_factor*radius + tipspacer_factor*radius
    #2*radius - t0_factor*radius - tipspacer_factor*radius = self.halfdriver
    radius = self.halfdriver/(2-self.t0_factor-self.tipspacer_factor)

    tipspacer = radius * self.tipspacer_factor
    t0 = radius*self.t0_factor
    t1 = radius - tipspacer - t0

    sin30 = 1/2
    cos30 = math.sqrt(3)/2
    # x is the beam direction

    def build_path(lst, ns, ex):
      return ((a,b,ns,ex) for a,b in zip(lst[:-1], lst[1:]))

    def rx(p):
      return -p[0],  p[1], p[2]
    def ry(p):
      return  p[0], -p[1], p[2]

    A = (radius*cos30, radius*sin30, 0)
    B = (A[0]-t1*cos30, A[1]+t1*sin30, 0)
    D = (0, radius, 0)
    C = (D[0]+t0*cos30, D[1]-t0*sin30, 0)
    E = rx(A)
    F = ry(E)
    G = ry(D)
    H = ry(C)
    II = ry(B)
    J = ry(A)

    S = (eps*cos30, eps*sin30, 0) 
    T = ry(S)

    n_seg0 = 21
    n_seg1 = 1
      
    tups = []
    tups.extend(build_path([S,A,B], n_seg0, False))
    tups.extend(build_path([C,D], 5, False))
    tups.extend(build_path([D,E,F,G], n_seg0, False))
    tups.extend(build_path([G,H], 5, False))
    tups.extend(build_path([II,J,T], n_seg0, False))
    tups.append((T, S, n_seg1, True))

    new_tups = []
    for (xoff, yoff, zoff) in [(0, 0, self.base)]:
      new_tups.extend([((x0+xoff, y0+yoff, z0+zoff), (x1+xoff, y1+yoff, z1+zoff), ns, ex) for ((x0, y0, z0), (x1, y1, z1), ns, ex) in tups])

    return new_tups
