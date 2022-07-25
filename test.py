import random
import pprint

participants = {'Dima': 200,
                'Edik': 199,
                'Pavlo': 100,
                'Oleksii': 1,
                }


def build_list():
    big_list = []

    summary_count = sum(participants.values())
    prev_name = ''
    while summary_count:
        names_list = [name for name, points in participants.items() if points > 0]
        if len(names_list) == 1:
            name = names_list[0]
            index = random.randrange(0, len(big_list) - 1)
            big_list.insert(index, name)
            participants[name] -= 1
            summary_count -= 1

        else:
            name = random.choice(names_list)
            if name != prev_name:
                big_list.append(name)
                participants[name] -= 1
                summary_count -= 1
                prev_name = name

    return big_list


if __name__ == '__main__':
    list_ = build_list()
    pprint.pprint(list_)
    print(len(list_))
