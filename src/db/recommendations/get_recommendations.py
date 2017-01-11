'''
  module for getting recommendations from items
  This module should be item agnostic
'''

import src.db.db_lib as db

def get_album_recommendation_data(request_body):
  '''
  gets recommenation data associated with an album (album and its tracks)
  '''

  ids = [str(item_id) for item_id in request_body['track_ids']]
  ids.append(str(request_body['album_id']))

  query_string = "SELECT * from recommendations where item_id IN (%s)"

  args = ', '.join(['%s' for _ in ids])
  query_string = query_string % args

  return db.execute_db_query("Helix", query_string, ids)


def get_user_recommendations(user_id):
  '''
   gets all recommendations associated with a user
  '''

  query_string = "SELECT * FROM recommendations\
  INNER JOIN items ON (recommendations.item_id = items.item_id)\
  where from_user_id = %s or to_user_id = %s\
  order by time_recommended DESC"

  return db.execute_db_query("Helix", query_string, [user_id, user_id])



def calculate_rec_score():
  '''
    Calculates a user's recommendations score
  '''
  pass
  # score = 0
  # for rec in recommendations:
  #   score +=
