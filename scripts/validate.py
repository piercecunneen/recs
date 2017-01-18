'''
Methods associated with request validation

'''

def validate_request(valid_body, request_body):
  '''
    validate response by comparing actual request body with the api validaiton body
  '''
  required_fields = {key:valid_body[key] for key in valid_body if valid_body[key]['required']}
  num_required_fields_seen = 0
  for key in request_body:
    if key in required_fields and type_match(valid_body[key]['type'], request_body[key]):
      num_required_fields_seen += 1
      continue
    elif key in valid_body and type_match(valid_body[key]['type'], request_body[key]):
      continue
    else:
      return False
  return num_required_fields_seen == len(required_fields)

def type_match(valid_body_string, field):
  '''
    Returns true if the field has the correct type
  '''
  if valid_body_string == "int":
    return isinstance(field, int) or isinstance(field, long)
  elif valid_body_string == "string" or valid_body_string == "char" and len(field) == 1:
    return isinstance(field, str) or isinstance(field, unicode)
  elif valid_body_string == "object":
    return isinstance(field, dict)
  elif valid_body_string == "list":
    return isinstance(field, list)
  else:
    return True
