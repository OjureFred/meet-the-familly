from unittest import TestCase

from family_tree.member import Member, Gender

class TestMember(TestCase):

    def setUp(self):
        self.member = Member(1, 'Azima', 'Male')
        self.mother = Member(2, 'Mother', 'Female')
        self.father = Member(3, 'Dad', 'Male')
        self.mothers_sister_a = Member(4, 'MotherSisterA', 'Female')
        self.mothers_sister_b = Member(5, 'MotherSisterB', 'Female')
        self.mothers_brother_a = Member(6, 'MotherBrotherA', 'Male')
        self.mothers_brother_b = Member(7, 'MotherBrotherB', 'Male')
        self.fathers_sister_a = Member(8,'FatherSisterA', 'Female')
        self.fathers_sister_b = Member(9, 'FatherSisterB', 'Female')
        self.fathers_brother_a = Member(10, 'FatherBrotherA', 'Male')
        self.fathers_brother_b = Member(11, 'FatherBrotherB', 'Male')
        self.spouse = Member(12, 'Wife', 'Female')
        self.brother_a = Member(13, 'BrotherA', 'Male')
        self.brother_b  = Member(14, 'BrotherB', 'Male')
        self.sister_a = Member(15, 'SisterA', 'Female')
        self.sister_b = Member(16, 'SisterB', 'Female')
        self.son_a = Member(17, 'SonA', 'Male')
        self.son_b = Member(18, 'SonB', 'Male')
        self.daughter_a = Member(19, 'DaughterA', 'Female')
        self.daughter_b = Member(20, 'DaughterB', 'Female')
        self.paternal_grandmother = Member(21, 'PaternalGrandmother', 'Female')
        self.maternal_grandmother = Member(22, 'MaternalGrandmother', 'Female')


        #setup relationships

        #adding our parents
        self.member.set_mother(self.mother)
        self.member.set_father(self.father)

        #adding our siblings
        self.father.add_child(self.brother_a)
        self.father.add_child(self.brother_b)
        self.father.add_child(self.sister_a)
        self.father.add_child(self.sister_b)
        self.mother.add_child(self.brother_a)
        self.mother.add_child(self.brother_b)
        self.mother.add_child(self.sister_a)
        self.mother.add_child(self.sister_b)
        self.father.add_child(self.member)
        self.mother.add_child(self.member)

        #Add spouse
        self.member.set_spouse(self.spouse)
        self.spouse.set_spouse(self.member)

        #Add our paternal aunts and uncles
        self.paternal_grandmother.add_child(self.fathers_sister_a)
        self.paternal_grandmother.add_child(self.fathers_sister_b)
        self.paternal_grandmother.add_child(self.fathers_brother_a)
        self.paternal_grandmother.add_child(self.fathers_brother_b)
        self.paternal_grandmother.add_child(self.father)
        self.father.set_mother(self.paternal_grandmother)

        #Adding maternal aunts and uncles
        self.maternal_grandmother.add_child(self.mothers_sister_a)
        self.maternal_grandmother.add_child(self.mothers_sister_b)
        self.maternal_grandmother.add_child(self.mothers_brother_a)
        self.maternal_grandmother.add_child(self.mothers_brother_b)
        self.maternal_grandmother.add_child(self.mother)
        self.mother.set_mother(self.maternal_grandmother)

        #Adding our sons and daughters
        self.member.add_child(self.son_a)
        self.member.add_child(self.son_b)
        self.member.add_child(self.daughter_a)
        self.member.add_child(self.daughter_b)



    
    def test_setter_methods(self):
        
        #Test parents
        self.assertEqual(self.member.mother.name, 'Mother')
        self.assertEqual(self.member.father.name, 'Dad')
        self.assertEqual(self.member in self.member.father.children, True)
        self.assertEqual(self.member in self.member.mother.children, True)

        #Test siblings
        self.assertEqual(len(self.member.mother.children), 5)
        self.assertEqual(self.brother_a in self.member.mother.children, True)
        self.assertEqual(self.brother_b in self.member.mother.children, True)
        self.assertEqual(self.sister_a in self.member.mother.children, True)
        self.assertEqual(self.sister_a in self.member.mother.children, True)
        self.assertEqual(len(self.member.mother.children), 5)
        self.assertEqual(self.brother_a in self.member.father.children, True)
        self.assertEqual(self.brother_b in self.member.father.children, True)
        self.assertEqual(self.sister_a in self.member.father.children, True)
        self.assertEqual(self.sister_a in self.member.father.children, True)

        #Test spouse
        self.assertEqual(self.member.spouse.name, 'Wife')

        #Test both paternal and maternal aunts and uncles
        self.assertEqual(len(self.member.mother.mother.children), 5)
        self.assertEqual(self.mothers_brother_a in self.member.mother.mother.children, True)
        self.assertEqual(self.mothers_brother_b in self.member.mother.mother.children, True)
        self.assertEqual(self.mothers_sister_a in self.member.mother.mother.children, True)
        self.assertEqual(self.mothers_sister_a in self.member.mother.mother.children, True)
        self.assertEqual(len(self.member.father.mother.children), 5)
        self.assertEqual(self.fathers_brother_a in self.member.father.mother.children, True)
        self.assertEqual(self.fathers_brother_b in self.member.father.mother.children, True)
        self.assertEqual(self.fathers_sister_a in self.member.father.mother.children, True)
        self.assertEqual(self.fathers_sister_a in self.member.father.mother.children, True)
    
    def test_get_relationship_methods(self):
        self.assertEqual(len(self.member.get_relationship('paternal_aunt')), 2)
        self.assertEqual(len(self.member.get_relationship('paternal_uncle')), 2)
        self.assertEqual(len(self.member.get_relationship('maternal_aunt')), 2)
        self.assertEqual(len(self.member.get_relationship('maternal_uncle')), 2)
        self.assertEqual(len(self.member.get_relationship('siblings')), 4)
        self.assertEqual(len(self.member.get_relationship('son')), 2)
        self.assertEqual(len(self.member.get_relationship('daughter')), 2)
        self.assertEqual(len(self.member.spouse.get_relationship('brother_in_law')), 2)
        self.assertEqual(len(self.member.spouse.get_relationship('sister_in_law')), 2)
