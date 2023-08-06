# CoMRAD Framework - Component-MVC Rapid Appliction Driven Framework 

![CoMRAD Logo - Panda and Python hugging](docs/images/CoMRAD.jpeg)


## Opinionated, Component-Driven MVC Framework For Data Apps

* **Router** - This is the entry point for the application. It is responsible for routing the request to the appropriate controller and action. It also handles the response from the controller and sends it back to the client.

* **Session** - This is the application state. A simple key-value store. Custom class can be provided but has to behave like a dict

* **Model** - This is the current view state. It is a key-value store. It is updated by the controller and used by the view to render the current view of the application. 

* **Controller** - Provides the business logic for the application. It is responsible for handling the request and returning the response. It updates the model from the current request, and then returns the appropriate response, which can either be a view, and error or a redirect (full semantics of HTTP Response should be possible - but for now we will only support 200, 302, 400, 404, 500)

* **View** - This is the presentation layer. It is responsible for rendering the model to the client. For PATCh this will be a set of patch components.

* **Component** - A component is a part of a view. It is responsible for sending the information to the front end required for the component to render. It is also responsible for updating the model with the current state of the component. It can also indicate if it is complete or if there are any errors.

* **Page** - A page is a semantic structure to help configuration. It combines a view and a controller representing a single page in the application. We provide default configuration, such as requiring all input components with a required flag to be filled in before the controller redirects to the next view.

* **Application** - This is the top level object. It is responsible for configuring the application. It is responsible for creating the router, model, controller and view. It is also responsible for creating the page objects and configuring them.

In our standard application, each view must have a unique 'name' used for the routing. The first view should always be called 'index'. 

The current view name is stored in the session under the key 'view'. 

Each view has a controller associated with it. The controller is responsible for updating the model with the current state of the application. Then making a decision as to whether to render the view or redirect to another view.

To keep configuration to a minimum, components can be 'smart' and manage their own state. For example, a text input component can manage its own value. This means that the controller does not need to update the model with the current value of the input component. This is a trade off between configuration and flexibility. Of course, the controller can override any changes made by the component.

Similarly a component can indicate if it's "complete", i.e. that its state is fully configured or it can flag any errors relating to the state of the component. 

The default controller will pass over all components and check if they are complete. If all components are complete and there are no errors, then the controller will redirect to the next view. 

Some Pages may be 'final', i.e. they represent the end-point of a flow. In this case, the controller will not redirect to the next view, but instead will re-render the current view.

A very simple configuration may look like:

```python
from patch import Application, Page, TextInput, Button, Paragraph

app = Application()

app.add_page(Page(
    name='index',
    controller={'next': 'greeting'},
    components=[TextInput(name='name', required=True)],
))

def reset_handler(session, model, request):
    """
    This function is called when the user clicks the button.

    Buttons are automatically submitted to the server, unless `submit=False` 
    is set on the Button.
    """
    model.clear()

def render_greeting_page(session, model, request):
    """
    Instead of providing a fixed list of components, we can also set a function
    that will be used to decide which components to show, and their configuration.
    """
    return [
        Paragraph(f'Hello {model['name']}'),
        Button('Back', handler=action_reset)
        ]

app.add_page(Page(
    name='greeting',
    components=say_hello,
))
```

Some components can also take a render function. For a chart
component, for example, the render function would be called when the controller asks the component to update the model and state
and convert the response to an object suitable for the front-end to render.

```python

## Standard components:

* Button - a clickable button that either sets a value in the model or runs a handler function

* ButtonBar - a layout component that renders a set of buttons in a row

* Chart - a component that renders a chart - the chart is

* Checkbox - a component that renders a checkbox

* DateSelect - a component that renders a date picker

* Expando - an expanding section of the page

* FileUpload - a component that renders a file upload

* Fragment - a single component that can hold others but is itself invisible

* Paragraph - a component that renders a paragraph of text

* Select - a component that renders a select box

* TextInput - a component that renders a text input

