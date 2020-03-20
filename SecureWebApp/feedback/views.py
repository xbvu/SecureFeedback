# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask import current_app as app

from SecureWebApp.feedback.models import Feedback, feedback_list
from SecureWebApp.config import DefaultConfig
from SecureWebApp.extensions import db

feedback = Blueprint('feedback', __name__, url_prefix='/feedback')


@feedback.route('/', methods=['GET'])
def feedback_index():
    rating_counter = {'1':0,'2':0,'3':0,'4':0,'5':0,}
    rating_percentages = {}
    fbs = feedback_list.get()
    for fb in fbs:
        rating_counter[str(fb['rating'])] += 1
    total_ratings = len(fbs)
    rating_sum = 0
    for k in rating_counter.keys():
        percentage = rating_counter[k] / (total_ratings + 0.0000000001) * 100
        rating_percentages[k] = percentage
        rating_sum+=int(k)*rating_counter[k]

    average_rating_float = rating_sum/(total_ratings+0.000000001)
    average_rating = '{:.1f}'.format(average_rating_float)

    return render_template('feedback.html', feedback=fbs, rating_counter=rating_counter,
                           rating_percentages=rating_percentages, total_ratings=total_ratings,
                           average_rating=average_rating, error_message="")


@feedback.route('/post', methods=['POST'])
def feedback_post():
    rating_str = request.form.get('rate')
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    comment = request.form.get('comment')

    if not rating_str:
        flash('Please rate the item.', 'is-danger')
        return redirect(url_for('feedback.feedback_index'))
        # return render_template('feedback.html', feedback=feedback_list.get(), error_message='Please rate the item.')
    try:
        rating = int(rating_str)
    except ValueError:
        flash('Rating should be an integer.', 'is-danger')
        return redirect(url_for('feedback.feedback_index'))

    if rating not in [1, 2, 3, 4, 5]:
        flash('Rating should be between 1 and 5.', 'is-danger')
        return redirect(url_for('feedback.feedback_index'))

    if not name: name = "Anonymous"
    if len(name) > 32:
        flash('Username is too long.', 'is-danger')
        return redirect(url_for('feedback.feedback_index'))

    if email:
        if len(email) > 128:
            flash('Email is too long.', 'is-danger')
            return redirect(url_for('feedback.feedback_index'))
    if subject:
        if len(subject) > 32:
            flash('Subject is too long.', 'is-danger')
            return redirect(url_for('feedback.feedback_index'))
    if comment:
        if len(comment) > 256:
            flash('Comment is too long.', 'is-danger')
            return redirect(url_for('feedback.feedback_index'))

    with app.app_context():
        new_group = Feedback(rating=rating,
                             name=name,
                             email=email,
                             subject=subject,
                             comment=comment,
                             time_added=datetime.datetime.utcnow())
        db.session.add(new_group)
        db.session.commit()

    flash('Feedback posted!', 'is-link')
    return redirect(url_for('feedback.feedback_index'))
