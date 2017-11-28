from django import forms


class PollForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=200)
    choice_text = forms.CharField(label='Choice1', max_length=200)
    choice_text2 = forms.CharField(label='Choice2', max_length=200)
    
    def clean(self):
        cleaned_data = super(PollForm, self).clean()
        question_text = cleaned_data.get('question_text')
        choice_text = cleaned_data.get('choice_text')
        choice_text2= cleaned_data.get('choice_text2')
        
        if not question_text and not choice_text and not choice_text2:
            raise forms.ValidationError('You have to write something!')