module test

import StdEnv

Start = fac 5

fac :: Int -> Int
fac 0 = 1
fac n = n * fac (n-1) 
