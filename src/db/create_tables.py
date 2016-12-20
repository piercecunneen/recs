import psycopg2 as pg

def create_table(db_name, table_name, column_names, column_types):
  conn = pg.connect("dbname=%s" %(db_name))
  curr = conn.cursor()

  columns = ["%s %s" %(pair[0], pair[1]) for pair in zip(column_names, column_types)]
  create_string = "CREATE TABLE %s (%s)" %(table_name, ', '.join(columns))

  curr.execute(create_string)
  conn.commit()

  curr.close()
  conn.close()
