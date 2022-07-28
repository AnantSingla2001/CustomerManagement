from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    #a decorator is a function which contains another function as a parameter and helps to add on extra functionality before the original function is called
	def wrapper_func(request, *args, **kwargs):
	   #it doesn't get executed until wrapper function is executed 
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
			#if a group for a user exists then assign the first value of the group list to group though here is only one group associated to each user
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function




   
    