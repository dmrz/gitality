from urlparse import urlparse

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('user',)

    def clean_repo_url(self):
        """
        Validates whether given repo url has
        format github.com/username/reponame
        """
        repo_url = self.cleaned_data['repo_url']
        parsed = urlparse(repo_url)
        domain, path_fragments = parsed.netloc, parsed.path.split('/')[1:]
        if domain != 'github.com' or len(path_fragments) != 2:
            raise forms.ValidationError(_(u'Wrong GitHub repo URL'))
        return repo_url
