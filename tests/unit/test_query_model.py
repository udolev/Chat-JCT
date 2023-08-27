import pytest

from pydantic import ValidationError

from app.routers.chat.models.query_model import Query, QueryMessage

def test_query_model_valid():
    query_json = {
        "temperature": 1,
        "model": "gpt-3.5-turbo",
        "context": [{"role":"system", "content":"My name is koko"}]
    }

    q = Query(**query_json)

def test_query_model_invalid_temp():
    query_json = {
        "temperature": 3,
        "model": "gpt-3.5-turbo",
        "context": []
    }

    with pytest.raises(ValidationError):
        q = Query(**query_json)

def test_query_model_invalid_engine():
    query_json = {
        "temperature": 0,
        "model": "gpt-3.5-turbo",
        "llm_engine":"lalala",
        "context": []
    }
    
    with pytest.raises(ValidationError):
        q = Query(**query_json)

def test_query_model_invalid_message_len():
    query_json = {
        "temperature": 0,
        "model": "gpt-3.5-turbo",
        "context": [{"role":"koko", "content":'"My name is koko"'}]
    }
    
    with pytest.raises(ValidationError):
        q = Query(**query_json)

def test_query_model_invalid_message_len():
    query_json = {
        "temperature": 0,
        "model": "gpt-3.5-turbo",
        "context": [{"role":"koko", "content":'a'*1_000_000}]
    }
    
    with pytest.raises(ValidationError):
        q = Query(**query_json)


def test_query_to_json():
    q = Query(context=[QueryMessage(role='user', content='hi'), QueryMessage(role='system', content='hi2')])
    query_dict = q.dict()
    assert query_dict
    assert query_dict['context'][0]['role'] == 'user'
