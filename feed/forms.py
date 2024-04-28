from django import forms
from .models import Content, FeedImage
from django.forms import inlineformset_factory

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body_text', 'content_type']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class FeedImageForm(forms.ModelForm):
    class Meta:
        model = FeedImage
        fields = ['image']

# Content 객체와 연결된 FeedImage 객체들을 처리할 수 있는 FormSet 생성
# extra -> 처리할 수 있는 이미지 필드 개수(동적으로 javascript로 업데이트 해야함)
FeedImageFormSet = inlineformset_factory(Content, FeedImage, form=FeedImageForm, extra=5, can_delete=True)
    

class ReviewContentForm(ContentForm):
    class Meta(ContentForm.Meta):
        fields = ContentForm.Meta.fields + ['product', 'seller']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        seller = cleaned_data.get("seller")

        if not product or not seller:
            raise forms.ValidationError("구매한 상품만 리뷰할 수 있습니다.")
        return cleaned_data