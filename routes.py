from flask import Blueprint, render_template, request, redirect, url_for, abort
from models import db, User, Post, Reply

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def view_home_feed():
    """Main Discussion Feed (Homepage)

    - Fetch all Post records ordered newest first
    - Render index.html with posts
    """
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/post/new', methods=['GET', 'POST'])
def create_new_thread():
    """Display form to create a new thread and handle submission."""
    if request.method == 'POST':
        title_input = request.form.get('title', '').strip()
        content_input = request.form.get('content', '').strip()
        user_id_input = request.form.get('user_id')  # temporary static user selection

        if not title_input or not content_input or not user_id_input:
            # Minimal validation: require title, content and user_id
            # Incomplete submissions re-render the form with a 400 status
            return render_template('create_post.html', error='Title, content and user are required.'), 400

        try:
            user_id_int = int(user_id_input)
        except (TypeError, ValueError):
            return render_template('create_post.html', error='Invalid user id.'), 400

        # Optional: ensure user exists
        user = User.query.get(user_id_int)
        if not user:
            return render_template('create_post.html', error='Selected user not found.'), 400

        new_post = Post(title=title_input, content=content_input, user_id=user_id_int)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.view_home_feed'))

    return render_template('create_post.html')


@main.route('/post/<int:post_id>', methods=['GET'])
def view_single_thread(post_id):
    """View a single thread and its replies."""
    post = Post.query.get_or_404(post_id)
    return render_template('thread.html', post=post)


@main.route('/post/<int:post_id>/reply', methods=['POST'])
def post_thread_reply(post_id):
    """Create a reply for the given thread and persist it."""
    parent_post = Post.query.get_or_404(post_id)

    content_input = request.form.get('content', '').strip()
    user_id_input = request.form.get('user_id')

    if not content_input or not user_id_input:
        # Minimal validation; redirect back to thread with error message could be preferred
        abort(400, description='Reply content and user_id are required.')

    try:
        user_id_int = int(user_id_input)
    except (TypeError, ValueError):
        abort(400, description='Invalid user_id')

    user = User.query.get(user_id_int)
    if not user:
        abort(400, description='User not found')

    new_reply = Reply(content=content_input, user_id=user_id_int, post_id=parent_post.id)
    db.session.add(new_reply)
    db.session.commit()

    return redirect(url_for('main.view_single_thread', post_id=post_id))


def init_app(app):
    """Helper to register the blueprint on a Flask app."""
    app.register_blueprint(main)
