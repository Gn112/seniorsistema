from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Vaga, PerfilCandidato

class FormularioRegistroUsuario(UserCreationForm):

    user_type = forms.ChoiceField(
        choices=Usuario.TIPOS_DE_USUARIO,
        label='Tipo de Usuário',
        widget=forms.RadioSelect
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'user_type') 

    def save(self, commit=True):

        user = super().save(commit=False)
        
        user.user_type = self.cleaned_data['user_type'] 
        
        if commit:
            user.save()
            
        return user

class FormularioVaga(forms.ModelForm):

    class Meta:
        model = Vaga
        
        exclude = ('empresa', 'created_at')

class FormularioPerfilCandidato(forms.ModelForm):
    class Meta:
        model = PerfilCandidato
        fields = ('pretensao_salarial', 'experiencia', 'ultima_escolaridade')