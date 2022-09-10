from Action import Action

class ActionsList:
    def __init__(self, data):
        self.data = data
        self.actions = [Action(x) for x in self.data]

    def CanNotReachHandler(self, target):
        for act in self.actions:
            act.CanNotReachHandler(target)