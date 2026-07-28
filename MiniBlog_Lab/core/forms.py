from django import forms


class DemoRequestForm(forms.Form):
    student = forms.CharField(
        label="Student name",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "example: Dima Dimanson",
                "class": "form-control",
            }
        )
    )

    email = forms.EmailField(
        label="Email address",
    )

    course = forms.ChoiceField(
        label="Course",
        choices=[
            ("python", "Python"),
            ("java", "Java"),
            ("flask", "Flask"),
            ("Django", "Django"),
        ]
    )

    subscribe = forms.BooleanField(
        label="Subscribe to newsletter",
        required=False,
    )

    notes = forms.CharField(
        label="Additional notes",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Write something about yourself...",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )

    def clean_student(self):
        student = self.cleaned_data["student"]

        if student.lower() == "admin":
            raise forms.ValidationError(
                "This username is not allowed."
            )

        return student

    @property
    def clean(self):
        cleaned_data = super().clean

        course = cleaned_data.get("course")
        email = cleaned_data.get("email")

        if course == "django" and not email.endswith("@company.com"):
            raise forms.ValidationError(
                "Django course requires a company email address."
            )

        return cleaned_data
