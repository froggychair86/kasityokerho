import db

def add_meeting(topic, description, date, start_time, end_time, user_id):
    sql = """INSERT INTO meetings (topic, description, date, start_time, end_time, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [topic, description, date, start_time, end_time, user_id])

def get_meetings():
    sql = "SELECT id, topic FROM meetings ORDER BY id DESC"
    return db.query(sql)

def get_meeting(meeting_id):
    sql = """SELECT meetings.id,
                    meetings.topic,
                    meetings.description,
                    meetings.date,
                    meetings.start_time,
                    meetings.end_time,
                    users.id user_id,
                    users.username
             FROM meetings, users
             WHERE meetings.user_id = users.id AND
                   meetings.id = ?"""
    return db.query(sql, [meeting_id])[0]

def update_meeting(meeting_id, topic, description, date, start_time, end_time):
    sql = """UPDATE meetings SET topic = ?,
                                 description = ?,
                                 date = ?,
                                 start_time = ?,
                                 end_time = ?
                             WHERE id = ?"""
    db.execute(sql, [topic, description, date, start_time, end_time, meeting_id])

def remove_meeting(meeting_id):
    sql = "DELETE FROM meetings WHERE id = ?"
    db.execute(sql, [meeting_id])