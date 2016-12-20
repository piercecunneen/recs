"""
Destroys tables within the database.
Most commonly used during teardown stage
"""

import recs.src.db.db_lib as db

def drop_table(db_name, table_name):
  """
  Inputs:
    db_name: type(string)
    table_name: type(string)
  returns:
    type:
      pg.Error or NoneType)
    description:
      result of recs/src/db/db_lib.execute_db_query, which
      is either an error or None (if query successful)
  """
  query_string = "DROP table %s" %(table_name)
  error = db.execute_db_query(db_name, query_string, [])
  return error
