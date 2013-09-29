from urlparse import urlparse

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from south.modelsinspector import add_introspection_rules
from uuslug import slugify
from github3 import login

from core.models import TimeStampedModel
from core.utils import cached_property

add_introspection_rules([], ['^autoslug\.AutoSlugField'])


class Project(TimeStampedModel):
    """
    Represents project object.
    """

    name = models.CharField(_(u'name'), max_length=128, unique=True)
    slug = AutoSlugField(populate_from='name', slugify=slugify)

    repo_url = models.URLField(
        _('repo url'),
        help_text=_(u'Publicly accessible GitHub repo URL'),
        max_length=256,
        unique=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='projects'
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'project')
        verbose_name_plural = _(u'projects')

    def __unicode__(self):
        return u'{}'.format(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('projects:project_detail', (), {'slug': self.slug})

    @property
    def commits_count(self):
        return self.progress.commit_count

    @property
    def additions_count(self):
        return self.progress.additions_count

    @property
    def deletions_count(self):
        return self.progress.deletions_count

    @property
    def latest_commits(self):
        return self.commits.order_by('-last_modified')[:15]

    @property
    def github_repo_obj(self):
        logged_in = login(
            settings.GITHUB_BOT_NAME,
            settings.GITHUB_BOT_PASSWORD)
        vals = self.github_user_repo_name
        if len(vals) != 2:
            return
        repo = logged_in.repository(*vals)
        return repo

    @cached_property(ttl=0)
    def github_user_repo_name(self):
        """
        Returns Github repo username and repo
        name list, e.g. [johndoe, coolrepo].
        """
        return filter(None, urlparse(self.repo_url).path.split('/'))
