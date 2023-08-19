from django.contrib import admin
from .models import Despesa, Receita, Saldo, Extrato, Cartao_credito, Cheque_esp, Compras_cartao


# Register your models here.


class Receita_admin (admin.ModelAdmin):
    
    list_display = ('id' ,'nome', 'valor', 'data_entrada','dp_rc',)
    search_fields = ('^nome',)
    ordering = ('nome', )

class Despesa_admin (admin.ModelAdmin):
    
    list_display = ('nome' ,'id', 'valor','prioridade', 'data_entrada','data_vencimento','parcelas','status', 'data_paga','changed','dp_rc',)
    search_fields = ('^nome',)
    ordering = ('nome', )
    
class Saldo_admin (admin.ModelAdmin):
    
    list_display = ('id_usuario' , 'saldo' ,'data', 'id')
    search_fields = ('^saldo',)
    ordering = ('saldo', )
    
class Extrato_admin (admin.ModelAdmin):
    
    list_display = ( 'receita', 'despesa','saldo', 'data')
    search_fields = ('^saldo',)
    ordering = ('saldo', )

class Cartao_admin  (admin.ModelAdmin):
    
    list_display = ( 'id_usuario', 'Marca','saldo_cartao')
    search_fields = ('^marca',)
    ordering = ('id_usuario', )


class Cheque_admin  (admin.ModelAdmin):
    
    list_display = ( 'id_usuario', 'saldo_cheque','limite','juros', 'banco')
    search_fields = ('^id_usuario',)
    ordering = ('id_usuario', )

class Compras_Cartao_admin (admin.ModelAdmin):
    
    list_display = ('nome', 'valor', 'data')
    search_fields = ('^nome',)
    ordering = ('nome', )



admin.site.register(Receita,Receita_admin)
admin.site.register(Despesa,Despesa_admin)
admin.site.register(Saldo,Saldo_admin)
admin.site.register(Extrato,Extrato_admin)
admin.site.register(Cartao_credito, Cartao_admin)
admin.site.register(Cheque_esp, Cheque_admin)
admin.site.register(Compras_cartao, Compras_Cartao_admin)
 







                      

                      
