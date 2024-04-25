import sqlite3

con = sqlite3.connect("db/user_DB.db")
cur = con.cursor()


class User:
    def __init__(self, message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        
        classes = "Не указан"
        role = "Не указана"
        teacher = "Не указан"
        name = f"{first_name} {last_name}"
        
        try:
            cur.execute('INSERT INTO users (id, name, username, classes, role, name_teacher) VALUES (?, ?, ?, ?, ?, ?)',
                              (user_id, name, username, classes, role, teacher))
        except Exception:
            cur.execute("""UPDATE users SET id=id, name=?, username=?, classes=classes, role=role, name_teacher=name_teacher WHERE id = ?""",
                              (name, username, user_id))
        
        con.commit()
    
    def add_class(self, message, text_class):
        cur.execute("""UPDATE users SET id=id, name=name, username=username, classes=?, role=role, name_teacher=name_teacher WHERE id=?""",
                    (text_class, message.chat.id))
        con.commit()

    def check(self, message):        
        result = cur.execute("SELECT classes FROM users WHERE id=?", (message.chat.id,)).fetchall()
        return result if result[0][0] != "Не указан" else None
    
    def add_role(self, message, text_role):
        cur.execute("""UPDATE users SET id=id, name=name, username=username, classes=classes, role=?, name_teacher=name_teacher WHERE id=?""",
                    (text_role, message.chat.id))
        con.commit()
    
    def get_role(self, user_id):
        return cur.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchall()[0][0]
    
    def add_sub(self, message, text_subject):
        cur.execute("""UPDATE users SET id=id, name=name, username=username, classes=classes, role=role, name_teacher=? WHERE id=?""",
                    (text_subject, message.chat.id))
        con.commit()
    
    def get_sub(self, message):
        return cur.execute("SELECT name_teacher FROM users WHERE id = ?", (message.chat.id,)).fetchall()[0][0]
    