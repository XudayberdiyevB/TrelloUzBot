# Users
ALL_USERS = "select * from users"
GET_USER_BY_CHAT_ID = "select * from users where chat_id = %s"
REGISTER_USER = """
    insert into
    users(chat_id, first_name, last_name, username)
    VALUES (%s, %s, %s, %s)
"""
UPDATE_USER_TRELLO_BY_CHAT_ID = """
    update users
    set trello_username = %s, trello_id = %s
    where chat_id = %s
"""

# Boards
UPSERT_BOARDS = """
    insert into boards(name, trello_id)
    values (%s, %s)
    on conflict (trello_id)
    do update set name=excluded.name 
"""
GET_BOARD_BY_TRELLO_ID = """
    select * from boards where trello_id = %s
"""

# Lists
UPSERT_LISTS = """
    insert into lists(name, trello_id, board_id)
    values (%s, %s, %s)
    on conflict (trello_id)
    do update set name=excluded.name, board_id=excluded.board_id 
"""
