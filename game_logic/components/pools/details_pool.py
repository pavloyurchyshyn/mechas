import inspect
from mechas.base.parts.detail import BaseDetail
from mechas import details
from mechas.base.exceptions import ThisDetailClassDoesntExist
from game_logic.components.pools.skills_pool import SkillsPool
from common.id_generator import IdGenerator
from common.logger import Logger


class DetailsPool:
    logger = Logger()

    def __init__(self, skills_pool: SkillsPool, seed: int = None):
        self.skills_pool: SkillsPool = skills_pool
        self.details = []
        self.id_to_detail: dict = {}
        self.classes_dict: dict = {}
        self.collect_details_classes()
        self.id_generator = IdGenerator(seed=seed)

    def get_default_details(self, details_set, players_number) -> dict:
        default_details = {}
        self.logger.info(f'Creating default details: {details_set}')
        for i in range(players_number):
            default_details[i] = []
            for detail, num in details_set.items():
                for _ in range(num):
                    unique_id = self.id_generator.get_id()
                    self.add_detail_to_pool(detail, unique_id)
                    default_details[i].append(self.get_detail_by_id(unique_id))
        self.logger.info(f'Default details created: {default_details}')
        return default_details

    def get_class_by_name(self, name):
        return self.classes_dict.get(name)

    def load_details_list(self, details_list: [(str, int), ]):
        """
        List of tuples where first value class name. the second detail id.
        """
        self.details.clear()
        self.id_to_detail.clear()
        self.logger.info(f'Loading list: {len(details_list)} {details_list}')
        for class_name, unique_id in details_list:
            self.add_detail_to_pool(class_name, unique_id)
        self.logger.info(f'Details loaded {self.id_to_detail}')

    def get_detail_by_id(self, unique_id: str) -> BaseDetail:
        return self.id_to_detail.get(unique_id)

    def add_detail_to_pool(self, detail_class_name: str, unique_id: str = None) -> BaseDetail:
        unique_id = self.id_generator() if unique_id is None else unique_id
        detail_class = self.classes_dict.get(detail_class_name)

        if detail_class is None:
            raise ThisDetailClassDoesntExist(detail_class_name)

        detail: BaseDetail = detail_class(unique_id=unique_id)
        self.details.append(detail)
        self.id_to_detail[unique_id] = detail
        for skill in detail.skills:
            self.skills_pool.add_skill(skill, skill.unique_id)

        return detail

    def collect_details_classes(self):
        self.classes_dict.clear()
        for part in inspect.getmembers(details, inspect.isclass):
            self.classes_dict[part[1].name] = part[1]

    def get_dict(self):
        return [(detail.name, unique_id) for unique_id, detail in self.id_to_detail.items()]


if __name__ == '__main__':
    a = DetailsPool(SkillsPool())
    a.collect_details_classes()
    print(a.__dict__)
