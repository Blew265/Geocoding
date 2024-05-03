from fastapi import APIRouter, HTTPException, status, Depends

from .. import schemas, models, jwt_auth
from ..database import get_db, engine

from sqlalchemy.orm import Session

import httpx





models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/geocoding", tags=['Geocoding'])


async def get_geolocation(location: schemas.Location):
    async with httpx.AsyncClient() as client:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location.address}&key={location.api_key}"
        response = await client.get(url)
        response.raise_for_status()
        print(response)
        return response.json()


# Raw plug
@router.post("/", status_code=status.HTTP_200_OK)
async def geolocation(location: schemas.Location):
    return await get_geolocation(location)

# Creating
@router.post('/insertion', status_code=status.HTTP_200_OK)
async def insertion_of_geolocation(location: schemas.Location, db: Session= Depends(get_db), current_user: int = Depends(jwt_auth.get_current_user)):
    
    async with httpx.AsyncClient() as client:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location.address}&key={location.api_key}"
        response = await client.get(url)
        response.raise_for_status()
        print(response)

        data = response.json()
        result = data["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]

        cordinates = models.Cordinates(owner_id = current_user.id, address=location.address, latitude=lat, longitude=lng)
        db.add(cordinates)
        db.commit()
        db.refresh(cordinates)
        return {"message": "Geocoding result saved to database"}
   


# Reading/Fetching
@router.get("/search/{id}", status_code=status.HTTP_200_OK, )
async def read_cordinates(id: int, db: Session= Depends(get_db) ):
    cordinates = db.query(models.Cordinates).filter(models.Cordinates.id == id).all()
    if not cordinates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return cordinates

# Updating
# It only works if the smaller id exist, if it doesn't the data will take the lower id
@router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_location(id: int, location: schemas.Location , db: Session = Depends(get_db), current_user: int = Depends(jwt_auth.get_current_user)):
    cordinate_to_update = db.query(models.Cordinates).filter(models.Cordinates.owner_id == current_user.id).first()
    if not cordinate_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cordinate with id: {id} was not found")
    if cordinate_to_update.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    async with httpx.AsyncClient() as client:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location.address}&key={location.api_key}"
        response = await client.get(url)
        response.raise_for_status()
        print(response)

        data = response.json()
        result = data["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]

        cordinate_to_update.address = location.address
        cordinate_to_update.latitude = lat
        cordinate_to_update.longitude = lng

        db.commit()
        db.refresh(cordinate_to_update)
    return cordinate_to_update

# Deleting
@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_location(id: int, db: Session= Depends(get_db), current_user: int = Depends(jwt_auth.get_current_user)):
    cordinate_query = db.query(models.Cordinates).filter(models.Cordinates.id == id)
    cordinate = cordinate_query.first()

    if not cordinate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cordinate with id: {id} was not found")
    # Making the post private 

    cordinate_query.delete(synchronize_session=False)

    db.commit()
    return {'message': "location is deleted"}


