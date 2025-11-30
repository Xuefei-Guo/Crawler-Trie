from trie_search.trie import Trie

def test_trie_basic_operations():
    t = Trie()
    t["apple"] = {1}
    assert "apple" in t
    assert t["apple"] == {1}
    assert len(t) == 1
    
    t["app"] = {2}
    assert len(t) == 2
    assert t["app"] == {2}
    
    del t["apple"]
    assert "apple" not in t
    assert "app" in t
    assert len(t) == 1

def test_trie_wildcard_search():
    t = Trie()
    t["cat"] = 1
    t["cut"] = 2
    t["cot"] = 3
    t["dog"] = 4
    
    results = dict(t.wildcard_search("c*t"))
    assert len(results) == 3
    assert "cat" in results
    assert "cut" in results
    assert "cot" in results
    assert "dog" not in results

def test_trie_autocomplete():
    t = Trie()
    t["apple"] = 1
    t["application"] = 2
    t["app"] = 3
    t["banana"] = 4
    
    results = t.autocomplete("app")
    assert len(results) == 3
    assert "apple" in results
    assert "application" in results
    assert "app" in results
    assert "banana" not in results
    
    results = t.autocomplete("ban")
    assert len(results) == 1
    assert "banana" in results
    
    results = t.autocomplete("z")
    assert len(results) == 0
