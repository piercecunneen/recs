"""
Set of commonly used database functions that are shared
across the codebase
"""
import json
import MySQLdb

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
  conn = MySQLdb.connect(db="%s" %(db_name), user="root", passwd="5BrnH+")
  curr = conn.cursor()
  result = []
  try:
    curr.execute(query_string, args)
    conn.commit()
    result = curr.fetchall()
  except Exception as error: # pylint: disable=broad-except
    print error
  curr.close()
  conn.close()
  return result
