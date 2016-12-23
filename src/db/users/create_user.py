"""
Takes a new user's informatio and inserts them into
 the database

"""
import src.db.db_lib as db

def create_user(user_id, username, email):
  """
  Inputs:
    username:
      type: string
    email:
      type: string
    friends:
      type: list of strings
  returns:
    type:
      pg.Error or NoneType)
    description:
      result of recs/src/db/db_lib.execute_db_query, which
      is either an error or None (if query successful)
  """
  query_string = "INSERT INTO users (userid, username, email, verified) VALUES (%s, %s, %s, %s)"
  return db.execute_db_query("recs", query_string, [user_id, username, email, "0"])
