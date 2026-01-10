import unittest
from unittest.mock import MagicMock, patch
from state.graph import app

class TestLISA(unittest.TestCase):
    
    @patch('agents.architect.llm')
    @patch('agents.coder.llm')
    @patch('agents.reviewer.execute_python')
    @patch('agents.reviewer.llm')
    def test_full_successful_flow(self, mock_reviewer_llm, mock_execute, mock_coder_llm, mock_architect_llm):
        """
        Test a full successful run where Architect plans, Coder codes, and Reviewer passes it.
        """
        # Mock Architect
        mock_architect_llm.invoke.return_value = {
            "files": [{"filename": "hello.py", "description": "Prints hello"}], 
            "step_by_step_instructions": ["Write print"]
        }
        
        # Mock Coder
        mock_coder_content = MagicMock()
        mock_coder_content.content = "print('Hello')"
        mock_coder_llm.invoke.return_value = mock_coder_content
        
        # Mock Reviewer Execution (Success)
        mock_execute.return_value = {"return_code": 0, "stdout": "Hello", "stderr": ""}
        
        # Run Graph
        initial_state = {"user_request": "Make hello world", "retry_count": 0}
        final_state = app.invoke(initial_state)
        
        # Assertions
        self.assertEqual(final_state['review_feedback'], "Approved")
        self.assertIn("File hello.py PASSED", final_state['execution_output'])

if __name__ == '__main__':
    unittest.main()
