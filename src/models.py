from tortoise import fields, models

class Server(models.Model):
    id = fields.IntField(pk=True)