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
                 (user_id, item_id, item_type)\
                  VALUES (%s, %s, %s)"
  args = [
    favorite_data['user_id'],
    favorite_data['item_id'],
    favorite_data['item_type']
  ]

  db.add_item(favorite_data['item_id'], favorite_data['item_data'])

  return db.execute_db_query("Helix", query_string, args)
