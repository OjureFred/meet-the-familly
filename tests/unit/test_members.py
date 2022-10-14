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

    def test_set_mother(self):
        mother_demo_a = 'mother_demo_a'
        mother_demo_b = Member(2, 'MotherDemoB', 'Male')
        mother_demo_c = Member(3, 'Mom', 'Female')

        # error case
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_a)
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_b)

        # Success cases
        self.member.set_mother(mother_demo_c)
        self.assertEqual(self.member.mother.name, 'Mom')
        self.assertEqual(self.member.mother.gender.value, 'Female')
