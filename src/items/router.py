from typing import List, Union, Dict

from aioredis import Redis
from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.authv2.schemas import UserRead
from utils.producer import producer
from utils.redis import get_async_redis
from src.authv2.auth import get_current_user, get_current_user_or_pass
from src.items.manager import get_items_model
from src.authv2.manager import get_user_model
from src.items.schemas import Item as ItemSchema, ItemCreate, LikedBy
from utils.database import get_async_session
from src.authv2.models import Item, User, Category
from datetime import datetime,timedelta
from config import KAFKA_TOPIC, KAFKA_TOPIC_RECOMMENDATIONS
from src.recommendations.rec import RecWeigths, recsInit

router = APIRouter(
    tags=['items'],
    prefix="/items",
)

@router.get('/{id}',response_model=Union[List[ItemSchema],ItemSchema,Dict])
async def get_items(id:int = None,
                    redis:Redis = Depends(get_async_redis),
                    user:UserRead = Depends(get_current_user_or_pass),
                    session:AsyncSession = Depends(get_async_session)):
    if id:
        items_query = select(Item).where(Item.id == id)
        item = result = (await session.execute(items_query)).scalar()
        if result and user.id !=-1:
            await producer.send(topic=KAFKA_TOPIC_RECOMMENDATIONS, value={
                "user_id": user.id,
                "tags": (item.brand + ' ' + item.name).split(' '),
                'type': 'clicks',
                'category': item.category[0].name

            })
        # await recs.add(type='clicks', category=result.category[0].name, brand=result.brand, item_name=result.name)
    else:
        items_query = select(Item)
        result = (await session.execute(items_query)).scalars().all()
    if not result:
        return {"response":"empty"}
    return result

@router.post('/',response_model=Union[ItemSchema,Dict])
async def create_item(item_data: ItemCreate,
                      user:User = Depends(get_user_model),
                      session:AsyncSession = Depends(get_async_session)):
    categories = []
    item_data = item_data.dict()
    for category in item_data['category']:
        categories.append(category['name'])
    categories_query = select(Category).where(Category.name.in_(categories))

    categories = (await session.execute(categories_query)).scalars().all()
    item_data['category'] = categories
    item = Item(**item_data,
                expiring_at = datetime.utcnow() + timedelta(minutes=1)
                )
    session.add(item)
    user.items.append(item)
    await session.commit()
    return item


@router.post('/like/{item_id}')
async def like(item_id:int,
               redis:Redis = Depends(get_async_redis),

               user:User = Depends(get_user_model),
               session:AsyncSession = Depends(get_async_session)):
    recs = RecWeigths(redis,user)
    await recs.init()
    item = await get_items_model(id = item_id,session = session)
    if user not  in item.liked_by:
        item.liked_by.append(user)
        await producer.send(topic=KAFKA_TOPIC_RECOMMENDATIONS, value={
            "user_id": user.id,
            "tags": ( item.brand+ ' ' + item.name).split(' '),
            'type': 'likes',
            'category': item.category[0].name

        })
        await session.commit()

        return {'response':200}

    return {'response':400,'reason':'already liked'}
@router.post('/removeLike/{item_id}')
async def remove_like(item_id:int,
               redis:Redis = Depends(get_async_redis),
               user:User = Depends(get_user_model),
               session:AsyncSession = Depends(get_async_session)):
    recs = RecWeigths(redis,user)
    await recs.init()
    item = await get_items_model(id = item_id,session = session)
    if user   in item.liked_by:
        item.liked_by.remove(user)
        await session.commit()
        # await recs.remove(type = 'likes',category=item.category[0].name,name=item.name)
        await recs.save()
        return {'response':200}
    return {'response':400,'reason':'unliked'}





@router.get('/like/{item_id}',response_model=LikedBy)
async def like(item_id: int,
                # user_data: UserRead = Depends(get_current_user_or_pass),
               session: AsyncSession = Depends(get_async_session)):

    item = await get_items_model(id=item_id, session=session)
    # send data to item  recommendations (user_id,tags)

    return {"count":len(item.liked_by),"liked_by":item.liked_by}

@router.post('/search',response_model=List[ItemSchema])
async def search(search_key: str,
                 # item:Item = Depends(),
                 user_data: User = Depends(get_current_user),
                 session: AsyncSession = Depends(get_async_session), KAFKA_TOPIC_RECOMMENDATIONS=None):
    user_id = user_data.id
    items_query = select(Item).where(or_(Item.name.contains(search_key) , Item.brand.contains(search_key)) )
    items = (await session.execute(items_query)).scalars().fetchall()
    # send data to search recommendations (user_id,name,brand)

    #send data to item  recommendations (user_id,tags)
    await producer.send(topic=KAFKA_TOPIC_RECOMMENDATIONS,value={
        "user_id":user_id,
        "tags":[search_key],
        'type':'search'

    })
    await producer.flush()

    return items