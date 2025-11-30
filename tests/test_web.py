import pytest
from unittest.mock import patch, MagicMock
from trie_search.web import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Reset global state
    import trie_search.web
    # Set search_trie to a dummy value to prevent initialize_app from starting a build
    trie_search.web.search_trie = MagicMock() 
    trie_search.web.is_building = False
    trie_search.web.build_status = "Ready"
    # Reset config to defaults for testing
    trie_search.web.current_config = {
        "url": "https://example.com",
        "depth": 2
    }
    
    with app.test_client() as client:
        yield client

@patch('trie_search.web.threading.Thread')
def test_get_config(mock_thread, client):
    """Test getting the current configuration."""
    response = client.get('/api/config')
    assert response.status_code == 200
    data = response.get_json()
    assert 'config' in data
    assert data['config']['url'] == "https://example.com"
    assert data['config']['depth'] == 2
    assert 'is_building' in data
    assert 'status' in data

@patch('trie_search.web.threading.Thread')
def test_post_config(mock_thread, client):
    """Test updating the configuration."""
    # Mock the thread start to do nothing
    mock_thread_instance = MagicMock()
    mock_thread.return_value = mock_thread_instance
    
    new_config = {
        "url": "https://example.com",
        "depth": 1
    }
    
    response = client.post('/api/config', json=new_config)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Rebuild started"
    assert data['config']['url'] == "https://example.com"
    assert data['config']['depth'] == 1
    
    # Verify thread was started
    mock_thread.assert_called_once()
    mock_thread_instance.start.assert_called_once()

def test_search_empty(client):
    """Test search with empty query."""
    response = client.get('/search?query=')
    assert response.status_code == 200
    assert response.get_json() == []

def test_autocomplete_empty(client):
    """Test autocomplete with empty query."""
    response = client.get('/autocomplete?q=')
    assert response.status_code == 200
    assert response.get_json() == []
