import unittest
from review import build_prompt, validate_result
class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.docs = [{'name':'demo', 'text':'The sample is blue.'}]
    def test_exact_citation(self):
        result=validate_result('{"status":"supported","summary":"Blue","citations":[{"document":"demo","quote":"sample is blue"}]}',self.docs)
        self.assertEqual(result['status'],'supported')
    def test_fabricated_quote_rejected(self):
        with self.assertRaises(ValueError):
            validate_result('{"status":"supported","summary":"Red","citations":[{"document":"demo","quote":"red"}]}',self.docs)
    def test_conclusion_requires_citation(self):
        with self.assertRaises(ValueError):
            validate_result('{"status":"supported","summary":"yes","citations":[]}',self.docs)
    def test_empty_input(self):
        with self.assertRaises(ValueError):build_prompt('',self.docs)
    def test_empty_evidence(self):
        with self.assertRaises(ValueError):build_prompt('claim',[])
    def test_size_limit(self):
        with self.assertRaises(ValueError):build_prompt('claim',[{'name':'x','text':'x'*60001}])
if __name__=='__main__':unittest.main()
