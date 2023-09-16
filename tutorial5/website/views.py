from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Book
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    books = Book.query.all()
    return render_template("home.html", user=current_user, books=books)

@views.route("/add-book", methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book = request.form.get("book")
        book_author = request.form.get("author")
        status = request.form.get("status")

        if len(book) < 3:
            flash('Book name must be at least 4 characters long', category='error')
        else:
            new_book = Book(book=book, book_author=book_author, status=status,
                             author=current_user.id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('add_book.html', user=current_user)

@views.route("/edit-book/<id>", methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get(id)

    if not book:
        flash("Book does not exist.", category='error')
        return redirect(url_for('views.home'))
    if current_user.id != book.author:
        flash('You do not have permission to edit this book.', category='error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        new_book = request.form.get('book')
        new_author = request.form.get('book_author')
        new_status = request.form.get('status')

        book.book = new_book
        book.book_author = new_author
        book.status = new_status

        db.session.commit()
        flash('Book information updated successfully', category='success')
        return redirect(url_for('views.home'))

    return render_template('edit_book.html', book=book, user=current_user)
        

@views.route("/delete-book/<id>")
@login_required
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        flash("Book does not exist.", category='error')
    elif current_user.id != book.author:
        flash('You do not have permission to delete this book.', category='error')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted.', category='success')

    return redirect(url_for('views.home'))