		module 
test	 
		import /*sjnijevn */ StdEnv

Start 
	= +1 //2efevkfemv

:: 
 Object = {state
	::Int, 
	
	
	
	
	method::Int->Int,
 tostring:: Int -> String 
 }
MyObject = { state = 3, 
 method = (+) 1, 
	tostring 
	= toString
 }

:: Bag a :== [a]
lmao:: Int -> Bag Int	
lmao a = [a]

fac::Int->Int 
fac 0 = 0
fac 1 = 2
	
fac n 
  |    n == 0 = 0 
= n * fac (n-1)

g :: Int -> String 
g a = "Hel2130)()_>$#()J N)(#@$lo"

f7 :: [Int] -> [Int]
f7 [] = [2]
f7 [_,_,_:_] = [3]
f7 [_:b] =  [1] ++ b

:: Tree a b = N a b (Tree a b) (Tree a b) | L
specialTree :: (Tree Int Bool)
specialTree = (N 4 False L L)

h :: {Int} {Int} -> [(Int,Int)]
h a b = [(x, y) \\ x <-: a & y <-: b]

i :: [Int] -> [Int]
i a = [x \\ x <- a]

:: Tree2 a = Node a (Tree2 a) (Tree2 a) | Leaf
tree1 = Node 10 (Node 7 (Node 3 Leaf Leaf) (Node 15 Leaf Leaf)) (Node 5 Leaf (Node 10 Leaf Leaf))

j :: [Int] -> {Int}
j 
  a = {x 
			\\ 
  x <- a}
 
MyObject1 = { state = 3, method = (+) 12321, tostring = toString }
