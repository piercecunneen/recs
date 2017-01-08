'''
Adds music related items to items table
'''
import json
import src.db.db_lib as db


def add_item(item_id, item_data):
  '''
  Adds music item to the items table
  '''
  query_string = "INSERT INTO items\
               (item_id, item_data)\
                VALUES (%s, %s)"
  args = [item_id, json.dumps(item_data)]
  return db.execute_db_query("Helix", query_string, args)
