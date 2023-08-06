def escape(x: str):
    """Escapes most of the escape sequence in a string"""
    return x.replace("\n", "\\n"
        ).replace("\r", "\\r"
        ).replace("\t", "\\t"
        ).replace("\"", "\\\""
        ).replace("\\", "\\\\"
        ).replace("\b", "\\b")

def appropriate_snbt_type(x):
    if type(x) == bool: return SNBTBool(x)
    elif type(x) == str: return SNBTString(x)
    elif type(x) == dict: return SNBTCompound(x)
    elif type(x) == list:
        try: return SNBTByteArray(x)
        except ValueError:
            try: return SNBTIntArray(x)
            except ValueError:
                try: return SNBTLongArray(x)
                except ValueError:
                    return SNBTList(x)
    elif int(x) == x:
        try: return SNBTByte(x)
        except ValueError:
            try: return SNBTShort(x)
            except ValueError:
                try: return SNBTInt(x)
                except ValueError: return SNBTLong(x)
    elif type(x) == float:
        try: return SNBTFloat(x)
        except ValueError: return SNBTDouble(x)
    elif type(x).__name__.startswith("SNBT"):
        return x

apprsnbtype = appropriate_snbt_type

class SNBTByte:
    """Creates a byte SNBT value"""
    def __init__(self, x: int):
        if x in range(int(-2**7), int(2**7)):
            self.x = x
        else:
            raise ValueError(
                f"Input {x} is not in the range of byte."
            )
    def dump(self):
        return f"{self.x}b"

class SNBTBool:
    """Creates a boolean SNBT value"""
    def __init__(self, x: int | bool):
        if x in (0, 1, True, False):
            self.x = int(x)
        else:
            raise ValueError(
                f"Input {x} is not in the range of boolean."
            )
    def dump(self):
        return f"{self.x}b"

class SNBTShort:
    """Creates a short SNBT value"""
    def __init__(self, x):
        if x in range(int(-2**15), int(2**15)):
            self.x = x
        else:
            raise ValueError(
                f"Input {x} is not in the range of short."
            )
    def dump(self):
        return f"{self.x}s"

class SNBTInt:
    """Creates an integer SNBT value"""
    def __init__(self, x: int):
        if x in range(int(-2**31), int(2**31)):
            self.x = x
        else:
            raise ValueError(
                f"Input {x} is not in the range of integer."
            )
    def dump(self):
        return f"{self.x}"

class SNBTLong:
    """Creates a long SNBT value"""
    def __init__(self, x: int):
        if x in range(int(-2**63), int(2**63)):
            self.x = x
        else:
            raise ValueError(
                f"Input {x} is not in the range of long."
            )
    def dump(self):
        return f"{self.x}l"

class SNBTFloat:
    """Creates a float SNBT value"""
    def __init__(self, x: float):
        if -3.4E38 <= x < 3.4E38:
            self.x = x
        else:
            raise ValueError(
                f"Input {x} is not in the range of float."
            )
    def dump(self):
        return f"{self.x}f"

class SNBTDouble:
    """Creates a double SNBT value"""
    def __init__(self, x: float):
        self.x = x
    def dump(self):
        return f"{self.x}d"

class SNBTString:
    """Creates a string SNBT value"""
    def __init__(self, x: str):
        self.x = escape(x)
    def dump(self):
        return f"\"{self.x}\""

class SNBTList:
    """Creates a list SNBT value"""
    def __init__(self, x: list):
        self.x = [apprsnbtype(i) for i in x]
    def dump(self):
        return f"[{','.join([i.dump() for i in self.x])}]"

class SNBTCompound:
    """Creates a compound SNBT value"""
    def __init__(self, x: dict):
        self.keys = [escape(str(i)) for i in x.keys()]
        self.values = [apprsnbtype(i) for i in x.values()]
    def dump(self):
        return "{" + ",".join([f"\"{k}\":{v.dump()}" for k, v in zip(self.keys, self.values)]) + "}"

class SNBTByteArray:
    """Creates a byte array SNBT value"""
    def __init__(self, x: list):
        if all([type(apprsnbtype(i)) == SNBTByte for i in x]):
            self.x = x
        else:
            raise ValueError(
                f"Not all items in input {x} matches a byte."
            )
    def dump(self):
        return f"[B;{SNBTList(self.x).dump()[1:]}"

class SNBTIntArray:
    """Creates a int array SNBT value"""
    def __init__(self, x: list):
        if all([type(apprsnbtype(i)) == SNBTInt for i in x]):
            self.x = x
        else:
            raise ValueError(
                f"Not all items in input {x} matches an integer."
            )
    def dump(self):
        return f"[I;{SNBTList(self.x).dump()[1:]}"

class SNBTLongArray:
    """Creates a long array SNBT value"""
    def __init__(self, x: list):
        if all([type(apprsnbtype(i)) == SNBTLong for i in x]):
            self.x = x
        else:
            raise ValueError(
                f"Not all items in input {x} matches a long."
            )
    def dump(self):
        return f"[L;{SNBTList(self.x).dump()[1:]}"
