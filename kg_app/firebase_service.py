import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)


def send_push_notification(fcm_token: str, title: str, body: str, data: dict = None):
    """
    Send push notification to a single device token.
    """
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=fcm_token,
            data={k: str(v) for k, v in (data or {}).items()},
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    sound='default',
                    click_action='FLUTTER_NOTIFICATION_CLICK',
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(sound='default')
                )
            ),
        )

        response = messaging.send(message)
        return {"success": True, "message_id": response}

    except messaging.UnregisteredError:
        return {"success": False, "error": "Token is unregistered/invalid."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_import_notifications(fe_task_counts: dict, tl_task_counts: dict):
    """
    Send task assignment notifications to fe and tl users after Excel import.
    fe_task_counts: { 'Rudra1234': 25, ... }
    tl_task_counts: { 'TLUser1': 10, ... }
    """
    from .models import FCMToken

    # Merge both dicts — if same username exists in both roles, sum the counts
    all_counts = {}
    for username, count in fe_task_counts.items():
        all_counts[username] = all_counts.get(username, 0) + count
    for username, count in tl_task_counts.items():
        all_counts[username] = all_counts.get(username, 0) + count

    for username, task_count in all_counts.items():
        try:
            tokens = FCMToken.objects.filter(
                username=username,
                is_active=True
            )

            if not tokens.exists():
                print(f"[FCM] No active token for username: {username}")
                continue

            for token_obj in tokens:
                result = send_push_notification(
                    fcm_token=token_obj.fcm_token,
                    title="New Task Assigned",
                    body=f"{task_count} task{'s' if task_count != 1 else ''} assigned to you. Click here to view.",
                    data={
                        "screen": "tasks",
                        "task_count": str(task_count),
                        "username": username,
                    }
                )
                print(f"[FCM] Sent to {username}: {result}")

                # Deactivate invalid tokens automatically
                if not result["success"] and "unregistered" in result.get("error", "").lower():
                    token_obj.is_active = False
                    token_obj.save()

        except Exception as e:
            print(f"[FCM] Error sending to {username}: {str(e)}")