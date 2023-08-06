from . import graph
import itertools
class Transducer:
  def __init__(self, *args):
    self.args = [v if isinstance(v, Transducer) else Literal(v) for v in args]
  def __add__(self, other):
    return Concatenate(self, other)
  def __neg__(self):
    return Optional(self)
  def __or__(self, other):
    return Interchangeable(self, other)
  def __truediv__(self, other):
    return Alternatives(self, other)
  def __sub__(self, other):
    return Concatenate(self, Optional(other))
  def __call__(self, other):
    return ConcatenateNAssoc(self, other)
  def __div__(self, other):
    return Alternatives(self, other)
  def __iter__(self):
    raise NotImplementedError('Iteration not implemented for ' + self.__class__.__name__)
  def create_graph(self):
    return self.create_acceptor_graph()
  def create_acceptor_graph(self):
    raise NotImplementedError('Graph creation not implemented for ' + self.__class__.__name__)
  
class Optional(Transducer):
  '''
    Matches one or zero repetitions of the underlying transducer
  '''
  def __iter__(self):
    yield (), ()
    for a_in, _ in  self.args[0]:
      yield a_in, ()
  
  def create_acceptor_graph(self):
    g1 = self.args[0].create_acceptor_graph()
    g = graph.Graph()

    u = g.new_state()
    v = g.get_final_state()

    g.add_subgraph(u, v, g1)
    g.add_edge(u, v, None, None)
    return g

  def __repr__(self):
    return f'-({repr(self.args[0])})'

class Literal(Transducer):
  '''
    Matches text exactly
  '''
  def create_acceptor_graph(self):
    g = graph.Graph()
    g.add_edge(g.new_state(), g.get_final_state(), self.v, self.v)
    return g

  def __init__(self, v):
    self.v = v
  def __iter__(self):
    if self.v is not None:
      yield (self.v,), (self.v,);
  def __repr__(self):
    return repr(self.v)

class Concatenate(Transducer):
  '''
    Concatenate both input and output of the terms
  '''
  def create_acceptor_graph(self):
    g = graph.Graph()
    g1 = self.args[0].create_acceptor_graph()
    g2 = self.args[1].create_acceptor_graph()
    v1 = g.new_state()
    v2 = g.new_state()
    v3 = g.get_final_state()
    g.add_subgraph(v1, v2, g1)
    g.add_subgraph(v2, v3, g2)
    return g

  def __iter__(self):
    v1, v2 = self.args
    for a_in, a_out in v1:
      for b_in, b_out in v2:
        yield (a_in + b_in, a_out + b_out);
  def __repr__(self):
    v1, v2 = self.args
    return f'({repr(v1)}) + ({repr(v2)})'

class ConcatenateNAssoc(Concatenate):
  '''
    For convenience concatenation can be written as a python call syntax
    in that case it will not accept a prefix minus
  '''
  def __neg__(self):
    v1, v2 = self.args
    raise TypeError('Ambiguous prefix minus and suffix parents\n\n' 
                   + f'(-{v1}) + ({v2})\n'
                   + 'vs.\n'
                   + f'-({v1} + ({v2}))\n'
                   )
  def __repr__(self):
    v1, v2 = self.args
    return f'{repr(v1)} ({repr(v2)})'

class Interchangeable(Transducer):
  def create_acceptor_graph(self):

    # the same algorithm as for Alternatives
    g = graph.Graph()
    u = g.new_state()
    v = g.get_final_state()
    for sub_language in self.args:
      sub_graph = sub_language.create_acceptor_graph()
      g.add_subgraph(u, v, sub_graph)
    return g

  def create_graph(self):
    raise NotImplementedError('Graph creation not defined for Alternatives, try `create_acceptor_graph` instead')
    
  def __iter__(self):
    vals = itertools.chain(*self.args)
    v, out = next(vals)
    yield (v, out)
    for v,_ in vals:
      yield v, out
  def __repr__(self):
    v1, v2 = self.args
    return f'({repr(v1)}) | ({repr(v2)})'

class Alternatives(Transducer):
  '''
    alternatives 'a'/'b'/'c' means that each output
    has a different meaning.
  '''
  def create_acceptor_graph(self):
    g = graph.Graph()
    u = g.new_state()
    v = g.get_final_state()
    for sub_language in self.args:
      sub_graph = sub_language.create_acceptor_graph()
      g.add_subgraph(u, v, sub_graph)
    return g
  
  def __iter__(self):
    yield from itertools.chain(*self.args)
  def __repr__(self):
    v1, v2 = self.args
    return f'({repr(v1)}) / ({repr(v2)})'

class Acceptor(Transducer):
  '''
    A transducer for which the input is exactly the output
  '''
  def create_graph():
    g = self.G.create_acceptor()

  def __init__(self, G):
    self.G = G
  def __iter__(self, G):
    for w, _ in self.G:
      yield w, w
