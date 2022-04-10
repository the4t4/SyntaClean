module factorial	 
import StdEnv

Start = fac 5

fac::Int->Int
fac 0 = 0
fac 1 = 2
fac n = n * fac (-1)
