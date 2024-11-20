from antenna import *

def get_dipole_data():
  return { 'freq': 28.57, 'base': 7, 'length': 5.032}

class DipoleBuilder(AntennaBuilder):
  def __init__(self, freq, base, length):
    super().__init__(freq)
    self.params['base'] = base
    self.params['length'] = length

  def build_wires(self):
    eps = 0.05

    x = 0.5*self.length

    n_seg0 = 21
    n_seg1 = 3

    tups = []
    tups.extend([((-x,   0), (-eps, 0), n_seg0, False)])
    tups.extend([(( eps, 0), ( x,   0),    n_seg0, False)])
    tups.extend([((-eps, 0), ( eps, 0), n_seg1, True)])

    new_tups = []
    for (yoff, zoff) in [(0, self.base)]:
      new_tups.extend([((0, y0+yoff, z0+zoff), (0, y1+yoff, z1+zoff), ns, ex) for ((y0, z0), (y1, z1), ns, ex) in tups])

    return new_tups
