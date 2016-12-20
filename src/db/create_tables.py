import psycopg2 as pg

import db_lib


def create_table(db_name, table_name, column_names, column_types):
  columns = ["%s %s" %(pair[0], pair[1]) for pair in zip(column_names, column_types)]
  query_string = "CREATE TABLE %s (%s)" %(table_name, ', '.join(columns))
  error = db_lib.execute_db_query(db_name, query_string, [])
  return error
