from unittest import TestCase
from unittest.mock import patch, Mock

from family_tree.member import Member, Gender
from family_tree import constants
# from tests.unit import create_fake_member
from tests.unit.create_user import create_fake_member


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

    def test_set_father(self):
        father_demo_a = 'father_demo_a'
        father_demo_b = Member(4, 'FatherDemoB', 'Female')
        father_demo_c = Member(5, 'Dad', 'Male')

        # error case
        self.assertRaises(ValueError, self.member.set_father, father_demo_a)
        self.assertRaises(ValueError, self.member.set_father, father_demo_b)

        # Success cases
        self.member.set_father(father_demo_c)
        self.assertEqual(self.member.father.name, 'Dad')
        self.assertEqual(self.member.father.gender.value, 'Male')

    def test_set_spouse(self):
        spouse_demo_a = 'spouse_demo_a'
        spouse_demo_b = Member(4, 'SpouseDemoB', 'Male')
        spouse_demo_c = Member(5, 'Wife', 'Female')

        # error case
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_a)
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_b)

        # Success cases
        self.member.set_spouse(spouse_demo_c)
        self.assertEqual(self.member.spouse.name, 'Wife')
        self.assertEqual(self.member.spouse.gender.value, 'Female')

    def test_add_child(self):
        child_demo_a = 'child_demo_a'
        child_demo_b = Member(4, 'Daughter', 'Female')

        # error case
        self.assertRaises(ValueError, self.member.add_child, child_demo_a)

        # success case
        self.member.add_child(child_demo_b)
        self.assertEqual(len(self.member.children), 1)
        self.assertEqual(self.member.children[0].name, 'Daughter')
        self.assertEqual(self.member.children[0].gender.value, 'Female')

    def test_get_paternal_grandmother(self):
        member = Member(9, 'NewMember', 'Male')
        father = Member(10, 'NewMember_father', 'Male')
        grandmother = Member(11, 'NewMember_grandmother', 'Female')

        # Error case
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(), grandmother)

    def test_get_maternal_grandmother(self):
        member = Member(9, 'NewMember', 'Male')
        mother = Member(10, 'NewMember_father', 'Female')
        grandmother = Member(11, 'NewMember_grandmother', 'Female')

        # Error case
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.mother = mother
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(), grandmother)

    def test_get_spouse_mother(self):
        member = Member(9, 'NewMember', 'Male')
        spouse = Member(10, 'NewMember_spouse', 'Female')
        spouse_mother = Member(11, 'NewMember_spouse_mother', 'Female')

        # Error case
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother)

    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, 'Dad', 'Male')]),
        create_fake_member(children=[
            Member(3, 'Dad', 'Male'),
            Member(4, 'Uncle', 'Male')]),
        create_fake_member(children=[
            Member(3, 'Dad', 'Male'),
            Member(4, 'Uncle', 'Male'),
            Member(5, 'Aunt', 'Female')])
    ])
    def test_get_paternal_aunt(self, mock_get_paternal_grandmother):

        # Check if get_paternal_grandmother has been replaced by a Mock object
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)

        # Check for None value
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])

        paternal_aunts = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunts), 1)
        self.assertEqual(paternal_aunts[0].name, 'Aunt')
        self.assertEqual(paternal_aunts[0].gender, Gender.female)

        # Check that mock_get_paternal_grandmother was called
        mock_get_paternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, 'Dad', 'Male')]),
        create_fake_member(children=[
            Member(3, 'Aunt', 'Female'),
            Member(4, 'Dad', 'Male')]),
        create_fake_member(children=[
            Member(3, 'Dad', 'Male'),
            Member(4, 'Uncle', 'Male'),
            Member(5, 'Aunt', 'Female')])
    ])
    def test_get_paternal_uncle(self, mock_get_paternal_grandmother):
        self.member.father = Member(3, 'Dad', 'Male')

        # Check if get_paternal_grandmother has been replaced by a Mock object
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)

        # Check for None value
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])

        paternal_uncles = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncles), 1)
        self.assertEqual(paternal_uncles[0].name, 'Uncle')
        self.assertEqual(paternal_uncles[0].gender, Gender.male)

        # Check that mock_get_paternal_grandmother was called
        mock_get_paternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, 'Mom', 'Female')]),
        create_fake_member(children=[
            Member(3, 'Mom', 'Female'),
            Member(4, 'Uncle', 'Male')]),
        create_fake_member(children=[
            Member(3, 'Mom', 'Female'),
            Member(4, 'Uncle', 'Male'),
            Member(5, 'Aunt', 'Female')])
    ])
    def test_get_maternal_aunt(self, mock_get_maternal_grandmother):
        self.member.mother = Member(3, 'Mom', 'Female')

        # Check if get_paternal_grandmother has been replaced by a Mock object
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)

        # Check for None value
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])

        maternal_aunts = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunts), 1)
        self.assertEqual(maternal_aunts[0].name, 'Aunt')
        self.assertEqual(maternal_aunts[0].gender, Gender.female)

        # Check that mock_get_paternal_grandmother was called
        mock_get_maternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, 'Mom', 'Female')]),
        create_fake_member(children=[
            Member(3, 'Aunt', 'Female'),
            Member(4, 'Mom', 'Female')]),
        create_fake_member(children=[
            Member(3, 'Mom', 'Female'),
            Member(4, 'Uncle', 'Male'),
            Member(5, 'Aunt', 'Female')])
    ])
    def test_get_maternal_uncle(self, mock_get_maternal_grandmother):
        self.member.mother = Member(3, 'Mom', 'Female')

        # Check if get_paternal_grandmother has been replaced by a Mock object
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)

        # Check for None value
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])

        maternal_uncles = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncles), 1)
        self.assertEqual(maternal_uncles[0].name, 'Uncle')
        self.assertEqual(maternal_uncles[0].gender, Gender.male)

        # Check that mock_get_paternal_grandmother was called
        mock_get_maternal_grandmother.assert_called_with()

    def test_get_son(self):
        member = Member(5, 'Dummy', 'Male')
        son = Member(6, 'Son', 'Male')
        daughter = Member(7, 'Daughter', 'Female')

        self.assertEqual(member.get_son(), [])
        member.children.append(daughter)
        self.assertEqual(member.get_son(), [])
        member.children.append(son)
        sons = member.get_son()
        self.assertEqual(len(sons), 1)
        self.assertEqual(sons[0].name, 'Son')
        self.assertEqual(sons[0].gender, Gender.male)

    def test_get_daughter(self):
        member = Member(5, 'Dummy', 'Male')
        son = Member(6, 'Son', 'Male')
        daughter = Member(7, 'Daughter', 'Female')

        self.assertEqual(member.get_daughter(), [])
        member.children.append(son)
        self.assertEqual(member.get_daughter(), [])
        member.children.append(daughter)
        daughters = member.get_daughter()
        self.assertEqual(len(daughters), 1)
        self.assertEqual(daughters[0].name, 'Daughter')
        self.assertEqual(daughters[0].gender,  Gender.female)

    def test_get_siblings(self):
        member = Member(5, 'Dummy', 'Male')
        mother = Member(6, 'Mother', 'Female')
        son = Member(7, 'Son', 'Male')
        daughter = Member(8, 'Daughter', 'Female')

        self.assertEqual(member.get_siblings(), [])
        member.mother = mother
        self.assertEqual(member.get_siblings(), [])
        mother.children.extend([member, son, daughter])
        member.mother = mother
        siblings = member.get_siblings()
        self.assertEqual(len(siblings), 2)

    @patch('family_tree.member.Member.get_siblings')
    @patch('family_tree.member.Member.get_daughter')
    @patch('family_tree.member.Member.get_son')
    @patch('family_tree.member.Member.get_sister_in_law')
    @patch('family_tree.member.Member.get_brother_in_law')
    @patch('family_tree.member.Member.get_maternal_uncle')
    @patch('family_tree.member.Member.get_maternal_aunt')
    @patch('family_tree.member.Member.get_paternal_uncle')
    @patch('family_tree.member.Member.get_paternal_aunt')
    def test_get_relationship(self, mock_get_paternal_aunt, mock_get_paternal_uncle,
                              mock_get_maternal_aunt, mock_get_maternal_uncle,
                              mock_get_brother_in_law, mock_get_sister_in_law, mock_get_son,
                              mock_get_daughter,
                              mock_get_siblings):

        self.assertEqual(self.member.get_relationship('invalid_relation'), [])

        self.member.get_relationship('paternal_aunt')
        mock_get_paternal_aunt.assert_called_with()

        self.member.get_relationship('paternal_uncle')
        mock_get_paternal_uncle.assert_called_with()

        self.member.get_relationship('maternal_aunt')
        mock_get_maternal_aunt.assert_called_with()

        self.member.get_relationship('maternal_uncle')
        mock_get_maternal_uncle.assert_called_with()

        self.member.get_relationship('brother_in_law')
        mock_get_brother_in_law.assert_called_with()

        self.member.get_relationship('sister_in_law')
        mock_get_sister_in_law.assert_called_with()

        self.member.get_relationship('son')
        mock_get_son.assert_called_with()

        self.member.get_relationship('daughter')
        mock_get_daughter.assert_called_with()

        self.member.get_relationship('siblings')
        mock_get_siblings.assert_called_with()
    
    @patch('family_tree.member.Member.get_siblings', return_value=[
        create_fake_member(
            name="A", gender=Gender.male, spouse=create_fake_member(
                name="B", gender=Gender.female, spouse=create_fake_member(
                    name="A")
            )
        ),
        create_fake_member(
            name="C", gender=Gender.female, spouse=create_fake_member(
                name="D", gender=Gender.male, spouse=create_fake_member(
                    name="C")
            )
        ),
        create_fake_member(
            name="C", gender=Gender.female
        )
    ])
    def test_get_sibling_spouses(self, mock_get_siblings):
        self.assertEqual(len(self.member.get_sibling_spouses()), 0)
    
    def test_get_spouse_siblings(self):
        self.assertEqual(len(self.member.get_spouse_siblings()), 0)
        self.member.spouse = create_fake_member(name="Wife")
        self.member.spouse.get_siblings.return_value = [
            create_fake_member(name="A"),
            create_fake_member(name="B")
        ]
        #self.assertEqual(len(self.member.get_spouse_siblings()), 2)
    
    @patch('family_tree.member.Member.get_spouse_siblings', return_value =
        [
            create_fake_member(name="A", gender = Gender.male),
            create_fake_member(name ="B", gender = Gender.female)
        ]
    )
    @patch('family_tree.member.Member.get_sibling_spouses', return_value =
        [
            create_fake_member(name="C", gender = Gender.male),
            create_fake_member(name="D", gender = Gender.female)
        ])
    def test_get_brother_in_law(self, mock_get_sibling_spouses, mock_get_spouse_siblings):
        self.assertEqual(len(self.member.get_brother_in_law()), 2)
    
    @patch('family_tree.member.Member.get_spouse_siblings', return_value =
        [
            create_fake_member(name="A", gender = Gender.male),
            create_fake_member(name ="B", gender = Gender.female)
        ]
    )
    @patch('family_tree.member.Member.get_sibling_spouses', return_value =
        [
            create_fake_member(name="C", gender = Gender.male),
            create_fake_member(name="D", gender = Gender.female)
        ])
    def test_get_sister_in_law(self, mock_get_sibling_spouses, mock_get_spouse_siblings):
        self.assertEqual(len(self.member.get_brother_in_law()), 2)
