'''
  module for adding favorites
  This module should be item agnostic
'''
import src.db.db_lib as db


def add_favorite(favorite_data):
  '''
    adds a user's favorite
  '''

  query_string = "INSERT INTO favorites\
                 (user_id, item_id, item_type, time_favorited)\
                  VALUES (%s, %s, %s, current_timestamp)"
  args = [
    favorite_data['user_id'],
    favorite_data['item_id'],
    favorite_data['item_type']
  ]

  return db.execute_db_query("Helix", query_string, args)
