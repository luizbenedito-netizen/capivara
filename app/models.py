from django.db import models

class CadGrupos(models.Model):
    idgrupo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.IntegerField()
    descricao = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cad_grupos'


class CadGruposPermissoes(models.Model):
    idgrupo = models.ForeignKey(CadGrupos, models.DO_NOTHING, db_column='idgrupo')
    idpermissao = models.ForeignKey('CadPermissoes', models.DO_NOTHING, db_column='idpermissao')

    class Meta:
        managed = False
        db_table = 'cad_grupos_permissoes'

class CadPermissoes(models.Model):
    idpermissao = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    caminho = models.TextField(blank=True, null=True)
    tipo = models.IntegerField()
    rota = models.CharField(max_length=255, blank=True, null=True)
    idpai = models.IntegerField(blank=True, null=True)
    icone = models.CharField(max_length=45, blank=True, null=True)
    ordem = models.IntegerField(blank=True, null=True)
    ativo = models.BooleanField()
    descricao = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cad_permissoes'


class CadTipos(models.Model):
    categoria = models.IntegerField()
    cod = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=45)
    campo = models.CharField(max_length=45, blank=True, null=True)
    ordem = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cad_tipos'


class CadUsuarios(models.Model):
    idusuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    tokensenha = models.CharField(max_length=50, blank=True, null=True)
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cad_usuarios'


class CadUsuariosGrupos(models.Model):
    idusuario = models.ForeignKey(CadUsuarios, models.DO_NOTHING, db_column='idusuario')
    idgrupo = models.ForeignKey(CadGrupos, models.DO_NOTHING, db_column='idgrupo')

    class Meta:
        managed = False
        db_table = 'cad_usuarios_grupos'


class CadUsuariosPermissoes(models.Model):
    cad_usuarios_idusuario = models.ForeignKey(CadUsuarios, models.DO_NOTHING, db_column='cad_usuarios_idusuario')
    idpermissao = models.ForeignKey(CadPermissoes, models.DO_NOTHING, db_column='idpermissao')
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cad_usuarios_permissoes'

# ----------------------------------------------------------------------------------------------------------

class ContaTipo(models.Model):
    idusuario = models.IntegerField(db_column='idusuario')
    tipo_conta = models.CharField(max_length=50)
    status = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'contas_tipo'
        verbose_name = 'Tipo de Conta'
        verbose_name_plural = 'Tipos de Conta'
    def __str__(self):
        return self.tipo_conta


class Conta(models.Model):
    idusuario = models.IntegerField(db_column='idusuario')
    tipo_conta = models.ForeignKey(
        ContaTipo,
        on_delete=models.RESTRICT,
        db_column='tipo_conta',
        related_name='contas'
    )
    nome_conta = models.CharField(max_length=100)
    icone = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_removido = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'contas'
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
    def __str__(self):
        return self.nome_conta


class Receita(models.Model):
    idusuario = models.IntegerField(db_column='idusuario')
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, db_column='idconta')
    tipo_receita = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data_adicionada = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1)
    data_remocao = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'receitas'
        verbose_name = 'Receita'

    def __str__(self):
        return f"{self.tipo_receita} - {self.valor}"


class Despesa(models.Model):
    FORMA_PAGAMENTO = [
        ('avista', 'À Vista'),
        ('parcelado', 'Parcelado'),
    ]

    idusuario = models.IntegerField(db_column='idusuario')
    conta_origem = models.ForeignKey(Conta, on_delete=models.CASCADE, db_column='idconta_origem', null=True)
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    subgrupo = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_removido = models.DateTimeField(blank=True, null=True)
    data_vencimento = models.DateField()
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO)
    parcela_atual = models.IntegerField(default=1)
    total_parcelas = models.IntegerField(default=1)
    descricao = models.TextField(blank=True, null=True)
    comprovante_path = models.FileField(upload_to='comprovantes/', blank=True, null=True)

    class Meta:
        db_table = 'despesas'
        verbose_name = 'Despesa'

    def __str__(self):
        return self.nome
