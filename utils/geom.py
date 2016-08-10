from selenium.webdriver.remote.webelement import WebElement   

from . import exc

class Point(object):

    def __init__(self, x: float, y: float):
        try: 
            self.x = float(x)
            self.y = float(y)
        except ValueError: 
            raise ClassParamsConvertError(self)

        self.is_ok()

    def is_ok(self): 
        assert self.x >= 0 
        assert self.y >= 0


class Rect(object): 

    def __init__(self, x: float, y: float, width: float, height: float): 
        try: 
            self.x      = float(x)
            self.y      = float(y)
            self.width  = float(width)
            self.height = float(height)
        except ValueError: 
            raise ClassParamsConvertError(self)

        self.is_ok()


    def __iter__(self): 
        self.is_ok()

        yield self.x
        yield self.y
        yield self.x + self.width 
        yield self.y + self.height

        self.is_ok()


    def is_ok(self): 
        assert self.x      >= 0.0 
        assert self.y      >= 0.0
        assert self.width  >= 0.0
        assert self.height >= 0.0


    def area(self) -> float: 
        self.is_ok()
        return self.width * self.height


    @classmethod
    def from_selenium_element(cls, elem):
        assert isinstance(elem, WebElement)

        return cls(x     =elem.location['x'],
                   y     =elem.location['y'],
                   width =elem.size['width'],
                   height=elem.size['height']) 
 