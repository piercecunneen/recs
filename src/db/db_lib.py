"""
Set of commonly used database functions that are shared
across the codebase
"""
import json
import MySQLdb
import logging
import os

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
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
    print CLOUDSQL_CONNECTION_NAME
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
      # Connect using the unix socket located at
      # /cloudsql/cloudsql-connection-name.
      cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

      conn = MySQLdb.connect(
            db=db_name,
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
      
      conn = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)
  except Exception as e:
    logging.info(e)
  curr = conn.cursor()
  result = []
  logging.info(query_string)
  try:
    curr.execute(query_string, args)
    conn.commit()
    result = curr.fetchall()
  except Exception as error: # pylint: disable=broad-except
    logging.info(error)
  curr.close()
  conn.close()
  return result
