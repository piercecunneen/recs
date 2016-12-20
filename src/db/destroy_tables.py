import psycopg2 as pg

import db_lib

def drop_table(db_name, table_name):
  query_string = "DROP table %s" %(table_name)
  error = db_lib.execute_db_query(db_name, query_string, [])
  return error
