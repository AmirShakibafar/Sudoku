from icecream import ic
from copy import deepcopy
from constraint import Constraint
import random

class Sudoku:
    def __init__(self,  difficulty, board=[[-1 for i in range(9)] for j in range(9)]):
        self.difficulty = difficulty
        self.board = deepcopy(board)
        self.variables: set = set([f"{x},{y}"  for x in range(9) for y in range(9)])
        self.domains: dict = {}
        self.constraints: dict = {}
        random.seed()
        for var in self.variables:
            self.domains[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(self.domains[var])
            
            self.constraints[var] = []
        
        self.initilizing_constraints()
        self.playable_board, self.playing_assignmnet = self.get_playable_board(difficulty)

    def add_constraint(self, constraint: Constraint):
        for var in constraint.variables:
            self.constraints[var].append(constraint) 
    
    def initilizing_constraints(self):
        for i in range(9):
            # Row constraints
            constraint = Constraint([f"{i},{j}" for j in range(9)])
            self.add_constraint(constraint)
            # Column constraints
            constraint = Constraint([f"{j},{i}" for j in range(9)])
            self.add_constraint(constraint)

        # Subgrid constraints
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                constraint = Constraint([f"{i+k},{j+l}" for k in range(3) for l in range(3)])
                self.add_constraint(constraint)      
                      
    def are_we_good(self, var, assignment) -> bool:
        for constraint in self.constraints[var]:
            if not constraint.is_satisfied(assignment):
                return False
            
        return True
    
    def MRV(self, assignment):
        unassigned_variables = [var for var in self.variables if var not in assignment]
        random.shuffle(unassigned_variables)
        mrv = unassigned_variables[0]
        for var in unassigned_variables:
    
            if len(self.domains[mrv]) > len(self.domains[var]):
                mrv = var
        
            if len(self.domains[mrv]) == 1:
                return mrv
        return mrv
    
    def initial_domain_reduction(self, assignment):
        for var in assignment.keys():
            self.decrease_neighbor_domains(var, assignment[var])
        
    def decrease_neighbor_domains(self, var1, value):
        for constraint in self.constraints[var1]:
            for var2 in constraint.variables:
                if var1 == var2:
                    continue
                domains = deepcopy(self.domains[var2])
                
                if value in self.domains[var2]:
                    domains.remove(value)
                
                self.domains[var2] = domains
                    
    def forward_checking(self, var, value, assignment):
        original_domains = deepcopy(self.domains)
        self.decrease_neighbor_domains(var, value)
        for constraint in self.constraints[var]:
            for neighbor in constraint.variables:
                # checks to see if we already have any value for unassigned variables
                if neighbor not in assignment and not self.domains[neighbor]:
                    self.domains = original_domains
                    return False
        return True
    
    def backtracking_search(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        # choosing what to assign next
        variable = self.MRV(assignment)
        for value in self.domains[variable]:
            local_assignment = deepcopy(assignment)
            local_assignment[variable] = value
            if self.are_we_good(variable, local_assignment):
                original_domains = deepcopy(self.domains)
                if self.forward_checking(variable, value, local_assignment):
                    result = self.backtracking_search(local_assignment)
                    if result is not None:
                        return result
                    self.domains = deepcopy(original_domains)
                
                
        return None
    
    def get_partial_assignment(self):
        # checks for already assigned variables
        assignment = {} 
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != -1:
                    assignment[f"{i},{j}"] = self.board[i][j]
        return assignment 
    
    def run(self):
        partial_assignment = self.get_partial_assignment()
        self.initial_domain_reduction(partial_assignment)
        assignment = self.backtracking_search(partial_assignment)
        return assignment
    
    def get_random_variable(self, assignmnet):
        random_key = random.choice(list(assignmnet.keys()))
        return random_key
        
    def generate_random_assignment(self, number_of_visible_squares):
        assignment = self.run()
        self.update_final_board(assignment)
        visible_squares: dict = {}
        for _ in range(number_of_visible_squares):
            random_key = self.get_random_variable(assignment)
            visible_squares[random_key] = assignment[random_key]
        return visible_squares
    
    
    def return_playable_board(self, assignment):
        board = [[-1 for i in range(9)] for j in range(9)]
        if not assignment:
            return False
        for var in assignment.keys():
            var_index = var.split(",")
            i = int(var_index[0])
            j = int(var_index[1])
            board[i][j] = assignment[var]
        return board
    
    def get_playable_board(self, difficulty):
        if difficulty == 1:
            assignment = self.generate_random_assignment(75)
        elif difficulty == 2:
            assignment = self.generate_random_assignment(50)
        else:
            assignment = self.generate_random_assignment(25)
            
        return self.return_playable_board(assignment), assignment
    
    def remove_from_playing_assignmnet(self, row, col):
        if f"{row},{col}" in self.playing_assignmnet:
            del self.playing_assignmnet[f"{row},{col}"]
        
    def place_number_on_board(self, row, col, number):
        self.playable_board[row][col] = number
        self.playing_assignmnet[f"{row},{col}"] = number
        if self.are_we_good(var=f"{row},{col}", assignment=self.playing_assignmnet):
            return True
        return False
    
    def check_finished(self):
        if len(self.playing_assignmnet) == 81:
            for var in self.playing_assignmnet:
                if not self.are_we_good(var, self.playing_assignmnet):
                    return False
            return True
        return False
      
    def update_final_board(self, assignment):
        if not assignment:
            return False
        for var in assignment.keys():
            var_index = var.split(",")
            i = int(var_index[0])
            j = int(var_index[1])
            self.board[i][j] = assignment[var]
    


    
    