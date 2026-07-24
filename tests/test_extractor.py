import tempfile,pytest
from src.extractor import extract_text
def test_txt():
    with tempfile.NamedTemporaryFile(suffix='.txt',mode='w',delete=False) as f: f.write('Hello world');n=f.name
    assert 'Hello world' in extract_text(n)
def test_unsupported():
    with pytest.raises(ValueError,match='Unsupported'): extract_text('f.xyz')
