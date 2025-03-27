# Classe vector

class Vector:
    def __init__(self, iterable):
        self._vector = [elemento for elemento in iterable] # Comprensio de llista
        
    def __repr__(self):
        return f"Vector({self._vector})"
        
    def __str__(self): #
        cadena = "<"
        for elemento in self._vector:
            cadena += f" {elemento}"
        cadena += " >"
        return cadena

    def __getitem__(self, key): # Permet accedir als elements del vector
        return self._vector[key]

    def __setitem__(self, key, value): # Permet canviar els elements dels vectors
        self._vector[key] = value

    def __len__(self): # Retorna la llargada del vector
        return len(self._vector)

    def __add__(self,other): # Permet fer la operacio de suma
        if isinstance(other, (int, float, complex)): #Mecanisma per saber si l'objecte es d'un tipus
            return Vector([elemento+other for elemento in self]) #expresion for elemento in iterable
        else:
            if len(self) != len(other): raise ValueError("Els vectors no son de la mateixa longitud")
            return Vector([self_ + other_ for self_, other_ in zip(self,other)]) #suma de dos vectors

    __radd__ = __add__ # Per fer aplicar la propietat commutativa.

    def __neg__(self): # Per aplicar la negacio
        return Vector([-elemento for elemento in self])

    def __sub__(self, other): # Resta
        return -(-self +other)

    def __rsub__(self, other): # Resta commutada
        return -self + other
    
    