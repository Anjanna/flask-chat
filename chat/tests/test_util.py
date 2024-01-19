from chat.util import generate_uuid

def test_generate_uuid():
    first_random_id = generate_uuid()
    second_random_id = generate_uuid()
    assert first_random_id != second_random_id
