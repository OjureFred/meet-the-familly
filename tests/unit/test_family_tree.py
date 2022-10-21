from unittest import TestCase
from unittest.mock import patch, Mock

from family_tree.family_tree import FamilyTree
#from tests.unit import create_fake_member
from tests.unit.create_user import create_fake_member

class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()
    
    def test_initialization(self):
        self.assertEqual(self.ftree.family_tree, {})
    @patch('family_tree.family_tree.Member.set_father')
    @patch('family_tree.family_tree.Member.set_mother')
    @patch('family_tree.family_tree.Member.add_child')
    @patch('family_tree.family_tree.Member', return_value = create_fake_member(id =1, name='Zim', gender='Male'))
    def test_add_child(self, mock_member):
        result = self.ftree.add_child('Zim', 'Male', 'Mother')
        mock_member.assert_called_with(1, 'Zim', 'Male')
        self.assertEqual(isinstance(self.ftree.family_tree.get('Zim', None), Mock), True)
        self.assertEqual(result, 'CHILD_ADDITION_SUCCEEDED')

        mother = create_fake_member(id=2, name='Mother', gender='Female')
        father = create_fake_member(id=3, name='Father', gender='Male')

        self.assertEqual(self.ftree.add_child('Zim2', 'Male', 'Mother'), 'PERSON_NOT_FOUND')
        self.ftree.family_tree['Mother'] = mother
        self.assertEqual(self.ftree.add_child('Zim2', 'Male', 'Mother'), 'CHILD_ADDITION_FAILED')
        self.ftree.family_tree['Father'] = father
        self.ftree.family_tree['Mother'] = mother

        self.assertEqual(self.ftree.add_child('Zim2', 'Male', 'Mother'), 'CHILD_ADDITION_SUCCEEDED')
        
