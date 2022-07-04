

class SkillsPool:
    def __init__(self):
        self.skills = []
        self.id_to_skill: dict = {}

    def get_skill_by_id(self, unique_id):
        return self.id_to_skill.get(unique_id)

    def add_skill(self, skill, unique_id):
        self.id_to_skill[unique_id] = skill
