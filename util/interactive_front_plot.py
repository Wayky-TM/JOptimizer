# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:25:37 2021

@author: Wayky
"""

import re
import os

from core.engine import OptimizationEngine
from jmetal.lab.visualization.interactive import *

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import webbrowser


class SolutionsInteractivePlot:
    
    def __init__(self,
                  # composite_problem: CompositeProblem,
                  engine: OptimizationEngine,
                  title: str = 'Pareto front approximation',
                  reference_front: List[S] = None,
                  reference_point: list = None,
                  axis_labels: list = None):
        
        self.title = title
        # self.composite_problem = composite_problem
        self.engine = engine
        self.reference_front = reference_front
        self.reference_point = reference_point
        self.axis_labels = axis_labels
        
        
    def plot(self, front, objectives_list: List[str], label=None, normalize: bool = False, filename: str = None, format: str = 'HTML'):
        """ Plot a front of solutions (2D, 3D or parallel coordinates).

        :param front: List of solutions.
        :param label: Front name.
        :param normalize: Normalize the input front between 0 and 1 (for problems with more than 3 objectives).
        :param filename: Output filename.
        """
        if not isinstance(label, list):
            label = [label]

        objectives = self.engine.problem_parameters.options["objectives"]
        
        if objectives<2 or len(objectives_list)<2 or len(objectives_list)>3:
            raise ValueError("'%s' only supports 2D and 3D plots" % (type(self).__name__))
            
        data = {}
        
        for obj_index in range(objectives):
            data[self.engine.problem_parameters.options["objectives_names"][obj_index]] = [ solution.objectives[obj_index] for solution in front ]
        
        data["Index"] = [ i for i in range(0,len(front)) ]
        
        dataframe = pd.DataFrame( data=data )
        
        if len(objectives_list)==2:
            fig = px.scatter_3d(dataframe,
                                x=objectives_list[0],
                                y=objectives_list[1],
                                z=objectives_list[2],
                                custom_data=['Index'])
            
            fig.update_traces(
            hovertemplate="<br>".join([
                objectives_list[0] + ": %{x}",
                objectives_list[1] + ": %{y}",
                objectives_list[2] + ": %{z}",
                "Index: %{customdata[0]}",
            ])
        )
            fig.write_html("plot.html")
            webbrowser.open('file://' + os.path.realpath("plot.html"))
            os.remove("plot.html")
            
        
        elif len(objectives_list)==3:    
            fig = px.scatter_3d(dataframe,
                                x=objectives_list[0],
                                y=objectives_list[1],
                                z=objectives_list[2],
                                custom_data=['Index'])
            
            fig.update_traces(
            hovertemplate="<br>".join([
                objectives_list[0] + ": %{x}",
                objectives_list[1] + ": %{y}",
                objectives_list[2] + ": %{z}",
                "Index: %{customdata[0]}",
            ])
        )
            fig.write_html("plot.html")
            webbrowser.open('file://' + os.path.realpath("plot.html"))
            os.remove("plot.html")
            
        


# class SolutionsInteractivePlot( InteractivePlot ):
    
#     def __init__(self,
#                  composite_problem: CompositeProblem,
#                  title: str = 'Pareto front approximation',
#                  reference_front: List[S] = None,
#                  reference_point: list = None,
#                  axis_labels: list = None):
        
#         super(SolutionsInteractivePlot, self).__init__(title=title, reference_front=reference_front, reference_point=reference_point, axis_labels=axis_labels)
#         self.composite_problem = composite_problem
        
        
#     def plot(self, front, label=None, normalize: bool = False, filename: str = None, format: str = 'HTML'):
#         """ Plot a front of solutions (2D, 3D or parallel coordinates).

#         :param front: List of solutions.
#         :param label: Front name.
#         :param normalize: Normalize the input front between 0 and 1 (for problems with more than 3 objectives).
#         :param filename: Output filename.
#         """
#         if not isinstance(label, list):
#             label = [label]

#         self.layout = go.Layout(
#             margin=dict(l=80, r=80, b=80, t=150),
#             height=800,
#             title='{}<br>{}'.format(self.plot_title, label[0]),
#             scene=dict(
#                 xaxis=dict(title=self.axis_labels[0:1][0] if self.axis_labels[0:1] else None),
#                 yaxis=dict(title=self.axis_labels[1:2][0] if self.axis_labels[1:2] else None),
#                 zaxis=dict(title=self.axis_labels[2:3][0] if self.axis_labels[2:3] else None)
#             ),
#             hovermode='closest'
#         )

#         # If any reference front, plot
#         if self.reference_front:
#             points, _ = self.get_points(self.reference_front)
#             trace = self.__generate_trace(points=points, legend='Reference front', normalize=normalize,
#                                           color='black', size=2)
#             self.data.append(trace)

#         # If any reference point, plot
#         if self.reference_point:
#             points = pd.DataFrame(self.reference_point)
#             trace = self.__generate_trace(points=points, legend='Reference point', color='red', size=8)
#             self.data.append(trace)

#         # Get points and metadata
#         points, _ = self.get_points(front)
        
#         # metadata = list(solution.__str__() for solution in front)
        
#         metadata = []
        
#         for solution in front:
#             variables = self.composite_problem.recover_variables( solution )[0]
#             vars_string = "\n".join([ variable[0].keyword+str(variable[1]) for variable in variables ])
#             metadata.append( vars_string )
        

#         trace = self.__generate_trace(points=points, metadata=metadata, legend='Front approximation',
#                                       normalize=normalize)
#         self.data.append(trace)
#         self.figure = go.Figure(data=self.data, layout=self.layout)

#         # Plot the figure
#         if filename:
#             if format == 'HTML':
#                 self.export_to_html(filename)
#             else:
#                 pio.write_image(self.figure, filename + '.' + format)


#     def __generate_trace(self, points: pd.DataFrame, legend: str, metadata: list = None, normalize: bool = False,
#                          **kwargs):
#         dimension = points.shape[1]

#         # tweak points size for 3D plots
#         marker_size = 8
#         if dimension == 3:
#             marker_size = 4

#         # if indicated, perform normalization
#         if normalize:
#             points = (points - points.min()) / (points.max() - points.min())

#         marker = dict(
#             color='#236FA4',
#             size=marker_size,
#             symbol='circle',
#             line=dict(
#                 color='#236FA4',
#                 width=1
#             ),
#             opacity=0.8
#         )
#         marker.update(**kwargs)

#         if dimension == 2:
#             trace = go.Scattergl(
#                 x=points[0],
#                 y=points[1],
#                 mode='markers',
#                 marker=marker,
#                 name=legend,
#                 customdata=metadata
#             )
#         elif dimension == 3:
#             trace = go.Scatter3d(
#                 x=points[0],
#                 y=points[1],
#                 z=points[2],
#                 mode='markers',
#                 marker=marker,
#                 name=legend,
#                 customdata=metadata
#             )
#         else:
#             dimensions = list()
#             for column in points:
#                 dimensions.append(
#                     dict(range=[0, 1],
#                          label=self.axis_labels[column:column + 1][0] if self.axis_labels[column:column + 1] else None,
#                          values=points[column])
#                 )

#             trace = go.Parcoords(
#                 line=dict(
#                     color='#236FA4'
#                 ),
#                 dimensions=dimensions,
#                 name=legend,
#             )

#         return trace

