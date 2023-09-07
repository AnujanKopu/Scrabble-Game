from bag import Character
from collections import defaultdict

class GADDAGNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class GADDAG:
    def __init__(self):
        self.root = GADDAGNode()
        self.word_set = set()
    
    def build_from_file(self, filepath: str):
        with open(filepath, 'r') as f:
            words = [line.strip().upper() for line in f if line.strip()]
        
        self.word_set = set(words)
        
        for word in words:
            if len(word) < 2:
                continue
            
            for i in range(len(word) + 1):
                prefix = word[:i]
                suffix = word[i:]
                
                reversed_prefix = prefix[::-1]
                path = reversed_prefix + '#' + suffix
            
                node = self.root
                for char in path:
                    if char not in node.children:
                        node.children[char] = GADDAGNode()
                    node = node.children[char]
                node.is_terminal = True
    
    def can_form_word(self, word: str, rack: list[Character]) -> bool:
        word = word.upper()
        rack_chars = [c.name for c in rack]
        rack_count = defaultdict(int)
        for char in rack_chars:
            if char != 'BLANK':
                rack_count[char] += 1
            else:
                rack_count['_'] += 1
        
        blank_count = rack_count.get('_', 0)
        
        for char in word:
            if rack_count.get(char, 0) > 0:
                rack_count[char] -= 1
            elif blank_count > 0:
                blank_count -= 1
            else:
                return False
        
        return True
    
    def find_words_from_rack(self, rack: list[Character], board_state=None, anchor=None, direction=None):
        if board_state is None:
            return self._find_all_words(rack)
        else:
            return self._find_anchor_words(rack, board_state, anchor, direction)
    
    def _find_all_words(self, rack: list[Character]) -> list[str]:
        words = []
        rack_chars = [c.name for c in rack]
        
        def dfs(node, remaining_rack, current_word, is_reversed):
            if node.is_terminal and len(current_word) >= 2:
                words.append(current_word)
            
            if '#' in node.children:
                separator_node = node.children['#']
                for char, child_node in separator_node.children.items():
                    if char in remaining_rack:
                        new_rack = remaining_rack.copy()
                        new_rack.remove(char)
                        dfs(child_node, new_rack, current_word + char, False)
                    elif '_' in remaining_rack:
                        new_rack = remaining_rack.copy()
                        new_rack.remove('_')
                        dfs(child_node, new_rack, current_word + char, False)
            
            for char, child_node in node.children.items():
                if char == '#':
                    continue
                if char in remaining_rack:
                    new_rack = remaining_rack.copy()
                    new_rack.remove(char)
                    if is_reversed:
                        dfs(child_node, new_rack, char + current_word, True)
                    else:
                        dfs(child_node, new_rack, current_word + char, False)
                elif '_' in remaining_rack:
                    new_rack = remaining_rack.copy()
                    new_rack.remove('_')
                    if is_reversed:
                        dfs(child_node, new_rack, char + current_word, True)
                    else:
                        dfs(child_node, new_rack, current_word + char, False)
        
        dfs(self.root, rack_chars, "", False)
        return list(set(words))
    
    def _find_anchor_words(self, rack: list[Character], board_state, anchor, direction):
        words = []
        rack_chars = [c.name for c in rack]
        col, row = anchor
        
        if direction:
            cross_letters = self._get_cross_letters_vertical(board_state, col, row)
        else:
            cross_letters = self._get_cross_letters_horizontal(board_state, col, row)
        
        def extend_left(node, remaining_rack, word_so_far, pos, min_pos):
            if node.is_terminal and pos < min_pos:
                if '#' in node.children:
                    extend_right(node.children['#'], remaining_rack, word_so_far, pos, direction)
            
            if pos > 0:
                if board_state[col][row + pos - 1] is not None:
                    letter = board_state[col][row + pos - 1].name
                    if letter in node.children:
                        extend_left(node.children[letter], remaining_rack, letter + word_so_far, pos - 1, min_pos)
                else:
                    for char in remaining_rack:
                        if char in node.children:
                            new_rack = remaining_rack.copy()
                            new_rack.remove(char)
                            extend_left(node.children[char], new_rack, char + word_so_far, pos - 1, min_pos)
                        elif '_' in remaining_rack:
                            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                if letter in node.children:
                                    new_rack = remaining_rack.copy()
                                    new_rack.remove('_')
                                    extend_left(node.children[letter], new_rack, letter + word_so_far, pos - 1, min_pos)
            
            if '#' in node.children:
                extend_right(node.children['#'], remaining_rack, word_so_far, pos, direction)
        
        def extend_right(node, remaining_rack, word_so_far, pos, direction):
            if node.is_terminal:
                full_word = word_so_far
                if self._validate_word_placement(full_word, board_state, anchor, direction):
                    words.append((full_word, anchor, direction))
            
            if pos < 14:
                if board_state[col][row + pos + 1] is not None:
                    letter = board_state[col][row + pos + 1].name
                    if letter in node.children:
                        extend_right(node.children[letter], remaining_rack, word_so_far + letter, pos + 1, direction)
                else:
                    for char in remaining_rack:
                        if char in node.children:
                            new_rack = remaining_rack.copy()
                            new_rack.remove(char)
                            extend_right(node.children[char], new_rack, word_so_far + char, pos + 1, direction)
                        elif '_' in remaining_rack:
                            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                if letter in node.children:
                                    new_rack = remaining_rack.copy()
                                    new_rack.remove('_')
                                    extend_right(node.children[letter], new_rack, word_so_far + letter, pos + 1, direction)
        
        if direction:
            extend_left(self.root, rack_chars, "", 0, row)
        else:
            extend_left(self.root, rack_chars, "", 0, col)
        
        return words
    
    def _get_cross_letters_horizontal(self, board_state, col, row):
        if row > 0 and board_state[col][row - 1] is not None:
            return board_state[col][row - 1].name
        if row < 14 and board_state[col][row + 1] is not None:
            return board_state[col][row + 1].name
        return None
    
    def _get_cross_letters_vertical(self, board_state, col, row):
        if col > 0 and board_state[col - 1][row] is not None:
            return board_state[col - 1][row].name
        if col < 14 and board_state[col + 1][row] is not None:
            return board_state[col + 1][row].name
        return None
    
    def _validate_word_placement(self, word, board_state, anchor, direction):
        return True
    
    def is_valid_word(self, word: str) -> bool:
        return word.upper() in self.word_set

