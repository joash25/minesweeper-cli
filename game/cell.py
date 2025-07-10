class Cell:
    """
    Represents a single cell in the game board

    Each cell has:
    - a `visible` property that determines if it is revealed to the player
    - a `value` which can be any integer >= -1 (e.g., -1 for a mine, 
      or a number indicating nearby mines)
    """

    def __init__(self, visible: bool = False, value: int = 0) -> None:
        self.visible = visible  
        self.value = value

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, _visible: bool) -> None:
        if not isinstance(_visible, bool):
            raise TypeError(
                f"Invalid type for 'visible' in {self.__class__.__name__}"
                f": expected bool, got {type(_visible).__name__}")

        self._visible = _visible

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, _value: int) -> None:
        if not isinstance(_value, int):
            raise TypeError(
                f"Invalid type for 'value' in {self.__class__.__name__}"
                f": expected int, got {type(_value).__name__}")
        
        if _value < -1:
            raise ValueError(
                f"Invalid value for 'value' in {self.__class__.__name__}"
                f": must be >= -1, got {_value}")
        
        self._value = _value
