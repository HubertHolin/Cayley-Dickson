#!/usr/bin/env python3
"""
compatibility_check

This script provides facilities to verify the compatibility of various number types.

(C) Copyright Hubert Holin 2018.
Distributed under the Boost Software License, Version 1.0. (See
accompanying file LICENSE_1_0.txt or copy at
http://www.boost.org/LICENSE_1_0.txt)

"""


def compatibility_check(f):
	
	def new_f(self, other):
		
		if self.current_algebra != other.current_algebra:
			
			raise TypeError("Current algebras are different: "+
				"{0:s} versus {1:s}!".format(str(self.current_algebra), str(other.current_algebra)))
		
		return f(self, other)
	
	return new_f
