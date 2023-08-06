import numpy as np
from numpy import floor, random, sin, cos, acos, PI
from functools import reduce, map
from .spycio import nNorm

def throw(message, errorClass=Exception):
  raise errorClass(message)

'''
  @abstract JSON object has $key string among keys
 
 
  @param {Object} object
  @param {String} key
  @return {Object}
'''
def objectHasKey(object, key):
  return key in object.keys()

'''
  @abstract n-norm of a number
 
  @param {Array} arr
  @param {Number} n
  @return {Number}
''' 
def countarr(arr):
  obj = {}

  for i in range(len(arr)):
    obj[arr[i]] = (obj[arr[i]] or 0) + 1
  
  return obj

'''
  @abstract returns prime factors for non-zero natural numbers
 
  @param {String} task_msg
'''
def factorize(n): 
  if (not isinstance(n, int)):
    throw('It is impossible to factorize \'{n}\'. It MUST be a number!'.format(n), TypeError)

  if ((n-floor(n) != 0) or (n < 1)):
    throw("The provided number must not be zero and must be natural.", TypeError)

  factors = []

  if (n == 1):
    factors = [1]
  else:
    # Start divisor with value 2
    divisor = 2

    while (n >= 2):
      if (n % divisor == 0):
        factors.append(divisor)
        n /= divisor
      else:
        divisor+=1

  return countarr(factors)

'''
  @abstract returns true/false for prime/non-prime number
 
  @param {Number} number
  @return {boolean}
'''
def isPrime(number):
  if (isinstance(number, int)):
    throw('It is impossible to factorize \'{number}\'. It MUST be a number!'.format(number))
  else:
    factors=factorize(number)
    return len(factors.keys()) == 1 and factors.values()[0] == 1

'''
  @abstract converts randian to degree angle
 
  @param {Number} radian_angle
  @return {NUmber}
'''
def radianToDegree(angle_radian): 
  return (180 * angle_radian) / PI

'''
  @abstract converts degree to randian angle
 
  @param {Number} radian_angle
  @return {Number}
'''
def degreeToRadian(angle_degree): 
  return (PI * angle_degree) / 180

'''
  @abstract return haversine function sin^2(theta)
 
  @param {Number} radian_angle
  @return {NUmber}
'''
def hav(theta_radian): 
  return sin(theta_radian / 2) ** 2

'''
  @abstract return
 
  @param {Array} radian_angle
  @return {Array}
'''
def geoToSpher(lat_degree, lng_degree):
  return [PI / 2 - degreeToRadian(lng_degree), degreeToRadian(lat_degree)]

'''
  @abstract decimal part of a number
 
  @param {Number} number
  @return {Number}
'''
def decimalPart(number): 
  return number - floor(number)

'''
  @abstract xor operator
 
  @param {Number} min
  @param {Number} b
  @return {Number}
'''
def abrand(min, max):
  rvalue=min + (max - min) * random()

  return throw("The latter number must be greater than the former.") if min >= max else rvalue

'''
  @abstract transformation map of spherical to cartesian coordinates
  The 3D representation order corresponds to (z, x, y)
 
  @param {boolean} a
  @param {boolean} b
  @return {boolean}
'''
def spherToCart(coords, R):
  prodFun=lambda prod_, angle: prod_ * sin(angle)
  
  def prodsin(angles): 
    return 1 if len(angles) == 0 else reduce(prodFun, angles, 1)

  s2cRecur = lambda coords_, index: prodsin(coords_[0:index]) * cos(coords_[index])
  prev_coords = coords.slice(0, len(coords))
  curr_coord = coords[len(coords) - 1]
  last_coord=[R * prodsin(prev_coords) * sin(curr_coord)]

  spherDistFun=lambda coord, index: R * s2cRecur(prev_coords, index)  

  return map(spherDistFun, prev_coords).append(last_coord)

'''
  @abstract an spherical coordinate of dimension n has:
   1. Dimension greater than 2;
   2. Entries from index:
     a. 0 to indexn-2 : between [-pi, pi];
     b. indexn-1      : between [0, 2 pi];
 
  @param {Array} u
  @return {Boolean}
'''
def isSpherical(u):
  isBetweenmPIandpPI=lambda result, elem: result and elem >= -PI and elem <= PI
  isBetween0and2PI=lambda result, elem: result and elem >= 0 and elem <= 2 * PI
  
  return not (
    len(u) >= 2 and \
      reduce(isBetweenmPIandpPI, u[0:len(u) - 1], True) and \
      reduce(isBetween0and2PI, u[len(u) - 1:len(u)], True)
  )

'''
  @abstract dot product
 
  @param {Array} arr
  @return {Number}
'''
def dot(a, b):
  sumFun=lambda m, n: m + n
  prodFun=lambda x: x[0] * x[1]

  return reduce(sumFun, map(prodFun, zip(a,b)), 0)

'''
  @abstract vector argument based on n-norm
 
  @param {Array} u
  @param {Array} v
  @param {Number} n
  @return {Number}
'''
def arguv(u, v, n):
  return acos(dot(u, v) / (nNorm(u, n) * nNorm(v, n)))
