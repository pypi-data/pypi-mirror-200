import requests
import json 
import urllib

class Api:
    def __init__(self) -> None:
        self.base_url = 'https://the-one-api.dev/v2/'

        # Messages for http response status codes
        self.response_status_msg = {
            '401' : 'Error: 401 Unauthorized request. Please check that you are using the correct access token.',
            '404' : 'Error: 404 Endpoint not found.',
            '429' : 'Error. 429 Too many requests. Slow down.'

            # add more here ..
        }

    def request(self, access_token : str, endpoint_path: str) -> dict:
        """
        Make a get request and fetch data from https://the-one-api.dev/v2/

        :param access_token str
        :param endpoint_path str
        :return str
        """
    
        # Initiate request
        response = requests.get(
            url = self.base_url + endpoint_path,
            headers = { "Authorization": "Bearer " + access_token }
        )

        # Parse the response
        if response.status_code == 200:
            # Make sure the text is json.
            try:
                return json.loads(response.text)
            except:
                return "Response included invalid JSON: " + response.text

        # Return errors
        try:
            return self.response_status_msg[str(response.status_code)]
        except:
            return 'Bad request. Status code not found.'
        

class Endpoint(Api):
    def __init__(self) -> None:
        super().__init__()
        self.access_token = ''


class Movie(Endpoint):
    """
    List of all movies, including the "The Lord of the Rings" and the "The Hobbit" trilogies
    """
    def __init__(self) -> None:
        super().__init__()
        self.endpoint_name = type(self).__name__.lower()

    def fetch_all(self, options = {}, filter = ''):
        """
        Return a list of all movies

        :param options dict
            example: { 
                     'limit' : 100,
                     'page' : 2,
                     'offset' : 3,
                     'sort' : 'name:asc'
                     }
        :return dict
        """
        endpoint_path = self.endpoint_name
        if options:
            query_params = urllib.parse.urlencode(options)
            endpoint_path += '?' + query_params

        # try extracting filter from option
        endpoint_path += ('?' if not options else '&') + filter
        print(endpoint_path)

        return self.request(
            access_token = self.access_token, 
            endpoint_path=endpoint_path
        )

    def fetch_one(self, _id : str, with_quotes = False, options = {}) -> dict:
        """
        Fetch a specific movie by id

        :param _id str
        :param with_quotes bool ->> Request all movie quotes for one 
                                    specific movie (only working for the LotR trilogy)

        :param options dict 
            example with_quotes: /quote?sort=character:desc
        :return dict
        """

        endpoint_path = self.endpoint_name + '/' + _id

        # Request quotes for this movie 
        if with_quotes:
            endpoint_path += '/quote'

            # Check if sorting etc.
            if options:
                query_params = urllib.parse.urlencode(options)
                endpoint_path += '?' + query_params

        return self.request(
            access_token = self.access_token, 
            endpoint_path = endpoint_path
        )
        
