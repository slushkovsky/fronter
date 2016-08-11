import inspect

class _Point(object): 

    def __init__(self, x, y): 
        self._types = inspect.getfullargspec(self.__init__).annotations

        assert 'x' in self._types
        assert 'y' in self._types

        try: 
            self.x = self._types['x'](x)
            self.y = self._types['y'](y)
        except:
            ClassParamsConvertError(self)

        self.validate()

    def __str__(self): 
        return '<Point x={}, y={}>'.format(self.x, self.y)

    def __norm_types(self): 
        self.x      = self._types['x'](self.x)
        self.y      = self._types['y'](self.y)

    def validate(self):
        self.__norm_types()

        assert self.x >= self._types['x'](0)
        assert self.y >= self._types['y'](0) 


class Point(_Point):

    def __init__(self, x: int, y: int): 
        super().__init__(x, y)


class PointF(_Point):

    def __init__(self, x: float, y: float): 
        super().__init__(x, y)