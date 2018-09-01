from django.db.models import Q
from .models import Dialog


def get_dialogs_with_user(user_1, user_2):
	"""
	To get the dialog between user_1 and user_2
	"""
	return Dialog.objects.filter(Q(owner=user_1, opponent=user_2) | Q(owner=user_2, opponent=user_1))
