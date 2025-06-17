from typing import Callable
import panel as pn
from typing import List

import pandas as pd
import math

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import push_notebook

from reactflow import ReactFlow, ReactFlowNode, NodePort, PortDirection, PortPosition


class TextInputNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Text Input"
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.BOTTOM, name="output")]

    def __init__(self, ):
        self.text_input = pn.widgets.TextInput(value="", width=100)

    def create(self, ):
        return pn.layout.Column(
                                    self.text_input, 
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self,):
        pass

    def set_watched_variables(self, funct:Callable):
        self.text_input.param.watch(funct, "value")

    def get_node_json_value(self):
        return {"value" : self.text_input.value}


df = pd.DataFrame({
    "sinus": [math.sin(t/10) for t in range(50)],
    "cosinus": [math.cos(t/10) for t in range(50)],
    "atan": [math.atan(t/10) for t in range(50)],
})


class InputDataFrameNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Input DataFrame"
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.BOTTOM, name="output")]

    def __init__(self):
        self.df = df

    def create(self, ):
        return pn.layout.Column(
                                    pn.pane.Markdown("Some pandas DataFrame"),
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self,):
        pass

    def set_watched_variables(self, funct:Callable):
        pass

    def get_node_json_value(self):
        return {"dataframe" : self.df}


class ColumnSelectNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Column select"
    ports:List[NodePort] = [
            NodePort(direction=PortDirection.INPUT, position=PortPosition.TOP, name="input"),
            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.BOTTOM, name="output")
        ]

    def __init__(self):
        self.df_columns = pn.widgets.Select(options=[], width=100)
        self.column_value = pd.DataFrame()

    def create(self, ):
        return pn.layout.Column(
                                    self.df_columns, 
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self,):
        if len(self.plugged_nodes["input"]) == 0:
            self.df_columns.options = []
            self.column_value = []
        else:
            self.df_columns.options = list(self.plugged_nodes["input"][0].get_node_json_value()["dataframe"].columns)

            if self.df_columns.value in self.df_columns.options:
                self.column_value = list(self.plugged_nodes["input"][0].get_node_json_value()["dataframe"][self.df_columns.value])

    def set_watched_variables(self, funct:Callable):
        self.df_columns.param.watch(funct, "value")

    def get_node_json_value(self):
        return {"value" : self.column_value}


class BokehPlotNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Bokeh plot"
    ports:List[NodePort] = [
            NodePort(direction=PortDirection.INPUT, position=PortPosition.TOP, name="input"),
        ]

    def __init__(self):
        self.data = {"x_values":[], 'y_values': []}
        self.source = ColumnDataSource(data=self.data)

        self.p = figure(width=500, height=500)
        self.p.line(x="x_values", y='y_values', source=self.source)

        self.bokeh = pn.pane.Bokeh(self.p)

    def create(self, ):
        return pn.layout.Column(
                                    self.bokeh, 
                                    name=self.name, 
                                    align="center"
                                )
    
    def update(self,):
        if len(self.plugged_nodes["input"]) == 0:
            self.source.data = {"y_values": [], "x_values": []}
        else:
            self.source.data = {"x_values":list(range(len(self.plugged_nodes["input"][0].get_node_json_value()["value"]))), 
                                "y_values": list(self.plugged_nodes["input"][0].get_node_json_value()["value"])}

        print(self.source.data)
        pn.io.push_notebook(self.bokeh)

    def set_watched_variables(self, funct:Callable):
        pass

    def get_node_json_value(self):
        return {}



ReactFlow(nodes_classes = [TextInputNode, InputDataFrameNode, ColumnSelectNode, BokehPlotNode]).show()