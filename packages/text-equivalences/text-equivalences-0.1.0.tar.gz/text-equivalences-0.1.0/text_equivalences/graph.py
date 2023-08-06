from collections import namedtuple, defaultdict

Transition = namedtuple('Transition', ['u', 'v', 'ilabel', 'olabel'])

class Graph:
  def __init__(self):
    self.num_states = 0
    self.final_state = None
    self.edges = defaultdict(list)

  def get_final_state(self):
    if self.final_state is None:
      self.final_state = self.new_state()
    return self.final_state
  
  def new_state(self):
    self.num_states += 1
    return self.num_states-1
  
  def add_edge(self, u,v,ilabel,olabel):
    assert u != v
    self.edges[u].append(Transition(u, v, ilabel, olabel))
  
  def add_subgraph(self,u,v,g):
    assert g.final_state is not None
    s = defaultdict(self.new_state)
    s[0] = u;
    s[g.get_final_state()] = v
    for u1 in range(g.num_states):
      for _, v1, i, o in g.edges[u1]:
        self.add_edge(s[u1], s[v1], i, o)

  def dump(self, fh):
    for u in range(self.num_states):
      for u,v,i,o in self.edges[u]:
        if i is None:
          i = '<eps>'
        if o is None:
          o = '<eps>'
        fh.write(f'{u}\t{v}\t{i}\t{o}\t0.0\n')
    if self.final_state is not None:
      fh.write(f'{self.final_state} 0.0')
  
  def edge_list(self):
    return sorted([e for u in range(self.num_states) for e in self.edges[u]], 
      key=lambda e:(e.u, e.v, 
        str(e.ilabel) if e.ilabel is not None else '', 
        str(e.olabel) if e.olabel is not None else ''
      ))