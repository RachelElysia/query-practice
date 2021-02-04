"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={user_id} email={email}>".format(
            user_id=self.user_id,
            email=self.email)


class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id={movie_id} title={title}>".format(
            movie_id=self.movie_id,
            title=self.title)


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Rating rating_id={rating_id} movie_id={movie_id} "
                "user_id={user_id} score={score}>").format(
            rating_id=self.rating_id,
            movie_id=self.movie_id,
            user_id=self.user_id,
            score=self.score)

# all_users = User.query.all()

# # Find the user with the email cats@gmail.com.
# email_cats_gmail = User.query.filter_by(email='cats@gmail.com').one()

# # Find any movies with the exact title “Cape Fear”.
# movie_cape_fear = Movie.query.filter_by(title='Cape Fear').all()

# # Find all users with the zipcode 90703.
# user_zip_90703 = User.query.filter_by(zipcode=90703).all()

# # Find all ratings of with the score of 5.
# rating_is_5 = Rating.query.filter_by(score=5).all()

# # Find the rating for the movie whose id is 7, from the user whose id is 6.
# rating_user6_movie7 = Rating.query.filter((movie.movie_id==7) & (user.user_id==6)).first()

# # Find all ratings that are larger than 3.
# rating_larger3 = Rating.query.filter(rating.score>3).all()

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hw_ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
