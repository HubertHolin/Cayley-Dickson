#!/usr/bin/env python3
"""
cayley_dickson

This script provides a facilty to create objects via the Cayley-Dickson doubling method.

(C) Copyright Hubert Holin 2018.
Distributed under the Boost Software License, Version 1.0. (See
accompanying file LICENSE_1_0.txt or copy at
http://www.boost.org/LICENSE_1_0.txt)

"""

from compatibility_check import *


def cayley_dickson_doubling(base, structural):
	
	if base.base_ring != structural.base_ring:
		
		raise TypeError("Base rings are different between 'base' and 'structural': "+
				"{0:s} versus {1:s}!".format(str(base.base_ring), str(structural.base_ring)))
	
	
	class cayley_dickson_doubling:
		
		base_ring = structural.base_ring
		
		
		current_algebra = ('doubling', base.current_algebra, structural)
		
		
		@classmethod
		def collect_structurals(cls):
			
			real_flat = ()
			
			if hasattr(base, 'collect_structurals'):
				
				real_flat += base.collect_structurals()
			
			real_flat += (structural,)
			
			return real_flat
		
		
		def dump(self):
			
			return self.components[0].dump()+self.components[1].dump()
		
		
		def flatten(self):
			
			return self.components[0].flatten()+self.components[1].flatten()
		
		
		def upcast(factor):
			
			try:
				
				if factor.current_algebra != __class__.current_algebra:
					
					try:
						
						try:
							
							return cayley_dickson_doubling(factor)
						
						except:
							
							return cayley_dickson_doubling(base(factor))
					
					except:
						
						return cayley_dickson_doubling(base.upcast(factor))
				
				else:
					
					return factor
			
			except:
				
				return __class__.upcast(base.upcast(factor))
		
		
		def downcast(element):
			
			if element.current_algebra == __class__.base_ring:
				
				return element
			
			else:
				
				return __class__.downcast(element.components[0])
		
		
		def is_invertible(self):
			
			return self.cayley_norm().downcast().is_invertible()
		
		
		def is_unimodular(self):
			
			return self.cayley_norm().downcast() ==\
				structural.__class__.neutral_element_for_multiplication()
		
		
		def __init__(self, component_0 = base(), component_1 = base()):
			
			if	((component_0.current_algebra != self.current_algebra[1]) or
				(component_1.current_algebra != self.current_algebra[1])):
				
				raise TypeError("A component is from a different algebra: "+
					"{0:s} and {1:s} (expected {2:s})!".format(str(component_0.current_algebra),
					str(component_1.current_algebra), str(self.current_algebra[1])))
			
			self.components = (component_0, component_1)
		
		
		@compatibility_check
		def __add__(self, other):
			
			return cayley_dickson_doubling(self.components[0] + other.components[0],
				self.components[1] + other.components[1])
		
		
		@compatibility_check
		def __sub__(self, other):
			
			return cayley_dickson_doubling(self.components[0] - other.components[0],
				self.components[1] - other.components[1])
		
		
		def __neg__(self):
			
			return cayley_dickson_doubling(-self.components[0], -self.components[1])
		
		
		@compatibility_check
		def __mul__(self, other):
			
			new_component_0 = self.components[0]*other.components[0]
			new_component_0 -= self.current_algebra[2] @ (other.components[1].conjugate()*self.components[1])
			
			new_component_1 = self.components[1]*other.components[0].conjugate()
			new_component_1 += other.components[1]*self.components[0]
			
			return cayley_dickson_doubling(new_component_0, new_component_1)
		
		
		def __rmatmul__(self, other):
		# We hijack this operator to represent the external product
			
			if other.current_algebra != self.base_ring:
				
				raise TypeError("First factor is not in the second factor's base ring: "+
					"{0:s} versus {1:s}!".format(other.current_algebra, self.base_ring))
			
			else:
				
				return cayley_dickson_doubling(other @ self.components[0],
					other @ self.components[1])
		
		
		def inverse(self):
			
			if not __class__.is_invertible(self):
				
				raise ZeroDivisionError("{0:s} is not invertible!".format(self))
			
			return self.cayley_norm().downcast().inverse() @ self.conjugate()
		
		
		@compatibility_check
		def __truediv__(self, other):
			
			return self * other.inverse()
		
		
		def __pow__(self, a_power):
		# We adapt the Binary Exponentiation algorithm (without modulo!)
			
			#result = __class__.upcast(base(1))
			#print(__class__.base_ring)
			result = __class__.upcast(1)
			
			auxilliary = cayley_dickson_doubling(self.components[0], self.components[1])
			
			while a_power:
				
				if a_power % 2:	# If power is odd
					
					result = result * auxilliary
				
				# Divide the power by 2
				a_power >>= 1
				
				# Multiply base to itself
				auxilliary = auxilliary * auxilliary
			
			return result
		
		
		def conjugate(self):
			
			return cayley_dickson_doubling(self.components[0].conjugate(), -self.components[1])
		
		
		def cayley_trace(self):
			
			return self+self.conjugate()
		
		
		def cayley_norm(self):
			
			return self*self.conjugate()
		
		
		def __eq__(self, other):
			
			if not hasattr(other, 'current_algebra'):
				
				return False
			
			elif self.current_algebra != other.current_algebra:
				
				return False
			
			else:
				
				return self.components == other.components
		
		
		def __ne__(self, other):
			
			if not hasattr(other, 'current_algebra'):
				
				return True
			
			elif self.current_algebra != other.current_algebra:
				
				return True
			
			else:
				
				return self.components != other.components
		
		
		def __str__(self):
			
			structural_constants = __class__.collect_structurals()
			
			da_length = len(structural_constants)
			
			da_string = "{0} ".format(self.flatten())
			da_string += "{"
			
			if da_length > 1:
				
				for idx in range(da_length-1):
					
					da_string += "{0:s}, ".format(structural_constants[idx])
				
				da_string += "{0:s}".format(structural_constants[-1])
			
			else:
				
				da_string += "{0:s}".format(structural_constants[0])
			
			da_string += "}"
			
			return da_string
		
		
		def __repr__(self):
			
			structural_constants = __class__.collect_structurals()
			
			da_length = len(structural_constants)
			
			da_string = "{0} ".format(self.flatten())
			da_string += "{"
			
			if da_length > 1:
				
				for idx in range(da_length-1):
					
					da_string += "{0:s}, ".format(structural_constants[idx])
				
				da_string += "{0:s}".format(structural_constants[-1])
			
			else:
				
				da_string += "{0:s}".format(structural_constants[0])
			
			da_string += "}"
			
			return da_string
		
		
		def __format__(self, spec):
			
			structural_constants = __class__.collect_structurals()
			
			da_length = len(structural_constants)
			
			da_string = "{0} ".format(self.flatten())
			da_string += "{"
			
			if da_length > 1:
				
				for idx in range(da_length-1):
					
					da_string += "{0:s}, ".format(structural_constants[idx])
				
				da_string += "{0:s}".format(structural_constants[-1])
			
			else:
				
				da_string += "{0:s}".format(structural_constants[0])
			
			da_string += "}"
			
			return da_string
	
	
	return cayley_dickson_doubling

