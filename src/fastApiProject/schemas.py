# from pydantic import BaseModel
#
#
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
# class UserBase(BaseModel):
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#
#     class Config:
#         orm_mode = True
#
#
class PredictResult:
    pass


class CrawlResult:
    city_id: int
    category_id: int


class PostTokenSchema:
    code: int


class PostCreateSchema:
    token: str
    brand_model: str | None
    business_ref: str | None
    business_type: str | None
    cat_1: str | None
    cat_2: str | None
    cat_3: str | None
    category: str | None
    city: str | None
    credit: str | None
    district: str | None
    gender: str | None
    image_count: str | None
    originality: str | None
    price: str | None
    rent: str | None
    status: str | None
    image_url: str | None
    title: str | None
    web_url: str | None
    unavailable_after: str | None
    description: str | None
    chat_enabled: str | None
    suggestion_tokens: str | None
    elevator: str | None
    not_elevator: str | None
    parking: str | None
    depot: str | None
    district_persian: str | None
    city_persian: str | None
    category_slug_persian: str | None
    top_description_text: str | None
    middle_description_text: str | None
    bottom_description_text: str | None
    red_text: str | None
    checkable: str | None
    label: str | None
    label_color: str | None
    note: str | None
    standard_label_color: str | None
    is_checked: str | None
    has_divider: str | None
    padded: str | None
    has_chat: str | None
    city_name: str | None
    last_post_date: str | None
    first_post_date: str | None
    map_type: str | None
    latitude: str | None
    longitude: str | None
    radius: str | None
    map_image_url: str | None
    balcony: str | None
