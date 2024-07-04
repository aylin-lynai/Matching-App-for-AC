from models import db, flask_app as app

def clear_all_tables():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    clear_all_tables()
    print("All tables have been cleared.")
