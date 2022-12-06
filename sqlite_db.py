import sqlite3 as sq
import random


async def db_connect() -> None:
    global db, cur

    db = sq.connect('santa_play.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS santa_1(id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id_user INTEGER, username STRING, "
        "id_recipient INTEGER, room INTEGER)")
    db.commit()


async def add_user(room, username, tg_id_user):
    user = cur.execute(
        "SELECT tg_id_user FROM santa_1 WHERE tg_id_user == '{USER_ID}' and room == '{ROOM}'".format(USER_ID=tg_id_user,
                                                                                                     ROOM=room)).fetchone()
    if not user:
        cur.execute("INSERT INTO santa_1(tg_id_user, username, room) VALUES(?, ?, ?)", (tg_id_user, username, room))
        db.commit()


async def rand(a):
    list_orig = a.copy()
    while True:
        k = False
        for i in range(len(a)):
            if list_orig[i] == a[i]:
                k = True
        if not k:
            break
        else:
            random.shuffle(a)
    return a


async def start_play(count, room):
    list_party = cur.execute("SELECT id FROM santa_1 WHERE room == '{ROOM}'".format(ROOM=room)).fetchall()
    party = []
    for i in range(len(list_party)):
        party.append(list_party[i][0])

    party_orig = party.copy()
    list_id_recipient = await rand(party)
    for i in range(count):
        id_recipient = list_id_recipient[i]
        cur.execute("UPDATE santa_1 SET id_recipient == ? WHERE id == ? and room == ?",
                    (id_recipient, party_orig[i], room))

    db.commit()


async def check_username_recipient(user_id):
    id_recipient = cur.execute(
        "SELECT id_recipient FROM santa_1 WHERE tg_id_user == '{USER_ID}'".format(USER_ID=user_id)).fetchall()

    names = []
    for i in range(len(id_recipient)):
        name = cur.execute("SELECT username FROM santa_1 WHERE id == '{ID}'".format(ID=id_recipient[i][0])).fetchall()
        names.append(name[0][0])
    return names


async def check_tg_id_recipient(user_id):
    id_recipient = cur.execute(
        "SELECT id_recipient FROM santa_1 WHERE tg_id_user == '{USER_ID}'".format(USER_ID=user_id)).fetchall()

    tg_id = []
    for i in range(len(id_recipient)):
        id_ = cur.execute(
            "SELECT tg_id_user FROM santa_1 WHERE id == '{ID}'".format(ID=id_recipient[i][0])).fetchall()
        tg_id.append(id_[0][0])

    return tg_id


async def delete(user_id):
    cur.execute("DELETE FROM santa_1 WHERE tg_id_user == '{ID}'".format(ID=user_id))


async def count_part(room):
    count = cur.execute("SELECT COUNT(*) FROM santa_1 WHERE room == ?", (room,)).fetchone()[0]
    return count
