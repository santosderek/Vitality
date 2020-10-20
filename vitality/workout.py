class Workout:
    def __init__(self, w_name, difficulty, w_id, about, exp_rewards):
        self.w_name = w_name
        self.difficulty = difficulty
        self.w_id = w_id
        self.about = about
        self.exp_rewards = exp_rewards

    def as_dict(self):
        return {
            "w_name" : self.w_name,
            "difficulty" : self.difficulty,
            "w_id" : self.w_id,
            "about" : self.about,
            "exp_rewards" : self.exp_rewards
        }