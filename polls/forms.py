from django import forms


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AuthorForm(BootstrapForm):
    anamech = forms.CharField()
    anameen = forms.CharField()
    amail = forms.CharField()
    cnamech1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '中文名称'}))
    cnameeg1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'English Name'}))
    cnamech2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '中文名称'}))
    cnameeg2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'English Name'}))
    czipcode = forms.IntegerField()
    addressch = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '中文地址'}))
    addressen = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'English Address'}))


class AuthorForm2(forms.Form):
    afnamech = forms.CharField()
    alnamech = forms.CharField()
    afnameen = forms.CharField()
    alnameen = forms.CharField()
    amail = forms.EmailField()
    cnamech1 = forms.CharField()
    cnamech2 = forms.CharField()
    cnameen1 = forms.CharField()
    cnameen2 = forms.CharField()
    czipcode = forms.CharField()
    country = forms.CharField()
    province = forms.IntegerField(required=False)
    city = forms.IntegerField(required=False)
    area = forms.IntegerField(required=False)
    addressch = forms.CharField(required=False)
    addressen = forms.CharField(required=False)


class PaperStep1Form(BootstrapForm):
    pname = forms.CharField()
    ptype = forms.ChoiceField(choices=[
        ('期刊[J]', '期刊[J]'),
        ('会议录[C]', '会议录[C]'),
        ('专利[P]', '专利[P]'),
        ('普通图书[M]', '普通图书[M]'),
        ('汇编[G]', '汇编[G]'),
        ('报纸[N]', '报纸[N]'),
        ('学位论文[D]', '学位论文[D]'),
        ('报告[R]', '报告[R]'),
        ('标准[S]', '标准[S]'),
        ('数据库[DB]', '数据库[DB]'),
        ('计算机程序[CP]', '计算机程序[CP]'),
        ('电子公告[EB]', '电子公告[EB]')
    ], widget=forms.Select(attrs={'v-model': "ptype"}))
    pifpub = forms.ChoiceField(choices=[
        ('true', True),
        ('false', False)
    ])
    pplace = forms.CharField(required=False)
    ppub = forms.CharField(required=False)
    pyear = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'min': 0}))
    ppage = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'min': 0}))
    ppath = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pplace'].widget.attrs['v-model'] = 'pplace'
        self.fields['ppub'].widget.attrs['v-model'] = 'ppub'
        self.fields['pyear'].widget.attrs['v-model'] = 'pyear'
        self.fields['ppage'].widget.attrs['v-model'] = 'ppage'
        self.fields['ppath'].widget.attrs['v-model'] = 'ppath'
