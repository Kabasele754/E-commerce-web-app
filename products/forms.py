

from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(max_length=50, required=True, label='Coupon Code')
