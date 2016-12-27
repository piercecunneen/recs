"""
Takes a new user's informatio and inserts them into
 the database

"""
import src.db.db_lib as db

def create_user(user):
  """
  user definition:
      {fb_id, name, email, lower_age_limit, upper_age_limit, gender}
  returns:
    type:
      pg.Error or NoneType)
    description:
      result of recs/src/db/db_lib.execute_db_query, which
      is either an error or None (if query successful)
  """
  query_string = "INSERT INTO users\
                 ( fb_id, name, email, lower_age_range, upper_age_range, gender)\
                  VALUES (%s, %s, %s, %s, %s, %s)"
  args = [
    user['fb_id'],
    user['name'],
    user['email'],
    user['lower_age_limit'],
    user['upper_age_limit'],
    user['gender']
  ]
  return db.execute_db_query("Helix", query_string, args)
