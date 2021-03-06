from django.test import SimpleTestCase, TestCase
from django.conf import settings
from django.contrib.auth.models import User

from mock import patch

from .forms import ProjectForm
from .models import Project


class ProjectFormTest(SimpleTestCase):

    def test_repo_url_validation(self):

        # Valid repo url
        post_data = {
            'name': 'Gitality',
            'repo_url': 'https://github.com/dmrz/gitality.git'
        }
        form = ProjectForm(post_data)
        self.assertTrue(form.is_valid())

        # Check that .git part is truncated
        self.assertEqual(form.cleaned_data['repo_url'], post_data['repo_url'].replace('.git', ''))

        # Invalid repo url
        post_data['repo_url'] = post_data['repo_url'].replace('github', 'othersite')
        form = ProjectForm(post_data)
        self.assertFalse(form.is_valid())

        self.assertIn('repo_url', form.errors)


class ProjectModelTest(TestCase):
    @patch('projects.models.login')
    def test_github_repo_obj(self, mock_login):
        u = User.objects.create(username='g24g24g24g')
        proj = Project.objects.create(
            name='sdf13f', repo_url='https://github.com/dmrz/gfh3h',
            user=u)
        proj.github_repo_obj
        mock_login.assert_called_once_with(
            settings.GITHUB_BOT_NAME, settings.GITHUB_BOT_PASSWORD)
        mock_login().repository.assert_called_once_with(
            'dmrz', 'gfh3h')
