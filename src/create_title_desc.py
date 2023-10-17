"""
Wrapper around OpenAI APIs.
"""
import os
import json

from validate_keys import get_key_from_env


_PROMPT_TEMPLATE = """
I want you to act as the title generator and provide information 
about the text. You should only provide short informative description
about the text. Use the following format for your response: "{
    "tile":"title for the text",
    "description": "Description about the text" 
    }"

"""


class GenerateTitleDesc:

    """Wrapper around OpenAI large language models.

    To use, you should have the ``openai`` python package installed, and the
    environment variable ``OPENAI_API_KEY`` set with your API key.
    """

    def __init__(
            self,
            screenshot_text: str,
            prompt: str = _PROMPT_TEMPLATE
    ):
        try:
            import openai
        except ImportError:
            raise ImportError(
                """Openai package not found, please install it with
                `pip install openai`
                """
            )
        try:
            import dotenv
        except ImportError:
            raise ImportError(
                """dotenv package not found , please install it with
                `pip install python-dotenv`
                """

            )
        

        self.screenshot_text = screenshot_text
        self.prompt = _PROMPT_TEMPLATE
        self.openai_name = "OPENAPI_KEY"

    @get_key_from_env
    def _generate(self, key_name):
        """Call out to OpenAI's endpoint with unique prompts."""
        import openai
        from dotenv import load_dotenv

        load_dotenv()

        if len(os.environ["OPENAPI_KEY"])>0:


            openai.api_key = os.environ["OPENAPI_KEY"]
            response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system", "content": (self.prompt)},
                                            {"role": "user", "content": ("Create Title and description of " + self.screenshot_text)}
                                        ],
                                        temperature=0.5,
                                        )

        
        return json.dumps(response['choices'][0]['message']['content'])


### usages of the class
if __name__=="__main__":
    screen_shot_text = "def add2number(a,b): return a+b"
    initialization = GenerateTitleDesc(screen_shot_text)
    print(initialization._generate(key_name="OPENAPI_KEY"))
    