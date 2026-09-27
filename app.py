from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import date, timedelta

app = Flask(__name__)


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    connection = sqlite3.connect("bookstreak.db")

    connection.row_factory = sqlite3.Row

    return connection


# =========================
# CREATE DATABASE
# =========================

def create_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            pages_read INTEGER DEFAULT 0
        )
    """)

    columns = connection.execute(
        "PRAGMA table_info(books)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    # Add last_read column if it does not exist

    if "last_read" not in column_names:

        connection.execute(
            "ALTER TABLE books ADD COLUMN last_read TEXT"
        )

    # Add pages_today column if it does not exist

    if "pages_today" not in column_names:

        connection.execute(
            "ALTER TABLE books ADD COLUMN pages_today INTEGER DEFAULT 0"
        )

    connection.commit()

    connection.close()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    connection = get_db_connection()

    # =========================
    # GET ALL BOOKS
    # =========================

    books = connection.execute(
        "SELECT * FROM books"
    ).fetchall()

    # =========================
    # TOTAL PAGES READ
    # =========================

    total_pages_read = connection.execute(
        "SELECT COALESCE(SUM(pages_read), 0) FROM books"
    ).fetchone()[0]

    # =========================
    # COMPLETED BOOKS
    # =========================

    completed_books = connection.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE pages_read = total_pages
        """
    ).fetchone()[0]

    # =========================
    # READING DATES
    # =========================

    reading_dates = connection.execute(
        """
        SELECT DISTINCT last_read
        FROM books
        WHERE last_read IS NOT NULL
        """
    ).fetchall()

    connection.close()

    # =========================
    # CALCULATE STREAK
    # =========================

    dates = []

    for row in reading_dates:

        dates.append(
            date.fromisoformat(row["last_read"])
        )

    dates = sorted(
        set(dates),
        reverse=True
    )

    streak = 0

    today = date.today()

    if dates:

        if dates[0] == today:

            streak = 1

            current_date = today

            for reading_date in dates[1:]:

                expected_date = (
                    current_date
                    - timedelta(days=1)
                )

                if reading_date == expected_date:

                    streak += 1

                    current_date = reading_date

                else:

                    break

    # =========================
    # CONVERT BOOKS
    # =========================

    books = [
        dict(book)
        for book in books
    ]

    # =========================
    # CALCULATE BOOK PROGRESS
    # =========================

    for book in books:

        if book["total_pages"] > 0:

            book["progress"] = int(
                (
                    book["pages_read"]
                    / book["total_pages"]
                ) * 100
            )

        else:

            book["progress"] = 0

        if book["pages_read"] == book["total_pages"]:

            book["completed"] = True

        else:

            book["completed"] = False

    # =========================
    # READING GOAL
    # =========================

    reading_goal = 5

    if reading_goal > 0:

        goal_progress = int(
            (
                completed_books
                / reading_goal
            ) * 100
        )

    else:

        goal_progress = 0

    if goal_progress > 100:

        goal_progress = 100

    books_remaining = max(
        reading_goal - completed_books,
        0
    )

    # =========================
    # DAILY READING GOAL
    # =========================

    daily_goal = 20

    pages_today = 0

    today_string = date.today().isoformat()

    for book in books:

        if book["last_read"] == today_string:

            pages_today += book["pages_today"]

    if daily_goal > 0:

        daily_goal_progress = int(
            (
                pages_today
                / daily_goal
            ) * 100
        )

    else:

        daily_goal_progress = 0

    if daily_goal_progress > 100:

        daily_goal_progress = 100

    # =========================
    # SEND DATA TO HTML
    # =========================

    return render_template(
        "index.html",

        books=books,

        total_pages_read=total_pages_read,

        completed_books=completed_books,

        streak=streak,

        reading_goal=reading_goal,

        goal_progress=goal_progress,

        books_remaining=books_remaining,

        daily_goal=daily_goal,

        pages_today=pages_today,

        daily_goal_progress=daily_goal_progress,

        render_git_commit=os.getenv("RENDER_GIT_COMMIT", "local")
    )


# =========================
# ADD BOOK
# =========================

@app.route(
    "/add",
    methods=["POST"]
)
def add_book():

    title = request.form["title"]

    author = request.form["author"]

    total_pages = int(
        request.form["total_pages"]
    )

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO books
        (title, author, total_pages, pages_read)

        VALUES (?, ?, ?, ?)
        """,

        (
            title,
            author,
            total_pages,
            0
        )
    )

    connection.commit()

    connection.close()

    return redirect("/")


# =========================
# UPDATE READING PROGRESS
# =========================

@app.route(
    "/update/<int:book_id>",
    methods=["POST"]
)
def update_progress(book_id):

    pages_read = int(
        request.form["pages_read"]
    )

    connection = get_db_connection()

    book = connection.execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        """,

        (book_id,)
    ).fetchone()

    if book and 0 <= pages_read <= book["total_pages"]:

        today = date.today().isoformat()

        # Calculate pages newly read today

        if book["last_read"] == today:

            pages_today = book["pages_today"] + max(
                pages_read - book["pages_read"],
                0
            )

        else:

            pages_today = 0

        connection.execute(
            """
            UPDATE books

            SET pages_read = ?,
                last_read = ?,
                pages_today = ?

            WHERE id = ?
            """,

            (
                pages_read,
                today,
                pages_today,
                book_id
            )
        )

        connection.commit()

    connection.close()

    return redirect("/")


# =========================
# EDIT BOOK
# =========================

@app.route(
    "/edit/<int:book_id>",
    methods=["POST"]
)
def edit_book(book_id):

    title = request.form["title"]

    author = request.form["author"]

    total_pages = int(
        request.form["total_pages"]
    )

    connection = get_db_connection()

    book = connection.execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        """,

        (book_id,)
    ).fetchone()

    if (
        book
        and total_pages >= book["pages_read"]
        and total_pages > 0
    ):

        connection.execute(
            """
            UPDATE books

            SET title = ?,
                author = ?,
                total_pages = ?

            WHERE id = ?
            """,

            (
                title,
                author,
                total_pages,
                book_id
            )
        )

        connection.commit()

    connection.close()

    return redirect("/")


# =========================
# DELETE BOOK
# =========================

@app.route(
    "/delete/<int:book_id>",
    methods=["POST"]
)
def delete_book(book_id):

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,

        (book_id,)
    )

    connection.commit()

    connection.close()

    return redirect("/")

# =========================
# JSON API
# =========================


@app.route("/api/books")
def api_books():

    connection = get_db_connection()

    books = connection.execute(
        "SELECT * FROM books"
    ).fetchall()

    connection.close()

    return {
        "books": [dict(book) for book in books]
    }

    # =========================
# HEALTH CHECK
# =========================


@app.route("/health")
def health():

    return {
        "status": "ok"
    }

# =========================
# RUN APPLICATION
# =========================


create_database()


if __name__ == "__main__":
    app.run(debug=True)
