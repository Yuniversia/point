from app.models.category import Category
from app.models.class_group import ClassGroup
from app.models.total_points import Total_point
from config import Config

import redis
from sqlalchemy import desc


r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# thread = Thread(target=my_func, args=('args'))

def max_point_cashing(group):
    for criterion in Category.query.all():
        max_point = Total_point.query.filter(Total_point.category_id == criterion.id).filter(Total_point.class_group.has(age_group=group)).order_by(desc(Total_point.total_point)).first()
        if not max_point:
            max_point = 0
        else:
            max_point = max_point.total_point
        r.set(f'{group}_{criterion.name}', max_point)

    return True

def cashing_top_by_group(group):
    classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()
    criteria = Category.query.all()
    
    total_activs = {}
    for school_class in classes: 
        activ_list = []

        for criterion in criteria:
            max_point = r.get(f'{group}_{criterion.name}') # Get data from redis to optimize code
            point = Total_point.query.filter_by(category_id=criterion.id, class_id=school_class.id).one_or_none()
            if point and max_point and int(max_point) != 0:
                activity = point.total_point / int(max_point)
            else:
                activity = 0
            
            activity = activity * criterion.coefficient
            activity = round(activity, 2)

            activ_list.append(activity)
            
            

        total_activs[f"{school_class.name}"] = sum(activ_list)

    sorted_activs = sorted(total_activs.items(), key=lambda item: item[1], reverse=True)

    r.delete(f"{group}_classes")

    for place, (key, value) in enumerate(sorted_activs):
        classe = ClassGroup.query.filter_by(age_group=group, name=key).one()
        mapping = {"name": key,
                   "id": classe.id,
                   "age_group": group,
                   "place": place,
                   "activity": round(value, 2)}
        r.hset(key, mapping=mapping)
        r.rpush(f"{group}_classes", str(key))