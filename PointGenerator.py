from GeometricElements import Point

#Class for handle and generate points within a line

class PointGenerator:
    
    def __init__(self, aFact, bFact):
        self.aFact = aFact
        self.bFact = bFact

    @classmethod
    def FromFactors(cls, aFact, bFact):
        "Creates a new instance of PointGenerator using line a and b factors."
        return cls(aFact, bFact)

    @classmethod
    def FromPoints(cls, p1, p2):
        "Creates a new instance of PointGenerator using two points p1 and p2."

        x1 = float(p1.x)
        y1 = float(p1.y)
        x2 = float(p2.x)
        y2 = float(p2.y)

        if x1 == x2:
            x1 += 0.01

        aFact = (y1 - y2) / (x1 - x2)
        bFact = y1 - aFact * x1

        return cls(aFact, bFact)

    def GetFromX(self, xValue):
        return Point(xValue, self.aFact * xValue + self.bFact)

    def GetFromY(self, yValue):
        return Point((yValue - self.bFact) / self.aFact, yValue)

#If it is the main module (for test purposes)
if __name__ == '__main__':
    print('Testing PointGenerator module...')
    pointGenerator = PointGenerator.FromPoints(Point(0,0), Point(2,1))

    print(pointGenerator.GetFromY(0))

