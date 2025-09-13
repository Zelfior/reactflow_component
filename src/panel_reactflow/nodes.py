""" List of nodes for default holoviz panel input widgets
"""
import datetime
import functools
from json import JSONEncoder
import json
from typing import List

import numpy as np
import panel as pn

from panel_reactflow.reactflow_api import NodePort, PortDirection, PortPosition
from panel_reactflow.workflow import WorkflowNode

class ArrayInputNode(WorkflowNode):
    """ Generic node containig an ArrayInput widget, provided text is given with the "value" key.
    """
    node_class_name = "Array Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.array_input = pn.widgets.ArrayInput(name="value", width=100)
        self.array_input.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.array_input, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.array_input.value}


class ButtonNode(WorkflowNode):
    """ Node containing a button that triggers an update.
    """
    node_class_name = "Button"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.button = pn.widgets.Button(name='Update', width=100)
        self.button.on_click(self.update)

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.button, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {}



class CheckBoxNode(WorkflowNode):
    """ Generic node containig a text input widget, provided text is given with the "value" key.
    """
    node_class_name = "Check Box"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.check_box = pn.widgets.Checkbox(name="value", width=100)
        self.check_box.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.check_box, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.check_box.value}



class ColorPickerNode(WorkflowNode):
    """ Generic node containig a color picker widget, provided color is given as HTML string with the "value" key.
    """
    node_class_name = "Color Picker"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.color_picker = pn.widgets.ColorPicker(name="Color", width=100)
        self.color_picker.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.color_picker, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.color_picker.value}



class DatePickerNode(WorkflowNode):
    """ Generic node containig a date picker widget, provided date is given with the "value" key.
    """
    node_class_name = "Date Picker"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.date_picker = pn.widgets.DatePicker(width=100)
        self.date_picker.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.date_picker, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.date_picker.value}



class DateRangePickerNode(WorkflowNode):
    """ Generic node containig a date range picker widget, provided date range is given with the "value" key.
    """
    node_class_name = "Date Range Picker"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.date_picker = pn.widgets.DateRangePicker(width=200)
        self.date_picker.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.date_picker, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.date_picker.value}



class FileInputNode(WorkflowNode):
    """ Generic node containig a file input widget, provided data is given with the "value" key.
    """
    node_class_name = "File Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.file_input = pn.widgets.FileInput(width=100)
        self.file_input.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.file_input, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.file_input.value}



class FloatInputNode(WorkflowNode):
    """ Generic node containig a float input widget, provided float is given with the "value" key.
    """
    node_class_name = "Float Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.float_input = pn.widgets.FloatInput(width=100)
        self.float_input.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.float_input, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.float_input.value}



class IntInputNode(WorkflowNode):
    """ Generic node containig a int input widget, provided integer is given with the "value" key.
    """
    node_class_name = "Int Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.int_input = pn.widgets.IntInput(width=100)
        self.int_input.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.int_input, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.int_input.value}



class SelectNode(WorkflowNode):
    """ Generic node containig a select widget, provided chosent item is given with the "value" key. The options are expected from a single connection under the "value" label.
    """
    node_class_name = "Select"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="Options", connection_count_limit=1),
                            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.error_message = pn.pane.Markdown("")
        self.error_message.visible = False

        self.select = pn.widgets.Select(options=[], width=100)
        self.select.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.error_message,
                                    self.select, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        if len(self.plugged_nodes["Options"]) == 1 :
            if "value" in self.plugged_nodes["Options"][0].get_node_json_value():
                options = self.plugged_nodes["Options"][0].get_node_json_value()["value"]
                if type(options) in [list, np.ndarray]:
                    self.select.options = [str(e) for e in options]
                    self.error_message.visible = False
                else:
                    self.select.options = []
                    self.error_message.object = "'options' found in input is not a list."
                    self.error_message.visible = True
            else:
                self.error_message.object = "No 'options' found in input dict."
                self.error_message.visible = True
        else:
            self.select.options = []
            self.error_message.object = "No node plugged in Options port"
            self.error_message.visible = True
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.select.value}



class MultiChoiceNode(WorkflowNode):
    """ Generic node containig a multi select widget, provided chosent item is given with the "value" key. The options are expected from a single connection under the "value" label.
    """
    node_class_name = "Multi Choice"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="Options", connection_count_limit=1),
                            NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.error_message = pn.pane.Markdown("")
        self.error_message.visible = False

        self.multi_choice = pn.widgets.MultiChoice(options=[], width=200)
        self.multi_choice.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.error_message,
                                    self.multi_choice, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        if len(self.plugged_nodes["Options"]) == 1 :
            if "value" in self.plugged_nodes["Options"][0].get_node_json_value():
                options = self.plugged_nodes["Options"][0].get_node_json_value()["value"]
                if type(options) in [list, np.ndarray]:
                    self.multi_choice.options = [str(e) for e in options]
                    self.error_message.visible = False
                else:
                    self.multi_choice.options = []
                    self.error_message.object = "'options' found in input is not a list."
                    self.error_message.visible = True
            else:
                self.error_message.object = "No 'options' found in input dict."
                self.error_message.visible = True
        else:
            self.multi_choice.options = []
            self.error_message.object = "No node plugged in Options port"
            self.error_message.visible = True
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.multi_choice.value}



class TextInputNode(WorkflowNode):
    """ Generic node containig a text input widget, provided text is given with the "value" key.
    """
    node_class_name = "Text Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.OUTPUT, position=PortPosition.RIGHT, name="Output")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.text_input = pn.widgets.TextInput(value="", width=100)
        self.text_input.param.watch(self.update, "value")

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.text_input, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.update_outputs()

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {"value" : self.text_input.value}



class JSONEncoderToString(JSONEncoder):
    """ Special json encoder for numpy types and datetimes """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, tuple) and isinstance(obj[0], datetime.date):
            return [e.isoformat() for e in obj]
        return json.JSONEncoder.default(self, obj)

class PrintInputNode(WorkflowNode):
    """ Node displaying in a JSON pane the provided inputs.
    """
    node_class_name = "Print Input"
    """Node class name, as it will appear in the reactflow side bar."""
    ports:List[NodePort] = [NodePort(direction=PortDirection.INPUT, position=PortPosition.LEFT, name="Input")]
    """List of node ports"""

    def __init__(self, ):
        super().__init__()

        self.json = pn.pane.JSON(object={}, depth=-1, encoder = JSONEncoderToString)

    def create(self, ):
        """Function called by the Reactflow class to instanciate the content of the node
        """
        return pn.layout.Column(
                                    self.json, 
                                    name=self.name, 
                                    align="center",
                                    margin=0
                                )
    
    def update(self, _):
        """Update the node content based on the input ports.

        Parameters
        ----------
        _ : Any
            Event requesting the update
        """
        self.json.object = {
                node.name:node.get_node_json_value() 
                for node in self.plugged_nodes["Input"]
             }

    def get_node_json_value(self):
        """ Returns a dictionnary describing the node content, this dictionnary can be obtain by other nodes in their update call.
        
        Returns
        ----------
        Dict[str, Any]
            Node properties
        """
        return {}

