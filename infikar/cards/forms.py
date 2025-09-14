from django import forms
from .models import Card, CardTemplate, LinkContent


class CardCreateForm(forms.ModelForm):
    """Form for creating a new card"""
    
    class Meta:
        model = Card
        fields = ['title', 'card_type', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter card title'
            }),
            'card_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Card Title'
        self.fields['card_type'].label = 'Card Type'
        self.fields['is_published'].label = 'Publish immediately'
        
        # Add help text
        self.fields['title'].help_text = 'Choose a descriptive title for your card'
        self.fields['card_type'].help_text = 'Select the type of content for this card'
        self.fields['is_published'].help_text = 'Check to make this card visible to others immediately'


class LinkCreateForm(forms.ModelForm):
    """Form for creating/editing links"""
    
    class Meta:
        model = LinkContent
        fields = ['title', 'url', 'link_text', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter link title'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'https://example.com'
            }),
            'link_text': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Button text (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Enter description (optional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Link Title'
        self.fields['url'].label = 'URL'
        self.fields['link_text'].label = 'Button Text'
        self.fields['description'].label = 'Description'
        self.fields['image'].label = 'Image'
        
        # Add help text
        self.fields['title'].help_text = 'The title that will be displayed for this link'
        self.fields['url'].help_text = 'The URL this link will point to'
        self.fields['link_text'].help_text = 'Text for the button (leave empty to use title)'
        self.fields['description'].help_text = 'Optional description for this link'
        self.fields['image'].help_text = 'Optional image for this link'
