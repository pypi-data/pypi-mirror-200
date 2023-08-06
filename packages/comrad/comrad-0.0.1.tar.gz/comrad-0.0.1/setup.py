# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comrad', 'comrad.app', 'comrad.util', 'pyodide_dill']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.6,<0.4.0',
 'jinja2>=3.1.2,<4.0.0',
 'prpc-python[cli]>=0.9.1,<0.10.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0']

extras_require = \
{'examples': ['pandas>=1.5.2,<2.0.0', 'numpy>=1.23.5,<2.0.0'],
 'jupyter': ['jupyterlab>=3.6.0,<4.0.0',
             'matplotlib>=3.5.2,<4.0.0',
             'tqdm>=4.64.1,<5.0.0',
             'openpyxl>=3.1.0,<4.0.0',
             'plotly>=5.13.0,<6.0.0'],
 'pyodide': ['openpyxl>=3.1.0,<4.0.0', 'plotly>=5.13.0,<6.0.0'],
 'web': ['flask>=2.2.2,<3.0.0', 'flask-cors>=3.0.10,<4.0.0']}

entry_points = \
{'prpc_python': ['d2i-patch = d2i_patch.api:app']}

setup_kwargs = {
    'name': 'comrad',
    'version': '0.0.1',
    'description': 'A framework for quickly deploying simple Python applications.',
    'long_description': '# CoMRAD Framework - Component-MVC Rapid Appliction Driven Framework \n\n![CoMRAD Logo - Panda and Python hugging](docs/images/CoMRAD.jpeg)\n\n\n## Opinionated, Component-Driven MVC Framework For Data Apps\n\n* **Router** - This is the entry point for the application. It is responsible for routing the request to the appropriate controller and action. It also handles the response from the controller and sends it back to the client.\n\n* **Session** - This is the application state. A simple key-value store. Custom class can be provided but has to behave like a dict\n\n* **Model** - This is the current view state. It is a key-value store. It is updated by the controller and used by the view to render the current view of the application. \n\n* **Controller** - Provides the business logic for the application. It is responsible for handling the request and returning the response. It updates the model from the current request, and then returns the appropriate response, which can either be a view, and error or a redirect (full semantics of HTTP Response should be possible - but for now we will only support 200, 302, 400, 404, 500)\n\n* **View** - This is the presentation layer. It is responsible for rendering the model to the client. For PATCh this will be a set of patch components.\n\n* **Component** - A component is a part of a view. It is responsible for sending the information to the front end required for the component to render. It is also responsible for updating the model with the current state of the component. It can also indicate if it is complete or if there are any errors.\n\n* **Page** - A page is a semantic structure to help configuration. It combines a view and a controller representing a single page in the application. We provide default configuration, such as requiring all input components with a required flag to be filled in before the controller redirects to the next view.\n\n* **Application** - This is the top level object. It is responsible for configuring the application. It is responsible for creating the router, model, controller and view. It is also responsible for creating the page objects and configuring them.\n\nIn our standard application, each view must have a unique \'name\' used for the routing. The first view should always be called \'index\'. \n\nThe current view name is stored in the session under the key \'view\'. \n\nEach view has a controller associated with it. The controller is responsible for updating the model with the current state of the application. Then making a decision as to whether to render the view or redirect to another view.\n\nTo keep configuration to a minimum, components can be \'smart\' and manage their own state. For example, a text input component can manage its own value. This means that the controller does not need to update the model with the current value of the input component. This is a trade off between configuration and flexibility. Of course, the controller can override any changes made by the component.\n\nSimilarly a component can indicate if it\'s "complete", i.e. that its state is fully configured or it can flag any errors relating to the state of the component. \n\nThe default controller will pass over all components and check if they are complete. If all components are complete and there are no errors, then the controller will redirect to the next view. \n\nSome Pages may be \'final\', i.e. they represent the end-point of a flow. In this case, the controller will not redirect to the next view, but instead will re-render the current view.\n\nA very simple configuration may look like:\n\n```python\nfrom patch import Application, Page, TextInput, Button, Paragraph\n\napp = Application()\n\napp.add_page(Page(\n    name=\'index\',\n    controller={\'next\': \'greeting\'},\n    components=[TextInput(name=\'name\', required=True)],\n))\n\ndef reset_handler(session, model, request):\n    """\n    This function is called when the user clicks the button.\n\n    Buttons are automatically submitted to the server, unless `submit=False` \n    is set on the Button.\n    """\n    model.clear()\n\ndef render_greeting_page(session, model, request):\n    """\n    Instead of providing a fixed list of components, we can also set a function\n    that will be used to decide which components to show, and their configuration.\n    """\n    return [\n        Paragraph(f\'Hello {model[\'name\']}\'),\n        Button(\'Back\', handler=action_reset)\n        ]\n\napp.add_page(Page(\n    name=\'greeting\',\n    components=say_hello,\n))\n```\n\nSome components can also take a render function. For a chart\ncomponent, for example, the render function would be called when the controller asks the component to update the model and state\nand convert the response to an object suitable for the front-end to render.\n\n```python\n\n## Standard components:\n\n* Button - a clickable button that either sets a value in the model or runs a handler function\n\n* ButtonBar - a layout component that renders a set of buttons in a row\n\n* Chart - a component that renders a chart - the chart is\n\n* Checkbox - a component that renders a checkbox\n\n* DateSelect - a component that renders a date picker\n\n* Expando - an expanding section of the page\n\n* FileUpload - a component that renders a file upload\n\n* Fragment - a single component that can hold others but is itself invisible\n\n* Paragraph - a component that renders a paragraph of text\n\n* Select - a component that renders a select box\n\n* TextInput - a component that renders a text input\n\n',
    'author': 'Kaj Siebert',
    'author_email': 'kaj@k-si.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
