from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Error(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Error'
        verbose_name_plural = 'Errors'


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    highlighted = models.TextField()
    #project = models.OneToOneField(Project, on_delete=models.PROTECT, null=True, blank=True)
    errors = models.ManyToManyField(Error, related_name='snippet')

    # CASCADE: si borro un proyecto tambien va a borrar el snipet. si hago snippet.project.delete() borra el snippet y el project.
    # PROTECT: si borro el snippet no va a borrar el project. 1- p = s.project  2-borro el snippet: In [8]: s.delete()  3- p.delete() finalmente borro el project

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet. 
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


class Comment(models.Model):
    SUPERVISOR = (
        ('junior', 'junior'),
        ('senior', 'senior'),
        ('semisenior', 'semisenior')
    )
    supervisor = models.CharField(choices=SUPERVISOR, max_length=100)
    description = models.TextField()
    # CASCADE: si borro un Snippet tambien va a borrar el Comment. si hago comment.snippet.delete() borra el snippet y el comment.
    # SET_NULL: Set the ForeignKey null; this is only possible if null is True.
    snippet = models.ForeignKey(Snippet, on_delete=models.SET_NULL,
                                related_name="comments", null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
