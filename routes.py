from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Post, Reply
import random, string

main = Blueprint('main', __name__)


def generate_unique_deleted_username():
    """Generates a unique 'deleted-user-<specialcode>' username with a 5-10 character code."""
    allowed_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        code_length = random.randint(5, 10)
        special_code = ''.join(random.choice(allowed_chars) for _ in range(code_length))
        candidate_username = f"deleted-user-{special_code}"
        
        # Check if code collision exists in database
        existing = db.session.scalar(db.select(User).filter_by(username=candidate_username))
        if not existing:
            return candidate_username, special_code

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.view_home_feed'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            return render_template('register.html', error='All fields are required.'), 400

        # Check for duplicate username
        if db.session.scalar(db.select(User).filter_by(username=username)):
            return render_template('register.html', error='Username already taken.'), 400

        # Check for duplicate email
        if db.session.scalar(db.select(User).filter_by(email=email)):
            return render_template('register.html', error='Email is already registered.'), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.view_home_feed'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.view_home_feed'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = db.session.scalar(db.select(User).filter_by(username=username))
        
        if not user or not user.check_password(password):
            return render_template('login.html', error='Invalid username or password.'), 400
        
        login_user(user)
        return redirect(url_for('main.view_home_feed'))
    
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.view_home_feed'))


@main.route('/', methods=['GET'])
def view_home_feed():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_new_thread():
    if request.method == 'POST':
        title_input = request.form.get('title', '').strip()
        content_input = request.form.get('content', '').strip()
        
        if not title_input or not content_input:
            return render_template('create_post.html', error='Title and content required.'), 400
        
        new_post = Post(title=title_input, content=content_input, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('main.view_home_feed'))
    
    return render_template('create_post.html')


@main.route('/post/<int:post_id>', methods=['GET'])
def view_single_thread(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template('thread.html', post=post)


@main.route('/post/<int:post_id>/reply', methods=['POST'])
@login_required
def post_thread_reply(post_id):
    parent_post = db.get_or_404(Post, post_id)
    content_input = request.form.get('content', '').strip()
    
    if not content_input:
        abort(400, description='Reply content required.')
    
    new_reply = Reply(content=content_input, user_id=current_user.id, post_id=parent_post.id)
    db.session.add(new_reply)
    db.session.commit()
    
    return redirect(url_for('main.view_single_thread', post_id=post_id))


@main.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_thread(post_id):
    post = db.get_or_404(Post, post_id)
    
    # Authorization check: only author can edit
    if post.user_id != current_user.id:
        abort(403)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            return render_template('edit_post.html', post=post, error='Title and content required.'), 400
        
        post.title = title
        post.content = content
        db.session.commit()
        
        return redirect(url_for('main.view_single_thread', post_id=post.id))
    
    return render_template('edit_post.html', post=post)


@main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_thread(post_id):
    post = db.get_or_404(Post, post_id)
    
    # Authorization check: only author can delete
    if post.user_id != current_user.id:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('main.view_home_feed'))


@main.route('/reply/<int:reply_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reply(reply_id):
    reply = db.get_or_404(Reply, reply_id)
    
    # Authorization check: only author can edit
    if reply.user_id != current_user.id:
        abort(403)
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        
        if not content:
            return render_template('edit_reply.html', reply=reply, error='Reply content required.'), 400
        
        reply.content = content
        db.session.commit()
        
        return redirect(url_for('main.view_single_thread', post_id=reply.post_id))
    
    return render_template('edit_reply.html', reply=reply)


@main.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        new_username, special_code = generate_unique_deleted_username()
        
        # Anonymize account details
        current_user.username = new_username
        current_user.email = f"deleted-{special_code}@deleted.local"
        current_user.password_hash = "ACCOUNT_DEACTIVATED"
        
        db.session.commit()
        logout_user()
        
        return redirect(url_for('main.view_home_feed'))
    
    return render_template('delete_account.html')

@main.route('/reply/<int:reply_id>/delete', methods=['POST'])
@login_required
def delete_reply(reply_id):
    reply = db.get_or_404(Reply, reply_id)
    
    # Authorization check: only author can delete
    if reply.user_id != current_user.id:
        abort(403)
    
    target_post_id = reply.post_id
    db.session.delete(reply)
    db.session.commit()
    
    return redirect(url_for('main.view_single_thread', post_id=target_post_id))


def init_app(app):
    app.register_blueprint(main)