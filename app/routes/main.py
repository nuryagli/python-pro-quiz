from flask import Blueprint, render_template
from flask_login import current_user
from ..models import User
from sqlalchemy import func
from .. import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    highest_score = db.session.query(func.max(User.highest_score)).scalar() or 0
    return render_template('main/index.html', highest_score=highest_score)
