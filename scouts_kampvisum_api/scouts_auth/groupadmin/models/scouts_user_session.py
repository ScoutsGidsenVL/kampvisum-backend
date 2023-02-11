import jwt
from typing import List
from datetime import datetime

from django.db import models, connections
from django.db.models import JSONField
from django.utils.timezone import now, make_aware

from scouts_auth.auth.settings import InuitsOIDCSettings
from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField, TimezoneAwareDateTimeField, OptionalTextField

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSessionQueryset(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScoutsUserSessionManager(models.Manager):
    def get_queryset(self):
        return ScoutsUserSessionQuerySet(self.model, using=self._db)

    def purge_expired(self):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"delete from scouts_auth_scoutsusersession sasus where sasus.expiration <= '{now()}'")

    def get_session_data(self, username: str, expiration: datetime) -> dict:
        self.purge_expired()
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select sasus.data as data from scouts_auth_scoutsusersession sasus where sasus.username = '{username}' and sasus.expiration > '{now()}' and sasus.data is not null"
            )
            result = cursor.fetchone()
            if result:
                return result[0]
        return {}


class ScoutsUserSession(models.Model):

    objects = ScoutsUserSessionManager()

    username = RequiredCharField()
    expiration = TimezoneAwareDateTimeField()
    data = JSONField(null=True)


class ScoutsToken:
    """
    Models a JWT as delivered by the scouts keycloak.

    @see https://www.iana.org/assignments/jwt/jwt.xhtml
    @see https://www.rfc-editor.org/rfc/rfc7519#section-4.1.1
    """

    # rfc7519: expiration time of the jwt
    _exp: datetime = TimezoneAwareDateTimeField()
    # rfc7519: time of issuance
    _iat: datetime = TimezoneAwareDateTimeField()
    # rfc7519: optional string identifying this jwt
    jti: str = OptionalCharField()
    # rfc7519: string or uri identifying the issuer of the jwt
    iss: str = OptionalCharField()
    # rfc7519: string or uri identifying the subject of the jwt
    sub: str = OptionalCharField()
    # rfc7519: identifies the media type that is prepended in the Authorization header, e.g. Bearer
    typ: str = OptionalCharField()
    # time of authentication
    _auth_time: datetime = TimezoneAwareDateTimeField()
    # keycloak client id
    azp: str = OptionalCharField()
    # session identifier
    session_state: str = OptionalCharField()
    # Authentication Context Class Reference
    acr: str = OptionalCharField()
    # list of CORS uri's
    _allowed_origins: str = OptionalCharField()
    # space separated list of scopes
    scope: str = OptionalCharField()
    # indicates if the user has verified his/her email
    email_verified: str = OptionalCharField()
    # full name for the user
    name: str = OptionalCharField()
    # username
    preferred_username: str = OptionalCharField()
    # user's first name
    given_name: str = RequiredCharField()
    # user's last name
    family_name: str = OptionalCharField()
    # user's email address
    email: str = OptionalCharField()

    def validate(self) -> bool:
        if self.preferred_username and self.exp:
            return True
        raise ScoutsAuthException(
            "JWT token does not contain the preferred_username or expiration time")

    @ property
    def exp(self) -> datetime:
        return self._exp

    @ exp.setter
    def exp(self, exp: int):
        self._exp = make_aware(datetime.fromtimestamp(exp))

    @ property
    def iat(self) -> datetime:
        return self._iat

    @ iat.setter
    def iat(self, iat: int):
        self._iat = make_aware(datetime.fromtimestamp(iat))

    @ property
    def auth_time(self) -> datetime:
        return self._auth_time

    @ auth_time.setter
    def auth_time(self, auth_time: int):
        self._auth_time = make_aware(datetime.fromtimestamp(auth_time))

    @ property
    def allowed_origins(self) -> List[str]:
        return self._allowed_origins.split(",") if self.allowed_origins else []

    @ allowed_origins.setter
    def allowed_origins(self, allowed_origins: List[str]):
        self._allowed_origins = ",".join(
            allowed_origin for allowed_origin in allowed_origins) if allowed_origins else ''

    @ staticmethod
    def from_access_token(access_token: str):
        if access_token:
            decoded = {}
            try:
                decoded = jwt.decode(
                    access_token,
                    # algorithms=[
                    #     InuitsOIDCSettings.get_oidc_signing_algorithm()],
                    algorithms=["RS256"],
                    # verify=InuitsOIDCSettings.get_oidc_verify_jwt(),
                    verify=False,
                    # options={
                    #     "verify_signature": InuitsOIDCSettings.get_oidc_verify_jwt_signature()},
                    options={"verify_signature": False},
                )
            except Exception as exc:
                raise ScoutsAuthException(
                    "Unable to decode JWT token - Do you need a refresh ?", cause=exc)

            if decoded:
                token = ScoutsToken()

                token.exp = decoded.get("exp", None)
                token.iat = decoded.get("iat", None)
                token.auth_time = decoded.get("auth_time", None)
                token.jti = decoded.get("jti", None)
                token.iss = decoded.get("iss", None)
                token.sub = decoded.get("sub", None)
                token.typ = decoded.get("typ", None)
                token.azp = decoded.get("azp", None)
                token.session_state = decoded.get("session_state", None)
                token.acr = decoded.get("acr", None)
                token.allowed_origins = decoded.get(
                    "allowed_origins", None)
                token.scope = decoded.get("scope", None)
                token.email_verified = decoded.get("email_verified", None)
                token.name = decoded.get("name", None)
                token.preferred_username = decoded.get(
                    "preferred_username", None)
                token.given_name = decoded.get("given_name", None)
                token.family_name = decoded.get("family_name", None)
                token.email = decoded.get("email", None)

                token.validate()

                return token