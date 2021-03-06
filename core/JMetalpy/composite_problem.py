
import threading

from enum import Enum, unique

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import core.JMetalpy.composite_solution as CS

                  
from core.problem_parameters import *
from core.evaluator import Evaluator
from core.null import NullSolution

import util.string_utils as su
import util.arg_parsing as AP
from util.type_check import is_integer, to_integer


"""
    TODO:
        -Make variables typechecking work without using classes __name__ attr.
"""

@unique
class ARGS_MODES(Enum):
    NORMAL=0
    KEYWORD=1
    UNPACKED=2



class CompositeProblem(jprob.Problem[CS.CompositeSolution], ABC):
        
    def __init__(self,
                 evaluator: Evaluator,
                 problem_parameters: ProblemParameters):
        
        if len(problem_parameters.variables) < 1:
            raise ValueError( "%s.__init__(): at least one variable needed" % (type(self).__name__) )
            
        self.problem_parameters = problem_parameters
        self.evaluator = evaluator
        self.number_of_objectives = evaluator.number_of_objectives
        
        self.variables = { var.keyword:var for var in self.problem_parameters.variables }
        self.constants = { const.keyword:const for const in self.problem_parameters.constants }
        
        self.float_count = 0
        self.integer_count = 0
        self.binary_count = 0
        self.permutation_solution_count = 0
        
        self.float_lower_bounds = []
        self.float_upper_bounds = []
        
        self.integer_lower_bounds = []
        self.integer_upper_bounds = []
        
        self.permutations = []
        
        var_args = self._compile_call_arguments()
        
        # print(var_args)
        
        self.included_variables_dict = {}
        self.argument_list = []
        
        for argument in var_args:
            
            if argument[0] in self.variables:
                """ Format: (Var, index, Mode [, keyword]) """
                
                var = self.variables[argument[0]]
                
                if var not in self.included_variables_dict:
                
                    if type(var) == FloatVectorVariable:
                        index = (self.float_count,self.float_count+var.length)
                        self.float_count += var.length
                        self.float_lower_bounds.extend( [var.lower_bound]*var.length )
                        self.float_upper_bounds.extend( [var.upper_bound]*var.length )
                        
                    elif type(var) == FloatVariable:
                        index = (self.float_count,self.float_count+1)
                        self.float_count += 1
                        self.float_lower_bounds.append(var.lower_bound)
                        self.float_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == IntegerVectorVariable:
                        index = (self.integer_count, self.integer_count+var.length)
                        self.integer_count += var.length
                        self.integer_lower_bounds.extend( [var.lower_bound]*var.length )
                        self.integer_upper_bounds.extend( [var.upper_bound]*var.length )
                        
                    elif type(var) == DiscretizedVectorVariable:
                        index = (self.integer_count, self.integer_count+var.length)
                        self.integer_count += var.length
                        self.integer_lower_bounds.extend( [0]*var.length )
                        self.integer_upper_bounds.extend( [var.resolution]*var.length )
                        
                    elif type(var) == IntegerVariable:
                        index = (self.integer_count,self.integer_count+1)
                        self.integer_count += 1
                        self.integer_lower_bounds.append(var.lower_bound)
                        self.integer_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == DiscretizedFloatVariable:
                        index = (self.integer_count,self.integer_count+1)
                        self.integer_count += 1
                        self.integer_lower_bounds.append(0)
                        self.integer_upper_bounds.append(var.resolution)
                        
                    elif isinstance(var,BinaryVariable) or isinstance(var,BooleanVariable):
                        index = (self.binary_count,self.binary_count+1)
                        self.binary_count += 1
                        
                    # elif type(var) == BinaryVectorVariable or type(var) == BooleanVectorVariable:
                    elif isinstance(var,BinaryVectorVariable) or isinstance(var,BooleanVectorVariable):
                    # elif type(var).__name__ == BinaryVectorVariable.__name__ or type(var).__name__ == BooleanVectorVariable.__name__:
                        index = (self.binary_count,self.binary_count+var.length)
                        self.binary_count += var.length
                        
                    elif type(var) == PermutationVariable:
                        index = self.permutation_solution_count
                        self.permutation_solution_count += 1
                        self.permutations.append( var.elements )
                        
                    else:
                        raise Exception( "%s.__init__(): Variable of unsuitable type: %s" % (type(self).__name__,type(var)) )
                    
                    self.included_variables_dict[var] = index
                    
                else:
                    index = self.included_variables_dict[var]
                    
                if argument[1] is ARGS_MODES.KEYWORD:
                    self.argument_list.append( (var, index, argument[1], argument[2]) )
                
                else:
                    self.argument_list.append( (var, index, argument[1]) )
                    
            
            elif argument[0] in self.constants:
                """ Format: (Var, Mode [, keyword]) """
                if argument[1] is ARGS_MODES.KEYWORD:
                    self.argument_list.append( (self.constants[argument[0]], argument[1], argument[2]) )
                    
                else:
                    self.argument_list.append( (self.constants[argument[0]], argument[1]) )
                
            
            else:
                raise Exception("CompositeProblem.__init__(): wrong argument '%'" % (argument[0]))
        
        # Coeffiecients in {-1,1} to transform minimization problems to maximization
        self.objective_transformation_vector = [ int(boolean)*2 - 1 for boolean in self.problem_parameters.options["objectives_minimize"] ]
        
        self.solution_shape = ( self.float_count, self.integer_count, self.binary_count, self.permutation_solution_count )
        
        self.include_float = self.float_count > 0
        self.include_integer = self.integer_count > 0
        self.include_binary = self.binary_count > 0
        self.include_permutation = self.permutation_solution_count > 0
        
        
        if (len(self.problem_parameters.variables) + len(self.problem_parameters.constants)) != evaluator.number_of_variables:
            raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
        
        self.evaluations_lock = threading.Lock()
        self.evaluations = 0
        
        

    def _generate_args( self, solution: CS.CompositeSolution ):
        
        args = []
        kwargs = {}
        
        for arg in self.argument_list:
            
            if isinstance(arg[0], Constant):
                
                if arg[1] is ARGS_MODES.NORMAL:
                    args.append( arg[0].value )
                
                elif arg[1] is ARGS_MODES.KEYWORD:
                    kwargs[arg[-1]] = arg[0].value
                    
                elif arg[1] is ARGS_MODES.UNPACKED:
                    args.extend( arg[0].value )
                    
                else:
                    raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                    
            elif isinstance(arg[0], Variable):
                
                if type(arg[0]) == FloatVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]]
                    
                elif type(arg[0]) == FloatVectorVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == IntegerVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == IntegerVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                    
                elif type(arg[0]) == DiscretizedFloatVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]    
                    value = arg[0].to_float( value )
                    
                elif type(arg[0]) == DiscretizedVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                    value = arg[0].to_float( value )
                
                elif type(arg[0]) == BinaryVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]]
                    value = int(value)
                    
                elif type(arg[0]) == BinaryVectorVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]:arg[1][1]]
                    value = [ int(bit) for bit in value ]
                    
                elif type(arg[0]) == BooleanVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]]
                    
                elif type(arg[0]) == BooleanVectorVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == PermutationVariable:
                    value = solution.permutation_solutions[arg[1][0]].variables
                    
                    
                if arg[2] is ARGS_MODES.NORMAL:
                    args.append( value )
                
                elif arg[2] is ARGS_MODES.KEYWORD:
                    kwargs[arg[-1]] = value
                    
                elif arg[2] is ARGS_MODES.UNPACKED:
                    args.extend( value )
                    
                else:
                    # raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                    raise ValueError("%s._generate_args(): invalid arg type" % (type(self).__name__))
                
            else:
                raise ValueError("%s._generate_args(): invalid symbol type: %s" % (type(self).__name__, type(arg[0])))
                
                
                
        return args, kwargs

    def _compile_call_arguments(self):
        
        arg_string = su.remove_whitespaces( self.problem_parameters.options["call_args"] )
        arg_tokens = arg_string.split(',')
        
        arg_list = []
        
        for token in arg_tokens:
            
            ret = AP.token_is_kwarg(token)    
            
            if ret != None:
                arg_list.append( (ret[1],ARGS_MODES.KEYWORD,ret[0]) )
                
            else:
                ret = AP.token_is_unpacked_arg(token)
                
                if ret!=None:
                    arg_list.append( (ret,ARGS_MODES.UNPACKED) )
                        
                else:
                    if AP.token_is_arg(token):
                        arg_list.append( (token,ARGS_MODES.NORMAL) )

        return arg_list
    

    def create_solution(self) -> jsol.CompositeSolution:
        
        kwargs = {}
        
        if self.solution_shape[0] > 0: # Floats
            temp_solution = jsol.FloatSolution(lower_bound=self.float_lower_bounds, upper_bound=self.float_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ random.uniform(lower, upper) for lower, upper in zip(self.float_lower_bounds, self.float_upper_bounds) ]
            kwargs["float_solutions"] = [temp_solution]
        
        if self.solution_shape[1] > 0: # Integers
            temp_solution = jsol.IntegerSolution(lower_bound=self.integer_lower_bounds, upper_bound=self.integer_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ random.uniform(lower, upper) for lower, upper in zip(self.integer_lower_bounds, self.integer_upper_bounds) ]
            kwargs["integer_solutions"] = [temp_solution]
            
        if self.solution_shape[2] > 0: # Binary
            temp_solution = jsol.BinarySolution( number_of_variables=1, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [[ bool(random.getrandbits(1)) for i in range(self.solution_shape[2]) ]]
            kwargs["binary_solutions"] = [temp_solution]
            
        if self.solution_shape[3] > 0: # Permutation
        
            permutation_solutions = []
        
            for permutation in self.permutations:
                temp_solution = jsol.PermutationSolution(number_of_objectives=self.number_of_objectives, number_of_constraints=0 )    
                temp_solution.variables = random.shuffle( permutation )
                permutation_solutions.append( temp_solution )
                
            
            kwargs["permutation_solutions"] = permutation_solutions
        
        # print(kwargs)
        
        return CS.CompositeSolution( number_of_objectives=to_integer(self.problem_parameters.options["objectives"]),
                                     number_of_constraints=to_integer(self.problem_parameters.options["constraints"]),
                                     **kwargs )
    
    
    
    def evaluate( self, solution: jsol.CompositeSolution):
        
        args, kwargs = self._generate_args(solution)
        # solution.objectives = self.evaluator.evaluate( *args, **kwargs )
        solution.objectives = [ coefficient*objective for objective, coefficient in zip(self.evaluator.evaluate( *args, **kwargs ),self.objective_transformation_vector) ]
        
        with self.evaluations_lock:
            self.evaluations += 1
        
        return solution
    
    def recover_variables( self, solution: jsol.CompositeSolution ):
        
        variables_list = []
        variables_dictionary = {}
        
        for arg in self.argument_list:
                    
            if isinstance(arg[0], Variable):
                
                if type(arg[0]) == FloatVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]]
                    
                elif type(arg[0]) == FloatVectorVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == IntegerVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == IntegerVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                    
                elif type(arg[0]) == DiscretizedFloatVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]    
                    value = arg[0].to_float( value )
                    
                elif type(arg[0]) == DiscretizedVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                    value = arg[0].to_float( value )
                
                elif type(arg[0]) == BinaryVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]]
                    value = int(value)
                    
                elif type(arg[0]) == BinaryVectorVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]:arg[1][1]]
                    value = [ int(bit) for bit in value ]
                    
                elif type(arg[0]) == BooleanVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]]
                    
                elif type(arg[0]) == BooleanVectorVariable:
                    value = solution.binary_solutions[0].variables[0][arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == PermutationVariable:
                    value = solution.permutation_solutions[arg[1][0]].variables
                    
                else:
                    raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                    
                var = ( arg[0], value )
                variables_list.append( var )
                variables_dictionary[arg[0].keyword] = var
                objectives_list = [ coefficient*objective for coefficient, objective in zip(self.objective_transformation_vector, solution.objectives) ]
                
            elif isinstance(arg[0], Constant):
                pass
                
            else:
                raise ValueError("_generate_args(): invalid symbol type: %s" % (type(arg[0])))
                
        
        return (variables_list, variables_dictionary, objectives_list)
    
    def get_name(self):
        return "CompositeProblem"
        