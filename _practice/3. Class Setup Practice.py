# 1. Define Class for complex numbers
import math
class ZNumber():
    # Constructor
    def __init__(self, real:int, imag:int):
        self.real = real
        self.imag = imag

    # Utility methods
    def mod(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def arg(self):
        return math.atan2(self.imag, self.real)

# 2. Define program entry point.
def main():
    z = ZNumber(42,84)
    print(z.mod(),z.arg())

if __name__ == '__main__':
    main()
