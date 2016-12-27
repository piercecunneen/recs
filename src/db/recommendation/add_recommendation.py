'''
  module for adding recommendations from one user to another
  This module should be item agnostic
'''

import src.db.db_lib as db

def add_recommendation(request_object):
  '''
    add a single recommendation from user A to user B
  '''
  # -1 for rating means no rating given yet
  query_string = "INSERT INTO recommendations\
                 (from_user_id, to_user_id, item_id, time_recommended, rating)\
                  VALUES (%s, %s, %s, current_timestamp, -1)"
  args = [
    request_object['from_user_id'],
    request_object['to_user_id'],
    request_object['item_id']
  ]

  return db.execute_db_query("Helix", query_string, args)
