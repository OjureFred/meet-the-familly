from unittest import TestCase
from unittest.mock import patch
#from geektrust import Geektrust
from family_tree.geektrust import Geektrust

class TestGeekTrust(TestCase):

    def setUp(self):
        self.geektrust_app = Geektrust()
    
    @patch('geektrust.Geektrust.construct_add_child_method_call', return_value = 'self.family_tree.add_child("Member", "Male", "Mother")')
    @patch('geektrust.Geektrust.construct_add_spouse_method_call', return_value = 'self.family_tree.add_spouse("Wife", "Female", "Spouse")')
    @oatch('geektrust.Geektrust.construct_get_relationship_method_call', return_value= 'self.family.get_relationship("Member", "Brother_in_law")')
    def test_translate(self, mock_construct_get_relationship_method_call, mock_construct_add_spouse_method_call, mock_construct_add_child_method_call ):
        with patch('builtins.open', create = True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_vlue = (
                'ADD_CHILD Mother Member Male',
                'ADD_SPOUSE Spouse Wife Female',
                'GET_RELATIONSHIP Member Brother_in_law'
            )
            self.geektrust_app.translate('dummy_file.txt')
            self.assertEqual(
                result,
                [
                    'self.family_tree.add_child("Member", "Male", "Mother")',
                    'self.family_tree.add_spouse("Wife", "Female", "Spouse")',
                    'self.family_tree.get_relationship("Member", "Brother_in_law")'
                ]
            )