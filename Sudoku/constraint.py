class Constraint:
    def __init__(self, variables: set):
        if len(variables) != 9:
            raise Exception("not enough variables to create a constraint")
        
        self.variables = variables

    def is_satisfied(self, assignment: dict) -> bool:
        currently_assigned = [var for var in self.variables if var in assignment]
        
        for var1 in currently_assigned:
            for var2 in currently_assigned:
                
                if var1 == var2:
                    continue
                
                if assignment[var1] == assignment[var2]:
                    return False
                
        return True
    
