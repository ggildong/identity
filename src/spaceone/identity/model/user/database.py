from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel


class MFA(EmbeddedDocument):
    state = StringField(
        max_length=20, choices=("ENABLED", "DISABLED"), default="DISABLED"
    )
    mfa_type = StringField(max_length=20)
    options = DictField()

    def to_dict(self):
        return dict(self.to_mongo())


class User(MongoModel):
    user_id = StringField(max_length=40, unique_with="domain_id", required=True)
    password = BinaryField(default=None)
    name = StringField(max_length=128, default="")
    state = StringField(max_length=20, default="PENDING", choices=("ENABLED", "DISABLED", "PENDING"))
    email = StringField(max_length=255, default="")
    email_verified = BooleanField(default=False)
    auth_type = StringField(max_length=20, choices=("LOCAL", "EXTERNAL"))
    role_type = StringField(
        max_length=20,
        default="USER",
        choices=('SYSTEM', 'SYSTEM_ADMIN', 'DOMAIN_ADMIN', 'WORKSPACE_OWNER', 'WORKSPACE_MEMBER', 'USER'),
    )
    mfa = EmbeddedDocumentField(MFA)
    required_actions = ListField(StringField(choices=("UPDATE_PASSWORD",)), default=[])
    language = StringField(max_length=7, default="en")
    timezone = StringField(max_length=50, default="UTC")
    api_key_count = IntField(default=0)
    tags = DictField(Default=None)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    last_accessed_at = DateTimeField(default=None, null=True)

    meta = {
        "updatable_fields": [
            "password",
            "name",
            "state",
            "email",
            "email_verified",
            'role_type',
            "mfa",
            "language",
            "timezone",
            "required_actions",
            "tags",
            "api_key_count",
            "last_accessed_at",
        ],
        "minimal_fields": [
            "user_id",
            "name",
            "state",
            'auth_type',
            "role_type"
        ],
        "ordering": [
            "name",
            "user_id"
        ],
        "indexes": [
            "state",
            "auth_type",
            "role_type",
        ],
    }
