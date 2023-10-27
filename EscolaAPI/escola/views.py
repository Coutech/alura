import csv
from django.http import HttpResponse
from rest_framework import viewsets, generics
from escola.models import Aluno, Curso, Matricula
from escola.serializer import AlunoSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasAlunoSerializer, ListaAlunosMatriculadosEmUmCurso
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos(as)."""
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
                
class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos."""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    
class MatriculasViewSet(viewsets.ModelViewSet):
    """Exibindo todos as matriculas."""
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    
class ListaMatriculasAluno(generics.ListAPIView):
    """Listando todas as matriculas do aluno(a)."""
    def get_queryset(self):
        queryset = Matricula.objects.filter(aluno_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasAlunoSerializer
    
class ListaAlunosMatriculados(generics.ListAPIView):
    """Listando alunos(as) matriculados(as) em um curso."""
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaAlunosMatriculadosEmUmCurso

class ExportCSV(generics.ListAPIView):
    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()
    
    def set_date_range(self):
        self.data_de = self.request.query_params.get('data_nasc_de')
        self.data_ate = self.request.query_params.get('data_nasc_ate')
        
        # Define as datas caso não haja parâmetros na solicitação
        if not self.data_de:
            self.data_de = '1900-01-01' # Data inicial
            
        if not self.data_ate:
            self.data_ate = datetime.now().strftime('%Y-%m-%d') # Data final

    def filter_queryset(self, queryset):
        self.set_date_range()
        
        if self.data_de and self.data_ate:
            queryset = queryset.filter(data_nascimento__range=[self.data_de, self.data_ate])

        return queryset

    def list(self, *args, **kwargs):
        self.set_date_range()
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="alunos_{self.data_de}_{self.data_ate}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nome', 'RG', 'CPF', 'Data de Nascimento'])  # Cabeçalho

        for aluno in queryset:
            writer.writerow([aluno.nome, aluno.rg, aluno.cpf, aluno.data_nascimento])

        return response