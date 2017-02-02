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
                 (from_user_id, to_user_id, item_id, item_type, time_recommended, rating)\
                  VALUES (%s, %s, %s, %s, current_timestamp, -1)"
  args = [
    request_object['from_user_id'],
    request_object['to_user_id'],
    request_object['item_id'],
    request_object['item_type']
  ]

  db.add_item(request_object['item_id'], request_object['item_data'])

  return db.execute_db_query("Helix", query_string, args)


def add_rec_rating(request_object):
  '''
    add a rating for a recommendation
  '''
  # -1 for rating means no rating given yet
  query_string = "UPDATE recommendations\
                 SET rating = %s, modified = current_timestamp\
                 WHERE rec_id = %s"
  args = [
    request_object['rating'],
    request_object['rec_id']
  ]

  return db.execute_db_query("Helix", query_string, args)
