from unittest import TestCase
from unittest.mock import patch
from geektrust import Geektrust

class TestGeekTrust(TestCase):

    def setUp(self):
        self.geektrust_app = Geektrust()
    
    def test_construct_add_child_method_call(self):
        result_one_args = self.geektrust_app.construct_add_child_method_call("Shan")
        result_two_args = self.geektrust_app.construct_add_child_method_call("Shan", "Male")
        result_three_args = self.geektrust_app.construct_add_child_method_call("Shan", "Mother", "Male")
        self.assertEqual(result_one_args, None)
        self.assertEqual(result_two_args, 'self.family_tree.add_child("Shan", "Male")')
        self.assertEqual(result_three_args, 'self.family_tree.add_child("Mother", "Male", "Shan")')
    
    def test_construct_add_spouse_method_call(self):
        result_two_args = self.geektrust_app.construct_add_spouse_method_call("Wife", "Female")
        result_three_args = self.geektrust_app.construct_add_spouse_method_call("Husband", "Wife", "Female")
        self.assertEqual(result_two_args, None)
        self.assertEqual(result_three_args, 'self.family_tree.add_spouse("Wife", "Female", "Husband")')
    
    def test_construct_get_relationship_method_call(self):
        result_one_args = self.geektrust_app.construct_get_relationship_method_call("Name")
        result_two_args = self.geektrust_app.construct_get_relationship_method_call("Name", "Brother_in_law")
        result_invalid_args = self.geektrust_app.construct_get_relationship_method_call("Name", "Random")
        self.assertEqual(result_one_args, None)
        self.assertEqual(result_two_args, 'self.family_tree.get_relationship("Name", "Brother_in_law")')
        self.assertEqual(result_invalid_args, None)
    
    @patch('geektrust.Geektrust.construct_add_child_method_call', return_value = 'self.family_tree.add_child("Member", "Male", "Mother")')
    @patch('geektrust.Geektrust.construct_add_spouse_method_call', return_value = 'self.family_tree.add_spouse("Wife", "Female", "Spouse")')
    @patch('geektrust.Geektrust.construct_get_relationship_method_call', return_value= 'self.family.get_relationship("Member", "Brother_in_law")')
    def test_translate(self, mock_construct_get_relationship_method_call, mock_construct_add_spouse_method_call, mock_construct_add_child_method_call ):
        with patch('builtins.open', create = True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = (
                'ADD_CHILD Mother Member Male',
                'ADD_SPOUSE Spouse Wife Female',
                'GET_RELATIONSHIP Member Brother_in_law'
            )
            result = self.geektrust_app.translate('dummy_file.txt')
            # self.assertEqual(
            #     result,
            #     [
            #         'self.family_tree.add_child("Member", "Male", "Mother")',
            #         'self.family_tree.add_spouse("Wife", "Female", "Spouse")',
            #         'self.family_tree.get_relationship("Member", "Brother_in_law")'
            #     ]
            # )