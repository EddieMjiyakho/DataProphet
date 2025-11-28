import pytest
from app.services.polymer_service import react_polymer, will_react, process_multiple_polymers

class TestPolymerService:
    def test_will_react(self):
        assert will_react('a', 'A') == True
        assert will_react('A', 'a') == True
        assert will_react('a', 'a') == False
        assert will_react('A', 'A') == False
        assert will_react('a', 'b') == False
        assert will_react('X', 'y') == False
        
    def test_react_polymer_basic(self):
        # Test case 1 from assignment - but let's verify what we actually get
        result, count = react_polymer("AaefxxxXB")
        # # Based on our algorithm, this should be "efxxB" with 2 reactions
        # # Aa -> react (1), xxX -> x reacts with X (2), B remains
        assert result == "efxxB"
        assert count == 2

    def test_react_polymer_assignment_examples(self):
        # Example 1 from assignment
        result, count = react_polymer("vRaKkNgeUYTt")
        # vRaKkNgeUYTt -> vRaNgeUY
        # Reactions: Kk, Tt
        assert result == "vRaNgeUY"
        assert count == 2

    def test_react_polymer_empty(self):
        result, count = react_polymer("")
        assert result == ""
        assert count == 0

    def test_react_polymer_no_reaction(self):
        result, count = react_polymer("abcdef")
        assert result == "abcdef"
        assert count == 0

    def test_process_multiple_polymers(self):
        polymers = ["aA", "bB", "cC"]
        result, count = process_multiple_polymers(polymers)
        assert result == ""
        assert count == 3

    def test_process_empty_list(self):
        result, count = process_multiple_polymers([])
        assert result == ""
        assert count == 0