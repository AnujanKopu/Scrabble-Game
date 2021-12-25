
import enum
#from enum import Enum
from collections import deque
from random import sample


class Bag():
    def create(self):
        class Character(enum.Enum):
            BLANK=0
            A=1
            B=2
            C=3
            D=4
            E=5
            F=6
            G=7
            H=8
            I=9
            J=10
            K=11
            L=12
            M=13
            N=14
            O=15
            P=16
            Q=17
            R=18
            S=19
            T=20
            U=21
            V=22
            W=23
            X=24
            Y=25
            Z=26

        self.dominos =  deque(sample([Character(index) for index,value in enumerate((2,9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1)) for _ in range(value)],100))

    def setup(self):
        return tuple(self.dominos.popleft() for i in range(7))

    def grab_next(self):
        return self.dominos.popleft()

    
    

