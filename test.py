import pickle


class TestObj():
    def __init__(self):
        self.a = {'1': 2}

    def print(self):
        print('============== all ok', self.a)



data = pickle.dumps(TestObj())
print(data)
data = pickle.loads(data)
print(data)
data.print()
