import imp
from json import load
from auth.user_fastapi import fastapi_users,current_user
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Body,Form
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from models import models
from database.database import get_async_session
from cloudinary import uploader
from typing import List
from ml.model_ini import savedModel
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
from schemas import schemas
from schemas.user_schemas import UserDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
IMG_SIZE =224
import cloudinary
from dotenv import load_dotenv
load_dotenv()
import os
router = APIRouter(prefix='/files')

cloudinary.config(
    cloud_name= os.environ["CLOUD_NAME"],
    api_key= os.environ["API_KEY"],
    api_secret =os.environ["API_SECRET"]
)
dicti = ["apple_scab","apple_black_rot","apple_rust","apple",
           "blueberry",
           "cherry_mildew","cherry",
           "corn_gray","corn_rust","corn_leaf_blight","corn",
           "grape_black_rot","grape_black_measels","grape_blight","grape",
           "orange",
           "peach_bacteria","peach","pepper_bell_bacteria","pepper_bell",
           "poatato_early_blight","potato_late_blight","potato",
           "raspberry","soyabean","squash_mildew","strawberry_scab","strawberry",
           "tomato","tomato","tomato","tomato","tomato","tomato","tomato","tomato","tomato","tomato"
        ]

@router.post('/',response_model=schemas.File,tags=['file'])
async def upload(cap:str = Form(...) , file: UploadFile = File(...) ,db: AsyncSession = Depends(get_async_session), get_current_user:UserDB = Depends (current_user)):
    result = uploader.upload(file.file)
    url = result.get("url")
    new_image = models.Images(caption=cap, url= url , user_id = get_current_user.id)
    db.add(new_image)
    await db.commit()
    await db.execute("commit")
    return new_image

@router.get('/',tags=['file'])
async def getfile(db: AsyncSession = Depends(get_async_session)):
    data = await db.execute(select(models.Images))
    return data.mappings().all()

@router.post('/free',tags=['file'])
def upload(file: UploadFile = File(...)):
    img = tf.io.decode_image(
        file.file.read(), channels=3, dtype=tf.dtypes.uint8, name=None,
         expand_animations=False
         )
    img = tf.image.resize(img, [224,224], antialias=True)
    img = np.expand_dims(img, axis=0)
    result=savedModel.predict(img)
    print (result)
    result = result[0]
    result = result.tolist()
    return (max(result)*100,dicti[result.index(max(result))])
