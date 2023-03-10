from psycopg2.extras import RealDictCursor

from db import connection, queries
from trello import TrelloManager


def sync_boards(trello_username):
    trello = TrelloManager(trello_username)
    boards = trello.get_boards()
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        for board in boards:
            trello_board_id = board.get("id")
            cur.execute(queries.UPSERT_BOARDS, (board.get("name"), trello_board_id))
            connection.commit()
            cur.execute(queries.GET_BOARD_BY_TRELLO_ID, (trello_board_id,))
            db_board = cur.fetchone()  # from db
            sync_lists(trello, trello_board_id, db_board.get("id"))


def sync_lists(trello, trello_board_id, board_id):
    board_lists = trello.get_lists_on_a_board(trello_board_id)
    with connection.cursor() as cur:
        for board_list in board_lists:
            cur.execute(
                queries.UPSERT_LISTS, (board_list.get("name"), board_list.get("id"), board_id)
            )
            connection.commit()
