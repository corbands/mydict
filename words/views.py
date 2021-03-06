# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from words.models import Word

def word_edit(request, word_id):
	word = get_object_or_404(Word, pk=word_id)

	if request.user == word.user:
		can_edit = True
	else:
		can_edit = False

	return render(request, 'words/word_edit.html', {'word': word, 'can_edit':can_edit})

def word_edited(request, word_id):
	# TODO: вместо request post вынести всё в forms. перевести на CBV views
	if request.POST.__contains__('save'):
		word = get_object_or_404(Word, pk=word_id)
		word.english = request.POST['english'];
		word.russian = request.POST['russian'];
		word.save()
	elif request.POST.__contains__('delete'):
		word = get_object_or_404(Word, pk=word_id)
		word.delete()

	return redirect('users:account', username = request.user.username)
