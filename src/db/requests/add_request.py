'''
  module for adding requests from one user to another
  This module should be item agnostic
'''
import src.db.db_lib as db

def add_request(request_object):
  '''
    add a single request from user A to user B
  '''
  query_string = "INSERT INTO requests\
                 (from_user_id, to_user_id, item_type, time_requested, fufilled)\
                  VALUES (%s, %s, %s, current_timestamp, 'false')"
  args = [
    request_object['from_user_id'],
    request_object['to_user_id'],
    request_object['item_type']
  ]

  return db.execute_db_query("Helix", query_string, args)
