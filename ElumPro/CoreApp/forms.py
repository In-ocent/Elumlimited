from .models import ProjectInquiry
from django import forms


from .models import ProjectMessage


class ProjectMessageForm(forms.ModelForm):
    class Meta:
        model = ProjectMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Your Message'}),
        }


# CONTACT PAGE


class ProjectInquiryForm(forms.ModelForm):
    class Meta:
        model = ProjectInquiry
        fields = ['full_name', "phone_number",
                  'email', 'service_category', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'John Doe', 'class': 'w-full bg-black border border-gray-800 rounded-lg px-4 py-3 text-white focus:border-[#46B4B1] outline-none'}),
            'phone_number': forms.TextInput(attrs={'id': 'id_phone_number', 'class': 'w-full bg-black border border-gray-800 rounded-lg px-4 py-3 text-white focus:border-[#46B4B1] outline-none', }),
            'email': forms.EmailInput(attrs={'placeholder': 'john@company.com', 'class': 'w-full bg-black border border-gray-800 rounded-lg px-4 py-3 text-white focus:border-[#46B4B1] outline-none'}),
            'service_category': forms.Select(attrs={'class': 'w-full bg-black border border-gray-800 rounded-lg px-4 py-3 text-white focus:border-[#46B4B1] outline-none'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your project...', 'class': 'w-full bg-black border border-gray-800 rounded-lg px-4 py-3 text-white focus:border-[#46B4B1] outline-none'}),
        }
