"""
Set of commonly used database functions that are shared
across the codebase
"""
import json
import psycopg2 as pg
import psycopg2.errorcodes as errorcodes

def add_item(item_id, item_data):
  '''
  Adds item to the items table
  '''
  query_string = "INSERT INTO items\
               (item_id, item_data)\
                VALUES (%s, %s)"
  args = [item_id, json.dumps(item_data)]
  return execute_db_query("Helix", query_string, args)

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
  except pg.Error as err:
    return errorcodes.lookup(err.pgcode)
  try:
    result = curr.fetchall()
  except pg.ProgrammingError:
    result = None

  curr.close()
  conn.close()
  return result
