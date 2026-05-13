from flask import render_template

from app.error import error

@error.app_errorhandler(404)
def handle_404(e):
    print("404 error handler is running")
    return render_template("errors/handle_404.html"), 404

@error.app_errorhandler(403)
def handle_403(e):
    return render_template("errors/handle_403.html"), 403

@error.errorhandler(500)
def handle_500():
    return render_template("errors/handle_500"), 500