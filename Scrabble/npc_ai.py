from bag import Character
from board import Board, Slot, Play, Word, HORIZONTAL, VERTICAL
from gaddag import GADDAG
from random import choice, shuffle
from collections import defaultdict
from copy import deepcopy

class MoveCandidate:
    def __init__(self, word: str, start_col: int, start_row: int, direction: bool, tiles_used: list[Character]):
        self.word = word
        self.start_col = start_col
        self.start_row = start_row
        self.direction = direction
        self.tiles_used = tiles_used
        self.score = 0
        self.estimated_points = 0

class MoveGenerator:
    def __init__(self, gaddag: GADDAG, board: Board):
        self.gaddag = gaddag
        self.board = board
    
    def generate_moves(self, rack: list[Character]) -> list[MoveCandidate]:
        moves = []
        
        if self.board.board[7][7] is None:
            moves.extend(self._generate_first_move(rack))
        else:
            anchors = self._find_anchor_squares()
            for anchor in anchors:
                moves.extend(self._generate_moves_from_anchor(rack, anchor))
        
        return moves
    
    def _generate_first_move(self, rack: list[Character]) -> list[MoveCandidate]:
        moves = []
        all_words = self.gaddag._find_all_words(rack)
        
        for word in all_words:
            if len(word) <= 7:
                for start_col in range(7 - len(word) + 1, 8):
                    start_row = 7
                    if self._can_place_word(word, start_col, start_row, HORIZONTAL, rack):
                        tiles_used = self._get_tiles_for_word(word, rack)
                        move = MoveCandidate(word, start_col, start_row, HORIZONTAL, tiles_used)
                        moves.append(move)
        
        return moves
    
    def _find_anchor_squares(self) -> list[tuple[int, int]]:
        anchors = []
        for col in range(15):
            for row in range(15):
                if self.board.board[col][row] is None:
                    if self._is_anchor(col, row):
                        anchors.append((col, row))
        return anchors
    
    def _is_anchor(self, col: int, row: int) -> bool:
        if self.board.board[col][row] is not None:
            return False
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_col, new_row = col + dx, row + dy
            if 0 <= new_col < 15 and 0 <= new_row < 15:
                if self.board.board[new_col][new_row] is not None:
                    return True
        return False
    
    def _generate_moves_from_anchor(self, rack: list[Character], anchor: tuple[int, int]) -> list[MoveCandidate]:
        moves = []
        col, row = anchor
        
        for direction in [HORIZONTAL, VERTICAL]:
            left_part = self._get_left_part(col, row, direction)
            right_part = self._get_right_part(col, row, direction)
            
            if left_part and right_part:
                continue
            
            if left_part:
                prefix = left_part
                max_length = 7
            else:
                prefix = ""
                max_length = min(7, 15 - (row if direction == HORIZONTAL else col))
            
            rack_chars = [c.name for c in rack]
            
            for word in self.gaddag._find_all_words(rack):
                if len(word) <= max_length:
                    if prefix and word.startswith(prefix):
                        word_suffix = word[len(prefix):]
                        if self._can_form_from_rack(word_suffix, rack_chars):
                            tiles_used = self._get_tiles_for_word(word_suffix, rack)
                            start_col = col - (len(prefix) if direction == HORIZONTAL else 0)
                            start_row = row - (len(prefix) if direction == VERTICAL else 0)
                            move = MoveCandidate(word, start_col, start_row, direction, tiles_used)
                            moves.append(move)
                    elif not prefix:
                        if self._can_form_from_rack(word, rack_chars):
                            tiles_used = self._get_tiles_for_word(word, rack)
                            move = MoveCandidate(word, col, row, direction, tiles_used)
                            moves.append(move)
        
        return moves
    
    def _get_left_part(self, col: int, row: int, direction: bool) -> str:
        if direction == HORIZONTAL:
            if row == 0:
                return ""
            result = []
            for r in range(row - 1, -1, -1):
                if self.board.board[col][r] is None:
                    break
                result.insert(0, self.board.board[col][r].name)
            return "".join(result)
        else:
            if col == 0:
                return ""
            result = []
            for c in range(col - 1, -1, -1):
                if self.board.board[c][row] is None:
                    break
                result.insert(0, self.board.board[c][row].name)
            return "".join(result)
    
    def _get_right_part(self, col: int, row: int, direction: bool) -> str:
        if direction == HORIZONTAL:
            if row == 14:
                return ""
            result = []
            for r in range(row + 1, 15):
                if self.board.board[col][r] is None:
                    break
                result.append(self.board.board[col][r].name)
            return "".join(result)
        else:
            if col == 14:
                return ""
            result = []
            for c in range(col + 1, 15):
                if self.board.board[c][row] is None:
                    break
                result.append(self.board.board[c][row].name)
            return "".join(result)
    
    def _can_place_word(self, word: str, start_col: int, start_row: int, direction: bool, rack: list[Character]) -> bool:
        if direction == HORIZONTAL:
            if start_row + len(word) > 15:
                return False
            for i, char in enumerate(word):
                if self.board.board[start_col][start_row + i] is not None:
                    if self.board.board[start_col][start_row + i].name != char:
                        return False
        else:
            if start_col + len(word) > 15:
                return False
            for i, char in enumerate(word):
                if self.board.board[start_col + i][start_row] is not None:
                    if self.board.board[start_col + i][start_row].name != char:
                        return False
        
        return True
    
    def _can_form_from_rack(self, word: str, rack_chars: list[str]) -> bool:
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
    
    def _get_tiles_for_word(self, word: str, rack: list[Character]) -> list[Character]:
        tiles = []
        rack_copy = rack.copy()
        rack_chars = [c.name for c in rack_copy]
        
        for char in word:
            found = False
            for i, tile in enumerate(rack_copy):
                if tile.name == char:
                    tiles.append(rack_copy.pop(i))
                    found = True
                    break
            
            if not found:
                for i, tile in enumerate(rack_copy):
                    if tile.name == 'BLANK':
                        tiles.append(rack_copy.pop(i))
                        break
        
        return tiles

class MoveEvaluator:
    def __init__(self, board: Board):
        self.board = board
        self.points_map = {
            Character(0): 0, Character(1): 1, Character(5): 1, Character(9): 1,
            Character(12): 1, Character(14): 1, Character(15): 1, Character(18): 1,
            Character(19): 1, Character(20): 1, Character(21): 1, Character(4): 2,
            Character(7): 2, Character(2): 3, Character(3): 3, Character(13): 3,
            Character(16): 3, Character(6): 4, Character(8): 4, Character(22): 4,
            Character(23): 4, Character(25): 4, Character(11): 5, Character(10): 8,
            Character(24): 8, Character(17): 10, Character(26): 10
        }
    
    def evaluate_move(self, move: MoveCandidate, difficulty: int) -> int:
        if difficulty == 0:
            return 1
        
        points = self._estimate_points(move)
        move.estimated_points = points
        
        if difficulty == 1:
            return points
        
        if difficulty == 2:
            board_control = self._evaluate_board_control(move)
            rack_balance = self._evaluate_rack_balance(move)
            return points + board_control + rack_balance
        
        return points
    
    def _estimate_points(self, move: MoveCandidate) -> int:
        total_points = 0
        word_multiplier = 1
        
        for i, char in enumerate(move.word):
            if move.direction == HORIZONTAL:
                col, row = move.start_col, move.start_row + i
            else:
                col, row = move.start_col + i, move.start_row
            
            if col < len(move.tiles_used):
                tile = move.tiles_used[col if move.direction == VERTICAL else i]
            else:
                continue
            
            letter_points = self.points_map.get(tile, 0)
            
            if (col, row) in self.board.charcter_evaluator.modifier_map:
                modifier = self.board.charcter_evaluator.modifier_map[(col, row)]
                if modifier.value == 1:
                    word_multiplier *= 2
                    letter_points *= 1
                elif modifier.value == 2:
                    word_multiplier *= 3
                    letter_points *= 1
                elif modifier.value == 3:
                    letter_points *= 2
                elif modifier.value == 4:
                    letter_points *= 3
            
            total_points += letter_points
        
        return total_points * word_multiplier
    
    def _evaluate_board_control(self, move: MoveCandidate) -> int:
        score = 0
        for i, char in enumerate(move.word):
            if move.direction == HORIZONTAL:
                col, row = move.start_col, move.start_row + i
            else:
                col, row = move.start_col + i, move.start_row
            
            if (col, row) in self.board.charcter_evaluator.modifier_map:
                modifier = self.board.charcter_evaluator.modifier_map[(col, row)]
                if modifier.value == 2 or modifier.value == 3:
                    score += 5
        
        return score
    
    def _evaluate_rack_balance(self, move: MoveCandidate) -> int:
        vowels = {'A', 'E', 'I', 'O', 'U'}
        remaining = [t.name for t in move.tiles_used if t.name != 'BLANK']
        vowel_count = sum(1 for t in remaining if t in vowels)
        consonant_count = len(remaining) - vowel_count
        
        if 2 <= vowel_count <= 3 and 3 <= consonant_count <= 5:
            return 3
        return 0

class NPCPlayer:
    def __init__(self, name: str, difficulty: int, gaddag: GADDAG):
        self.name = name
        self.difficulty = difficulty
        self.gaddag = gaddag
        self.move_generator = None
        self.move_evaluator = None
    
    def initialize_for_board(self, board: Board):
        self.move_generator = MoveGenerator(self.gaddag, board)
        self.move_evaluator = MoveEvaluator(board)
    
    def select_move(self, rack: list[Character]) -> MoveCandidate:
        if not self.move_generator:
            return None
        
        moves = self.move_generator.generate_moves(rack)
        
        if not moves:
            return None
        
        if self.difficulty == 0:
            return choice(moves)
        
        for move in moves:
            score = self.move_evaluator.evaluate_move(move, self.difficulty)
            move.score = score
        
        if self.difficulty == 1:
            return max(moves, key=lambda m: m.score)
        
        moves.sort(key=lambda m: m.score, reverse=True)
        if len(moves) > 5:
            moves = moves[:5]
        
        return choice(moves) if self.difficulty == 2 else moves[0]

