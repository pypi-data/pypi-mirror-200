class AttrDict:
    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
                self.__dict__[key] = self._deep_convert(value)
    
    def _deep_convert(self, value):
        if type(value) == list:
            return [self._deep_convert(x) for x in value]
        elif type(value) == set:
            return {self._deep_convert(x) for x in value}
        elif type(value) == dict:
            return AttrDict(**value)            
        else:
            return value
        
    @classmethod
    def from_dict(cls, input):
        assert type(input) == dict, f"invalid input type {type(input)}: only dict is available"
        return cls(**input)
    
    def __getattr__(self, key):
        return None # fallback to None if key not exists in self.__dict__
    
    def __setattr__(self, key, value):
        assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
        if type(value) == dict:
            value = AttrDict(**value)
        self.__dict__[key] = value
        
    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None
    
    def __setitem__(self, key, value):
        assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
        if type(value) == dict:
            value = AttrDict(**value)
        self.__dict__[key] = value
        
    def __delitem__(self, key):
        del self.__dict__[key]
    
    def __repr__(self):
        dict_str = [ repr(key) + ": " + repr(value) for key, value in self.__dict__.items() ]
        return "{" + ', '.join(dict_str) + "}"
    
    def __str__(self):
        return self.__repr__()
    
    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()
    
    def items(self):
        return self.__dict__.items()