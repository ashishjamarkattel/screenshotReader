"Creates api route for the knowledge base from the screenshot"


import os
from fastapi import (
    APIRouter,
    File,
    UploadFile
)

from src.create_knowledgebase import FAISS
from src.read_screenshot import ReadScreenShot
from src.create_title_desc import GenerateTitleDesc

#define the router
router_add_knowledge = APIRouter()
IMAGES_PATH = "../images"


@router_add_knowledge.post("/add_knowledge")
def add_knowledge(
    user_id: str,
    file: UploadFile = File(...),
    ):
    try:
        contents = file.file.read()
        screenshot_name = os.path.join(IMAGES_PATH, file.filename)
        with open(screenshot_name, 'wb') as f:
            f.write(contents)
        try:
            if os.path.isfile(screenshot_name):
                screenshot_text = ReadScreenShot(screenshot_name).parse()
                tile_desc_json = GenerateTitleDesc(screenshot_text=screenshot_text)._generate(key_name="OPENAPI_KEY")
            else:
                filename = None             
        except FileNotFoundError:
            return {"message": "There was an problem saving the file"}
        
        emb = FAISS.embed_document(tile_desc_json)
        emb.add_vector_to_faiss(user_id)
        return {"message": "Knowledge succesfully added"}

            
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
