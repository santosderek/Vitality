class Workout:
    def __init__(self, name, difficulty, id, about=None, exp_rewards=None):
        self.name = name
        self.difficulty = difficulty
        self.id = id
        self.about = about
        self.exp_rewards = exp_rewards

    def as_dict(self):
        return {
            "name" : self.name,
            "difficulty" : self.difficulty,
            "id" : self.id,
            "about" : self.about,
            "exp_rewards" : self.exp_rewards
        }