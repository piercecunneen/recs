import psycopg2 as pg


def execute_db_query(db_name, query_string, args):
  conn = pg.connect("dbname=%s" %(db_name))
  curr = conn.cursor()

  try:
    curr.execute(query_string, args)
    conn.commit()
  except pg.OperationalError as e:
    return e

  curr.close()
  conn.close()