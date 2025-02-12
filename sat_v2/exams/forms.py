from django import forms
from .models import Exam, ReadingPassage, Question, Choice

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'time_limit', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '180'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class PassageQuestionForm(forms.Form):
    """Form for adding a passage with its question and choices"""
    passage_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        label="Reading Passage"
    )
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Question"
    )
    choice_1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Choice 1"
    )
    choice_2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Choice 2"
    )
    choice_3 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Choice 3"
    )
    choice_4 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Choice 4"
    )
    correct_choice = forms.ChoiceField(
        choices=[(1, 'Choice 1'), (2, 'Choice 2'), (3, 'Choice 3'), (4, 'Choice 4')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Correct Answer"
    )

    def save(self, exam, section):
        """Create the passage, question, and choices"""
        passage = ReadingPassage.objects.create(
            exam=exam,
            text=self.cleaned_data['passage_text'],
            section=section
        )
        
        question = Question.objects.create(
            passage=passage,
            text=self.cleaned_data['question_text']
        )
        
        for i in range(1, 5):
            Choice.objects.create(
                question=question,
                text=self.cleaned_data[f'choice_{i}'],
                is_correct=(i == int(self.cleaned_data['correct_choice']))
            )
        
        return passage