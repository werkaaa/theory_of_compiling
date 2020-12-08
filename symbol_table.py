class SymbolTable(object):

  def __init__(self, parent, name):  # parent scope and symbol table name
    self.table = {}
    self.name = name
    self.scopes = []
    self.scopes.append(parent)
    self.scope_id = 0
    self.scopes_local_tables = []


  def put(self, name, symbol):
    # To make sure that we are not keeping ID -> ID
    if symbol.type == 'ID':
      symbol = self.get(symbol.name)

    if self.scope_id > 0:
      self.scopes_local_tables[-1][name] = symbol
      if not name in self.table.keys():
        self.table[name] = symbol
    else:
      self.table[name] = symbol

  def put_local(self, name, symbol):
    # To make sure that we are not keeping ID -> ID
    if symbol.type == 'ID':
      symbol = self.get(symbol.name)
    self.scopes_local_tables[-1][name] = symbol

  def get(self, name):
    # First we check the value in local scope
    if self.scope_id > 0:
      for scope_local_table in reversed(self.scopes_local_tables):
        if name in scope_local_table.keys():
          return scope_local_table[name]

    # If the variable wasn't in local scope we take value from global scope
    if name in self.table.keys():
      return self.table[name]

    return None

  def get_parent_scope(self):
    if self.scope_id > 0:
        return self.scopes[self.scope_id-1]
    return None

  def push_scope(self, name):
    self.scopes.append(name)
    self.scope_id += 1
    self.scopes_local_tables.append({})

  def get_scope(self):
    return self.scopes[self.scope_id]

  def pop_scope(self):
    self.scope_id -= 1
    self.scopes_local_tables.pop()
    return self.scopes.pop()
