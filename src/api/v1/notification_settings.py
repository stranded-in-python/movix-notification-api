from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from auth.users import get_current_user
from models.notification_settings import ChannelSettings, NotificationSettings
from services.abc import (NotificationChannelSettingsServiceABC,
                          NotificationSettingsServiceABC)
from services.notification_settings import get_channel_settings_service, get_notification_settings_service

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
        get_channel_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_channel_settings_service.create_channel_setting(channel, enabled, user.user_id)
    return Response(status_code=status.HTTP_200_OK)

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
        get_channel_settings_service
    ),
) -> list[ChannelSettings]:
    return await notification_channel_settings_service.get_channel_settings(user.user_id)


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
        get_channel_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_channel_settings_service.change_channel_settings(channel, enabled, user.user_id)
    return Response(status_code=status.HTTP_200_OK)

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
        get_channel_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_channel_settings_service.delete_channel_settings(channel, user.user_id)
    return Response(status_code=status.HTTP_200_OK)


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
        get_notification_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_settings_service.create_notification_setting(notification_id, disabled, user.user_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/notification-settings/",
    response_model=NotificationSettings,
    summary="Get a list of user notification settings",
    description='Receive or not exact notification by sending boolean in "DISABLED" parameter',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def change_notification_settings(
    user=Depends(get_current_user),
    notification_settings_service: NotificationSettingsServiceABC = Depends(
        get_notification_settings_service
    ),
) -> list[NotificationSettings]:
    return await notification_settings_service.get_notification_settings(user.user_id)

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
        get_notification_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_settings_service.change_notification_settings(notification_id, disabled, user.user_id)
    return Response(status_code=status.HTTP_200_OK)

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
        get_notification_settings_service
    ),
) -> Response(status_code=status.HTTP_200_OK):
    await notification_settings_service.delete_notification_settings(notification_id, user.user_id)
    return Response(status_code=status.HTTP_200_OK)
