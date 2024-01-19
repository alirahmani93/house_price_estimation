from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ARRAY, JSON, FLOAT
from sqlalchemy.orm import relationship, registry

from .database import Base, engine


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())


class City(BaseModel):
    __tablename__ = "city"

    name = Column(String, index=True)

    # cities = relationship("Post", back_populates="cities")


class Category(BaseModel):
    __tablename__ = "category"

    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)


# class VacancyType(BaseModel):
#     __tablename__ = "vacancy_type"
#
#     name = Column(String, index=True)
#     code = Column(Integer, unique=True, index=True)
#     is_active = Column(Boolean, default=True)
#

# class Vacancy(BaseModel):
#     __tablename__ = "vacancy"
#
#     type = relationship("VacancyType", back_populates="Vacancies")
#     name = Column(String, index=True)
#     is_active = Column(Boolean, default=True)
class VacancyType(BaseModel):
    __tablename__ = "vacancy_type"

    name = Column(String, index=True)
    code = Column(Integer, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    # vacancies = relationship("Vacancy", back_populates="type")  # Update relationship name


class Vacancy(BaseModel):
    __tablename__ = "vacancy"

    # type_id = Column(Integer, ForeignKey('vacancy_type.id'))  # Add foreign key column
    # type = relationship("VacancyType", back_populates="vacancies")  # Update relationship name

    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)


class PostToken(BaseModel):
    __tablename__ = "post_token"

    code = Column(String, index=True, unique=True)

    # post_tokens = relationship("Post", back_populates="post_token")


class Post(BaseModel):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)

    # token_id = Column(Integer, ForeignKey('post_token.id'))
    # token = relationship("PostToken", back_populates="post_tokens")
    token = Column(String, index=True, )  # unique=True)

    # city_id = Column(Integer, ForeignKey('city.id'))
    # city = relationship("City", back_populates="cities")

    image_count = Column(Integer, nullable=True, )
    title = Column(String, nullable=True, )
    top_description_text = Column(String, nullable=True, )
    middle_description_text = Column(String, nullable=True, )
    bottom_description_text = Column(String, nullable=True, )
    red_text = Column(String, nullable=True, )
    checkable = Column(String, nullable=True, )
    label = Column(String, nullable=True, )
    label_color = Column(String, nullable=True, )
    note = Column(String, nullable=True, )
    standard_label_color = Column(String, nullable=True, )
    is_checked = Column(String, nullable=True, )
    has_divider = Column(String, nullable=True, )
    padded = Column(String, nullable=True, )
    has_chat = Column(String, nullable=True, )
    city_name = Column(String, nullable=True, )
    district_persian = Column(String, nullable=True, )
    city_persian = Column(String, nullable=True, )
    category_slug_persian = Column(String, nullable=True, )
    last_post_date = Column(Integer, nullable=True, )
    first_post_date = Column(Integer, nullable=True, )
    brand_model = Column(String, nullable=True)
    business_ref = Column(String, nullable=True)
    business_type = Column(String, nullable=True)
    cat_1 = Column(String, nullable=True)
    cat_2 = Column(String, nullable=True)
    cat_3 = Column(String, nullable=True)
    category = Column(String, nullable=True)
    city = Column(String, nullable=True)
    credit = Column(String, nullable=True)
    district = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    originality = Column(String, nullable=True)
    price = Column(String, nullable=True)
    rent = Column(String, nullable=True)
    status = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    unavailable_after = Column(String, nullable=True)
    description = Column(String, nullable=True)
    chat_enabled = Column(String, nullable=True)
    suggestion_tokens = Column(JSON, nullable=True)
    elevator = Column(String, nullable=True)
    parking = Column(String, nullable=True)
    depot = Column(String, nullable=True)
    map_type = Column(String, nullable=True)
    latitude = Column(FLOAT, nullable=True)
    longitude = Column(FLOAT, nullable=True)
    radius = Column(String, nullable=True)
    map_image_url = Column(String, nullable=True)
    balcony = Column(String, nullable=True)

    @classmethod
    def columns_name(cls):
        return {
            'brand_model': 'brand_model',
            'business_ref': 'business_ref',
            'business_type': 'business_type',
            'cat_1': 'cat_1',
            'cat_2': 'cat_2',
            'cat_3': 'cat_3',
            'category': 'category',
            'city': 'city',
            'credit': 'credit',
            'district': 'district',
            'gender': 'gender',
            'image_count': 'image_count',
            'originality': 'originality',
            'price': 'price',
            'rent': 'rent',
            'status': 'status',
            'token': 'token',
            'image_url': 'image_url',
            'title': 'title',
            'web_url': 'web_url',
            'unavailable_after': 'unavailable_after',
            'description': 'description',
            'chat_enabled': 'chat_enabled',
            'suggestion_tokens': 'suggestion_tokens',
            'elevator': 'آسانسور',
            'not_elevator': 'آسانسور ندارد',
            'parking': 'پارکینگ',
            'depot': 'انباری',
            'district_persian': 'district_persian',
            'city_persian': 'city_persian',
            'category_slug_persian': 'category_slug_persian',
            'top_description_text': 'top_description_text',
            'middle_description_text': 'middle_description_text',
            'bottom_description_text': 'bottom_description_text',
            'red_text': 'red_text',
            'checkable': 'checkable',
            'label': 'label',
            'label_color': 'label_color',
            'note': 'note',
            'standard_label_color': 'standard_label_color',
            'is_checked': 'is_checked',
            'has_divider': 'has_divider',
            'padded': 'padded',
            'has_chat': 'has_chat',
            'city_name': 'city_name',
            'last_post_date': 'last_post_date',
            'first_post_date': 'first_post_date',
            'map_type': 'map_type',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'radius': 'radius',
            'map_image_url': 'map_image_url',
            'balcony': 'بالکن',

        }
