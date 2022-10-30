class FamilyTree:

    def __init__(self):
        self.family_tree = {}
    

    
    def add_child(self):
        return 'CHILD_ADDITION_SUCCEEDED'
    
    def add_spouse(self):
        return 'SPOUSE_ADDITION_SUCCEEDED'
    
    def get_relationship(self):
        return 'NONE'


class Geektrust:

    def __init__(self):
        self.family_tree = FamilyTree()
    
    def translate(self, filename):
        with open(filename, 'r') as fr:
            instructions = fr.readlines()


if __name__ == '__main__':
    print('Hello Geektrust')