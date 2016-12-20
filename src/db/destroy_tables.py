import psycopg2 as pg

def drop_table(db_name, table_name):
  conn = pg.connect("dbname=%s" %(db_name))
  curr = conn.cursor()

  drop_string = "DROP TABLE %s" %(table_name)

  curr.execute(drop_string)
  conn.commit()

  curr.close()
  conn.close()
