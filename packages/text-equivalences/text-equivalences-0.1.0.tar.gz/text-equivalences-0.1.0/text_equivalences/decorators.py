import ast, inspect
from . import transducer

def _unindent(source):
  indent = None
  rows = source.split('\n')
  for r in rows:
    if r.strip() != '' and not r.strip().startswith('#'):
      if indent is None:
        indent = ''
        for c in r:
          if not c.isspace():
            break
          indent += c
      elif len(r) > len(indent):
        for i in range(len(indent)):
          if indent[i] != r[i]:
            indent = indent[:i]
  return '\n'.join(r[len(indent):] if r.startswith(indent) else r for r in rows)
class TransducerFunction(ast.NodeTransformer):
  def __init__(self, method):
    self.__original_method = method;
    src = inspect.getsource(method)
    unindented_src = _unindent(src)
    self.__original_ast = ast.parse(unindented_src)
    self.defined = set()
    self.auto_quoted = set()
    for arg in self.__original_ast.body[0].args.args:
      self.defined.add(arg.arg)
    self.ast = self.generic_visit(self.__original_ast)
    #self.ast.fix_missing_locations()
    self.code = compile(self.ast, method.__name__, mode='exec')
    namespace = method.__globals__
    for k,v in transducer.__dict__.items():
      namespace[k] = v
    exec(self.code, namespace)
    
    self.new_method = namespace[method.__name__]
  def ilabels(self):
    for i,o in self():
      yield i
  def olabels(self):
    for i,o in self():
      yield o
  def pairs(self):
    return self()
  def __iter__(self):
    return self()
  def __call__(self, *args, **kwargs):
    return self.new_method(*args, **kwargs);
  def visit_FunctionDef(self, node):
    # remove the `some_decorator` decorator from the AST
    # we don’t need to keep applying it.
    if node.decorator_list:
      node.decorator_list = [
        n for n in node.decorator_list
        if not (isinstance(n, ast.Name) and n.id == 'TransducerFunction')
      ]
    return self.generic_visit(node)
  
  def visit_Call(self, node):
    if isinstance(node.func, ast.Name) and node.func.id in self.auto_quoted:
      if len(node.args) != 1:
        raise SyntaxError('Name ' + ast.func.id + ' was quoted')
      c = ast.Call(self.make_literal(node.func.id, node.func), 
                      args=[self.generic_visit(node.args[0])], keywords=[])
      
      ast.copy_location(c, node)
      return c
      
    return self.generic_visit(node);

  def make_literal(self, s, node):
    self.auto_quoted.add(s)
    literal = ast.Name('Literal', ctx=ast.Load())
    arg = ast.Str(s)
    ast.copy_location(literal, node)
    ast.copy_location(arg, node)
    c = ast.Call(func=literal, args=[arg], keywords=[])
    ast.copy_location(c, node)
    return c

  def visit_Name(self, node):
    if node.id not in self.defined and isinstance(node.ctx, ast.Load):
      return self.make_literal(node.id, node)
    else:
      self.defined.add(node.id)
    return self.generic_visit(node)
  def visit_Constant(self, node):
    return self.make_literal(node.s, node)
  
  def visit_Str(self, node):
    
    return self.make_literal(node.s, node)
  
