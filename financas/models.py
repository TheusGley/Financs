from django.db import models
from django.contrib.auth.models import User



Prioridades = [
        ('Alta Prioridade', 'Alta Prioridade'),
        ('Media Prioridade', 'Media Prioridade'),
        ('Baixa Prioridade', 'Baixa Prioridade'),
    ]
Status = [
    ('Pago', 'Pago'),
    ('Pendente', 'Pendente'),
    ('Vencida', 'Vencida')
]
dp_rc = [ 
         ('Despesa', 'Despesa' ),
         ('Receita' , 'Receita')
         ]
 
 
 
Changed = [
    ('Sim','Sim'),
    ('Não', 'Não')
] 

class Receita (models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField()
    dp_rc =  models.CharField(max_length=50, choices=dp_rc)

    def __str__(self):
        return self.nome
    
class Despesa (models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    prioridade = models.CharField(max_length=50, choices=Prioridades)
    data_entrada = models.DateField()
    data_vencimento = models.DateField()
    parcelas = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Status)
    data_paga = models.DateField()
    changed = models.CharField(max_length=50, choices=Changed)
    dp_rc =  models.CharField(max_length=50, choices=dp_rc)
    
    
    

    def __str__(self):
        return self.nome
    
class Cartao_credito (models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    Marca =  models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_cartao = models.DecimalField(max_digits=10, decimal_places=2)
    
         
    def __str__(self):
       return str(self.Marca)
   
class Cheque_esp (models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    saldo_cheque = models.DecimalField(max_digits=10, decimal_places=2)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    juros = models.DecimalField(max_digits=10, decimal_places=1)
    banco =  models.CharField(max_length=100)
    
            
    def __str__(self):
       return str(self.saldo_cheque)
   
    
    
class Saldo(models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    cartao_credito = models.ForeignKey(Cartao_credito, on_delete=models.CASCADE, null=True)
    cheque_esp = models.ForeignKey(Cheque_esp, on_delete=models.CASCADE, null=True)
    
        
    def __str__(self):
       return str(self.saldo)
   
class Extrato(models.Model):
    id_usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE)
    data = models.DateField()
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
       return str(self.saldo)

class Compras_cartao (models.Model):
    cartao_credito = models.ForeignKey(Cartao_credito, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
 
    
    def __str__(self):
       return str(self.nome)
    
