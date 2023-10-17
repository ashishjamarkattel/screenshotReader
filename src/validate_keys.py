""" Validate and Return key from environment variable if exist"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_key_from_env(
        function
):
    def get_key(self, key_name):

        if key_name in os.environ and os.environ[key_name]:
            return function(self, key_name)
        else:
            raise ValueError(
                f"Cannot find {key_name} ,please add it to environment variable"
                f"  `{key_name}` as a named parameter."
            )
        
    return get_key