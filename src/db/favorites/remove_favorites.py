'''
  module for removing favorites from database
  This module should be item agnostic
'''
import src.db.db_lib as db

def remove_favorite(request_body):
  '''
    removes a user's favorite
  '''

  user_id = request_body['user_id']
  item_id = request_body['item_id']

  query_string = "DELETE from favorites where user_id = %s AND item_id = %s"

  args = [
    user_id,
    item_id
  ]

  return db.execute_db_query("Helix", query_string, args)
