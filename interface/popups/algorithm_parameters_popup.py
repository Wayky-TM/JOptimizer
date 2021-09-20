# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 13:43:33 2021

@author: Wayky
"""

import sys
sys.path.append(r"./../..")

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter.ttk import Notebook
    from tkinter import messagebox    
    from tkinter import scrolledtext
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2


from win32api import GetSystemMetrics
from collections import defaultdict

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float


"""
    Window for algorithm parameter specification
"""
def algorithm_parameters_popup( controller: tk.Tk,
                                algorithm_parameters: AlgorithmParameters,
                                problem_parameters: ProblemParameters ):   
    
    # Variables for automatic spacing & scaling
    first_col_anchor_offset = 0.05
    second_col_anchor_offset = 0.45
    vertical_anchor_offset = 0.07
    vertical_spacing = 0.25
    
    error_hor_anchor = first_col_anchor_offset
    error_vert_anchor = 0.82
    error_vert_spacing = 0.1

    var_types = { type(x) for x in problem_parameters.variables }   

    def save_close():
        
        nonlocal error_textbox
        
        error_textbox.config(state=NORMAL)
        error_textbox.delete('1.0', END)
        error_textbox.config(state=DISABLED)
        
        error_list = []
        
        algorithm = optionAlgorithm.get()
        population_size = entry_popsize.get()

        """
            Saving correct values
        """
        
        # Algorithm
        algorithm_parameters.choice = algorithm

        # Population size
        if not is_integer(population_size) or int(population_size)<1:
            error_list.append( "Parameter 'Population size' must be a positive, non-zero integer" )
        else:
            algorithm_parameters.general_parameters["population_size"] = population_size
            
        
        # Crossover operator
        if variable_types.FloatVariable in var_types:    
            
            # Crossover
            if fOptionCrossover.get() == AlgorithmParameters.FLOAT_CROSSOVER.SBX:
                if not is_float(fCrossoverParams["probability"].get()) or (float(fCrossoverParams["probability"].get())<0.0 or float(fCrossoverParams["probability"].get())>1.0):
                    error_list.append( "Crossover parameter 'Probability' for float variables must be a real number in [0,1]" )
                    
                if not is_float(fCrossoverParams["distribution_index"].get()) or (float(fCrossoverParams["distribution_index"].get())<0.0):
                    error_list.append( "Crossover parameter 'Distribution index' for float variables must be a positive real number" )
                    
            elif fOptionCrossover.get() == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION:
                if not is_float(fCrossoverParams["probability"].get()) or (float(fCrossoverParams["probability"].get())<0.0 or float(fCrossoverParams["CR"].get())>1.0):
                    error_list.append( "Crossover parameter 'CR' for float variables must be a real number in [0,1]" )
                    
                if not is_float(fCrossoverParams["F"].get()):
                    error_list.append( "Crossover parameter 'F' for float variables must be a real number" )
                    
            # Mutation
            if not is_float(fMutationParams["probability"].get()) or (float(fMutationParams["probability"].get())<0.0 or float(fMutationParams["probability"].get())>1.0):
                error_list.append( "Mutation parameter 'Probability' for float variables must be a real number in [0,1]" )
                    
            if fOptionMutation.get() == AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL:
                if not is_float(fMutationParams["distribution_index"].get()) or float(fMutationParams["distribution_index"].get())<0.0:
                    error_list.append( "Mutation parameter 'Distribution index' for float variables must be a positive real number" )
                    
            elif fOptionMutation.get() == AlgorithmParameters.FLOAT_MUTATION.UNIFORM:
                if not is_float(fMutationParams["perturbation"].get()):
                    error_list.append( "Mutation parameter 'Perturbation' for float variables must be a real number" )
            
            elif fOptionMutation.get() == AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM:
                if not is_float(fMutationParams["perturbation"].get()):
                    error_list.append( "Mutation parameter 'Perturbation' for float variables must be a real number" )
                    
                if not is_float(fMutationParams["max_iterations"].get()) or float(fMutationParams["max_iterations"].get())<0.0:
                    error_list.append( "Mutation parameter 'Max. iterations' for float variables must be a positive real number" )
                
            if len(error_list)==0:
                algorithm_parameters.float_crossover_choice = fOptionCrossover.get()
                algorithm_parameters.float_mutation_choice = fOptionMutation.get()
                
                for key,widget in fCrossoverParams.items():
                    algorithm_parameters.float_crossover_parameters[key] = widget.get()
                    
                for key,widget in fMutationParams.items():
                    algorithm_parameters.float_mutation_parameters[key] = widget.get()
            
            
        if variable_types.IntegerVariable in var_types or variable_types.DiscretizedFloatVariable in var_types:
            
            if not is_float(iCrossoverParams["probability"].get()) or (float(iCrossoverParams["probability"].get())<0.0 or float(iCrossoverParams["probability"].get())>1.0):
                error_list.append( "Crossover parameter 'Probability' for integer variables must be a real value in [0,1]" )
                
            if not is_float(iCrossoverParams["distribution_index"].get()) or (float(iCrossoverParams["distribution_index"].get())<0.0):
                error_list.append( "Crossover parameter 'Distribution index' for integer variables must be a positive real number" )
                
            if not is_float(iMutationParams["probability"].get()) or (float(iMutationParams["probability"].get())<0.0 or float(iMutationParams["probability"].get())>1.0):
                error_list.append( "Mutation parameter 'Probability' for integer variables must be a real value in [0,1]" )
                
            if not is_float(iMutationParams["distribution_index"].get()) or (float(iMutationParams["distribution_index"].get())<0.0):
                error_list.append( "Mutation parameter 'Distribution index' for integer variables must be a positive real number" )
                
            if len(error_list)==0:
                algorithm_parameters.int_crossover_choice = iOptionCrossover.get()
                algorithm_parameters.int_mutation_choice = iOptionMutation.get()
            
                for key,widget in iCrossoverParams.items():
                    algorithm_parameters.int_crossover_parameters[key] = widget.get()
            
                for key,widget in iMutationParams.items():
                    algorithm_parameters.int_mutation_parameters[key] = widget.get()
                
        
        if variable_types.BinaryVariable in var_types:
            
            if not is_float(bCrossoverParams["probability"].get()) or (float(bCrossoverParams["probability"].get())<0.0 or float(bCrossoverParams["probability"].get())>1.0):
                error_list.append( "Crossover parameter 'Probability' for binary variables must be a real value in [0,1]" )
            
            if not is_float(bMutationParams["probability"].get()) or (float(bMutationParams["probability"].get())<0.0 or float(bMutationParams["probability"].get())>1.0):
                error_list.append( "Mutation parameter 'Probability' for binary variables must be a real value in [0,1]" )
            
            if len(error_list)==0:
                algorithm_parameters.binary_crossover_choice = bOptionCrossover.get()
                algorithm_parameters.binary_mutation_choice = bOptionMutation.get()
                
                for key,widget in bCrossoverParams.items():
                        algorithm_parameters.binary_crossover_parameters[key] = widget.get()
                        
                for key,widget in bMutationParams.items():
                        algorithm_parameters.binary_mutation_parameters[key] = widget.get()
        
        if variable_types.PermutationVariable in var_types:
            #TODO
            pass
            
        """
            Algorithm-specific error checking
        """
        
        if algorithm in [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO, AlgorithmParameters.SUPPORTED_ALGORITHMS.MOCELL]:
            
            if optionSelection.get() == AlgorithmParameters.SELECTION.NARY_RANDOM:
                if not is_integer(selectionWidgetsEntries["number_of_solutions"].get()) or int(selectionWidgetsEntries["number_of_solutions"].get())<1:
                    error_list.append( "Selection parameter 'Number of solutions' must be a positive, non-zero integer" )
            
            if optionSelection.get() == AlgorithmParameters.SELECTION.RANKING_AND_CROWDING:
                if not is_integer(selectionWidgetsEntries["max_population_size"].get()) or int(selectionWidgetsEntries["max_population_size"].get())<1:
                    error_list.append( "Selection parameter 'Max. population size' must be a positive, non-zero integer" )
            
            if len(error_list)==0:
                algorithm_parameters.selection_choice = optionSelection.get()
                
                for key,widget in selectionWidgetsEntries.items():
                    algorithm_parameters.selection_parameters[key] = widget.get()
                
        
        if algorithm in [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO]:
            
            # Offspring size
            offspring_size = offspringSize.get()
            
            if not is_integer(offspring_size) or int(offspring_size)<1:
                error_list.append( "Parameter 'Offspring size' must be a positive, non-zero integer" )
            else:
                algorithm_parameters.general_parameters["offspring_size"] = offspringSize.get()
            
        elif algorithm == AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD:
            
            # Aggregation function
            algorithm_parameters.specific_options["aggregative"] = aggregationOption.get()
            
            # TODO: check aggregation parameters' correctness
            for key,value in aggregationParams.items():
                algorithm_parameters.specific_parameters["aggregative"][key] = value.get()
            
            # Neighborhood size
            neighborhood_size = neighborhoodSize.get()
            
            if not is_integer(neighborhood_size) or int(neighborhood_size)<1:
                error_list.append( "Parameter 'Neighborhood size' must be a positive, non-zero integer" )
            else:
                algorithm_parameters.specific_options["neighborhood_size"] = neighborhood_size
                
            # Neighborhood sel. prob.
            neighborhood_sel_prob = neighborhoodSelProb.get()
            
            if not is_float(neighborhood_sel_prob) or float(neighborhood_sel_prob) < 0:
                error_list.append( "Parameter 'Neighborhood selection prob.' takes a positive real value" )
            else:
                algorithm_parameters.specific_options["neighborhood_selection_probability"] = neighborhood_sel_prob
            
            # Max. of n replaced
            max_of_n_replaced = maxOfNReplaced.get()
            
            if not is_integer(max_of_n_replaced) or int(max_of_n_replaced)<1:
                error_list.append( "Parameter 'Max. replaced' must be a positive, non-zero integer" )
            else:
                algorithm_parameters.specific_options["max_number_of_replaced_solutions"] = max_of_n_replaced
            
            # Weight files path
            if not weightFilesPath.get():
                error_list.append( "Select a folder for weight files" )
            else:
                #TODO: Proper path error checking
                algorithm_parameters.specific_options["weight_files_path"] = weightFilesPath.get()
            
        elif algorithm == AlgorithmParameters.SUPPORTED_ALGORITHMS.MOCELL:
            
            # TODO: check errors in parameters' values
            algorithm_parameters.specific_options["archive"] = archiveOption.get()
            
            for key,value in archiveParams.items():
                algorithm_parameters.specific_paramaters["archive"][key] = value.get()
            
            algorithm_parameters.specific_options["neighborhood"] = neighborhoodOption.get()
            
            for key,value in neighborhoodParams.items():
                algorithm_parameters.specific_parameters["neighborhood"][key] = value.get()
                
                
        
        if (len(error_list) == 0):
            win.destroy()
            
        else:
            error_textbox.config(state=NORMAL)
            
            for warning in error_list:
                error_textbox.insert(END, "-" + warning + "\n", 'error_warning')
                
            error_textbox.tag_config('error_warning', foreground='red')
            error_textbox.config(state=DISABLED)


    def _update_frames(selection):
        
        nonlocal labelframe_operators
        nonlocal labelframe_evol
        
        def _browse_weights(): 
            nonlocal weightFilesPath
            
            path = filedialog.askdirectory(initialdir = "C:\Program Files (x86)\CST Studio Suite 2020\AMD64\python_cst_libraries",
                                                      title = "Select a Folder")
            
            weightFilesPath.config(state=tk.NORMAL)
            weightFilesPath.insert( 0, path )
            weightFilesPath.config(state="readonly")
            
        def _evolutionary_parameters():
            pass
            
        
        def _GA_parameters():
            nonlocal optionSelection
            nonlocal selectionParams
            # nonlocal optionCrossover
            # nonlocal crossoverParams
            # nonlocal optionMutation
            # nonlocal mutationParams
            nonlocal offspringSize
            
            nonlocal labelframe_operators
            
            labelframe_operators.place_forget()
            
            # Show 'offspring' widgets
            offspringText.place(relx=0.45,rely=0.07)
            offspringSize.place(relx=0.61, rely=0.07, relwidth=0.15)
            
            # Show Selection parameters
            selectionText.place(relx=0.05,rely=0.07+vOffsetEvol)
            option_selection.place(relx=0.16, rely=0.065+vOffsetEvol, relwidth=0.3)
            _selection_parameters( optionSelection.get() ) # Show selection parameter widgets
        
        def _NSGAII_parameters():
            _GA_parameters()
        
        def _MOCELL_parameters():
            nonlocal archiveOption
            nonlocal archiveParams     
            nonlocal neighborhoodOption
            nonlocal neighborhoodParams
            
            nonlocal labelframe_operators
            
            # Show Selection parameters
            selectionText.place(relx=0.05,rely=0.07+vOffsetEvol)
            option_selection.place(relx=0.16, rely=0.065+vOffsetEvol, relwidth=0.3)
            _selection_parameters( optionSelection.get() ) # Show selection parameter widgets
            
            # Hide 'offspring' widgets
            offspringText.place_forget()
            offspringSize.place_forget()
            
            # Show specific parameters frame
            labelframe_operators.place(relx=0.05,rely=0.56)
            
            Label(labelframe_operators, text="Archive").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset)
            optionList_archive = [ option for option in AlgorithmParameters.MOCELL_ARCHIVE ]
            archiveOption = tk.StringVar(labelframe_operators)
            archiveOption.set(AlgorithmParameters.MOCELL_ARCHIVE.CROWDING_DISTANCE)
            option_archive = tk.OptionMenu(labelframe_operators, archiveOption, *optionList_archive)
            option_archive.config(width=10, state=DISABLED)
            option_archive.place(relx=0.145, rely=vertical_anchor_offset - 0.01, relwidth=0.26) 
            
            Label(labelframe_operators, text="Max. size").place(relx=0.435,rely=vertical_anchor_offset)           
            archiveParams["maximum_size"] = tk.Entry(labelframe_operators, state=NORMAL)
            archiveParams["maximum_size"].insert(0, algorithm_parameters.specific_parameters["archive"]["maximum_size"])
            archiveParams["maximum_size"].place(relx=0.544, rely=vertical_anchor_offset, relwidth=0.1)
            
            Label(labelframe_operators, text="Neighborhood").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset + vertical_spacing)
            optionList_neighborhood = [ option for option in AlgorithmParameters.MOCELL_NEIGHBORHOOD ]
            neighborhoodOption = tk.StringVar(labelframe_operators)
            neighborhoodOption.set( AlgorithmParameters.MOCELL_NEIGHBORHOOD.C9 )
            option_neighborhood = tk.OptionMenu(labelframe_operators, neighborhoodOption, *optionList_neighborhood)
            option_neighborhood.config(width=10, state=DISABLED)
            option_neighborhood.place(relx=0.215, rely=vertical_anchor_offset + vertical_spacing - 0.04) 

            # TODO: variable options depending on chosen neighborhood operator
            Label(labelframe_operators, text="Rows").place(relx=second_col_anchor_offset,rely=vertical_anchor_offset + vertical_spacing)           
            neighborhoodParams["rows"] = tk.Entry(labelframe_operators, state=NORMAL)
            neighborhoodParams["rows"].insert(0, algorithm_parameters.specific_parameters["neighborhood"]["rows"])
            neighborhoodParams["rows"].place(relx=0.52, rely=vertical_anchor_offset + vertical_spacing, relwidth=0.1)
            
            Label(labelframe_operators, text="Columns").place(relx=0.66,rely=vertical_anchor_offset + vertical_spacing)           
            neighborhoodParams["columns"] = tk.Entry(labelframe_operators, state=NORMAL)
            neighborhoodParams["columns"].insert(0, algorithm_parameters.specific_parameters["neighborhood"]["columns"])
            neighborhoodParams["columns"].place(relx=0.77, rely=vertical_anchor_offset + vertical_spacing, relwidth=0.1)
            
            
            
            
        
        def _MOEAD_parameters():
            nonlocal optionSelection
            nonlocal selectionParams
            # nonlocal optionCrossover
            # nonlocal crossoverParams
            # nonlocal optionMutation
            # nonlocal mutationParams
            nonlocal weightFilesPath
            nonlocal aggregationOption
            nonlocal neighborhoodSize
            nonlocal neighborhoodSelProb
            nonlocal maxOfNReplaced
            
            nonlocal labelframe_operators
            
            # Hide 'offspring' widgets
            offspringText.place_forget()
            offspringSize.place_forget()
            
            # Hide Selection parameters
            option_selection.place_forget()
            selectionText.place_forget()
            
            _selection_parameters("") # Remove all selection parameter widgets
            
            # Show specific parameters frame
            labelframe_operators.place(relx=0.05,rely=0.56)
        
            Label(labelframe_operators, text="Aggregative").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset)
            optionList_aggregation = [ option for option in AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION ]
            aggregationOption = tk.StringVar(labelframe_operators)
            
            if algorithm_parameters.specific_options["aggregative"] not in optionList_aggregation:
                algorithm_parameters.specific_options["aggregative"] = optionList_aggregation[0]
                
            aggregationOption.set( optionList_aggregation[0] )
            option_aggregation = tk.OptionMenu(labelframe_operators, aggregationOption, *optionList_aggregation)
            option_aggregation.config(width=10, state=DISABLED)
            option_aggregation.place(relx=0.2, rely=vertical_anchor_offset - 0.01) 
            
            Label(labelframe_operators, text="Dimension").place(relx=second_col_anchor_offset,rely=vertical_anchor_offset)           
            aggregationParams["dimension"] = tk.Entry(labelframe_operators, state=NORMAL)
            aggregationParams["dimension"].insert(0, algorithm_parameters.specific_parameters["aggregative"]["dimension"])
            aggregationParams["dimension"].place(relx=0.575, rely=vertical_anchor_offset, relwidth=0.1)
            
            Label(labelframe_operators, text="Weights folder path").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset + vertical_spacing)
            weightFilesPath = tk.Entry(labelframe_operators, state=NORMAL)
            weightFilesPath.insert(0, algorithm_parameters.specific_options["weight_files_path"])
            weightFilesPath.place(relx=0.26, rely=vertical_anchor_offset + vertical_spacing, relwidth=0.52)
            weightFilesPath.config(state=DISABLED)
            button_browse_weights = tk.Button( labelframe_operators,  text="Browse", command=lambda: _browse_weights() ).place(relx=0.805, rely=vertical_anchor_offset + vertical_spacing - 0.0125, relwidth=0.1)
            
            Label(labelframe_operators, text="Neighborhood size").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset + 2*vertical_spacing)
            neighborhoodSize = tk.Entry(labelframe_operators, state=NORMAL)
            neighborhoodSize.insert(0, algorithm_parameters.specific_options["neighborhood_size"])
            neighborhoodSize.place(relx=0.26, rely=vertical_anchor_offset + 2*vertical_spacing, relwidth=0.135)
            
            Label(labelframe_operators, text="Neighborhood selection prob.").place(relx=second_col_anchor_offset,rely=vertical_anchor_offset+ 2*vertical_spacing)
            neighborhoodSelProb = tk.Entry(labelframe_operators, state=NORMAL)
            neighborhoodSelProb.insert(0, algorithm_parameters.specific_options["neighborhood_selection_probability"])
            neighborhoodSelProb.place(relx=0.78, rely=vertical_anchor_offset + 2*vertical_spacing, relwidth=0.1)
            
            Label(labelframe_operators, text="Max. replaced").place(relx=first_col_anchor_offset,rely=vertical_anchor_offset + 3*vertical_spacing)
            maxOfNReplaced = tk.Entry(labelframe_operators, state=NORMAL)
            maxOfNReplaced.insert(0, algorithm_parameters.specific_options["max_number_of_replaced_solutions"])
            maxOfNReplaced.place(relx=0.22, rely=vertical_anchor_offset + 3*vertical_spacing, relwidth=0.135)
        
        # Cleaing error textbox
        error_textbox.config(state=NORMAL)
        error_textbox.delete('1.0', END)
        error_textbox.config(state=DISABLED)
        
        # Frame is cleared from all widgets, ready for a new option list
        # TODO: efficient implementation using pack_forget() instead of destroy()
        for widget in labelframe_operators.winfo_children():
            widget.destroy()
        
            
        if selection == "GA (Single)":
            _GA_parameters()
            
        elif selection == "NSGAII":
            _NSGAII_parameters()
            
        if selection == "Mocell":
            _MOCELL_parameters()
            
            
        elif selection == "MOEAD":
            _MOEAD_parameters()
        
    def _selection_parameters( selection ):
        
        nonlocal selectionWidgetsText
        nonlocal selectionWidgetsEntries
        
        for key,widget in selectionWidgetsText.items():
            widget.destroy()
            
        for key,widget in selectionWidgetsEntries.items():
            widget.destroy()
            
        selectionWidgetsText = {}
        selectionWidgetsEntries = {}
            
        if selection == AlgorithmParameters.SELECTION.NARY_RANDOM:
            selectionWidgetsText["number_of_solutions"] = Label(labelframe_evol, text="Number of solutions")
            selectionWidgetsText["number_of_solutions"].place(relx=0.48, rely=0.07+vOffsetEvol)
    
            selectionWidgetsEntries["number_of_solutions"] = tk.Entry(labelframe_evol, state=NORMAL )
            selectionWidgetsEntries["number_of_solutions"].insert(0, algorithm_parameters.selection_parameters["number_of_solutions"])
            selectionWidgetsEntries["number_of_solutions"].place(relx=0.7, rely=0.07+vOffsetEvol, relwidth=0.1)
            
        elif selection == AlgorithmParameters.SELECTION.RANKING_AND_CROWDING:
            selectionWidgetsText["max_population_size"] = Label(labelframe_evol, text="Max. population size")
            selectionWidgetsText["max_population_size"].place(relx=0.48, rely=0.07+vOffsetEvol)
            
            selectionWidgetsEntries["max_population_size"] = tk.Entry(labelframe_evol, state=NORMAL )
            selectionWidgetsEntries["max_population_size"].insert(0, algorithm_parameters.selection_parameters["max_population_size"])
            selectionWidgetsEntries["max_population_size"].place(relx=0.7, rely=0.07+vOffsetEvol, relwidth=0.1)
            
    def _crossover_parameters_float( selection ):
        
        nonlocal fCrossoverParams
        nonlocal fCrossoverWidgetsText
        
        for key,widget in fCrossoverParams.items():
            widget.destroy()
            
        for key,widget in fCrossoverWidgetsText.items():
            widget.destroy()
        
        fCrossoverParams = {}
        fCrossoverWidgetsText = {}
        
        if selection == AlgorithmParameters.FLOAT_CROSSOVER.SBX:
            fCrossoverWidgetsText["probability"] = Label(real_tab, text="Probability")
            fCrossoverWidgetsText["probability"].place(relx=0.435,rely=0.1)
            fCrossoverParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fCrossoverParams["probability"].insert(0, algorithm_parameters.float_crossover_parameters["probability"])
            fCrossoverParams["probability"].place(relx=0.56, rely=0.1, relwidth=0.1)
            
            if not is_float(algorithm_parameters.float_crossover_parameters["distribution_index"]):
                algorithm_parameters.float_crossover_parameters["distribution_index"] = "20.0"
            
            fCrossoverWidgetsText["distribution_index"] = Label(real_tab, text="Distribution index")
            fCrossoverWidgetsText["distribution_index"].place(relx=0.69,rely=0.1)
            fCrossoverParams["distribution_index"] = tk.Entry(real_tab, state=NORMAL )
            fCrossoverParams["distribution_index"].insert(0, algorithm_parameters.float_crossover_parameters["distribution_index"])
            fCrossoverParams["distribution_index"].place(relx=0.885, rely=0.1, relwidth=0.1)
            
        elif selection == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION:
            fCrossoverWidgetsText["probability"] = Label(real_tab, text="Rate")
            fCrossoverWidgetsText["probability"].place(relx=0.435,rely=0.1)
            fCrossoverParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fCrossoverParams["probability"].insert(0, algorithm_parameters.float_crossover_parameters["probability"])
            fCrossoverParams["probability"].place(relx=0.48, rely=0.1, relwidth=0.1)
            
            fCrossoverWidgetsText["F"] = Label(real_tab, text="F")
            fCrossoverWidgetsText["F"].place(relx=0.635,rely=0.1)
            fCrossoverParams["F"] = tk.Entry(real_tab, state=NORMAL )
            fCrossoverParams["F"].insert(0, algorithm_parameters.float_crossover_parameters["F"])
            fCrossoverParams["F"].place(relx=0.665, rely=0.1, relwidth=0.1)
            
            if not is_float( algorithm_parameters.float_crossover_parameters["K"] ):
                algorithm_parameters.float_crossover_parameters["K"] = "0.5"
            
            fCrossoverWidgetsText["K"] = Label(real_tab, text="K")
            fCrossoverWidgetsText["K"].place(relx=0.82,rely=0.1)
            fCrossoverParams["K"] = tk.Entry(real_tab, state=NORMAL )
            fCrossoverParams["K"].insert(0, algorithm_parameters.float_crossover_parameters["K"])
            fCrossoverParams["K"].place(relx=0.85, rely=0.1, relwidth=0.1)
    
    def _crossover_parameters_permutation( selection ):
        pass
        
    def _mutation_parameters_float( selection ):
        
        nonlocal fMutationParams
        nonlocal fMutationWidgetsText
        
        for key,widget in fMutationParams.items():
            widget.destroy()
            
        for key,widget in fMutationWidgetsText.items():
            widget.destroy()
        
        fMutationParams = {}
        fMutationWidgetsText = {}
        
        if selection == AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM:
            
            fMutationWidgetsText["probability"] = Label(real_tab, text="Probability")
            fMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
            fMutationParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["probability"].insert(0, algorithm_parameters.float_mutation_parameters["probability"])
            fMutationParams["probability"].place(relx=0.56, rely=0.1+vOperatorsOffset, relwidth=0.1)
        
        if selection == AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL:
            
            fMutationWidgetsText["probability"] = Label(real_tab, text="Probability")
            fMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
            fMutationParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["probability"].insert(0, algorithm_parameters.float_mutation_parameters["probability"])
            fMutationParams["probability"].place(relx=0.56, rely=0.1+vOperatorsOffset, relwidth=0.1)
            
            if not is_float(algorithm_parameters.float_mutation_parameters["distribution_index"]):
                algorithm_parameters.float_mutation_parameters["distribution_index"] = "20.0"
            
            fMutationWidgetsText["distribution_index"] = Label(real_tab, text="Distribution index")
            fMutationWidgetsText["distribution_index"].place(relx=0.69,rely=0.1+vOperatorsOffset)
            fMutationParams["distribution_index"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["distribution_index"].insert(0, algorithm_parameters.float_mutation_parameters["distribution_index"])
            fMutationParams["distribution_index"].place(relx=0.885, rely=0.1+vOperatorsOffset, relwidth=0.1)
            
        if selection == AlgorithmParameters.FLOAT_MUTATION.UNIFORM:
            
            fMutationWidgetsText["probability"] = Label(real_tab, text="Probability")
            fMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
            fMutationParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["probability"].insert(0, algorithm_parameters.float_mutation_parameters["probability"])
            fMutationParams["probability"].place(relx=0.56, rely=0.1+vOperatorsOffset, relwidth=0.1)
            
            fMutationWidgetsText["perturbation"] = Label(real_tab, text="Perturbation")
            fMutationWidgetsText["perturbation"].place(relx=0.69,rely=0.1+vOperatorsOffset)
            fMutationParams["perturbation"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["perturbation"].insert(0, algorithm_parameters.float_mutation_parameters["perturbation"])
            fMutationParams["perturbation"].place(relx=0.835, rely=0.1+vOperatorsOffset, relwidth=0.1)
            
        if selection == AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM:
            
            fMutationWidgetsText["probability"] = Label(real_tab, text="Prob.")
            fMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
            fMutationParams["probability"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["probability"].insert(0, algorithm_parameters.float_mutation_parameters["probability"])
            fMutationParams["probability"].place(relx=0.508, rely=0.1+vOperatorsOffset, relwidth=0.07)
            
            if not is_float(algorithm_parameters.float_mutation_parameters["perturbation"]):
                algorithm_parameters.float_mutation_parameters["perturbation"] = "0.5"
            
            fMutationWidgetsText["perturbation"] = Label(real_tab, text="Perturb.")
            fMutationWidgetsText["perturbation"].place(relx=0.6,rely=0.1+vOperatorsOffset)
            fMutationParams["perturbation"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["perturbation"].insert(0, algorithm_parameters.float_mutation_parameters["perturbation"])
            fMutationParams["perturbation"].place(relx=0.7, rely=0.1+vOperatorsOffset, relwidth=0.07)
            
            if not is_float(algorithm_parameters.float_mutation_parameters["max_iterations"]):
                algorithm_parameters.float_mutation_parameters["max_iterations"] = "0.5"
            
            fMutationWidgetsText["max_iterations"] = Label(real_tab, text="Max. Iter.")
            fMutationWidgetsText["max_iterations"].place(relx=0.79,rely=0.1+vOperatorsOffset)
            fMutationParams["max_iterations"] = tk.Entry(real_tab, state=NORMAL )
            fMutationParams["max_iterations"].insert(0, algorithm_parameters.float_mutation_parameters["max_iterations"])
            fMutationParams["max_iterations"].place(relx=0.9, rely=0.1+vOperatorsOffset, relwidth=0.07)
            
    def _mutation_parameters_permutation( selection ):
        pass

    win = tk.Toplevel()
    win.wm_title("Optimizer Settings")
    win.resizable(False,False)

    #window_width = popup_width*0.7
    window_width = 600
    #window_height = popup_height*1.2
    window_height = 700

    win.geometry("%dx%d+%d+%d" % (window_width, window_height, ((screen_width/2)-((popup_width*0.7)/2)), ((screen_height/2)-((popup_height*0.7)/2))))
    win.grab_set() # Locking root window
    
        
    
    """
        Widgets for algorithm-specific parameters
    """
    
    # General EA parameters
    offspringSize = None
    optionSelection = None
    selectionParams = {}
    selectionWidgetsText = {}
    selectionWidgetsEntries = {}
    
    fOptionCrossover = None
    fCrossoverParams = {}
    fCrossoverWidgetsText = {}
    
    iOptionCrossover = None
    iCrossoverParams = {}
    iCrossoverWidgetsText = {}
    
    bOptionCrossover = None
    bCrossoverParams = {}
    bCrossoverWidgetsText = {}
    
    pOptionCrossover = None
    pCrossoverParams = {}
    pCrossoverWidgetsText = {}
    
    
    
    fOptionMutation = None
    fMutationParams = {}
    fMutationWidgetsText = {}
    
    iOptionMutation = None
    iMutationParams = {}
    iMutationWidgetsText = {}
    
    bOptionMutation = None
    bMutationParams = {}
    bMutationWidgetsText = {}
    
    pOptionMutation = None
    pMutationParams = {}
    pMutationWidgetsText = {}
    
    
    
    # MOEAD-specific parameters
    aggregationOption = None
    aggregationParams = {}
    neighborhoodSelProb = None
    neighborhoodSize = None
    maxOfNReplaced = None
    weightFilesPath = None
    
    
    
    #MOcell-specific parameters
    archiveOption = None
    archiveParams = {}     
    neighborhoodOption = None
    neighborhoodParams = {}  
    
    """
        Common parameters
    """
    
    # Frame for common parameters
    # labelframe_common = LabelFrame(win, text="General parameters", height=int(0.22*window_height), width=int(0.9*window_width))
    labelframe_common = LabelFrame(win, text="General parameters", height=110, width=540)
    labelframe_common.place(relx=0.05,rely=0.04)
    
    vOffsetEvol = 0.15
    
    # Frame for evolutionary parameters
    labelframe_evol = LabelFrame(win, text="Evolutionary parameters", height=int(0.32*window_height), width=int(0.9*window_width))
    labelframe_evol.place(relx=0.05,rely=0.215)
    tabs = ttk.Notebook( labelframe_evol )
    
    Label(labelframe_evol, text="Population size").place(relx=0.05,rely=0.07)
    entry_popsize = tk.Entry(labelframe_evol, state=NORMAL )
    entry_popsize.insert(0, algorithm_parameters.general_parameters["population_size"])
    entry_popsize.place(relx=0.23, rely=0.07, relwidth=0.15)
    
    offspringText = Label(labelframe_evol, text="Offspring size")
    # offspringText.place(relx=0.45,rely=0.07)
    offspringSize = tk.Entry(labelframe_evol, state=NORMAL )
    offspringSize.insert(0, algorithm_parameters.general_parameters["offspring_size"])
    offspringSize.place(relx=0.61, rely=0.07, relwidth=0.15)
    
    selectionText = Label(labelframe_evol, text="Selection")
    # selectionText.place(relx=0.05,rely=0.07+vOffsetEvol)
    optionList_Selection = [ option for option in AlgorithmParameters.SELECTION ]
    optionSelection = tk.StringVar(labelframe_evol)
    
    if algorithm_parameters.selection_choice not in optionList_Selection:
        algorithm_parameters.selection_choice = optionList_Selection[0]
    
    optionSelection.set( algorithm_parameters.selection_choice )
    option_selection = tk.OptionMenu(labelframe_evol, optionSelection, *optionList_Selection, command=_selection_parameters)
    option_selection.config(state=NORMAL)    
    option_selection.place(relx=0.16, rely=0.065+vOffsetEvol, relwidth=0.3)
    
    vOperatorsOffset = 0.45
    
    if variable_types.FloatVariable in var_types:
        real_tab = ttk.Frame(tabs)
        f_crossover_optionlist = [ option for option in AlgorithmParameters.FLOAT_CROSSOVER ]
        
        if algorithm_parameters.float_crossover_choice not in f_crossover_optionlist:
            algorithm_parameters.float_crossover_choice = f_crossover_optionlist[0]
            
        _crossover_parameters_float( algorithm_parameters.float_crossover_choice )
        
        Label( real_tab, text="Crossover" ).place( relx=0.03, rely=0.1 )
        fOptionCrossover = tk.StringVar(real_tab)
        fOptionCrossover.set( algorithm_parameters.float_crossover_choice )
        f_option_crossover = tk.OptionMenu(real_tab, fOptionCrossover, *f_crossover_optionlist, command=_crossover_parameters_float)
        f_option_crossover.config( state=NORMAL )
        f_option_crossover.place( relx=0.16, rely=0.09, relwidth=0.26 )
        
        f_mutation_optionlist = [ option for option in AlgorithmParameters.FLOAT_MUTATION ]
        
        if algorithm_parameters.float_mutation_choice not in f_mutation_optionlist:
            algorithm_parameters.float_mutation_choice = f_mutation_optionlist[0]
            
        _mutation_parameters_float( algorithm_parameters.float_mutation_choice )
        
        Label( real_tab, text="Mutation" ).place( relx=0.03, rely=0.1+vOperatorsOffset )
        fOptionMutation = tk.StringVar(real_tab)
        fOptionMutation.set( algorithm_parameters.float_mutation_choice )
        f_option_mutation = tk.OptionMenu(real_tab, fOptionMutation, *f_mutation_optionlist, command=_mutation_parameters_float)
        f_option_mutation.config( state=NORMAL )
        f_option_mutation.place( relx=0.16, rely=0.09+vOperatorsOffset, relwidth=0.26 )
        
        tabs.add( real_tab, text="Real" )
    
    
    if variable_types.IntegerVariable in var_types:
        int_tab = ttk.Frame(tabs)
        
        i_crossover_optionlist = [ option for option in AlgorithmParameters.INT_CROSSOVER ]
        
        Label( int_tab, text="Crossover" ).place( relx=0.03, rely=0.1 )
        iOptionCrossover = tk.StringVar(int_tab)
        iOptionCrossover.set(i_crossover_optionlist[0])
        i_option_crossover = tk.OptionMenu(int_tab, iOptionCrossover, *i_crossover_optionlist)
        i_option_crossover.config( state=DISABLED )
        i_option_crossover.place( relx=0.16, rely=0.09, relwidth=0.26 )
        
        iCrossoverWidgetsText["probability"] = Label(int_tab, text="Probability")
        iCrossoverWidgetsText["probability"].place(relx=0.435,rely=0.1)
        iCrossoverParams["probability"] = tk.Entry(int_tab, state=NORMAL )
        iCrossoverParams["probability"].insert(0, algorithm_parameters.int_crossover_parameters["probability"])
        iCrossoverParams["probability"].place(relx=0.56, rely=0.1, relwidth=0.1)
        
        if not is_float(algorithm_parameters.int_crossover_parameters["distribution_index"]):
            algorithm_parameters.int_crossover_parameters["distribution_index"] = "20.0"
        
        iCrossoverWidgetsText["distribution_index"] = Label(int_tab, text="Distribution index")
        iCrossoverWidgetsText["distribution_index"].place(relx=0.69,rely=0.1)
        iCrossoverParams["distribution_index"] = tk.Entry(int_tab, state=NORMAL )
        iCrossoverParams["distribution_index"].insert(0, algorithm_parameters.int_crossover_parameters["distribution_index"])
        iCrossoverParams["distribution_index"].place(relx=0.885, rely=0.1, relwidth=0.1)
        
        i_mutation_optionlist = [ option for option in AlgorithmParameters.INT_MUTATION ]
        
        Label( int_tab, text="Mutation" ).place( relx=0.03, rely=0.1+vOperatorsOffset )
        iOptionMutation = tk.StringVar(int_tab)
        iOptionMutation.set(i_mutation_optionlist[0])
        i_option_mutation = tk.OptionMenu(int_tab, iOptionMutation, *i_mutation_optionlist )
        i_option_mutation.config( state=DISABLED )
        i_option_mutation.place( relx=0.16, rely=0.09+vOperatorsOffset, relwidth=0.26 )
        
        iMutationWidgetsText["probability"] = Label(int_tab, text="Probability")
        iMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
        iMutationParams["probability"] = tk.Entry(int_tab, state=NORMAL )
        iMutationParams["probability"].insert(0, algorithm_parameters.int_mutation_parameters["probability"])
        iMutationParams["probability"].place(relx=0.56, rely=0.1+vOperatorsOffset, relwidth=0.1)
        
        if not is_float(algorithm_parameters.int_mutation_parameters["distribution_index"]):
            algorithm_parameters.int_mutation_parameters["distribution_index"] = "20.0"
        
        iMutationWidgetsText["distribution_index"] = Label(int_tab, text="Distribution index")
        iMutationWidgetsText["distribution_index"].place(relx=0.69,rely=0.1+vOperatorsOffset)
        iMutationParams["distribution_index"] = tk.Entry(int_tab, state=NORMAL )
        iMutationParams["distribution_index"].insert(0, algorithm_parameters.int_mutation_parameters["distribution_index"])
        iMutationParams["distribution_index"].place(relx=0.885, rely=0.1+vOperatorsOffset, relwidth=0.1)
        
        tabs.add( int_tab, text="Integer" )
    
    if variable_types.BinaryVariable in var_types:
        binary_tab = ttk.Frame(tabs)
        
        b_crossover_optionlist = [ option for option in AlgorithmParameters.BINARY_CROSSOVER ]
        
        Label( binary_tab, text="Crossover" ).place( relx=0.03, rely=0.1 )
        bOptionCrossover = tk.StringVar(binary_tab)
        bOptionCrossover.set(b_crossover_optionlist[0])
        b_option_crossover = tk.OptionMenu(binary_tab, bOptionCrossover, *b_crossover_optionlist)
        b_option_crossover.config( state=DISABLED )
        b_option_crossover.place( relx=0.16, rely=0.09, relwidth=0.26 )
        
        bCrossoverWidgetsText["probability"] = Label(binary_tab, text="Probability")
        bCrossoverWidgetsText["probability"].place(relx=0.435,rely=0.1)
        bCrossoverParams["probability"] = tk.Entry(binary_tab, state=NORMAL )
        bCrossoverParams["probability"].insert(0, algorithm_parameters.binary_crossover_parameters["probability"])
        bCrossoverParams["probability"].place(relx=0.56, rely=0.1, relwidth=0.1)
        
        b_mutation_optionlist = [ option for option in AlgorithmParameters.BINARY_MUTATION ]
        
        Label( binary_tab, text="Mutation" ).place( relx=0.03, rely=0.1+vOperatorsOffset )
        bOptionMutation = tk.StringVar(binary_tab)
        bOptionMutation.set(b_mutation_optionlist[0])
        b_option_mutation = tk.OptionMenu(binary_tab, bOptionMutation, *b_mutation_optionlist )
        b_option_mutation.config( state=DISABLED )
        b_option_mutation.place( relx=0.16, rely=0.09+vOperatorsOffset, relwidth=0.26 )
        
        bMutationWidgetsText["probability"] = Label(binary_tab, text="Probability")
        bMutationWidgetsText["probability"].place(relx=0.435,rely=0.1+vOperatorsOffset)
        bMutationParams["probability"] = tk.Entry(binary_tab, state=NORMAL )
        bMutationParams["probability"].insert(0, algorithm_parameters.binary_mutation_parameters["probability"])
        bMutationParams["probability"].place(relx=0.56, rely=0.1+vOperatorsOffset, relwidth=0.1)
        
        tabs.add( binary_tab, text="Binary" )
        
    if variable_types.PermutationVariable in var_types:
        #TODO
        pass
    
    # TODO: add support for 'permutation' type
    
    tabs.place( relx=0.015, rely=0.1+2*vOffsetEvol, relwidth=0.97, relheight=0.55 )
    
    # Frame for algorithm-specific parameters
    # labelframe_operators = LabelFrame(win, text="Algorithm-specific parameters", height=int(0.335*window_height), width=int(0.9*window_width))
    labelframe_operators = LabelFrame(win, text="Algorithm-specific parameters", height=160, width=540)
    labelframe_operators.place(relx=0.05,rely=0.56)
    labelframe_operators.place_forget()

    error_textbox_width = 0.695
    ttk.Button(win, text="Save and close", command=save_close).place(relx=error_hor_anchor + error_textbox_width + 0.025, rely=error_vert_anchor, relwidth=0.19, relheight=0.15)
    
    error_textbox = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Times New Roman", 9), state=NORMAL)
    error_textbox.pack()
    error_textbox.place(relx=error_hor_anchor, rely=error_vert_anchor, relwidth=error_textbox_width, relheight=0.15)

    Label(labelframe_common, text="Algorithm").place(relx=0.05,rely=0.07)
    # optionList_Algorithm = ["NSGAII", "MOEAD", "Mocell", "GA (Single)"]
    optionList_Algorithm = [ option for option in AlgorithmParameters.SUPPORTED_ALGORITHMS ]
    
    optionAlgorithm = tk.StringVar(labelframe_common)
    
    if algorithm_parameters.choice not in optionList_Algorithm:
        algorithm_parameters.choice = optionList_Algorithm[0]
        
    optionAlgorithm.set(algorithm_parameters.choice)
        
    option_algorithm = tk.OptionMenu(labelframe_common, optionAlgorithm, *optionList_Algorithm, command=_update_frames)
    option_algorithm.config(width=8)
    option_algorithm.place(relx=0.17, rely=0.056)

    vOffset1 = 0.5
    
    _update_frames(algorithm_parameters.choice)
    
    
    
    
    
    
    
    
    
    
    
    
    