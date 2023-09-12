from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from auth.users import get_current_user
from models.notification_settings import ChannelSettings, NotificationSettings
from services.abc import (NotificationChannelSettingsServiceABC,
                          NotificationSettingsServiceABC)
from services.notification_settings import get_channel_settings, get_notification_settings

router = APIRouter()


@router.post(
    "/channel-settings/",
    response_model=None,
    summary="Create user channel settings",
    description="Create user channel notifications setting",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_channel_settings(
    channel: str,
    enabled: bool,
    user=Depends(get_current_user),
    notification_channel_settings_service: NotificationChannelSettingsServiceABC = Depends(
        get_channel_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.get(
    "/channel-settings/",
    response_model=ChannelSettings,
    summary="Get list of channel user settings",
    description="Get user channel notifications setting",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_channel_settings(
    user=Depends(get_current_user),
    notification_channel_settings_service: NotificationChannelSettingsServiceABC = Depends(
        get_channel_settings
    ),
) -> list[ChannelSettings]:
    pass


@router.patch(
    "/channel-settings/",
    response_model=None,
    summary="Change user settings",
    description='Change user channel notifications settings by sending boolean in "ENABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_channel_settings(
    channel: str,
    enabled: bool,
    user=Depends(get_current_user),
    notification_channel_settings_service: NotificationChannelSettingsServiceABC = Depends(
        get_channel_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.delete(
    "/channel-settings/",
    response_model=None,
    summary="Delete user settings",
    description='Delete user channel notifications settings by sending boolean in "ENABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_channel_settings(
    channel: str,
    user=Depends(get_current_user),
    notification_channel_settings_service: NotificationChannelSettingsServiceABC = Depends(
        get_channel_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.post(
    "/notification-settings/",
    response_model=None,
    summary="Create user exact notification setting",
    description='Receive or not exact notification by sending boolean in "DISABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    notification_id: UUID,
    disabled: bool,
    user=Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(
        get_notification_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.get(
    "/notification-settings/",
    response_model=NotificationSettings,
    summary="Get user notification settings",
    description='Receive or not exact notification by sending boolean in "DISABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    user=Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(
        get_notification_settings
    ),
) -> list[NotificationSettings]:
    pass


@router.patch(
    "/notification-settings/",
    response_model=None,
    summary="Change user exact notification setting",
    description='Receive or not exact notification by sending boolean in "DISABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    notification_id: UUID,
    disabled: bool,
    user=Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(
        get_notification_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass


@router.delete(
    "/notification-settings/",
    response_model=None,
    summary="Delete user exact notification setting",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    notification_id: UUID,
    user=Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(
        get_notification_settings
    ),
) -> Response(status_code=status.HTTP_200_OK):
    pass
