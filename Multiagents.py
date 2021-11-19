
class Car:
    
    def __init__(self, geometria, topologia):
        self.geometria = geometria
        self.topologia = topologia

class Street:
    
    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin
        self.peso = 0
        
    def addCar(self):
        self.peso += 1
    
    def deleteCar(self):
        self.peso -= 1

class Direction:
    
    def __init__(self, nombre, coordenada):
        self.nombre = nombre
        self.coordenada = coordenada
        self.light = True
    
    def turnLight(self):
        self.light = not self.light
    
    def getLight(self):
        return self.light
    
    def changeCoord(self, coordenada):
        self.coordenada = coordenada

class City:
    
    def __init__(self, calles, direcciones):
        self.calles = calles
        self.direcciones = direcciones
        
        
if __name__ == "__main__":
    a = Direction("A",[1,1])
    b = Direction("B",[1,2])
    c = Direction("C",[1,3])
    d = Direction("D",[1,4])
    e = Direction("E",[1,5])
    f = Direction("F",[2,1])
    g = Direction("G",[2,2])
    h = Direction("H",[2,3])
    i = Direction("I",[2,4])
    j = Direction("J",[2,5])
    k = Direction("K",[3,1])
    l = Direction("L",[3,2])
    m = Direction("M",[3,3])
    n = Direction("N",[3,4])
    o = Direction("O",[3,5])
    p = Direction("P",[4,1])
    q = Direction("Q",[4,2])
    r = Direction("R",[4,3])
    s = Direction("S",[4,4])
    t = Direction("T",[4,5])
    
    direcciones = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t]
    
    aa = Street(a,f)
    ab = Street(b,a)
    ac = Street(b,g)
    ad = Street(c,b)
    af = Street(c,h)
    ag = Street(d,c)
    ah = Street(d,i)
    ai = Street(e,d)
    aj = Street(e,j)
    ak = Street(f,a)
    al = Street(f,k)
    am = Street(g,f)
    an = Street(h,g)
    ao = Street(i,h)
    ap = Street(i,d)
    aq = Street(i,n)
    ar = Street(j,i)
    as_ = Street(j,o)
    at = Street(k,f)
    au = Street(k,p)
    av = Street(k,l)
    aw = Street(l,m)
    ax = Street(m,n)
    ay = Street(n,i)
    az = Street(n,j)
    aaa = Street(n,o)
    aab = Street(o,t)
    aac = Street(p,k)
    aad = Street(p,q)
    aaf = Street(q,p)
    aag = Street(q,l)
    aah = Street(q,r)
    aai = Street(r,q)
    aaj = Street(r,m)
    aak = Street(r,s)
    aal = Street(s,r)
    aam = Street(s,n)
    aan = Street(s,t)
    aao = Street(t,s)
    
    calles = [aa,ab,ac,ad,af,ag,ah,ai,aj,ak,al,am,an,ao,ap,aq,ar,as_,at,au,av,aw,ax,ay,az,aaa,aab,aac,aad,aaf,aag,aah,aai,aaj,aak,aal,aam,aan,aao]
    
    ambiente = City(calles,direcciones)
    
    
    