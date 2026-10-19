import unittest
from unittest.mock import patch, call
# Import your exact quiz function from its file location (e.g., main.py or menus.py)
from main import run_cli_understanding_check

class TestCliUnderstandingCheck(unittest.TestCase):

    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_perfect_score(self, mock_print, mock_input):
        """
        Milestone B5/B6 Test: Simulates a user selecting the correct choice 
        for all three questions ("1", "2", "1") and checks if it returns a perfect score.
        """
        # Simulate a user typing the correct answers sequentially
        mock_input.side_effect = ["1", "2", "1"]
        
        # Run your pure function logic
        final_score = run_cli_understanding_check()
        
        # Verify the integer score equals 3 out of 3
        self.assertEqual(final_score, 3)
        
        # Assert that your custom percentage printing text was computed accurately
        mock_print.assert_any_call("\nPercentage = 100.0")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_partial_score(self, mock_print, mock_input):
        """
        Milestone B6 Test: Simulates a user getting some questions wrong.
        Verifies that the score counter accurately records failures.
        """
        # Q1: "1" (Correct), Q2: "1" (Incorrect - should be 2), Q3: "3" (Incorrect - should be 1)
        mock_input.side_effect = ["1", "1", "3"]
        
        final_score = run_cli_understanding_check()
        
        # The user only got 1 question right
        self.assertEqual(final_score, 1)
        
        # Formula verification: (1 / 3) * 100 = 33.33% rounded to two decimals
        mock_print.assert_any_call("\nPercentage = 33.33")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_zero_score(self, mock_print, mock_input):
        """
        Milestone B6 Test: Simulates a user selecting incorrect options for all tasks.
        Verifies that score does not drop below 0 and percentage matches 0.0.
        """
        # Simulating completely wrong selections ("3", "3", "3")
        mock_input.side_effect = ["3", "3", "3"]
        
        final_score = run_cli_understanding_check()
        
        self.assertEqual(final_score, 0)
        mock_print.assert_any_call("\nPercentage = 0.0")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_defensive_whitespace_handling(self, mock_print, mock_input):
        """
        Defensive Programming Test: Verifies that your inner `.strip()` logic 
        cleans accidental spaces from user keyboard entries.
        """
        # Answers padded with whitespace should be cleaned and accepted as correct
        mock_input.side_effect = ["  1  ", " 2", "1   "]
        
        final_score = run_cli_understanding_check()
        
        self.assertEqual(final_score, 3)
        mock_print.assert_any_call("\nPercentage = 100.0")

if __name__ == "__main__":
    unittest.main()
