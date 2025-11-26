import unittest
from unittest.mock import patch
import score_calculator

class TestScoreCalculator(unittest.TestCase):

    @patch('data_persistence.get_raw_project_data')
    def test_calculate_score_max(self, mock_get_data):
        """Test scenario where all documents are present (Score 10)."""
        mock_get_data.return_value = {
            'documents': [
                {'type': 'signedContract'},
                {'type': 'feasibilityStudy'},
                {'type': 'progressReport'},
                {'type': 'completionReport'}
            ]
        }
        
        result = score_calculator.calculate_transparency_score('test_max')
        self.assertEqual(result['transparency_score'], 10)
        self.assertEqual(result['alert_color'], 'GREEN')
        self.assertEqual(len(result['missing_documents_list']), 0)

    @patch('data_persistence.get_raw_project_data')
    def test_calculate_score_min(self, mock_get_data):
        """Test scenario where no documents are present (Score 0)."""
        mock_get_data.return_value = {
            'documents': []
        }
        
        result = score_calculator.calculate_transparency_score('test_min')
        self.assertEqual(result['transparency_score'], 0)
        self.assertEqual(result['alert_color'], 'RED')
        self.assertEqual(len(result['missing_documents_list']), 4)

    @patch('data_persistence.get_raw_project_data')
    def test_calculate_score_partial(self, mock_get_data):
        """Test scenario where signedContract is missing (Score 6.5 -> 6 or 7)."""
        # Present: feasibilityStudy (0.2), progressReport (0.25), completionReport (0.2)
        # Total: 0.65 -> Score 6.5 -> Round to 6 (Python 3 rounds to nearest even number for .5) or 7?
        # Python's round(0.65 * 10) = round(6.5) = 6.
        
        mock_get_data.return_value = {
            'documents': [
                {'type': 'feasibilityStudy'},
                {'type': 'progressReport'},
                {'type': 'completionReport'}
            ]
        }
        
        result = score_calculator.calculate_transparency_score('test_partial')
        # 0.2 + 0.25 + 0.2 = 0.65 * 10 = 6.5 -> round(6.5) = 6
        self.assertEqual(result['transparency_score'], 6)
        self.assertEqual(result['alert_color'], 'YELLOW')
        self.assertIn('Contrato Assinado', result['missing_documents_list'])

if __name__ == '__main__':
    unittest.main()
