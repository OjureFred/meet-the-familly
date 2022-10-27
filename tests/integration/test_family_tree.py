from unittest import TestCase

from family_tree.member import Member
from family_tree.family_tree import FamilyTree, Gender

class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()
    
    def test_add_child(self):
        result = self.ftree.add_child('Zim2', 'Male', 'Mother')
        self.assertEqual(result, 'CHILD_ADDITION_SUCCEEDED')
        self.assertEqual(self.ftree.family_tree.get('Father', None) is None, True)

        self.assertEqual(self.ftree.add_child('Zim', 'Male', 'Mother'), 'PERSON_NOT_FOUND')
        self.assertEqual(self.ftree.add_child('Zim', 'Male', 'Father'), 'PERSON_NOT_FOUND')

        mother = Member(2, 'Mother', 'Female')
        father = Member(5, 'Father', 'Male')
        self.ftree.family_tree['Father'] = father
        mother.spouse = father
        self.ftree.family_tree['Father'].set_spouse(mother)
        self.ftree.family_tree['Mother'] = mother
        
        self.assertEqual(self.ftree.add_child('Zim', 'Male', 'Mother'), 'CHILD_ADDITION_SUCCEEDED')
        self.assertEqual(self.ftree.family_tree.get('Zim', None) is not None, True)
    
    def test_add_spouse(self):
        self.assertEqual(self.ftree.add_spouse('Wife', 'Female', 'Zim'), 'SPOUSE_ADDITION_FAILED')
        dummy_member = Member(4, 'DummyMember', 'Male')
        self.ftree.family_tree['DummyMember'] = dummy_member
        spouse_a = Member(1, 'FakeMember', 'Female')
        spouse_b = Member(2, 'AlreadyMarried', 'Male')
        spouse_b.set_spouse(spouse_a)
        spouse_c = Member(3, 'Zim', 'Male')
        self.ftree.family_tree['FakeMember'] = spouse_a
        self.ftree.family_tree['AlreadyMarried'] = spouse_b
        self.ftree.family_tree['Zim'] = spouse_c
        self.assertEqual(self.ftree.add_spouse('Wife', 'Female', 'FakeMember'), 'SPOUSE_ADDITION_FAILED')
        self.assertEqual(self.ftree.add_spouse('Wife', 'Female', 'AlreadyMarried'), 'SPOUSE_ADDITION_FAILED')
        self.assertEqual(self.ftree.add_spouse('Wife', 'Female', 'Zim'), 'SPOUSE_ADDITION_SUCCEEDED')
        self.assertEqual(self.ftree.add_spouse('Wife', 'Female', 'Zim'), 'SPOUSE_ADDITION_FAILED')

