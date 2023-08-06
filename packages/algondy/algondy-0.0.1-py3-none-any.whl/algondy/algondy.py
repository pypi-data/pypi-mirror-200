def gcd(a, b): #a,bの最大公約数を求める
  if (b==0):
     return a
  else:
     return gcd(b,a%b)
  
def partial_sum(N,V,A): #N個の整数リストAからいくつかの整数を選んで総和をとった場合、総和をVにすることができるかの判断 False or Trueで返す
   ans = False
   for S in range(2 ** N):
      sum_S = sum(ai for idx, ai in enumerate(A) if S & (1 << idx))
      if sum_S == V:
         ans = True
   return ans
