import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_meeting(topic, description, date, start_time, end_time, user_id, classes):
    sql = """INSERT INTO meetings (topic, description, date, start_time, end_time, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [topic, description, date, start_time, end_time, user_id])

    meeting_id = db.last_insert_id()

    sql = "INSERT INTO meeting_class (meeting_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [meeting_id, title, value])

def participate(meeting_id, user_id):
    sql = "INSERT INTO participants (meeting_id, user_id) VALUES (?, ?)"
    db.execute(sql, [meeting_id, user_id])

def get_participants(meeting_id):
    sql = """SELECT users.id user_id, users.username
             FROM participants, users
             WHERE participants.meeting_id = ? AND participants.user_id = users.id
             ORDER BY participants.id"""
    return db.query(sql, [meeting_id])

def get_classes(meeting_id):
    sql = "SELECT title, value FROM meeting_class WHERE meeting_id = ?"
    return db.query(sql, [meeting_id])

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
    result = db.query(sql, [meeting_id])
    return result[0] if result else None

def update_meeting(meeting_id, topic, description, date, start_time, end_time, classes):
    sql = """UPDATE meetings SET topic = ?,
                                 description = ?,
                                 date = ?,
                                 start_time = ?,
                                 end_time = ?
                             WHERE id = ?"""
    db.execute(sql, [topic, description, date, start_time, end_time, meeting_id])

    sql = "DELETE FROM meeting_class WHERE meeting_id = ?"
    db.execute(sql, [meeting_id])

    sql = "INSERT INTO meeting_class (meeting_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [meeting_id, title, value])

def remove_meeting(meeting_id):
    sql = "DELETE FROM meeting_class WHERE meeting_id = ?"
    db.execute(sql, [meeting_id])
    sql = "DELETE FROM meetings WHERE id = ?"
    db.execute(sql, [meeting_id])

def find_meetings(query):
    sql = """SELECT id, topic
             FROM meetings
             WHERE topic LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])