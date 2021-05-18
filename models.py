from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)
    full_name = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=50, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    modified_at = fields.DatetimeField(auto_now=True, null=True)

    #myapis: fields.ReverseRelation["MyApis"]

    class PydanticMeta:
        exclude = ["password"]



class MyApis(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    description = fields.CharField(max_length=200, null=True)
    polling_frequency = fields.IntField()
    polling_unit = fields.CharField(max_length=12, null=True) #seconds/minute
    url = fields.CharField(max_length=100, null=True)
    http_headers = fields.CharField(max_length=100, null=True)
    query_params = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    created_by : fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        'models.Users', null=True, related_name="myapi_users"
    )


Tortoise.init_models(["models"], "models")
UserPydantic = pydantic_model_creator(Users, name="User")
UserOutPydantic = pydantic_model_creator(Users, name="UserOutPydantic")
UserInPydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
MyApiPydantic = pydantic_model_creator(MyApis, name="MyApi")
MyApisInPydantic = pydantic_model_creator(MyApis, name="MyApiIn", exclude_readonly=True)
#print (UserPydantic.schema_json(indent=2))

