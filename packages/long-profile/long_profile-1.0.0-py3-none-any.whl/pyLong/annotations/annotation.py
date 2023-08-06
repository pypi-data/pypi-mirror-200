class Annotation:
    def __init__(self):
        self._name = ""

        self._opacity = 1.

        self._order = 1

        self._visible = True

        self._active = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        if isinstance(opacity, (int, float)):
            if 0 <= opacity <= 1:
                self._opacity = opacity

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        if isinstance(order, int):
            if 0 < order:
                self._order = order

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if isinstance(active, bool):
            self._active = active