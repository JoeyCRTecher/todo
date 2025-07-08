import pytest
import math
import sys
from pathlib import Path

# Import the calculation function from todo_app
from todo_app import calculate_score

class TestScoreCalculations:
    """Tests for the priority scoring system"""
    
    def test_basic_score_calculation(self):
        """Test basic score calculation with normal values"""
        # Test case: Impact=5, Tractability=5, Uncertainty=5
        score = calculate_score(5, 5, 5)
        expected = (5 * 5) / 5
        assert score == expected
        assert score == 5.0
    
    def test_high_priority_score(self):
        """Test high priority task scoring"""
        # High impact, high tractability, low uncertainty = high priority
        score = calculate_score(9, 8, 2)
        expected = (9 * 8) / 2
        assert score == expected
        assert score == 36.0
    
    def test_low_priority_score(self):
        """Test low priority task scoring"""
        # Low impact, low tractability, high uncertainty = low priority
        score = calculate_score(2, 3, 8)
        expected = (2 * 3) / 8
        assert score == expected
        assert score == 0.75
    
    def test_edge_cases(self):
        """Test edge cases in score calculation"""
        # Test with minimum values
        score = calculate_score(1, 1, 1)
        assert score == 1.0
        
        # Test with maximum values
        score = calculate_score(10, 10, 10)
        assert score == 10.0
        
        # Test with zero tractability (should return 0)
        score = calculate_score(5, 0, 5)
        assert score == 0.0
        
        # Test with zero uncertainty (should return 0 to avoid division by zero)
        score = calculate_score(5, 5, 0)
        assert score == 0.0
    
    def test_floating_point_precision(self):
        """Test floating point precision in calculations"""
        # Test with values that result in non-integer scores
        score = calculate_score(7, 3, 4)
        expected = (7 * 3) / 4
        assert score == expected
        assert score == 5.25
        
        # Test with more complex decimal result
        score = calculate_score(8, 6, 7)
        expected = (8 * 6) / 7
        assert abs(score - expected) < 0.001  # Allow for floating point precision
    
    def test_score_ranges(self):
        """Test that scores fall within expected ranges"""
        # Test various combinations
        test_cases = [
            (1, 1, 1, 1.0),      # Minimum values
            (10, 10, 10, 10.0),  # Maximum values
            (5, 5, 5, 5.0),      # Balanced values
            (9, 8, 2, 36.0),     # High priority
            (2, 3, 8, 0.75),     # Low priority
            (7, 4, 6, 4.67),     # Medium priority
        ]
        
        for impact, tractability, uncertainty, expected in test_cases:
            score = calculate_score(impact, tractability, uncertainty)
            assert abs(score - expected) < 0.01
    
    def test_zero_handling(self):
        """Test handling of zero values"""
        # Zero tractability
        assert calculate_score(5, 0, 5) == 0.0
        
        # Zero uncertainty
        assert calculate_score(5, 5, 0) == 0.0
        
        # Zero impact (should be allowed)
        assert calculate_score(0, 5, 5) == 0.0
        
        # All zeros
        assert calculate_score(0, 0, 0) == 0.0
    
    def test_negative_values(self):
        """Test handling of negative values (should work but may not be realistic)"""
        # Negative impact
        score = calculate_score(-5, 5, 5)
        assert score == -5.0
        
        # Negative tractability
        score = calculate_score(5, -5, 5)
        assert score == -5.0
        
        # Negative uncertainty
        score = calculate_score(5, 5, -5)
        assert score == -5.0
    
    def test_large_numbers(self):
        """Test with large numbers to ensure no overflow"""
        # Large values
        score = calculate_score(1000, 1000, 1000)
        assert score == 1000.0
        
        # Very large values
        score = calculate_score(10000, 10000, 10000)
        assert score == 10000.0
    
    def test_score_consistency(self):
        """Test that the same inputs always produce the same output"""
        # Test multiple calls with same parameters
        for _ in range(10):
            score1 = calculate_score(5, 5, 5)
            score2 = calculate_score(5, 5, 5)
            assert score1 == score2
            assert score1 == 5.0
    
    def test_score_formula_validation(self):
        """Test that the formula (Impact × Tractability) ÷ Uncertainty is correctly implemented"""
        # Test with known values
        impact, tractability, uncertainty = 6, 4, 3
        expected = (impact * tractability) / uncertainty
        actual = calculate_score(impact, tractability, uncertainty)
        assert actual == expected
        assert actual == 8.0
        
        # Test with different values
        impact, tractability, uncertainty = 8, 7, 2
        expected = (impact * tractability) / uncertainty
        actual = calculate_score(impact, tractability, uncertainty)
        assert actual == expected
        assert actual == 28.0 