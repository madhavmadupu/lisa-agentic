import unittest
from unittest.mock import MagicMock, patch
from state.graph import app
from agents.coder import coder_node

class TestFixFlow(unittest.TestCase):
    
    @patch('agents.coder.llm')
    @patch('agents.coder.read_file')
    @patch('agents.coder.write_file')
    def test_coder_fix_flow(self, mock_write, mock_read, mock_llm):
        """
        Test that coder uses feedback to fix code.
        """
        # Setup specific mock behavior
        mock_response = MagicMock()
        mock_response.content = "Fixed Code"
        mock_llm.invoke.return_value = mock_response
        
        mock_read.return_value = "Original Broken Code"
        mock_write.return_value = "Success"
        
        # State simulating a failure loop
        state = {
            "plan": {"files": [{"filename": "broken.py", "description": "Needs fix"}]},
            "review_feedback": "Syntax Error",
            "execution_output": "Error on line 1",
            "retry_count": 1
        }
        
        # Run coder node directly
        result = coder_node(state)
        
        # Verify read_file was called (crucial for fix flow)
        mock_read.assert_called_with("broken.py")
        
        # Verify prompts contained the feedback
        # We can inspect the arguments passed to llm.invoke
        call_args = mock_llm.invoke.call_args
        input_dict = call_args[0][0] # First arg of first call
        
        # Check if feedback was injected into the prompt inputs
        self.assertIn("feedback", input_dict)
        self.assertEqual(input_dict["feedback"], "Syntax Error")
        self.assertEqual(input_dict["current_code"], "Original Broken Code")
        
        # Verify output
        self.assertIn("FIXED File: broken.py", result["code"])

if __name__ == '__main__':
    unittest.main()
