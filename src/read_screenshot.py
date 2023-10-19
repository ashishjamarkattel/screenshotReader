"Ëxtract the knowledge from the screenshot"

class ReadScreenShot:
    """ Extract text from the screenshot """

    def __init__(
            self,
            image_path: str,
            ) -> None:
      
        self.image_path = image_path

    def parse(self):
        """ Load the screenshot with Image and parse the screenshot """  
        try:
            import easyocr
        except ImportError:
            raise ImportError(
                "easyocr package not found, please install it with "
                "`pip install easyocr`"
            )
        
        reader = easyocr.Reader(['en']) # set easyocr for english language
        result = reader.readtext(self.image_path)  ## read the text from the image provided
        ##get the text from the image
        screenshot_text = ""
        if len(result)> 0:
            for items in result:
                screenshot_text+= items[1]

        return screenshot_text
    
if __name__ == "__main__":
    print("hre")
    screenshot_reader = ReadScreenShot('add2number.PNG')
    screenshot_reader.parse()
        

