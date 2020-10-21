class Workout:
    def __init__(self, id, creator_id, name, difficulty="easy", about=None, exp_rewards=None):
        self.id = id
        self.creator_id = creator_id
        self.name = name
        self.difficulty = difficulty
        self.about = about
        self.exp_rewards = exp_rewards


    def as_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "name": self.name,
            "difficulty": self.difficulty,
            "about": self.about,
            "exp_rewards": self.exp_rewards,
        }