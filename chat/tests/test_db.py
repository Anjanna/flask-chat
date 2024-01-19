from chat.db import ChatSession

def test_ping():
    session = ChatSession("test")
    result = session.ping_db()
    assert result['ok'] == 1
