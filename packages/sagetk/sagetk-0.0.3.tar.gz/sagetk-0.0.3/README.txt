The sagetk Python module

sagetk is a Python module for creating GUI applications using a HTML and CSS like syntax . It is built on top of classical tkinter library and provides a high-level interface for defining widgets, handling events, and managing application state.


INSTALLATIONS:

sagetk can be installed using pip:

pip install sagetk

It depends on few other packages, including,  pillow and html.parser, which will also be installed automatically.

USAGE

The basic usage of sagetk involves defining a document object that describes the structure and content of the GUI using a markup language similar to HTML. This document can include various widgets, such as buttons, labels, text areas, menus, and tables, as well as event handlers that respond to user interactions with the widgets.

Once the document is defined, it can be displayed in a window by calling the document() function from the sagetk module that serves the document and handles user interactions, such as clicks, key presses, and mouse movements.

The run() function can then be called to start the event loop and handle these interactions. This function blocks until the user closes the window or the program exits.


DOCUMENTATIONS

The sagetk module includes comprehensive documentation that covers the various widgets, events, functions, and classes available in the library. The documentation is available online at http://sagetk.atspace.cc, and can also be accessed programmatically using the help() function in Python.

EXAMPLES

The sagetk module includes several examples that demonstrate the usage and capabilities of the library. These examples cover a wide range of GUI applications, from simple calculators and text editors to more complex data analysis tools and scientific simulations.

The examples are located in the examples directory of the sagetk source distribution, and can be run by executing the corresponding Python scripts. They can also be used as templates or starting points for building custom GUI applications using sagetk.

//CREATING BUTTON
import sagetk as tk
tk.g=globals()
doc=""" 
<root>
<title>my app</title>
<button onclick="alert('hello world')">Click here</button>
</root>  
"""
tk.document(doc)
tk.run()


//CREATING INPUTS
import sagetk as tk
tk.g=globals()
doc=""" 
<root>
<title>my app</title>
<input type="text"></input>
</root>  
"""
tk.document(doc)
tk.run()


//CREATING TABLE
import sagetk as tk
tk.g=globals()
doc=""" 
<root>
<title>my app</title>
<table>
<tr>
<th>name</th>
<th>age</th>
</tr>
<tr>
<td>Mark</td>
<td>77</td>
</tr>
</table>
</root>  
"""
tk.document(doc)
tk.run()


//CREATING Menu
import sagetk as tk
tk.g=globals()
doc=""" 
<root>
<title>my app</title>
<menu>
<mi label=file>
<md onclick="func">open</md>
<sp></sp>
<md>save as</md>
</mi>
<mi label=edit>
<md alt="ctrl + x">cut</md>
<sp></sp>
<md alt="ctrl + c">copy</md>
</mi>
</menu>
</root>  
"""
tk.document(doc)
tk.run()





