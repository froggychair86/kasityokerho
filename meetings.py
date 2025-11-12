import db

def add_meeting(topic, description, date, start_time, end_time, user_id):
        sql = """INSERT INTO meetings (topic, description, date, start_time, end_time, user_id)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        db.execute(sql, [topic, description, date, start_time, end_time, user_id])