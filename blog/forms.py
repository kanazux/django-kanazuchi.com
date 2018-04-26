import re
from django import forms
from .models import Post
from .models import IpyTest


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('ip',)


class IpyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IpyForm, self).__init__(*args, **kwargs)
        self.fields['binary_ip'].widget.attrs['size'] = 40
        self.fields['binary_mask'].widget.attrs['size'] = 40

    class Meta:
        model = IpyTest
        fields = ('ip', 'network_ip', 'broadcast_ip', 'class_ip', 'cidr_mask',
                  'binary_ip', 'binary_mask')
        fields_required = ('binary_ip')

    def clean_binary_ip(self):
        cleaned_data = super(IpyForm, self).clean()
        ip_pattern = re.compile(r"([0|1]{8}\.){3}[0|1]{8}")
        binary_ip_data = cleaned_data.get('binary_ip')
        if not bool(ip_pattern.match(binary_ip_data)):
            raise forms.ValidationError("Binary Ip must be an ip in binary.")
