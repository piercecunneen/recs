"""
Set of commonly used database functions that are shared
across the codebase
"""
import psycopg2 as pg

def execute_db_query(db_name, query_string, args):
  """
  Inputs:
    db_name: type(string)
    query_string: type(string)
    args: type(list of strings)
  returns:
    type:
      pg.Error or NoneType)
  """
  conn = pg.connect("dbname=%s" %(db_name))
  curr = conn.cursor()

  try:
    curr.execute(query_string, args)
    conn.commit()
  except pg.OperationalError as err:
    return err

  curr.close()
  conn.close()
