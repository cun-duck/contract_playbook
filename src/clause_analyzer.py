import sqlite3
from rapidfuzz import fuzz

class ClauseAnalyzer:
    def __init__(self, db_path="data/clause_templates.db"):
        self.conn = sqlite3.connect(db_path)
    
    def get_ideal_clause(self, clause_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM clauses WHERE type=?", (clause_type,))
        result = cursor.fetchone()
        return result[0] if result else ""
    
    def compare_clauses(self, extracted, ideal):
        similarity = fuzz.ratio(extracted, ideal)
        differences = self._find_key_differences(extracted, ideal)
        return {"similarity": similarity, "differences": differences}
    
    def _find_key_differences(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        return list(words1.symmetric_difference(words2))[:5]