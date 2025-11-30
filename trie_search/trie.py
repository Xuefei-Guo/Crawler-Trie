from typing import Any, Iterable, Iterator
from collections.abc import MutableMapping


def character_to_key(char: str) -> int:
    """
    Given a character return a number between [0, 26] inclusive.

    Letters a-z should be given their position in the alphabet 0-25, regardless of case:
        a/A -> 0
        z/Z -> 25

    Any other character should return 26.
    """
    # get ASCII value of lowercase character
    ord_char = ord(char.lower())
    # a-z characters
    if 97 <= ord_char <= 122:
        return ord_char - 97
    # other characters
    return 26


def key_to_character(index: int) -> str:
    """
    Given an index between [0, 26], return the character.
    0-25 -> 'a' - 'z'
    26 -> '_'
    """
    return chr(index + 97) if index < 26 else '_'


class TrieNode:
    """
    A single node in a trie structure.
    Each node can have up to 27 children (a-z and other).
    """
    def __init__(self):
        # Initialize children as a list of None
        self.children: list[TrieNode | None] = [None] * 27
        self.value: Any = None
        self.is_end: bool = False


class Trie(MutableMapping):
    """
    Implementation of a trie class where each node in the tree can
    have up to 27 children based on next letter of key.
    (Using rules described in character_to_key.)
    """
    def __init__(self):
        self.root = TrieNode()
        self.size = 0


    def __getitem__(self, key: str) -> Any:
        """
        Given a key, return the value associated with it in the trie.

        If the key has not been added to this trie, raise `KeyError(key)`.
        If the key is not a string, raise `KeyError(key)`
        """
        if not isinstance(key, str):
            raise KeyError(f"key \"{key}\" must be a string")
        
        node = self.root
        for char in key:
            # get index for character
            index = character_to_key(char)
            child = node.children[index]
            # if child node does not exist, key is not present
            if child is None:
                raise KeyError(f"key \"{key}\" not found in trie")
            # move to child node
            node = child
        
        # if node is not an end of a key, key is not present
        if not node.is_end:
            raise KeyError(f"key \"{key}\" not found in trie")
        return node.value


    def __setitem__(self, key: str, value: Any) -> None:
        """
        Given a key and value, store the value associated with key.
        Like a dictionary, will overwrite existing data if key already exists.
        If the key is not a string, raise `KeyError(key)`
        """
        if not isinstance(key, str):
            raise KeyError(f"key \"{key}\" must be a string")
        
        node = self.root
        for char in key:
            # get index for character
            index = character_to_key(char)
            child = node.children[index]
            # if child node does not exist, create it
            if child is None:
                child = TrieNode()
                node.children[index] = child
            # move to child node
            node = child
        
        # if this is a new key, increment size
        if not node.is_end:
            self.size += 1
        # set value and mark as end of key
        node.value = value
        node.is_end = True


    def __delitem__(self, key: str) -> None:
        """
        Remove data associated with `key` from the trie.
        If the key is not a string, raise `KeyError(key)`
        """
        if not isinstance(key, str):
            raise KeyError(f"key \"{key}\" must be a string")
        
        self._delete(self.root, key, 0)


    def _delete(self, node: TrieNode | None, key: str, depth: int) -> bool:
        """
        Helper function to delete a key from the trie.
        Returns True if the node can be deleted, False otherwise.
        """
        if node is None:
            raise KeyError(f"key \"{key}\" not found in trie")
        
        # if we have reached the end of the key
        if depth == len(key):
            if not node.is_end:
                raise KeyError(f"key \"{key}\" not found in trie")
            # delete the value
            node.is_end = False
            node.value = None
            self.size -= 1
            # return if the node can be deleted
            return all(child is None for child in node.children)
        
        # the next character in the key
        index = character_to_key(key[depth])
        delete_child = self._delete(node.children[index], key, depth + 1)
        # if the child can be deleted, delete it
        if delete_child:
            node.children[index] = None
            # return if the node can be deleted
            return not node.is_end and all(child is None for child in node.children)
        
        # cannot delete this node
        return False


    def __len__(self) -> int:
        """
        Return the total number of entries currently in the trie.
        """
        return self.size


    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        Return an iterable of (key, value) pairs for every entry in the trie in alphabetical order.
        """
        return self._traverse(self.root, "")
        

    def _traverse(self, node: TrieNode, prefix: str) -> Iterator[tuple[str, Any]]:
        """
        Helper function to traverse the trie and yield (key, value) pairs.
        """
        # if this node is the end of a key, yield the key and value
        if node.is_end:
            yield (prefix, node.value)
        
        # traverse all children
        for index, child in enumerate(node.children):
            if child is not None:
                # get character from index
                char = key_to_character(index)
                # yield from child node generator
                yield from self._traverse(child, prefix + char)


    def wildcard_search(self, key: str) -> Iterable[tuple[str, Any]]:
        """
        Search for keys that match a wildcard pattern where a '*' can represent any character.

        For example:
            - c*t would match 'cat', 'cut', 'cot', etc.
            - ** would match any two-letter string.

        Returns: Iterable of (key, value) pairs meeting the given condition.
        """
        return self._wildcard_traverse(self.root, "", key)
        
    
    def _wildcard_traverse(self, node: TrieNode, prefix: str, key: str) -> Iterable[tuple[str, Any]]:
        """
        Helper function to traverse the trie for wildcard search.
        """
        # get matched key
        if len(prefix) == len(key):
            if node.is_end:
                # yield the key and value
                yield (prefix, node.value)
            return
        
        # get current character in key
        current_char = key[len(prefix)]
        if current_char == '*':
            # explore all children
            for index, child in enumerate(node.children):
                if child is not None:
                    char = key_to_character(index)
                    # yield from child nodes generator
                    yield from self._wildcard_traverse(child, prefix + char, key)
        else:
            index = character_to_key(current_char)
            # get the matched child node
            child = node.children[index]
            if child is not None:
                # yield from child nodes generator
                yield from self._wildcard_traverse(child, prefix + current_char, key)


    def autocomplete(self, prefix: str) -> list[str]:
        """
        Return a list of all keys in the trie that start with the given prefix.
        """
        node = self.root
        for char in prefix:
            index = character_to_key(char)
            child = node.children[index]
            if child is None:
                return []
            node = child
        
        return [key for key, _ in self._traverse(node, prefix)]
