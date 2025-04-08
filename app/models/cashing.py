import redis
import json

from app.models.category import Category
from app.models.class_group import ClassGroup
from app.models.total_points import Total_point
from sqlalchemy import desc


r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# thread = Thread(target=my_func, args=('args'))

def max_point_cashing():
    for criterion in Category.query.all():
        max_point = Total_point.query.filter_by(category_id=criterion.id).order_by(desc(Total_point.total_point)).first()
        if not max_point:
            max_point = 0
        else:
            max_point = max_point.total_point
        r.set(f'{criterion.name}', max_point)

    return True

def cashing_top_by_group(group):
    classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()
    criteria = Category.query.all()
    
    total_activs = {}
    coefficient_sum = Category.coefficient_sum()
    for school_class in classes: 
        activ_list = []

        for criterion in criteria:
            max_point = r.get(f'{criterion.name}') # Get data from redis to optimize code
            point = Total_point.query.filter_by(category_id=criterion.id, class_id=school_class.id).one_or_none()
            if point and max_point and int(max_point) != 0:
                activity = point.total_point / int(max_point)
            else:
                activity = 0
            
            activity = round(activity, 2)

            activity = activity * criterion.coefficient
            activ_list.append(activity)
            
            

        total_activs[f"{school_class.name}"] = sum(activ_list)
       # total_activs[f"{school_class.name}"] = round(sum(activ_list) / coefficient_sum, 2)

    sorted_activs = sorted(total_activs.items(), key=lambda item: item[1], reverse=True)
    # for key, item in sorted_activs:
    #     mapping[key] = item

    for place, (key, value) in enumerate(sorted_activs):
        mapping = {"name": key,
                   "place": place,
                   "activity": value}
        r.hset(key, mapping=mapping)
        r.rpush(f"{group}_classes", str(key))        

    # for place, (field, value) in enumerate(mapping.items()):
    #     r.hset(f"{group}", field, value)
    #     r.rpush(f"{group}_classes", str(field))