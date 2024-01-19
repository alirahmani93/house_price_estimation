from sqlalchemy import exists, ClauseElement, update
from sqlalchemy.orm import Session

from .database import get_db
from .models import City, Category, PostToken, Post
from .schemas import PostTokenSchema, PostCreateSchema


class BaseQuery:
    model = NotImplemented
    schema = NotImplemented

    def __init__(self, db: Session = None, *args, **kwargs):
        self.db = db if db is not None else get_db()

    @property
    def query(self):
        return self.db.query(self.model)

    def get_by_limit_offset(self, skip: int = 0, limit: int = 100):
        return self.query.offset(skip).limit(limit).all()

    def get_by_id(self, target_id: int):
        return self.query.filter(self.model.id == target_id).first()

    def update(self, target, **kwargs):
        # self.query.update().where(table.c.data == "value").values(status="X")
        update(self.model).where(self.model.c.token == target.token).values(**kwargs)
        return self.query.filter_by(**kwargs).first()

    # def update_setter(self):
    #     setattr(user, 'no_of_logins', User.no_of_logins + 1)

    def create(self, **post_token: schema):
        query = self.model(post_token)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query

    def get_all_active(self):
        return self.query.filter(self.model.is_active == True)

    def exists(self, target_code: str):
        return self.db.query(exists().where(self.model.code == target_code)).scalar()
        # return self.query.filter(self.model.code == target_code).exists().scalar()

    def get_or_create(self, model, defaults=None, **kwargs):
        instance = self.query.filter_by(**kwargs).one_or_none()
        if instance:
            return instance, False
        else:
            params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
            params.update(defaults or {})
            instance = model(**params)
            try:
                self.db.add(instance)
                self.db.commit()
            except Exception:
                self.db.rollback()
                instance = self.db.query(model).filter_by(**kwargs).one()
                return instance, False
            else:
                return instance, True


class CityQuery(BaseQuery):
    model = City


class CategoryQuery(BaseQuery):
    model = Category


class PostTokenQuery(BaseQuery):
    model = PostToken
    schema = PostTokenSchema

    def create(self, **post_token: schema):
        query = self.model(code=post_token['code'])
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query


class PostQuery(BaseQuery):
    model = Post
    schema = PostCreateSchema

    def get_by_token(self, token: str):
        return self.query.filter(self.model.token == token)

    def create(self, post: schema):
        query = None
        try:
            query = self.model(**post)
            self.db.add(query)
            self.db.commit()
            self.db.refresh(query)
        except:
            pass
        return query

    # def get_items(self, token):
    #     return self.db.query(Post).filter(self.model.token == token).all()

    def get_items(self, skip: int = 0, limit: int = 100):
        return self.db.query(Post).offset(skip).limit(limit).all()

    def update(self, token, **update_fields):
        self.db.execute(f"""UPDATE post SET {update_fields} WHERE post.token={token}""")

# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
