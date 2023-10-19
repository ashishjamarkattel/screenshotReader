" Api route for the knowledge base from the screenshot"


import os
from fastapi import (
    APIRouter,
    File,
    UploadFile
)

from src.create_knowledgebase import FAISS
from src.read_screenshot import ReadScreenShot
from src.create_title_desc import GenerateTitleDesc
import logging

#define the router
router = APIRouter()
IMAGES_PATH = "images"


@router.post("/add_knowledge")
def add_knowledge(
    user_id: str,
    file: UploadFile = File(...),
    ):
    try:
        print("Reading the file")
        contents = file.file.read()
        screenshot_name = os.path.join(IMAGES_PATH, file.filename)
        with open(screenshot_name, 'wb') as f:
            f.write(contents)
        print("File write successful")
        try:
            if os.path.isfile(screenshot_name):
                print("Reading screenshot")
                screenshot_text = ReadScreenShot(screenshot_name).parse()
                print("Screenshot read complete")
                print("Creating title and description")
                tile_desc_json = GenerateTitleDesc(screenshot_text=screenshot_text)._generate(key_name="OPENAPI_KEY")
                print("Creating title and description successful")
                        
        except FileNotFoundError:
            logging.warning(str(e))
            return {"message": "There was an problem saving the file"}
        
        print("Embedding the document and title using sentencepiece")
        emb = FAISS.embed_document(tile_desc_json)
        print("Embedding document completed")
        print("Adding knowledge and title to faiss")
        emb.add_vector_to_faiss(user_id)
        return {"message": "Knowledge succesfully added"}

            
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
