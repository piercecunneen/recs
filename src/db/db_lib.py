"""
Set of commonly used database functions that are shared
across the codebase
"""
import json
import os
import logging
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
  try:
    cloudsql_connection_name = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    cloudsql_user = os.environ.get('CLOUDSQL_USER')
    cloudsql_password = os.environ.get('CLOUDSQL_PASSWORD')
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
      cloudsql_unix_socket = os.path.join(
        '/cloudsql', cloudsql_connection_name
      )

      conn = MySQLdb.connect(
        db=db_name,
        unix_socket=cloudsql_unix_socket,
        user=cloudsql_user,
        passwd=cloudsql_password
      )
    else:
      conn = MySQLdb.connect(
        db=db_name,
        host=cloudsql_connection_name,
        user=cloudsql_user,
        passwd=cloudsql_password
      )
  except Exception as err: # pylint: disable=broad-except
    logging.error(err)
    return err
  curr = conn.cursor()
  result = []
  try:
    curr.execute(query_string, args)
    conn.commit()
    result = curr.fetchall()
  except Exception as error: # pylint: disable=broad-except
    logging.error(error)
  curr.close()
  conn.close()
  return result
