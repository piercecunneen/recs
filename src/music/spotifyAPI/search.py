import requests

baseSpotifyURL =  "https://api.spotify.com/v1/search?"

def makeRequest(request_string, method_type = "GET"):
  '''
  Sends request to spotify api, parses the returned result, and returns a dictionary 
  with either the error information or the results from spotify
  Inputs:
    request_string
      type = string
      description: 
        the 

  '''

  r = requests.get(''.join([baseSpotifyURL, request_string]))
  