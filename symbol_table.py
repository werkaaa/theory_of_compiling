class SymbolTable(object):

  def __init__(self, parent, name):  # parent scope and symbol table name
    self.table = {}
    self.var_scope_map = {}
    self.name = name
    self.scopes = []
    self.scopes.append(parent)
    self.scope_id = 0
    self.scopes_local_tables = [set()]


  def put(self, name, symbol):
    # To make sure that we are not keeping ID -> ID
    if symbol.type == 'ID':
      symbol = self.get(symbol.name)

    self.scopes_local_tables[self.scope_id].add(name)
    if name not in self.var_scope_map.keys():
      self.var_scope_map[name] = self.scope_id

    self.table[name] = symbol

  def get(self, name):
    if name in self.table.keys():
      return self.table[name]

    return None

  def push_scope(self, name):
    self.scopes.append(name)
    self.scope_id += 1
    self.scopes_local_tables.append(set())

  def get_scope(self):
    return self.scopes[self.scope_id]

  def pop_scope(self):
    scope_variables = self.scopes_local_tables.pop()
    for variable in scope_variables:
      if self.var_scope_map[variable] == self.scope_id:
        self.table.pop(variable)
        self.var_scope_map.pop(variable)
    self.scope_id -= 1

    return self.scopes.pop()
