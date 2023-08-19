from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login ,  logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime , locale 
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from io import BytesIO
from .models import *
from .forms import *
from xhtml2pdf import pisa
from babel.core import Locale
from babel.dates import format_date
import base64 

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str




def cadastro (request):
     
    if request.user.is_authenticated:
        id_usuario = request.user.id
        return redirect('index', id_usuario=id_usuario)
    elif request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        email_usuario= request.POST['email_usuario']
        senha_usuario = request.POST['senha_usuario']
        senha_usuario2 = request.POST['senha_usuario2']
        if senha_usuario == senha_usuario2 :
            
            user =  User.objects.create_user(username=nome_usuario,email=email_usuario,password=senha_usuario)
            
            id_usuario = request.user.id
           
            return redirect('index', id_usuario=id_usuario)
            
        else:
            error_message = 'As senhas não conferem'
            return render(request, 'registration/cadastro.html', {'error_message': error_message})
 

    else:
            error_message = 'Nome de usuário ou senha inválidos'
            return render(request, 'registration/cadastro.html', {'error_message': error_message})
 
 

def email_senha(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                # Cria o token de redefinição de senha
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                nome_usuario = user.username

                # Renderiza o template de e-mail de redefinição de senha
                email_subject = 'Recuperação de Senha'
                email_from = "gleydevelopment@gmail.com"
               
               
               
                email_body = f"Olá {nome_usuario} Tudo bem ? Foi feita uma solicitação de recuperação de senha para sua conta na Financs $. Para prosseguir o procedimento, acesse o link abaixo, http://financs.com.br/reset_senha/{uid}/{token}"
               
                # Envia o e-mail de redefinição de senha
                send_mail(email_subject, email_body,email_from, [email], fail_silently=False)

                return redirect('msg_senha')
            else:
                error_message = 'E-mail não encontrado'
                return render(request, 'login/email_senha.html', {'error_message': error_message})
        else:
            error_message = '   Digite um e-mail'
            return render(request, 'login/email_senha.html', {'error_message': error_message})
    else:
        return render(request, 'login/email_senha.html')

def msg_senha (request):
    
    
    
    return  render (request, 'login/msg_senha.html' )
    
    

User = get_user_model()


def reset_senha(request, uidb64, token):
    
    try:
        uid = force_str( urlsafe_base64_decode (uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and default_token_generator.check_token(user, token):
      
        
        if request.method == 'POST':
            password = request.POST['password']
            user.set_password(password)
            user.save()
            return redirect('login')  # Redireciona para a página de login após redefinir a senha
        else:
            return render(request, 'login/rec_senha.html', {'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'login/reset_senha_invalido.html')

   
    

def login_view(request):
    
    if request.user.is_authenticated:
        id_usuario = request.user.id
        return redirect('index', id_usuario=id_usuario)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            id_usuario = user.id
            return redirect('index', id_usuario=id_usuario)
        elif user is not None:
            db_username = User.objects.get(username=username)
            if db_username:
                error_message = 'Senha invalida'
                return render(request, 'login/login.html', {'error_message': error_message})   
            else: 
                error_message = 'Nome de usuário invalido'
                return render(request, 'login/login.html', {'error_message': error_message})
        else:
            error_message = 'Senha invalida'
            return render(request, 'login/login.html', {'error_message': error_message})
            
    else:
        return render(request, 'login/login.html')


     
@login_required

def logout_view (request):
    
    logout(request)
    
    return redirect ('login')

@login_required
def index (request, id_usuario):
    

    if int(id_usuario) == request.user.id:
        
                
        exist = Saldo.objects.filter(id_usuario = id_usuario)
        
        if exist: 
            mes_atual =  datetime.date.today().month    
            despesa = Despesa.objects.filter(id_usuario=id_usuario, data_vencimento__month=mes_atual)
            receita = Receita.objects.filter(id_usuario= id_usuario,  data_entrada__month=mes_atual)
            saldo = Saldo.objects.filter(id_usuario= id_usuario)
            cartao = Cartao_credito.objects.filter(id_usuario= id_usuario, )
            cheque = Cheque_esp.objects.filter(id_usuario= id_usuario)
            
            desired_locale = Locale('pt_BR')
            data_atual= datetime.datetime.today()
            mes_atual_str = format_date(data_atual, format='MMMM', locale=desired_locale)

            soma_despesa = despesa.aggregate(soma=Sum('valor'))
            total_despesa = soma_despesa['soma']
            
            soma_receita = receita.aggregate(soma=Sum('valor'))
            total_receita = soma_receita['soma']


            if cartao:   
                soma_credito = cartao.aggregate(soma=Sum('saldo_cartao'))
                total_credito = soma_credito['soma']
                saldo_credito  = '{:.2f}'.format(total_credito)
            else:
                saldo_credito = Decimal('0.0')
                total_credito = Decimal('0.0')
                

                
            if cheque:   
                soma_cheque = cheque.aggregate(soma=Sum('saldo_cheque'))
                total_cheque = soma_cheque['soma']
            else:
                total_cheque = Decimal('0.0')
                

            if total_receita is not None  and total_despesa is not None:
                saldo_total = int(total_receita) - int(total_despesa) 
                saldo_format = '{:.2f}'.format(saldo_total)
                
            else :   
                
                saldo_total = 0
                saldo_format = '{:.2f}'.format(saldo_total)
                    
                    
                total_despesa = soma_despesa['soma']
                total_receita = soma_receita['soma'] 
            
            extrato_despesa = Despesa.objects.filter(id_usuario=id_usuario, status="Pago").order_by('data_entrada')
            extrato_receita = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=mes_atual).order_by('data_entrada')
            resultados_lista = list(extrato_despesa) + list(extrato_receita)
            resultados = sorted(resultados_lista, key=lambda x: x.data_entrada)

            context = {
                'despesas':despesa,
                'receita': receita,
                'saldo':  saldo ,
                'despesa_total' : total_despesa,
                'receita_total' : total_receita,
                'mes_atual': mes_atual_str,
                'total_credito':total_credito,
                'saldo_credito':saldo_credito,
                'saldo_total': saldo_total,
                'saldo_format': saldo_format,
                'cheques': cheque,
                'resultados':resultados,
                
                }
            return render (request, 'index.html', context )
        else:
            return redirect ('novo_usuario', id_usuario)
    else:
        return redirect ('logout' )
        

@login_required

def novo_usuario(request,id_usuario):
    
    if Saldo.objects.filter(id_usuario=id_usuario):
        
        return render(request, 'login/novo_usuario.html')

        
    else :  
        saldo_obj = Saldo()
        saldo_obj.id_usuario = request.user
        saldo_obj.saldo = Decimal('0.0')
        saldo_obj.data =  datetime.datetime.today()
        saldo_obj.save()

        context = {
            
        }
    
   
    return render(request, 'login/novo_usuario.html', context)



# Despesas {
    
@login_required
def despesa_page (request,id_usuario,):
    
    
    data_atual = datetime.datetime.today()

    despesas = Despesa.objects.filter(parcelas__isnull=False)
    for despesa in despesas:
        if despesa.changed == "Sim":
            continue
        parcelas_1 = int(despesa.parcelas)
        parcelas = parcelas_1 - 1 
        despesa.changed ="Sim"
        despesa.save()
        data_vencimento = despesa.data_vencimento
        for _ in range(parcelas):
            
                data_vencimento +=  relativedelta(months=1)
                nova_despesa = Despesa()
                nova_despesa.id_usuario = despesa.id_usuario
                nova_despesa.nome = despesa.nome
                nova_despesa.valor = despesa.valor
                nova_despesa.prioridade = despesa.prioridade
                nova_despesa.data_entrada = despesa.data_entrada
                nova_despesa.data_vencimento = data_vencimento
                nova_despesa.parcelas = despesa.parcelas  
                nova_despesa.status = "Pendente"
                nova_despesa.data_paga = data_atual
                nova_despesa.changed = "Sim"
                nova_despesa.save()
                
    
    despesa_obj = Despesa.objects.filter(id_usuario=id_usuario)
    mes_atual =  datetime.date.today().month    
    despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, data_vencimento__month=mes_atual)
    num_mes = datetime.datetime.now().month
    desired_locale = Locale('pt_BR')
    data_atual= datetime.datetime.today()
    mes_atual_str = format_date(data_atual, format='MMMM', locale=desired_locale)

    
    num_mes = datetime.datetime.now().month
    
    
            
    context = { 'despesas':despesa_obj,
                'mes_atual': mes_atual_str,
                'num_mes': num_mes 
        
    }
    
    return render (request, 'despesa/despesa.html', context)

@login_required

def despesa_mes (request, id_usuario, num_mes):
    acao = request.GET.get("acao")
    desired_locale = Locale('pt_BR')    
    mes_atual = datetime.datetime.now().month

    if acao == 'ante':
        num_mes = int(num_mes) - 1
    elif acao == 'prox':
        num_mes = int(num_mes) + 1

    if int(num_mes)  < 1:
        return redirect('despesa', id_usuario)

    if int(num_mes)  > 12:
        return redirect('despesa', id_usuario)

    if int(num_mes)  > mes_atual:
        despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, data_vencimento__month=int(num_mes) )
    else:
        despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, data_vencimento__month=int(num_mes) )

    data_mes = datetime.datetime(1900, int(num_mes) , 1)
    mes_formatado = format_date(data_mes, format='MMMM', locale=Locale('pt_BR'))

    context = {
        'despesas': despesa_obj,
        'mes_atual': mes_formatado,
        'num_mes': int(num_mes) 
    }

    return render(request, 'despesa/despesa.html', context)

def cartoes (request, id_usuario):
    
    cartao_obj= Cartao_credito.objects.filter(id_usuario=id_usuario)


    
    
    context= {
        'cartao_obj' : cartao_obj
    }
    return render (request, 'despesa/cartoes.html', context ) 
     
    
@login_required
def paguei(request, id_despesa):
    
    data_atual = datetime.datetime.today()
    id_usuario = request.user.id
    if request.method == "GET":
        despesa_paga = Despesa.objects.get(id_usuario=id_usuario, id=id_despesa)
        despesa_paga.status = "Pago"
        despesa_paga.data_paga = data_atual
        despesa_paga.save()
        return redirect('despesa', id_usuario)
    else:
        despesa = Despesa.objects.get(id_usuario=id_usuario, id=id_despesa)
        despesa.status = "A Pagar"  # Ou qualquer outro status que você deseje definir
        despesa.save()
        return redirect('despesa', id_usuario)

@login_required
def delete(request, id_obj):
    
    id_usuario = request.user.id
    if request.method == "GET":
        despesa_obj = Despesa.objects.get(id_usuario=id_usuario, id=id_obj)
        despesa_obj.delete()
        return redirect('despesa', request.user.id)
    
   

@login_required
def add_despesa (request, id_usuario):
    
    
    data_atual = datetime.datetime.today()
    if request.method == 'POST':
        form = Add_despesa(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.id_usuario = request.user
            despesa.data_paga = data_atual
            despesa.changed = "Não"
            despesa.dp_rc = "Despesa"
            
            despesa.save()
            return redirect('despesa', id_usuario=id_usuario)
    else:
        form = Add_despesa()
    
    context = {
        'form': form
    }
    return render(request, 'despesa/add_despesa.html', context)
        

@login_required
def atualizar_despesa(request, id_despesa):
    
    # Verificar se o usuário está autenticado

    # Verificar se a despesa pertence ao usuário atual
    despesa = Despesa.objects.filter(id=id_despesa, id_usuario=request.user).first()
    id_usuario = request.user.id

    # Processar o formulário de atualização
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('despesa', id_usuario )
    else:
        form = DespesaForm(instance=despesa)

    context = {
        'form': form
    }
    
    return render(request, 'despesa/atualizar_despesa.html', context)
    
@login_required
def despesa_total (request,id_usuario):
    
    despesa_obj = Despesa.objects.filter(id_usuario=id_usuario)
    
    context = { 'despesas':despesa_obj
        
    }
    return render (request, 'despesa/despesa_total.html', context)

 
@login_required

def receita_page (request,id_usuario):
    desired_locale = Locale('pt_BR')
    data_atual= datetime.datetime.today()
    mes_atual = datetime.datetime.now().month
    
    
    mes_atual =  datetime.date.today().month    
    receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=mes_atual)
    num_mes = datetime.datetime.now().month
    
    mes_atual_str = format_date(data_atual, format='MMMM', locale=desired_locale)
    
    num_mes = datetime.datetime.now().month
    
    
            
    context = { 'receitas': receita_obj,
                'mes_atual': mes_atual_str,
                'num_mes': num_mes 
        
    }
    
   
    return render (request, 'receita/receitas.html', context)



    

@login_required
def add_receita (request, id_usuario):
    
    
    if request.method == 'POST':
        form = Add_receita(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.id_usuario = request.user
            receita.dp_rc = "Receita"
            receita.save()
            return redirect('receita', id_usuario=id_usuario)
    else:
        form = Add_receita()
    
    context = {
        'form': form
    }
    return render(request, 'receita/add_receita.html', context)
    
    
    
@login_required
def atualizar_receita(request, id_receita):

   
    # Verificar se a despesa pertence ao usuário atual
    receita = Receita.objects.filter(id=id_receita, id_usuario=request.user).first()
    id_usuario = request.user.id

    # Processar o formulário de atualização
    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('receita', id_usuario )
    else:
        form = ReceitaForm(instance=receita)

    context = {
        'form': form
    }
    
    return render(request, 'receita/atualizar_receita.html', context)
    
    
    
@login_required

def receita_mes (request, id_usuario, num_mes):
    
    acao = request.GET.get("acao")
    mes_atual = datetime.datetime.now().month
    desired_locale = Locale('pt_BR')
    
    
    if acao == 'ante' :   
        
        if int(num_mes) == int(mes_atual) or int(num_mes) <= 12 :
            
            receita_obj = Receita.objects.filter(id_usuario=id_usuario)
            numero_mes = int(num_mes) 
            if numero_mes > 1:  
                numero_mes -= 1    
                receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=numero_mes)
                data_mes = datetime.datetime.strftime(datetime.datetime(1900, numero_mes, 1)) 
                mes_formatado = format_date(data_mes, format='MMMM', locale=desired_locale)
                context = {
                    'receitas': receita_obj,
                    'mes_atual': mes_formatado,
                    'num_mes': numero_mes
                }
                return render( request,'receita/receitas.html', context) 
            elif numero_mes == 1 :
                receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=numero_mes)
                data_mes = datetime.datetime.strftime(datetime.datetime(1900, numero_mes, 1)) 
                mes_formatado = format_date(data_mes, format='MMMM', locale=desired_locale)

                context = {
                    'receitas': receita_obj,
                    'mes_atual': mes_formatado,
                    'num_mes': numero_mes
                }
                return render( request,'receita/receitas.html', context)  
            else:
                receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=numero_mes)
                mes_atual_desc = datetime.datetime.strftime(datetime.datetime(1900, numero_mes, 1), '%B')
                context = {
                    'receitas': receita_obj,
                    'mes_atual': mes_atual_desc,
                    'num_mes': numero_mes
                }
                return render( request,'receita/receitas.html', context) 
         
        else : 
            return render(request, 'receita/receitas.html', context) 
            
        
    elif acao == 'prox' : 
        
        if int(num_mes) > 12:
            return redirect ('receita', id_usuario)
        else :  
            receita_obj = Receita.objects.filter(id_usuario=id_usuario)
            
            receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=num_mes)
        
            mes_atual_desc = datetime.datetime.strftime(datetime.datetime(1900,  int(num_mes), 1), '%B')
            numero_mes = int(num_mes) 
            numero_mes += 1    
            
                    
            context = { 'receitas': receita_obj,
                        'mes_atual': mes_atual_desc,
                        'num_mes' : numero_mes
                
            }
            
            return render (request, 'receita/receitas.html', context)
        
    return redirect ('receita', id_usuario)
    
       
    

@login_required
   
def saldo_page (request,id_usuario):
   
    num_mes = datetime.datetime.now().month
    
    
    saldo_obj = Saldo.objects.get(id_usuario=id_usuario)
    if saldo_obj:
        despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, data_vencimento__month=num_mes)
        receita_atual = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=num_mes)
        cartao_obj = Cartao_credito.objects.filter(id_usuario=id_usuario)
        cheque_obj = Cheque_esp.objects.filter(id_usuario=id_usuario)
        
        mes_atual = datetime.datetime.strftime(datetime.datetime(1900, num_mes, 1), '%B')

        soma_despesa = despesa_obj.aggregate(soma=Sum('valor'))
        total_despesa = soma_despesa['soma']
        
        soma_receita = receita_atual.aggregate(soma=Sum('valor'))
        total_receita = soma_receita['soma']
    
        if cartao_obj:   
            soma_credito = cartao_obj.aggregate(soma=Sum('saldo_cartao'))
            total_credito = soma_credito['soma']
            saldo_credito  = '{:.2f}'.format(total_credito)
        else:
            saldo_credito = Decimal('0.0')
            

            
        if cheque_obj:   
            soma_cheque = cheque_obj.aggregate(soma=Sum('saldo_cheque'))
            total_cheque = soma_cheque['soma']
            saldo_credito  = '{:.2f}'.format(total_cheque)
            
        else:
            total_cheque = Decimal('0.0')
            


        if total_receita is not None  and total_despesa is not None:
            saldo_total = int(total_receita) - int(total_despesa) 
            saldo_obj.saldo = saldo_total 
            saldo_obj.save()
            saldo_format = '{:.2f}'.format(saldo_total)
        
        elif  total_receita is not None  and total_despesa is None:
            saldo_total = int(total_receita) 
            saldo_obj.saldo = saldo_total 
            saldo_obj.save()
            saldo_format = '{:.2f}'.format(saldo_total)
            
            
        elif  total_receita is None  and total_despesa is not None:
            saldo_total = int(total_despesa) 
            saldo_obj.saldo = saldo_total 
            saldo_obj.save()
            saldo_format = '{:.2f}'.format(saldo_total)
            
        else :   
            
            saldo_total = 0
            saldo_format = '{:.2f}'.format(saldo_total)
            
        if request.method == 'POST':
                form_cartao = CartaoForm(request.POST)
                if form_cartao.is_valid():
                    cartao_obj = Cartao_credito()
                    cartao_obj.Marca = form_cartao.cleaned_data['Marca']
                    cartao_obj.saldo_cartao = form_cartao.cleaned_data['saldo_cartao']
                    cartao_obj.limite = form_cartao.cleaned_data['limite']
                    cartao_obj.id_usuario = request.user
                    cartao_obj.save()
                    return redirect('saldo', id_usuario=id_usuario)
        else:
            form_cartao = CartaoForm()

        
            context = { 'saldo':saldo_obj,
                        'saldo_format':saldo_format,
                        'saldo_total':saldo_total,    
                        'saldo_credito':saldo_credito,
                        'mes_atual': mes_atual,
                        'form_cartao' : form_cartao,
                        'cartoes':cartao_obj,
                        'despesas': despesa_obj,
                        'receitas': receita_atual,
                        'cheques':cheque_obj,
                        'total_cheque':total_cheque 
                        
                        
                
            }
            return render (request, 'saldo/saldo.html', context)
        
        
        

        if request.method == 'POST':
            
                if form_cartao.is_valid():
                    cartao_obj = Cartao_credito()
                    cartao_obj.Marca = form_cartao.cleaned_data['Marca']
                    cartao_obj.saldo_cartao = form_cartao.cleaned_data['saldo_cartao']
                    cartao_obj.limite = form_cartao.cleaned_data['limite']
                    cartao_obj.id_usuario = request.user
                    cartao_obj.save()
                    return redirect('saldo', id_usuario=id_usuario)
        else:
            form_cartao = CartaoForm()

        
        context = { 'saldo':saldo_obj,
                    'saldo_format':saldo_format,
                    'saldo_total':saldo_total,    
                    'saldo_credito':saldo_credito,
                    'mes_atual': mes_atual,
                    'form_cartao' : form_cartao,
                    'cartoes':cartao_obj,
                    'receitas':receita_atual,
                    'despesas': despesa_obj,
                    'cheques':cheque_obj,
                    'total_cheque':total_cheque
                
                    
                    
        }
        return render (request, 'saldo/saldo.html', context)
    else:
        saldo_obj = Saldo()
        saldo_obj = request.user.id
        saldo_obj.saldo = 0,0   
        saldo_obj.save()

        return render (request, 'saldo/saldo.html', context)
        

@login_required
def atualizar_cartao(request, id_cartao):
    
    # Verificar se o usuário está autenticado

    # Verificar se a despesa pertence ao usuário atual
    cartao = Cartao_credito.objects.filter(id=id_cartao, id_usuario=request.user).first()
    id_usuario = request.user.id

    # Processar o formulário de atualização
    if request.method == 'POST':
        form = Cartao_att(request.POST, instance=cartao)
        if form.is_valid():
            form.save()
            return redirect('saldo', id_usuario )
    else:
        form = Cartao_att(instance=cartao)

    context = {
        'form': form
    }
    
    return render(request, 'saldo/atualizar_cartao.html', context)
        

@login_required


def add_cheque (request,id_usuario):
    
    if request.method == 'POST':
        form = ChequeForm(request.POST)
        if form.is_valid():
            cheque = form.save(commit=False)
            cheque.id_usuario = request.user
            cheque.save()
            return redirect('saldo', id_usuario=id_usuario)
    else:
        form = ChequeForm()
    
    context = {
        'form': form
    }
    return render(request, 'saldo/add_cheque.html', context)
        

@login_required
    
def extrato_page (request,id_usuario):
    
    num_mes = datetime.datetime.today().month
    data_atual = datetime.datetime.today()
    
    despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, status="Pago").order_by('data_paga')
    receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=num_mes).order_by('data_entrada')
    resultados_lista = list(despesa_obj) + list(receita_obj)
    resultados = sorted(resultados_lista, key=lambda x: x.data_entrada)
    saldo = Saldo.objects.get(id_usuario=id_usuario)
    
    context = { 'despesas':despesa_obj,
                'receitas' : receita_obj,
                'saldo': saldo,
                'resultados':resultados,
                'data_atual':data_atual
        
    }
    return render (request, 'extrato/extrato.html', context)
    
        
def extrato_pdf(request):
    # Renderize a página HTML que deseja transformar em PDF
    num_mes = datetime.datetime.today().month
    data_atual = datetime.datetime.today()
    id_usuario = request.user.id
    despesa_obj = Despesa.objects.filter(id_usuario=id_usuario, status="Pago").order_by('data_paga')
    receita_obj = Receita.objects.filter(id_usuario=id_usuario, data_entrada__month=num_mes).order_by('data_entrada')
    resultados_lista = list(despesa_obj) + list(receita_obj)
    resultados = sorted(resultados_lista, key=lambda x: x.data_entrada)
    saldo = Saldo.objects.get(id_usuario=id_usuario)
    
    context = { 'despesas':despesa_obj,
                'receitas' : receita_obj,
                'saldo': saldo,
                'resultados':resultados,
                'data_atual':data_atual
        
    }
    html = render(request, 'extrato/extrato_pdf.html', context)

    # Crie um buffer BytesIO para armazenar o PDF
    result = BytesIO()

    # Gerar o PDF a partir do HTML usando a biblioteca xhtml2pdf
    pdf = pisa.pisaDocument(BytesIO(html.content), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Erro ao gerar PDF', status=500)  
    
def scheduler_vencimento():
    
    data_atual = datetime.datetime.today()
    despesas = Despesa.objects.filter(data_vencimento__lt=data_atual)
    for despesa in despesas:
        despesa.status = "Vencida"
        despesa.save()
        
  

