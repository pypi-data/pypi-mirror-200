from django.db import models


class BaseModel(models.Model):
    cd_estabelecimento = models.CharField(
        "Estabelecimento",
        max_length=20,
        null=True,
        blank=True
    )
    nm_usuario_cri = models.CharField(
        "Usuario criacao",
        max_length=50,
        null=True,
        blank=True
    )
    nm_usuario_edi = models.CharField(
        "Usuario edicao",
        max_length=50,
        null=True,
        blank=True
    )
    nm_usuario_del = models.CharField(
        "Usuario delecao",
        max_length=50,
        null=True,
        blank=True
    )
    dt_criado = models.DateTimeField(
        "Criado em",
        auto_now_add=True
    )
    dt_atualizado = models.DateTimeField(
        "Atualizado em",
        auto_now=True
    )
    dt_deletado = models.DateTimeField(
        "Deletado em",
        null=True,
        blank=True
    )

    def delete(self):
        self.dt_deletado = True
        self.save()

    class Meta:
        abstract = True

