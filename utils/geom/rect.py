import inspect

class _Rect(object): 

    def __init__(self, x, y, width, height):
        self._types = inspect.getfullargspec(self.__init__).annotations

        assert 'x'      in self._types
        assert 'y'      in self._types
        assert 'width'  in self._types
        assert 'height' in self._types

        try: 
            self.x      = self._types['x'](x)
            self.y      = self._types['y'](y)
            self.width  = self._types['width'](width)
            self.height = self._types['height'](height)
        except:
            ClassParamsConvertError(self)

        self.validate()

    def __str__(self): 
        return '<Rect (x={}, y={}, {}x{})>'.format(self.x, self.y, 
                                                   self.width, self.height)

    def __norm_types(self): 
        self.x      = self._types['x']     (self.x)
        self.y      = self._types['y']     (self.y)
        self.width  = self._types['width'] (self.width)
        self.height = self._types['height'](self.height)

    def validate(self):
        self.__norm_types()

        assert self.x      >= self._types['x']     (0)
        assert self.y      >= self._types['y']     (0)
        assert self.width  >= self._types['width'] (0)
        assert self.height >= self._types['height'](0)

    def __iter__(self): 
        self.validate()
        yield self.x
        yield self.y
        yield self.x + self.width 
        yield self.y + self.height
        self.validate()
    
    def area(self): 
        self.validate()

        return self.width * self.height


class Rect(_Rect): 

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height) 


class RectF(_Rect): 

    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__(x, y, width, height) 
        