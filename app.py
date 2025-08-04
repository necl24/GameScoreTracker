from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_a_name = db.Column(db.String(50), nullable=False)
    team_b_name = db.Column(db.String(50), nullable=False)

    # Individual Player Names (nullable=True means they are optional)
    player_a1_name = db.Column(db.String(50), nullable=True)
    player_a2_name = db.Column(db.String(50), nullable=True)
    player_a3_name = db.Column(db.String(50), nullable=True)
    player_a4_name = db.Column(db.String(50), nullable=True)

    player_b1_name = db.Column(db.String(50), nullable=True)
    player_b2_name = db.Column(db.String(50), nullable=True)
    player_b3_name = db.Column(db.String(50), nullable=True)
    player_b4_name = db.Column(db.String(50), nullable=True)

    # Individual Player Scores (nullable=True and default=0 for numeric fields if optional)
    player_a1_score = db.Column(db.Integer, nullable=True, default=0)
    player_a2_score = db.Column(db.Integer, nullable=True, default=0)
    player_a3_score = db.Column(db.Integer, nullable=True, default=0)
    player_a4_score = db.Column(db.Integer, nullable=True, default=0)

    player_b1_score = db.Column(db.Integer, nullable=True, default=0)
    player_b2_score = db.Column(db.Integer, nullable=True, default=0)
    player_b3_score = db.Column(db.Integer, nullable=True, default=0)
    player_b4_score = db.Column(db.Integer, nullable=True, default=0)

    # Team Total Scores (calculated when submitting the form, not automatically by DB)
    team_a_total_score = db.Column(db.Integer, nullable=False)
    team_b_total_score = db.Column(db.Integer, nullable=False)

    game_date = db.Column(db.DateTime, default=datetime.utcnow)
    winner_name = db.Column(db.String(50)) # Still for the winning *team* name

    def __repr__(self):
        return '<Game %r>' % self.id


@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        # 1. Retrieve data from the form
        team_a_name = request.form['team_a_name'].strip()
        team_b_name = request.form['team_b_name'].strip()

        # Retrieve individual player names and scores (handle missing/empty fields)
        # Using .get('', '') for names ensures an empty string if not provided
        # Using (or 0) for scores handles empty string for int conversion, defaulting to 0
        player_a1_name = request.form.get('player_a1_name', '').strip()
        player_a1_score = int(request.form.get('player_a1_score') or 0)

        player_a2_name = request.form.get('player_a2_name', '').strip()
        player_a2_score = int(request.form.get('player_a2_score') or 0)

        player_a3_name = request.form.get('player_a3_name', '').strip()
        player_a3_score = int(request.form.get('player_a3_score') or 0)

        player_a4_name = request.form.get('player_a4_name', '').strip()
        player_a4_score = int(request.form.get('player_a4_score') or 0)

        player_b1_name = request.form.get('player_b1_name', '').strip()
        player_b1_score = int(request.form.get('player_b1_score') or 0)

        player_b2_name = request.form.get('player_b2_name', '').strip()
        player_b2_score = int(request.form.get('player_b2_score') or 0)

        player_b3_name = request.form.get('player_b3_name', '').strip()
        player_b3_score = int(request.form.get('player_b3_score') or 0)

        player_b4_name = request.form.get('player_b4_name', '').strip()
        player_b4_score = int(request.form.get('player_b4_score') or 0)

        # 2. Validation: Ensure at least one player name is provided per team
        team_a_has_player = (player_a1_name or player_a2_name or player_a3_name or player_a4_name)
        team_b_has_player = (player_b1_name or player_b2_name or player_b3_name or player_b4_name)

        if not team_a_has_player:
            # Re-render the page with an error message and preserve input values
            games = Game.query.order_by(Game.game_date.desc()).all() # Fetch existing games to display
            error_message = 'Team A must have at least one player name provided.'
            return render_template("index.html", games=games, error=error_message,
                                   team_a_name_val=team_a_name, team_b_name_val=team_b_name,
                                   player_a1_name_val=player_a1_name, player_a1_score_val=player_a1_score,
                                   player_a2_name_val=player_a2_name, player_a2_score_val=player_a2_score,
                                   player_a3_name_val=player_a3_name, player_a3_score_val=player_a3_score,
                                   player_a4_name_val=player_a4_name, player_a4_score_val=player_a4_score,
                                   player_b1_name_val=player_b1_name, player_b1_score_val=player_b1_score,
                                   player_b2_name_val=player_b2_name, player_b2_score_val=player_b2_score,
                                   player_b3_name_val=player_b3_name, player_b3_score_val=player_b3_score,
                                   player_b4_name_val=player_b4_name, player_b4_score_val=player_b4_score)

        if not team_b_has_player:
            # Re-render the page with an error message and preserve input values
            games = Game.query.order_by(Game.game_date.desc()).all() # Fetch existing games to display
            error_message = 'Team B must have at least one player name provided.'
            return render_template("index.html", games=games, error=error_message,
                                   team_a_name_val=team_a_name, team_b_name_val=team_b_name,
                                   player_a1_name_val=player_a1_name, player_a1_score_val=player_a1_score,
                                   player_a2_name_val=player_a2_name, player_a2_score_val=player_a2_score,
                                   player_a3_name_val=player_a3_name, player_a3_score_val=player_a3_score,
                                   player_a4_name_val=player_a4_name, player_a4_score_val=player_a4_score,
                                   player_b1_name_val=player_b1_name, player_b1_score_val=player_b1_score,
                                   player_b2_name_val=player_b2_name, player_b2_score_val=player_b2_score,
                                   player_b3_name_val=player_b3_name, player_b3_score_val=player_b3_score,
                                   player_b4_name_val=player_b4_name, player_b4_score_val=player_b4_score)

        # 3. Calculate Team Total Scores
        team_a_total_score = player_a1_score + player_a2_score + player_a3_score + player_a4_score
        team_b_total_score = player_b1_score + player_b2_score + player_b3_score + player_b4_score

        # 4. Determine Winner
        winner_name = None
        if team_a_total_score > team_b_total_score:
            winner_name = team_a_name
        elif team_b_total_score > team_a_total_score:
            winner_name = team_b_name
        # If it's a draw, winner_name remains None as initialized

        # 5. Create New Game Object
        new_game = Game(
            team_a_name=team_a_name,
            team_b_name=team_b_name,
            player_a1_name=player_a1_name,
            player_a1_score=player_a1_score,
            player_a2_name=player_a2_name,
            player_a2_score=player_a2_score,
            player_a3_name=player_a3_name,
            player_a3_score=player_a3_score,
            player_a4_name=player_a4_name,
            player_a4_score=player_a4_score,
            player_b1_name=player_b1_name,
            player_b1_score=player_b1_score,
            player_b2_name=player_b2_name,
            player_b2_score=player_b2_score,
            player_b3_name=player_b3_name,
            player_b3_score=player_b3_score,
            player_b4_name=player_b4_name,
            player_b4_score=player_b4_score,
            team_a_total_score=team_a_total_score,
            team_b_total_score=team_b_total_score,
            winner_name=winner_name
        )





        
        try:
            db.session.add(new_game)
            db.session.commit()
            return redirect('/')
        except:
            # FIX: This line's indentation was corrected.
            # It should be at the same level as 'db.session.add(new_task)' etc.
            return 'There was an issue adding your Game'
    else :
        games = Game.query.order_by(Game.game_date.desc()).all()
        return render_template("index.html", games=games)


@app.route('/delete/<int:id>')
def delete(id):
    Game_to_delete = Game.query.get_or_404(id)

    try:
        db.session.delete(Game_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that Game'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Retrieve the specific game from the database or return a 404 error if not found.
    game = Game.query.get_or_404(id)

    # This block handles the form submission (POST request).
    if request.method == 'POST':
        try:
            game.team_a_name = request.form['team_a_name'].strip()
            game.team_b_name = request.form['team_b_name'].strip()

            game.player_a1_name = request.form.get('player_a1_name', '').strip()
            game.player_a1_score = int(request.form.get('player_a1_score') or 0)
            game.player_a2_name = request.form.get('player_a2_name', '').strip()
            game.player_a2_score = int(request.form.get('player_a2_score') or 0)
            game.player_a3_name = request.form.get('player_a3_name', '').strip()
            game.player_a3_score = int(request.form.get('player_a3_score') or 0)
            game.player_a4_name = request.form.get('player_a4_name', '').strip()
            game.player_a4_score = int(request.form.get('player_a4_score') or 0)

            game.player_b1_name = request.form.get('player_b1_name', '').strip()
            game.player_b1_score = int(request.form.get('player_b1_score') or 0)
            game.player_b2_name = request.form.get('player_b2_name', '').strip()
            game.player_b2_score = int(request.form.get('player_b2_score') or 0)
            game.player_b3_name = request.form.get('player_b3_name', '').strip()
            game.player_b3_score = int(request.form.get('player_b3_score') or 0)
            game.player_b4_name = request.form.get('player_b4_name', '').strip()
            game.player_b4_score = int(request.form.get('player_b4_score') or 0)

            # 2. Recalculate the team total scores based on the updated individual scores.
            game.team_a_total_score = (
                game.player_a1_score + game.player_a2_score +
                game.player_a3_score + game.player_a4_score
            )
            game.team_b_total_score = (
                game.player_b1_score + game.player_b2_score +
                game.player_b3_score + game.player_b4_score
            )

            # 3. Determine the new winner.
            game.winner_name = None
            if game.team_a_total_score > game.team_b_total_score:
                game.winner_name = game.team_a_name
            elif game.team_b_total_score > game.team_a_total_score:
                game.winner_name = game.team_b_name
            
            db.session.commit()
            return redirect('/')
        except Exception:
           return 'There was an issue updating your game'

    else:
        return render_template('update.html', game=game)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

