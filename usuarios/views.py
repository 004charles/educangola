from django.shortcuts import render, redirect
from .models import Feedback, Usuario
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Usuario, Feedback


def obrigado(request):
    return render(request, 'obrigado.html')

def index(request):
    return render(request, 'index.html')

def Cadastrar_normal(request):
    status = request.GET.get('status')
    return render(request, 'cadastrar_normal.html', {'status':status}) 

def Login_normal(request):
    status = request.GET.get('status')
    return render(request, 'login_normal.html', {'status':status})

def Valida_login_normal(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()
    usuario = Usuario.objects.filter(email = email).filter(senha=senha)

    if len(usuario) == 0:
        return redirect('/usuarios/Login_normal?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id

    return redirect('/Educa_Angola/home?status=1')


def Valida_cadastro_normal(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/usuarios/Cadastrar_normal?status=1')

    if len(senha) < 8:
        return redirect('/usuarios/Cadastrar_normal?status=2')

    if len(usuario) > 0:
        return redirect('/usuarios/Cadastrar_normal?status=3')

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, senha = senha, email = email)
        usuario.save()
        return redirect('/usuarios/Cadastrar_normal?status=0')

    except:
        return redirect('/usuarios/Login_normal?status=4')



def create_pdf(feedback):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Funcionalidades: {feedback.funcionalidades}")
    p.drawString(100, 730, f"Tipo de Conteúdo: {feedback.tipo_conteudo}")
    p.drawString(100, 710, f"Grupos de Estudo: {feedback.grupos_estudo}")
    p.drawString(100, 690, f"Biblioteca de Recursos: {feedback.biblioteca_recursos}")
    p.drawString(100, 670, f"Tutorias Online: {feedback.tutorias_online}")
    p.drawString(100, 650, f"Integração: {feedback.integracao}")
    p.drawString(100, 630, f"Funcionalidades Móveis: {feedback.funcionalidades_moveis}")
    p.drawString(100, 610, f"Usabilidade: {feedback.usabilidade}")
    p.drawString(100, 590, f"Interação: {feedback.interacao}")
    p.drawString(100, 570, f"Feedback Geral: {feedback.feedback}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def feedback_view(request):
    if request.method == "POST":
        feedback = Feedback(
            funcionalidades=request.POST.get('funcionalidades'),
            tipo_conteudo=request.POST.get('tipo_conteudo'),
            grupos_estudo=request.POST.get('grupos_estudo'),
            biblioteca_recursos=request.POST.get('biblioteca_recursos'),
            tutorias_online=request.POST.get('tutoriais_online'),
            integracao=request.POST.get('integracao'),
            funcionalidades_moveis=request.POST.get('funcionalidades_moveis'),
            usabilidade=request.POST.get('usabilidade'),
            interacao=request.POST.get('interacao'),
            feedback=request.POST.get('feedback'),
        )
        feedback.save()

        # Criação do PDF em memória
        pdf_buffer = create_pdf(feedback)

        # Enviar o e-mail para todos os usuários cadastrados
        usuarios = Usuario.objects.all()
        subject = 'Novo Feedback Enviado'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'Um novo feedback foi enviado. Confira o PDF em anexo com as sugestões feitas pelos usuários.'

        for usuario in usuarios:
            email = EmailMessage(
                subject,
                message,
                from_email,
                [usuario.email],  # Enviar para o e-mail do usuário
            )
            email.content_subtype = 'html'  # Definindo o conteúdo como HTML, se necessário
            email.attach('feedback.pdf', pdf_buffer.getvalue(), 'application/pdf')  # Anexando o PDF

            # Enviar o e-mail
            email.send(fail_silently=False)

        return redirect('obrigado')  # Redireciona para a página de agradecimento
    return render(request, 'index.html')