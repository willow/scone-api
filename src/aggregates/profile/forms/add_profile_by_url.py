from django import forms
from django.forms.utils import ErrorList
from src.aggregates.topic.models import Topic


class AddProfileByUrlForm(forms.Form):
  url = forms.CharField(widget=forms.Textarea, label="Enter a url for a profile")

  def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
               error_class=ErrorList,
               label_suffix=None, empty_permitted=False):
    super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted)

    choices = [(str(t.id), str(t)) for t in Topic.objects.all()]
    self.fields['topic_types'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)
