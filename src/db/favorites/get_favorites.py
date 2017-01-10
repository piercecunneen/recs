'''
  module for getting favorites
'''
import src.db.db_lib as db

def get_album_favorite_data(request_body):
  '''
    gets all favorites associated with an album and it's tracks
  '''
  ids = [str(item_id) for item_id in request_body['track_ids']]
  ids.append(str(request_body['album_id']))

  query_string = "SELECT * from favorites where item_id = ANY (%s)"

  return db.execute_db_query("Helix", query_string, [ids])


def get_user_favorites(user_id):
  '''
   gets all favorites associated with a user
  '''

  query_string = "SELECT * FROM favorites\
  INNER JOIN items ON (favorites.item_id = items.item_id)\
  where user_id = %s\
  order by time_favorited DESC"

  return db.execute_db_query("Helix", query_string, [user_id])
