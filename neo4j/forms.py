from django import forms


class Neo4jConnectionForm(forms.Form):
    host = forms.CharField(initial='http://localhost:9999')


class Neo4jQueryForm(forms.Form):
    node = forms.IntegerField(label='Node ID')
    depth = forms.IntegerField(initial=1)
