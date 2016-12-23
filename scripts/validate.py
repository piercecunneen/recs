def validate_request(valid_body, request_body):
  '''
    validate response by comparing actual request body with the api validaiton body
  '''
  required_fields = {key:valid_body[key] for key in valid_body if valid_body[key]['required']}
  num_required_fields_seen = 0
  for key in request_body:
    if key in required_fields:
      num_required_fields_seen += 1
      continue
    elif key in valid_body:
      continue
    else:
      return False
  return num_required_fields_seen == len(required_fields)