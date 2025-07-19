from typing import Callable
import panel as pn
from typing import List

import pandas as pd
import math

from bokeh.plotting import figure
from bokeh.io import curdoc

from reactflow import ReactFlow, ReactFlowNode, NodePort, PortDirection, PortPosition


"""
    Creating objects used by default by the nodes
"""
p = figure()
p.line(x=[0], y=[0])

pn.state.curdoc = curdoc()

bokeh_plot = pn.pane.Bokeh(p, sizing_mode = "stretch_both")

df = pd.DataFrame({
    "sinus": [math.sin(t/10) for t in range(50)],
    "cosinus": [math.cos(t/10) for t in range(50)],
    "atan": [math.atan(t/10) for t in range(50)],
})



"""
    Nodes definition
"""
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


class InputDataFrameNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Input DataFrame"
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, 
                                        position=PortPosition.RIGHT, 
                                        name="Output", 
                                        display_name=True, 
                                        offset=35)]

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
            NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="DataFrame", offset=30, display_name=True),
            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output", offset=30, display_name=True)
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
        if len(self.plugged_nodes["DataFrame"]) == 0:
            self.df_columns.options = []
            self.column_value = []
        else:
            self.df_columns.options = list(self.plugged_nodes["DataFrame"][0].get_node_json_value()["dataframe"].columns)

            if self.df_columns.value in self.df_columns.options:
                self.column_value = list(self.plugged_nodes["DataFrame"][0].get_node_json_value()["dataframe"][self.df_columns.value])

    def set_watched_variables(self, funct:Callable):
        self.df_columns.param.watch(funct, "value")

    def get_node_json_value(self):
        return {"value" : self.column_value, "name":self.df_columns.value}
    


class BokehPlotNode(ReactFlowNode):
    child:pn.viewable.Viewable = None
    node_class_name = "Bokeh plot"
    ports:List[NodePort] = [
            NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="Title", offset=20, display_name=True),
            NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="Input", offset=40, display_name=True),
        ]

    def __init__(self):
        self.plot:pn.pane.Bokeh = bokeh_plot
        self.display_legend = pn.widgets.Checkbox(name="Display legend", value=True)

    def create(self, ):
        return pn.layout.Column(
                                    self.display_legend,
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    async def replace_figure(self,):
        self.plot.object = self.figure

    def update(self,):
        print("Updating plot...")
        self.figure = figure(width=500, height=500)

        for input_ in self.plugged_nodes["Input"]:
            x=list(range(len(input_.get_node_json_value()["value"])))
            y= list(input_.get_node_json_value()["value"])

            label = None
            if self.display_legend.value and "name" in input_.get_node_json_value():
                label = input_.get_node_json_value()["name"]

            self.figure.line(x=x, y=y, legend_label = label)

        if len(self.plugged_nodes["Title"]) != 0:
            title = self.plugged_nodes["Title"][0].get_node_json_value()

            if "value" in title and isinstance(title["value"], str):
                self.figure.title = title["value"]

            self.figure.legend

        pn.state.curdoc.add_next_tick_callback(self.replace_figure)

    def set_watched_variables(self, funct:Callable):
        pass

    def get_node_json_value(self):
        return {}

"""
    Panel definition and display
"""
pn.Row(
        ReactFlow(
                    nodes_classes = [TextInputNode, InputDataFrameNode, ColumnSelectNode, BokehPlotNode], 
                  ),
        bokeh_plot,
        sizing_mode = "stretch_both"
    ).show()