from fastapi import FastAPI, HTTPException, status

from domain.directory import DirectoryException
from domain.directory import TransientDirectory
from domain.models import Contact

app = FastAPI()
directory = TransientDirectory()


@app.post("/directory/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def add_contact(contact: Contact):
    try:
        directory.add(contact)
        return contact
    except DirectoryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/directory/{contact_name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_name: str):
    directory.remove(contact_name, strict=False)


@app.get("/directory/{contact_name}", response_model=Contact, status_code=status.HTTP_200_OK)
async def query_contact(contact_name: str):
    try:
        return directory.query(contact_name)
    except DirectoryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


