import builtins

_decoration = {
    'bold': '1',
    'underline': '4',
    'blink': '5',
    'reverse': '7',
}
_color = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
}
_background = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'magenta': '45',
    'cyan': '46',
    'white': '47',
}
_intense = {
    'black': '90',
    'red': '91',
    'green': '92',
    'yellow': '93',
    'blue': '94',
    'magenta': '95',
    'cyan': '96',
    'white': '97'
}
_background_intense = {
    'black': '100',
    'red': '101',
    'green': '102',
    'yellow': '103',
    'blue': '104',
    'magenta': '105',
    'cyan': '106',
    'white': '107'
}
_reset = '0'

def _setStyle(color=None, background=None, intense=False, background_intense=False, bold=False, underline=False, blink=False, reverse=False):
    styles = []
    if bold:
        styles.append(_decoration['bold'])
    if underline:
        styles.append(_decoration['underline'])
    if blink:
        styles.append(_decoration['blink'])
    if reverse:
        styles.append(_decoration['reverse'])
    if color is not None:
        color = color.lower()
        if color not in _color.keys():
            raise ValueError(f"Invalid color: {color}")
        
        if intense:
            styles.append(_intense[color])
        else:
            styles.append(_color[color])
    if background is not None:
        background = background.lower()
        if background not in _background.keys():
            raise ValueError(f"Invalid background: {background}")

        if background_intense:
            styles.append(_background_intense[background])
        else:
            styles.append(_background[background])
    
    if len(styles) == 0:
        styles.append(_reset)

    return f"\033[{';'.join(styles)}m"

def _resetStyle():
    return f"\033[{_reset}m"

class HKPrintTheme:
    def __init__(self):
        self.theme = {
            "success": {
                "color": "green",
                "background": None,
                "intense": False,
                "background_intense": False,
                "bold": False,
                "underline": False,
                "blink": False,
                "reverse": False
            },
            "error": {
                "color": "red",
                "background": None,
                "intense": False,
                "background_intense": False,
                "bold": False,
                "underline": False,
                "blink": False,
                "reverse": False
            },
            "warning": {
                "color": "yellow",
                "background": None,
                "intense": False,
                "background_intense": False,
                "bold": False,
                "underline": False,
                "blink": False,
                "reverse": False
            },
            "info": {
                "color": "cyan",
                "background": None,
                "intense": False,
                "background_intense": False,
                "bold": False,
                "underline": False,
                "blink": False,
                "reverse": False
            },
            "debug": {
                "color": None,
                "background": None,
                "intense": False,
                "background_intense": False,
                "bold": False,
                "underline": False,
                "blink": False,
                "reverse": False
            }
        }
        self._default_style = {
            "color": None,
            "background": None,
            "intense": False,
            "background_intense": False,
            "bold": False,
            "underline": False,
            "blink": False,
            "reverse": False
        }

    def setStyle(self, styleName, styleDict):
        assert isinstance(styleDict, dict), f"Invalid param:styleDict - {styleDict}"
        
        if styleName in self.theme.keys():
            defaultStyle = self.theme[styleName]
        else:
            defaultStyle = self._default_style

        if "color" in styleDict.keys():
            assert styleDict["color"].lower() in _color.keys(), f"Invalid value:styleDict.color - {styleDict['color']}"
            defaultStyle["color"] = styleDict["color"].lower()
        
        if "background" in styleDict.keys():
            assert styleDict["background"].lower() in _background.keys(), f"Invalid value:styleDict.background - {styleDict['background']}"
            defaultStyle["background"] = styleDict["background"].lower()
        
        if "intense" in styleDict.keys():
            assert isinstance(styleDict["intense"], bool), f"Invalid value:styleDict.intense - {styleDict['intense']}"
            defaultStyle["intense"] = styleDict["intense"]

        if "background_intense" in styleDict.keys():
            assert isinstance(styleDict["background_intense"], bool), f"Invalid value:styleDict.background_intense - {styleDict['background_intense']}"
            defaultStyle["background_intense"] = styleDict["background_intense"]
        
        if "bold" in styleDict.keys():
            assert isinstance(styleDict["bold"], bool), f"Invalid value:styleDict.bold - {styleDict['bold']}"
            defaultStyle["bold"] = styleDict["bold"]
        
        if "underline" in styleDict.keys():
            assert isinstance(styleDict["underline"], bool), f"Invalid value:styleDict.underline - {styleDict['underline']}"
            defaultStyle["underline"] = styleDict["underline"]

        if "blink" in styleDict.keys():
            assert isinstance(styleDict["blink"], bool), f"Invalid value:styleDict.blink - {styleDict['blink']}"
            defaultStyle["blink"] = styleDict["blink"]

        if "reverse" in styleDict.keys():
            assert isinstance(styleDict["reverse"], bool), f"Invalid value:styleDict.reverse - {styleDict['reverse']}"
            defaultStyle["reverse"] = styleDict["reverse"]

        self.theme[styleName] = defaultStyle            

def _print_template(*args, style, **kwargs):
    if len(args) > 0:
        args = list(args)
        args[0] = _setStyle(**style) + str(args[0])
        args[-1] = str(args[-1]) + _resetStyle()
        args = tuple(args)
    builtins.print(*args, **kwargs)

class HKPrint:
    def __init__(self, theme=None):
        assert theme is None or isinstance(theme, HKPrintTheme), f"Invalid param:theme - {theme}"
        
        if theme is None:
            self.theme = HKPrintTheme().theme
        else:
            self.theme = theme.theme
        
        for method_name in reversed(self.theme):
            setattr(self.__class__, method_name, lambda cls, *args, style=self.theme[method_name], **kwargs: _print_template(*args, style=style, **kwargs))
        
    def __call__(self, *args, **kwargs):
        builtins.print(*args, **kwargs)
