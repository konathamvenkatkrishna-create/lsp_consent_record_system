from app.models.user import User

def seed_dummy_users(db):
    dummy_users = [
        {"name": "Test User 1", "mobile": "9999999999", "email": "u1@test.com"},
        {"name": "Test User 2", "mobile": "8888888888", "email": "u2@test.com"},
        {"name": "Test User 3", "mobile": "7777777777", "email": "u3@test.com"},
        {"name": "Test User 4", "mobile": "6666666666", "email": "u4@test.com"},
    ]

    for u in dummy_users:
        exists = db.query(User).filter_by(mobile=u["mobile"]).first()
        if exists:
            continue
        user = User(**u)
        db.add(user)

    db.commit()
    print("[SEED] Dummy users inserted.")
