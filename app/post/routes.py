from app.post import post
from flask import render_template, redirect, flash, url_for, abort, request, jsonify
from flask_login import login_required, current_user
from app.post.forms import PostForm
from app import db
from app.models import Post, User

@post.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    legend = "What's on your mind?"
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You successfully made a post", "success")
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="Create New Post", form=form, legend=legend)

@post.route("/post/<int:post_id>")
@login_required
def view_post(post_id):
    post=db.session.get(Post, post_id)
    return render_template("post.html", post=post, title=f"Post {post.id} by {current_user}")

@post.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = db.session.get(Post, post_id)
    legend = "Update Post"

    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("main.home"))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template("create_post.html", title=f"Update Post {post_id}", form=form, legend = legend)

@post.route("/post/delete", methods=['POST'])
@login_required
def delete_post():
    data = request.get_json()
    post_id = data.get('postId')

    if(post_id):
        post = db.session.get(Post, post_id)
        if post.author != current_user:
            abort(403)

        db.session.delete(post)
        db.session.commit()
        flash("Deleted Successfully", "info")
        
    return jsonify({"redirect_url" : url_for("main.home")})

@post.route("/posts/by/<username>")
def user_posts(username):
    user = User.query.filter(User.username == username).first_or_404()
    page_number = request.args.get('page_number', 1, type=int)
    posts = db.paginate(Post.query.\
        filter(Post.user_id == user.id).\
        order_by(Post.date_posted.desc()),\
        page=page_number,
        per_page=5)
    
    return render_template("user_posts.html", title=f"Posts by {username}", posts=posts, user=user)