from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('game_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        score INTEGER
    )
''')
conn.commit()
conn.close()



# Game variables
target_number = None
attempts = 0


@app.route('/')
def index():
    return render_template('index_game.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    global target_number, attempts
    target_number = random.randint(1, 100)
    attempts = 0
    return redirect(url_for('play_game'))


@app.route('/play_game', methods=['GET', 'POST'])
def play_game():
    global target_number, attempts
    if request.method == 'POST':
        user_guess = int(request.form['user_guess'])
        attempts += 1

        if user_guess == target_number:
            return redirect(url_for('game_over', score=attempts))
        elif user_guess < target_number:
            message = 'Too low! Try again.'
        else:
            message = 'Too high! Try again.'

        return render_template('play_game.html', message=message)

    return render_template('play_game.html', message='')


@app.route('/game_over/<int:score>', methods=['GET', 'POST'])
def game_over(score):
    if request.method == 'POST':
        player_name = request.form['player_name']

        conn = sqlite3.connect('game_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)', (player_name, score))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('game_over.html', score=score)

# ... (previous code)

@app.route('/view_scores')
def view_scores():
    conn = sqlite3.connect('game_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scores ORDER BY score ASC')  # Order by score ascending
    scores = cursor.fetchall()
    conn.close()
    return render_template('view_scores.html', scores=scores)

# ... (remaining code)

if __name__ == '__main__':
    app.run(debug=True)
