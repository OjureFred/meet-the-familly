from family_tree.family_tree import FamilyTree

class Geektrust:

    def __init__(self):
        self.family_tree = FamilyTree()
    
    def construct_add_child_method_call(self, *args):
        if len(args) > 3 or len(args) < 2:
            return None
        if len(args) == 2:
            return 'self.family_tree.add_child("{}", "{}")'.format(
                args[0],
                args[1]
            )
        return 'self.family_tree.add_child("{}", "{}", "{}")'.format(
            args[1],
            args[2],
            args[0]
        )
    
    def construct_add_spouse_method_call(self, *args):
        if len(args) != 3:
            return None
        return 'self.family_tree.add_spouse("{}", "{}", "{}")'.format(
            args[1],
            args[2],
            args[0]
        )
    
    def construct_get_relationship_method_call(self, *args):
        if len(args) != 2:
            return None
        switch_relationship = {
            'Paternal_Aunt': 'paternal_aunt',
            'Paternal_Uncle': 'paternal_uncle',
            'Maternal_aunt': 'maternal_aunt',
            'Maternal_Uncle': 'maternal_uncle',
            'Brother_in_law': 'brother_in_law',
            'Sister_in_law': 'sister_in_law',
            'Son': 'son',
            'Daughter': 'daughter',
            'Siblings': 'siblings'
        }
        
        relationship_type = switch_relationship.get(args[1], None)
        if not relationship_type:
            return None
        return 'self.family_tree.get_relationship("{}", "{}")'.format(
            args[0],
            args[1]
            
        )
    
    
    def translate(self, filename):
        switch_construct_method = {
            'ADD_CHILD': self.construct_add_child_method_call,
            'ADD_SPOUSE': self.construct_add_spouse_method_call,
            'GET_RELATIONSHIP': self.construct_get_relationship_method_call
        }
        with open(filename, 'r') as fr:
            instructions = fr.readlines()
            for instruction in instructions:
                tokens = instruction.split(" ")
                construct_method = switch_construct_method.get(tokens[0], None)
                if not construct_method:
                    continue
                construct_method(*tuple(tokens[1:]))
    
    def execute(self, instructions):
        results = []
        for instruction in instructions:
            result = eval(instruction)
            if not result:
                continue
            results.append(result)
        return results
    
    def log(self, results):
        for result in results:
            print(result)
    
    def setup(self, filename):
        commands = self.translate(filename)
        self.execute(commands)
    
    def main(self, filename):
        self.setup('./setup.instructions.txt')
        commands = self.translate(filename)
        results = self.execute(commands)
        self.log(results)


if __name__ == '__main__':
    geektrust = Geektrust()
    filename = sys.argv[1]
    geektrust.main(filename)