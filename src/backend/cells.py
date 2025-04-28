from abc import ABC, abstractmethod
class Cell(ABC):
    @abstractmethod
    def evolve(self, neighbors:list):
        ...

    def chance(self):
        ...

class Water(Cell):
    '''
    Class for water cells
    '''
    def evolve(self, neighbors:list):
        ...

class Sand(Cell):
    '''
    Class for send cells
    '''
    def evolve(self, neighbors:list):
        ...

class Forest(Cell):
    '''
    Class for forest cells
    '''
    def evolve(self, neighbors:list):
        ...

class Void(Cell):
    '''
    Class for void cells
    '''
    def evolve(self, neighbors:list):
        ...

class Grass(Cell):
    '''
    Class for grass cells
    '''
    def evolve(self, neighbors:list):
        ...

class Plateau(Cell):
    '''
    Class for grass cells
    '''
    def evolve(self, neighbors:list):
        ...