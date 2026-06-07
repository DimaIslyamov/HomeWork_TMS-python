class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = None
        self.pepperoni = None
        self.mushrooms = None
        self.onions = None
        self.bacon = None

    def __str__(self):
        return (
            f"Pizza size '{self.size}' ingredients: "
            f"cheese: {self.cheese}, "
            f"pepperoni: {self.pepperoni}, "
            f"mushrooms: {self.mushrooms}, "
            f"onions: {self.onions}, "
            f"beacon: {self.bacon}"
        )
