from chatgpt_backend.services.openai_service import Openai_CompletionStream

def test_openai_completion():
    resp = Openai_CompletionStream([{
        'role': 'user',
        'content': 'Hello, my name is Pablo'
    }])
    for chunk in resp:
        try:
            yield chunk.choices[0]['delta']['content']
        except:
            pass
        
    assert resp is not None

