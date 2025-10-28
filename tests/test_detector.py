# tests/test_detector.py
import unittest
from analyzer.ast_detector import analyze_file

class DetectorTests(unittest.TestCase):
    def test_safe_file(self):
        res = analyze_file('data/samples/safe_code1.py')
        self.assertTrue(any('No known vulnerabilities' in r for r in res))

    def test_vulnerable_file(self):
        res = analyze_file('data/samples/vulnerable_code1.py')
        self.assertTrue(any('Hardcoded Password' in r for r in res))
        self.assertTrue(any('SQL Injection' in r for r in res))

if __name__ == '__main__':
    unittest.main()
