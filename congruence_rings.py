#!/usr/bin/env python3
"""
congruence_rings

This script provides congruence ring objects. Inspired (but different) from Jeremy Kun's
implementation (https://github.com/j2kun/elliptic-curve-signature,
https://jeremykun.com/2014/02/08/introducing-elliptic-curves/).
"""

from arithmetic import PGCD, Bézout
from compatibility_check import *


def congruence_ring(cardinal):
	
	class congruence_ring:	# Yes, the class and the enclosing function have the same name
		
		base_ring = ("congruence_ring", cardinal)
		
		current_algebra = base_ring
		
		
		def dump(self):
			
			return (self.__n,)
		
		
		def flatten(self):
			
			return (self.__n,)
		
		
		def upcast(factor):
			
			return __class__(factor)
		
		
		def neutral_element_for_multiplication():
			
			return __class__(1)
		
		
		def is_invertible(self):
			
			return PGCD(congruence_ring.base_ring[1], self.__n) == 1
		
		
		def is_unimodular(self):
			
			return (self.__n*self.__n) % congruence_ring.base_ring[1] == 1
		
		
		def __init__(self, n = 0):	# We will need a default constructor
			
			self.__n = n % congruence_ring.base_ring[1]
		
		
		@compatibility_check
		def __add__(self, other):
			
			return congruence_ring(self.__n + other.__n)
		
		
		@compatibility_check
		def __sub__(self, other):
			
			return congruence_ring(self.__n - other.__n)
		
		
		def __neg__(self):
			
			return congruence_ring(-self.__n)
		
		
		@compatibility_check
		def __mul__(self, other):
			
			return congruence_ring(self.__n * other.__n)
		
		
		def __matmul__(self, other):
		# We hijack this operator to represent the external product
			
			if self.current_algebra == other.current_algebra:
				
				return self*other
			
			else:
				
				return NotImplemented
		
		
		def inverse(self):
			
			if not __class__.is_invertible(self):
				
				raise ZeroDivisionError("{0:s} is not invertible!".format(self))
			
			u, v, pgcd = Bézout(self.__n, congruence_ring.base_ring[1])
			
			return congruence_ring(u)
		
		
		@compatibility_check
		def __truediv__(self, other):
			
			return self * other.inverse()
		
		
		def __pow__(self, a_power):
			
			return congruence_ring(pow(self.__n, a_power, cardinal))
		
		
		def conjugate(self):
			
			return congruence_ring(self.__n)
		
		
		def __eq__(self, other):
			
			if not hasattr(other, 'current_algebra'):
				
				return False
			
			elif self.current_algebra != other.current_algebra:
				
				return False
			
			else:
				
				return self.__n == other.__n
		
		
		def __ne__(self, other):
			
			if not hasattr(other, 'current_algebra'):
				
				return True
			
			elif self.current_algebra != other.current_algebra:
				
				return True
			
			else:
				
				return self.__n != other.__n
		
		
		def __str__(self):
			
			return str(self.__n)
		
		
		def __repr__(self):
			
			return "{0:d} [{1:d}]".format(self.__n, congruence_ring.base_ring[1])
		
		
		def __format__(self, spec):
			
			return "{0:d} [{1:d}]".format(self.__n, congruence_ring.base_ring[1])
	
	
	if cardinal <= 1:
		
		raise ValueError("For our intended use, we must have 'cardinal' > 1 "+
			"but 'cadinal' == {0:d}!".format(cardinal))
	
	return congruence_ring

