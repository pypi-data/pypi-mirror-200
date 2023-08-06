class AttrDict:
    def __init__(self, input=None, **kwargs):
        if input:
            assert type(input) == dict, f"invalid input type {type(input)}: only dict is available"
            for key, value in input.items():
                assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
                self.__dict__[key] = self._deep_convert(value)

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
            return AttrDict(value)            
        else:
            return value
    
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, input):
        return cls(input)
    
    def __getattr__(self, key):
        return None # fallback to None if key not exists in self.__dict__
    
    def __setattr__(self, key, value):
        assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
        if type(value) == dict:
            value = AttrDict(value)
        self.__dict__[key] = value
        
    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None
    
    def __setitem__(self, key, value):
        assert type(key) in [int, str], f"invalid key type {type(key)} : only int, str are available"
        if type(value) == dict:
            value = AttrDict(value)
        self.__dict__[key] = value
        
    def __delitem__(self, key):
        del self.__dict__[key]
    
    def __repr__(self):
        dict_str = [ repr(key) + ": " + repr(value) for key, value in self.__dict__.items() ]
        return "{" + ', '.join(dict_str) + "}"
    
    def __str__(self):
        return self.__repr__()
    
    def __len__(self):
        return len(self.__dict__)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def __iter__(self):
        return iter(self.__dict__)
    
    def __contains__(self, key):
        return key in self.__dict__
    
    def __copy__(self):
        return AttrDict(self.__dict__)
    
    def __deepcopy__(self, memo):
        return AttrDict(self.__dict__)
    
    def __add__(self, other):
        assert type(other) in [AttrDict, dict], f"invalid type {type(other)}: only AttrDict, dict are available"
        if type(other) == dict:
            other = AttrDict(other)
        return AttrDict(self.__dict__.update(other.__dict__))
    
    def __iadd__(self, other):
        assert type(other) in [AttrDict, dict], f"invalid type {type(other)}: only AttrDict, dict are available"
        if type(other) == dict:
            other = AttrDict(other)
        self.__dict__.update(other.__dict__)
        return self
    
    def __sub__(self, other):
        assert type(other) in [AttrDict, dict], f"invalid type {type(other)}: only AttrDict, dict are available"
        if type(other) == dict:
            other = AttrDict(other)
        return AttrDict({key: value for key, value in self.__dict__.items() if key not in other.__dict__})
    
    def __isub__(self, other):
        assert type(other) in [AttrDict, dict], f"invalid type {type(other)}: only AttrDict, dict are available"
        if type(other) == dict:
            other = AttrDict(other)
        self.__dict__ = {key: value for key, value in self.__dict__.items() if key not in other.__dict__}
        return self

    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()
    
    def items(self):
        return self.__dict__.items()
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    def pop(self, key, default=None):
        return self.__dict__.pop(key, default)
    
    def popitem(self):
        return self.__dict__.popitem()
    
    def clear(self):
        self.__dict__.clear()

    def update(self, other):
        assert type(other) in [AttrDict, dict], f"invalid type {type(other)}: only AttrDict, dict are available"
        if type(other) == dict:
            other = AttrDict(other)
        self.__dict__.update(other.__dict__)

    def setdefault(self, key, default=None):
        return self.__dict__.setdefault(key, default)
    
    def copy(self):
        return AttrDict(self.__dict__)
    
    def deepcopy(self):
        return AttrDict(self.__dict__)