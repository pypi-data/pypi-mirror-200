from flask import(
        Blueprint, flash, g, redirect, render_template, request, session, url_for
        )

from pool_log.db import get_db


bp = Blueprint('log', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    if "pool_id" in session:
        logs = db.execute(
                'SELECT id, created, temperature, ph, chlorine, cya, pressure, clarity'
                ' FROM log l WHERE pool = ?'
                ' ORDER BY created DESC',
                (session['pool_id'],)
                ).fetchall()
        pool = db.execute(
                'SELECT name, volume FROM pool WHERE id = ?',
                (session['pool_id'],)
                ).fetchone()
    else:
        return redirect(url_for('pool.select'))

    return render_template('log/index.html', logs=logs, pool=pool)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        # Get info from the form
        temperature = request.form['temperature']
        ph = request.form['ph']
        chlorine = request.form['chlorine']
        cya = request.form['cya']
        pressure = request.form['pressure']
        clarity = request.form['clarity']
        error = None
        # Add in errors

        if error is None:
            try:
                db = get_db()
                db.execute(
                        # Insert log values into db
                        'INSERT INTO log (temperature, ph, chlorine, cya, pressure, clarity, pool)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (temperature, ph, chlorine, cya, pressure, clarity, session['pool_id'])
                        )
                db.commit()
            except db.IntegrityError:
                # Add in the error
                pass
            else:
                return redirect(url_for('index'))

            flash(error)

        return redirect(url_for('index'))

    db = get_db()
    last_log = db.execute(
                'SELECT id, created, temperature, ph, chlorine, cya, pressure, clarity'
                ' FROM log l WHERE pool = ?'
                ' ORDER BY created DESC',
                (session['pool_id'],)
                ).fetchone()

    return render_template('log/create.html', last_log=last_log)

