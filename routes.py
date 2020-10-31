from app import app
from orm_operations import *
from flask import render_template, redirect, request, session


@app.route("/")
def index_page():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/posts")
def new_post_create():
    user = session.get("user")
    return render_template("posts.html", user=user)


@app.route("/posts", methods=["POST"])
def new_post_send():
    user = session.get("user")
    new_p = request.form['post']
    add_post(user, new_p)
    return redirect("/")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_handler():
    # print(f"id:{request.form['username']}, password:{request.form['password']}")
    success = check_user(request.form['username'], request.form['password'])
    if success:
        session["user"] = request.form['username']
    return redirect("/")


@app.route("/logout")
def logout_handler():
    session.pop("user")
    return redirect("/")


@app.route("/ban")
def ban_user():
    delete_user(session["user"])
    session.pop("user")
    return redirect("/")


@app.route("/register")
def register_page():
    return render_template("register.html", success=None)


@app.route("/register", methods=["POST"])
def register_handler():
    print(f"id:{request.form['username']}, password:{request.form['password']}")
    register_user(request.form['username'], request.form['password'])
    return redirect("/")


@app.route("/users/<username>")
def show_posts(username):
    posts = user_posts(username)
    user = session.get("user")
    return render_template("UserPosts.html", posts=posts, user=user, username=username)


@app.route("/users/<username>/<post>")
def g_post(username, post):
    user = session.get("user")
    if username == user:
        str = get_post(username, post)
        return render_template("changepost.html", user=user, str=str)
    else:
        redirect("/")


@app.route("/users/<username>/<post>", methods=["POST"])
def ch_post(username, post):
    user = session.get("user")
    if username == user:
        if (request.form["post"]!=""):
            change_post(username, post, request.form["post"])
        else:
            delete_post(username, post)
        return redirect("/users/"+username)
    else:
        redirect("/")


# @app.route("/users")
# def users():
#     #list = list_users()
#     return render_template("Users.html", list=list)

