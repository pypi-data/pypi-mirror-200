# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPL-3.0 2016-present Scille SAS

from __future__ import annotations

class ClientType:
    AUTHENTICATED: ClientType
    INVITED: ClientType
    ANONYMOUS: ClientType
    APIV1_ANONYMOUS: ClientType
    APIV1_ADMINISTRATION: ClientType
    def __hash__(self) -> int: ...

class InvitationDeletedReason:
    FINISHED: InvitationDeletedReason
    CANCELLED: InvitationDeletedReason
    ROTTEN: InvitationDeletedReason
    @classmethod
    def values(cls) -> list[InvitationDeletedReason]: ...
    @classmethod
    def from_str(cls, value: str) -> InvitationDeletedReason: ...
    @property
    def str(self) -> str: ...

class InvitationEmailSentStatus:
    SUCCESS: InvitationEmailSentStatus
    NOT_AVAILABLE: InvitationEmailSentStatus
    BAD_RECIPIENT: InvitationEmailSentStatus
    @classmethod
    def values(cls) -> list[InvitationEmailSentStatus]: ...
    @classmethod
    def from_str(cls, value: str) -> InvitationEmailSentStatus: ...
    @property
    def str(self) -> str: ...

class InvitationStatus:
    IDLE: InvitationStatus
    READY: InvitationStatus
    DELETED: InvitationStatus
    @classmethod
    def values(cls) -> list[InvitationStatus]: ...
    @classmethod
    def from_str(cls, value: str) -> InvitationStatus: ...
    @property
    def str(self) -> str: ...

class InvitationType:
    DEVICE: InvitationType
    USER: InvitationType
    @classmethod
    def values(cls) -> list[InvitationType]: ...
    @classmethod
    def from_str(cls, value: str) -> InvitationType: ...
    @property
    def str(self) -> str: ...

class RealmRole:
    OWNER: RealmRole
    MANAGER: RealmRole
    CONTRIBUTOR: RealmRole
    READER: RealmRole
    @classmethod
    def values(cls) -> list[RealmRole]: ...
    @classmethod
    def from_str(cls, value: str) -> RealmRole: ...
    @property
    def str(self) -> str: ...

class UserProfile:
    ADMIN: UserProfile
    STANDARD: UserProfile
    OUTSIDER: UserProfile
    @classmethod
    def values(cls) -> list[UserProfile]: ...
    @classmethod
    def from_str(cls, value: str) -> UserProfile: ...
    @property
    def str(self) -> str: ...
