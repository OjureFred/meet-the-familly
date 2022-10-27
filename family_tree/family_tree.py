from family_tree.member import Member, Gender

class FamilyTree:

    def __init__(self):
        self.family_tree = {}
    
    def add_child(self, name, gender, mother_name):
        _id = len(self.family_tree.keys()) + 1
        member = Member(_id, name, gender)
        if not self.family_tree:
            self.family_tree[name] = member
            return 'CHILD_ADDITION_SUCCEEDED'
        
        if name in self.family_tree:
            return 'CHILD_ADDITION_FAILED'
        
        mother = self.family_tree.get(mother_name, None)
        if not mother:
            return 'PERSON_NOT_FOUND'
        
        if  mother.gender != Gender.female:
            return 'CHILD_ADDITION_FAILED'
        
        father = mother.spouse
        if not father:
            return 'CHILD_ADDITION_FAILED'

        try:
            member.set_mother(mother)
            member.set_father(father)
            self.family_tree[mother_name].add_child(member)
            self.family_tree[father.name].add_child(member)
            self.family_tree[name] = member
            return 'CHILD_ADDITION_SUCCEEDED'
        except valueError:
            return 'CHILD_ADDITION_FAILED'
    
    def add_spouse(self, name, gender, spouse_name):
        _id = len(self.family_tree.keys()) + 1
        member = Member(_id, name, gender)
        if not self.family_tree:
            return 'SPOUSE_ADDITION_FAILED'
        
        if name in self.family_tree:
            return 'SPOUSE_ADDITION_FAILED'
        
        spouse = self.family_tree.get(spouse_name, None)
        if not spouse:
            return 'PERSON_NOT_FOUND'
        if spouse.gender == member.gender:
            return 'SPOUSE_ADDITION_FAILED'
        if spouse.spouse is not None:
            return 'SPOUSE_ADDITION_FAILED'
        
        try:
            member.set_spouse(self.family_tree[spouse_name])
            self.family_tree[spouse_name] = member
            self.family_tree[name] = member
            return 'SPOUSE_ADDITION_SUCCEEDED'
        except valueError:
            return 'SPOUSE_ADDITION_FAILED'