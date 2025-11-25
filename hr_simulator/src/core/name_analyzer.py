"""
Name Analyzer — Gender and Ethnicity Inference
Used to simulate biased HR systems that infer protected attributes from names
"""

from pathlib import Path
from typing import Tuple, Set


class NameAnalyzer:
    """
    Analyzes candidate names for gender and ethnicity cues.
    This simulates real-world bias in HR systems.
    """
    
    def __init__(self):
        """Load name databases"""
        data_dir = Path(__file__).parent.parent.parent / "data" / "names"
        
        self.female_names: Set[str] = set(
            (data_dir / "female_names.txt").read_text().strip().splitlines()
        )
        
        self.male_names: Set[str] = set(
            (data_dir / "male_names.txt").read_text().strip().splitlines()
        )
        
    def infer_gender(self, first_name: str) -> Tuple[str, float]:
        """
        Infer gender from first name.
        
        Args:
            first_name: Candidate's first name
            
        Returns:
            Tuple of (gender, confidence)
            - gender: "male", "female", or "unknown"
            - confidence: 0.0 to 1.0
        """
        first_name_lower = first_name.strip().lower()
        
        if first_name_lower in self.female_names:
            return ("female", 0.85)
        elif first_name_lower in self.male_names:
            return ("male", 0.85)
        else:
            return ("unknown", 0.0)
    
    def is_minority_name(self, full_name: str) -> Tuple[bool, float]:
        """
        Detect non-Western names (simulating ethnic bias).
        This is a simplified heuristic for demo purposes.
        
        Args:
            full_name: Candidate's full name
            
        Returns:
            Tuple of (is_minority, confidence)
        """
        name_lower = full_name.lower()
        
        # Common non-Western name patterns (for demo)
        minority_indicators = [
            "mohammed", "ahmed", "ali", "aisha", "fatima", "omar",
            "chen", "wang", "li", "zhang", "liu",
            "patel", "kumar", "singh", "sharma",
            "nguyen", "tran", "le",
            "rodriguez", "garcia", "hernandez", "martinez"
        ]
        
        for indicator in minority_indicators:
            if indicator in name_lower:
                return (True, 0.75)
        
        return (False, 0.0)
    
    def get_name_parts(self, full_name: str) -> Tuple[str, str]:
        """
        Split full name into first and last name.
        
        Args:
            full_name: Candidate's full name
            
        Returns:
            Tuple of (first_name, last_name)
        """
        parts = full_name.strip().split()
        
        if len(parts) >= 2:
            return (parts[0], parts[-1])
        elif len(parts) == 1:
            return (parts[0], "")
        else:
            return ("", "")
