class Features:
    def __init__(self, title=None, story=None, created=0, goal=0, category=0, finished=0):
        self.title = title
        self.story = story
        self.created = created
        self.goal = goal
        self.category = category
        self.finished = finished

class Data:
    def __init__(self, features=Features(), result=0):
        self.features = features
        self.result = result
