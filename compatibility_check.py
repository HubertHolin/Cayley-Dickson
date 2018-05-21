#!/usr/bin/env python3
"""
compatibility_check

This script provides facilities to verify the compatibility of various number types.
"""


def compatibility_check(f):
	
	def new_f(self, other):
		
		if self.current_algebra != other.current_algebra:
			
			raise TypeError("Current algebras are different: "+
				"{0:s} versus {1:s}!".format(str(self.current_algebra), str(other.current_algebra)))
		
		return f(self, other)
	
	return new_f
