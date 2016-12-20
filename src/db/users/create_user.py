"""
Takes a new user's informatio and inserts them into
 the database

"""
import recs.src.db.db_lib as db

def create_user(username, email):
  """
  Inputs:
    username: type(string)
    email:    type(string)
  returns:
    type:
      pg.Error or NoneType)
    description:
      result of recs/src/db/db_lib.execute_db_query, which
      is either an error or None (if query successful)
  """
  query_string = "INSERT INTO users (username, email, verified) VALUES (%s, %s, %s)"
  return db.execute_db_query("piercecunneen", query_string, [username, email, "0"])
