"""
Creates tables within the database.
Most commonly used during setup stage
"""
import src.db.db_lib as db

def create_table(db_name, table_name, column_names, column_types, foreign_keys, primary_keys):
  """
  Inputs:
    db_name: type(string)
    table_name: type(string)
    column_names: type(list of strings)
    column_types: type(list of strings)
  returns:
    type:
      pg.Error or NoneTyp
      e)
    description:
      result of recs/src/db/db_lib.execute_db_query, which
      is either an error or None (if query successful)
  """
  foreign_key_strings = ["FOREIGN KEY (%s) REFERENCES %s (%s)" %(fk['column'], fk['foreign_table'], fk['foreign_column']) for fk in foreign_keys]
  primary_key_strings = ["PRIMARY KEY (%s)" %(key) for key in primary_keys]
  columns = ["%s %s" %(pair[0], pair[1]) for pair in zip(column_names, column_types)]
  query_string = "CREATE TABLE %s (%s, %s, %s)" %(table_name, ', '.join(columns), ', '.join(foreign_key_strings), ', '.join(primary_key_strings))
  error = db.execute_db_query(db_name, query_string, [])
  return error
