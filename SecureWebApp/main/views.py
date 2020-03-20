from flask import Blueprint, render_template


main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET'])
def main_index():
    return render_template('index.html')
