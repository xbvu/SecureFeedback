import datetime
import humanize

from SecureWebApp.extensions import db


# Definition of source groups table.
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    subject = db.Column(db.String(64))
    comment = db.Column(db.Text)


class FeedbackList:

    def __init__(self):
        self.feedback_list = []

    def update(self):
        fbs = Feedback.query.all()
        self.feedback_list = []
        now = datetime.datetime.utcnow()
        for fb in fbs:
            duration = now - fb.time_added
            print(fb.time_added)
            feedback_entry = {'rating': fb.rating,
                              'name': fb.name,
                              'email': fb.email,
                              'subject': fb.subject,
                              'comment': fb.comment,
                              'time_ago': humanize.naturaltime(duration.total_seconds())}
            self.feedback_list.insert(0, feedback_entry)

    def get(self):
        self.update()
        return self.feedback_list


feedback_list = FeedbackList()