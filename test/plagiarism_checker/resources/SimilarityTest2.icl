module test2
import StdEnv

Start = fac 5

fac::Int->Int 
fac n 
| n == 0 = 0
| n == 1 = 1 
= n * fac (n-1)
