from orm import Session, Users
from sqlalchemy.exc import IntegrityError
import json


def register_user(user, password):
    s = Session()
    s.add(Users(name=user, password=password, post="[]"))
    try:
        s.commit()
        return True
    except IntegrityError:
        return False


def check_user(user, password):
    s = Session()
    c = s.query(Users).filter(Users.name == user, Users.password == password).count()
    return c > 0


def list_users():
    s = Session()
    return s.query(Users).all()


def delete_user(user):
    s = Session()
    s.query(Users).filter(Users.name == user).delete()
    s.commit()


# def change_password(user, new_password):
#     s = Session()
#     s.query(Users).filter(Users.name == user).update({Users.password: new_password})
#     s.commit()


def add_post(user, new_post):
    s = Session()
    us = s.query(Users).filter(Users.name == user).first()
    posts = us.post
    posts = json.loads(posts)
    posts.append(new_post)
    data = json.dumps(posts)
    s.query(Users).filter(Users.name == user).update({Users.post: data})
    s.commit()


def user_posts(username):
    s = Session()
    u = s.query(Users).filter(Users.name == username).first()
    return json.loads(u.post)


def get_post(username, post):
    s = Session()
    u = s.query(Users).filter(Users.name == username).first()
    posts = u.post
    posts = json.loads(posts)
    str = posts[int(post)]
    return str


def change_post(username, post, new_text):
    s = Session()
    u = s.query(Users).filter(Users.name == username).first()
    posts = u.post
    posts = json.loads(posts)
    posts[int(post)] = new_text
    data = json.dumps(posts)
    s.query(Users).filter(Users.name == username).update({Users.post: data})
    s.commit()


def delete_post(username, post):
    s = Session()
    u = s.query(Users).filter(Users.name == username).first()
    posts = u.post
    posts = json.loads(posts)
    posts.pop(int(post))
    data = json.dumps(posts)
    s.query(Users).filter(Users.name == username).update({Users.post: data})
    s.commit()