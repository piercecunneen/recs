'''
  module for getting favorites
  This module should be item agnostic
'''
import src.db.db_lib as db

def get_album_favorite_data(request_body):
  '''
    gets all favorites associated with an album and it's tracks
  '''
  ids = [str(item_id) for item_id in request_body['track_ids']]
  ids.append(str(request_body['album_id']))
  id_string = ', '.join(ids)

  query_string = "SELECT * from favorites where item_id in (%s)" %(id_string)
  args = []

  return db.execute_db_query("Helix", query_string, args)
