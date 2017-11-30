from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User



class PollForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=200,
                    widget = forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Question',
                    })
    )
    choice_text = forms.CharField(label='Choice1', max_length=200,
                    widget = forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'First choice..'
                    })
    )
    choice_text2 = forms.CharField(label='Choice2', max_length=200,
                    widget = forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Second choice..'
                    })
    )
    

    def clean(self):
        cleaned_data = super(PollForm, self).clean()
        question_text = cleaned_data.get('question_text')
        choice_text = cleaned_data.get('choice_text')
        choice_text2= cleaned_data.get('choice_text2')
        
        if not question_text and not choice_text and not choice_text2:
            raise forms.ValidationError('You have to write something!')


# class UserCreateForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreateForm, self).__init__(*args, **kwargs)

#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].help_text = None


#customized sign up form
class UserCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    username = forms.CharField(label=_("Username"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
        )
    
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }))

    class Meta:
        model = User
        fields = ("username",)

        


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#customized login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label = _("Username"),
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label = _("Password"),
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )