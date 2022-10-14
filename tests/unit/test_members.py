from unittest import TestCase
from family_tree.member import Member


class TestMember(TestCase):

    def setUp(self):
        self.member = Member(1, 'Fred', 'Male')

    def test_initialization(self):
        # Testinitialization
        self.assertEqual(isinstance(self.member, Member), True)

        # Testproperties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, 'Fred')
        self.assertEqual(self.member.gender.value, 'Male')
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # Test Edge case forgender
        self.assertRaises(ValueError, Member, 2, "SomeOtherPerson", 'Queer')
