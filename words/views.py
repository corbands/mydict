from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from words.models import Word

def word_edit(request, word_id):
	word = get_object_or_404(Word, pk=word_id)
	return render(request, 'words/word_edit.html', {'word': word})

def word_edited(request, word_id):
	if request.POST['action'] == 'Save':
		word = get_object_or_404(Word, pk=word_id)
		word.english = request.POST['english'];
		word.russian = request.POST['russian'];
		word.save()

	elif request.POST['action'] == 'Delete':
		word = get_object_or_404(Word, pk=word_id)
		word.delete()

#	latest_word_list = Word.objects.order_by('-pub_date')[:10]
#	context = { 'latest_word_list': latest_word_list }
	
	return HttpResponseRedirect(reverse('users:account', username=request.user.username))
