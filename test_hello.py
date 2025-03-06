import unittest
import io
import sys
from hello import hello

class TestHello(unittest.TestCase):
    def test_hello_output(self):
        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        hello()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check the output
        self.assertEqual(captured_output.getvalue(), "Hello from Claude Code!\n")

if __name__ == "__main__":
    unittest.main()