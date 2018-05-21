#!/usr/bin/env python3
"""
arithmetic

This script provides some classical arithmetic facilities.
"""

def PGCD(a, b):
	
	if a != int(a):
		
		raise TypeError(a, " is not an integer!")
	
	if b != int(b):
		
		raise TypeError(b, " is not an integer!")
	
	if abs(a) < abs(b):
		
		return PGCD(b, a)
	
	while abs(b) > 0:
		
		q,r = divmod(a,b)
		a,b = b,r
	
	return abs(a)


def Bézout(a, b):
	
	if a != int(a):
		
		raise TypeError(a, " is not an integer!")
	
	if b != int(b):
		
		raise TypeError(b, " is not an integer!")
	
	if abs(a) < abs(b):
		
		(u, v, pgcd) = Bézout(b, a)
		
		return (v, u, pgcd)
	
	if b == 0:
		
		return (1, 0, a)
	
	u_n, u_n_moins_1, v_n, v_n_moins_1 = 0, 1, 1, 0
	
	while abs(b) > 0:
		
		q, r = divmod(a,b)
		
		u_n_plus_1 = u_n_moins_1 - q*u_n
		v_n_plus_1 = v_n_moins_1 - q*v_n
		
		a, b = b, r
		u_n_moins_1, u_n, v_n_moins_1, v_n = u_n, u_n_plus_1, v_n, v_n_plus_1
	
	return (u_n_moins_1, v_n_moins_1, a)


def Jacobi(a, n):
	
	if a != int(a):
		
		raise TypeError(a, " is not an integer!")
	
	if n != int(n):
		
		raise TypeError(n, " is not an integer!")
	
	if n < 1:
		
		raise ValueError("{0:d} is strictly less than 1!".format(n))
	
	if n % 2 == 0:
		
		raise ValueError("{0:d} is even!".format(n))
	
	if n == 1:
		
		return 1
	
	the_pgcd = PGCD(a, n)
	
	if the_pgcd != 1:
		
		return 0
	
	n_mod_8 = n % 8
	
	the_factor_for_2 = (1 if ((n_mod_8 == 1) or (n_mod_8 == 7)) else -1)
	
	m = a % n
	
	global_factor = 1
	
	while m % 2 == 0:
		
		global_factor *= the_factor_for_2
		m >>= 1
	
	if m == 1:
		
		return global_factor
	
	else:
		
		n_mod_4 = n % 4
		m_mod_4 = m % 4
		
		reciprocity_factor = (1 if ((n_mod_4 == 1) or (m_mod_4 == 1)) else -1)
		
		return global_factor*reciprocity_factor*Jacobi(n, m)
