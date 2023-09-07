from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cadastro/',cadastro, name='cadastro'),
    path('',login_view, name='login'),
    path('logout',logout_view, name='logout'),    
    path('reset_senha/<str:uidb64>/<str:token>/', reset_senha, name='reset_senha'),   
    path('email_senha',email_senha, name='email_senha'),
    path('msg_senha',msg_senha, name='msg_senha'),    
    path('index/<id_usuario>/', index, name='index'),
    path('novousuario/<id_usuario>/', novo_usuario, name='novo_usuario'),
    path('despesa/<id_usuario>',despesa_page, name='despesa'),
    path('despesa/<id_usuario>/<num_mes>',despesa_mes, name='despesa_mes'),
    path('cartoes/<id_usuario>/',cartoes, name='cartoes'),    
    path('atualizar_compras/<id_compras>/',atualizar_compras, name='atualizar_compras'),    
    path('add_compra/<id_usuario>/',add_compras, name='add_compra'),       
    path('paguei/<id_despesa>/',paguei, name='paguei'),
    path('delete/<id_obj>/<instance>/',delete, name='delete'),    
    path('despesa_total/<id_usuario>/',despesa_total, name='despesa_total'),    
    path('add_despesa/<id_usuario>/',add_despesa, name='add_depesa'),
    path('atualizar_despesa/<id_despesa>/',atualizar_despesa, name='atualizar_despesa'),    
    path('receita/<id_usuario>/',receita_page, name='receita'),
    path('add_receita/<id_usuario>/',add_receita, name='add_receita'),
    path('atualizar_receita/<id_receita>/',atualizar_receita, name='atualizar_receita'),
    path('receita/<id_usuario>/<num_mes>',receita_mes, name='receita_mes'),
    path('saldo/<id_usuario>/',saldo_page, name='saldo'),
    path('atualizar_cartao/<id_cartao>', atualizar_cartao, name='atualizar_cartao'),
    path('add_cheque/<id_usuario>', add_cheque, name='add_cheque'),
    path('extrato/<id_usuario>/',extrato_page, name='extrato'), 
    path('extrato_compras/<id_usuario>/',extrato_compras, name='extrato_compras'),   
      
    path('add_despesa/<id_usuario>/',add_despesa, name='add_despesa'),
    path('extrato_pdf',extrato_pdf, name='extrato_pdf'),
    
    
    # path('request/',scheduler_parcelas, name='request'),
    
    
    
]
 