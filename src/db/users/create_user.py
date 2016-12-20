import src.db.db_lib as db

def create_user(username, email):

  query_string = "INSERT INTO users (username, email, verified) VALUES (%s, %s, %s)"
  return db.execute_db_query("piercecunneen", query_string, [username, email, "0"])

create_user("pierce", "pdc")