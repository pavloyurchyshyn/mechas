from obj_properties.rect_form import Rectangle


class VisualSlot(Rectangle):
    def __init__(self, x, y, size, slot):
        super(VisualSlot, self).__init__(x=x, y=y, size_x=size)
        self.slot = slot

    @property
    def is_full(self):
        return self.slot.is_full


class BodyVisualSlot(Rectangle):
    def __init__(self, x, y, size, body=None):
        super(BodyVisualSlot, self).__init__(x=x, y=y, size_x=size)
        self.body = body

    @property
    def is_full(self):
        return self.body is not None
