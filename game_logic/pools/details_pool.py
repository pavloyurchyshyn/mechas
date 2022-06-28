import inspect
from mechas.base.parts.detail import BaseDetail
from common.id_generator import get_unique_id
from mechas import details
from mechas.base.exceptions import ThisDetailClassDoesntExists


class DetailsPool:
    def __init__(self):
        self.details = []
        self.id_to_detail: dict = {}
        self.classes_dict: dict = {}
        self.collect_details_classes()

    def load_details_list(self, details_list: [(str, int), ]):
        """
        List of tuples where first value class name. the second detail id.
        """
        for class_name, unique_id in details_list:
            self.add_detail_to_pool(class_name, unique_id)

    def get_detail_by_id(self, unique_id) -> BaseDetail or None:
        return self.id_to_detail.get(unique_id)

    def add_detail_to_pool(self, detail_class_name: str, unique_id: int = None) -> BaseDetail:
        unique_id = get_unique_id() if unique_id is None else unique_id
        detail_class = self.classes_dict.get(detail_class_name)

        if detail_class is None:
            raise ThisDetailClassDoesntExists(detail_class_name)

        detail = detail_class(unique_id=unique_id)
        self.details.append(detail)
        self.id_to_detail[unique_id] = detail

        return detail

    def collect_details_classes(self):
        self.classes_dict.clear()
        for part in inspect.getmembers(details, inspect.isclass):
            self.classes_dict[part[1].name] = part[1]


if __name__ == '__main__':
    a = DetailsPool()
    a.collect_details_classes()
    print(a.__dict__)
