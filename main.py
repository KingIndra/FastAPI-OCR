# Imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from ocr import read_image
import base64


# Setup
app = FastAPI()

api_keys = ["akwrhgljnv13bvi2vfo0b0bw"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


# Models
class Image(BaseModel):
    user: str
    base64: str
    text: str | None = None

    def textract(self):
        file_path = f"files/{self.user}.png"

        with open(file_path, "wb") as fh:
            data = base64.b64decode(self.base64)
            fh.write(data)
            
        self.text = read_image(file_path)


# Routes
@app.get("/ocr", dependencies = [Depends(api_key_auth)])
async def add_item(image: Image):
    image.textract()
    return image.text

