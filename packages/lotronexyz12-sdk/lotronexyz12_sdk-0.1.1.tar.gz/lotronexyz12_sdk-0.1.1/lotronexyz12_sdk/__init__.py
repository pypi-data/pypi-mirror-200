import os
from . import endpoints

class LOTR_SDK:
    def __init__(self, access_token = None) -> None:
        """
        Init

        :param access_token str|None, optional
        :return None
        """
        super().__init__()

        self.configs = {}

        # Set the access token if the user wants to pass in here.
        if access_token is not None:
            self.configs['access_token'] = access_token

        # run config on start
        self.run_config()

    def run_config(self):
        """
        Parse config files for access tokens etc.

        :return None
        """
        config_file = './config'
        # Check if config file exists
        if not os.path.exists(config_file):
            print('Config file named "config" missing in root directory.')
            exit()

        # Read file
        lines = ''
        with open(config_file, 'r') as f:
            lines = f.readlines()
    
        for line in lines:
            data = line.split('=')
            # For now skip over a bad config line missing an equal sign
            if len(data) == 2:
                self.configs[ data[0] ] = data[1]
    
    def getEndPointClass(self, class_name : str):
        """
        Return a class of Endpoint type, ie - Movie

        :param class_name str
        :return Endpoint
        """
        # Get class attribute
        return getattr(endpoints, class_name)()


    def endpoint(self, endpoint : str) -> endpoints.Endpoint:
        """
        Fetch data for a specific endpoint

        :param endpoint str
        :param _id str (if present will fetch one specific movie)
        :return endpoints.Endpoint
        """
        # Check if access token exists
        if 'access_token' not in self.configs:
            print('Access token missing from configuration file.')
            exit()

        # Check if endpoint exists
        try:
            requested_endpoint = self.getEndPointClass(endpoint.capitalize())
            requested_endpoint.access_token = self.configs['access_token']
        except:
            print('Error: Endpoint [' + endpoint + '] does not exist')
            exit()

        return requested_endpoint
