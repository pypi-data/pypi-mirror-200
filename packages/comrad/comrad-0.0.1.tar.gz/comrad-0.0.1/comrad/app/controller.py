class Controller:
    def __init__(self, model: dict) -> None:
        self.model = model

    def do(self):
        """do next step: render the view or redirect to another view"""
        pass

    def update(self):
        """update the model with the current state of the application"""
        pass
