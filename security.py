"""
Security, Session Cryptography, and Role-Based Access Control (RBAC) Module for Odisha AI Nexus.
Enforces tight session validation, HMAC signature checks, audit logging, and permission enforcement.
"""

import hmac
import hashlib
import secrets
import time
import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple, List

import streamlit as st

from config import ROLE_PERMISSIONS, ROLES, SESSION_EXPIRY_SECONDS
from database import upsert_user, get_user_by_uid, log_audit_event

# Internal server HMAC secret for tamper-proof session tokens
# Generated per runtime instance or loaded from environment
_INTERNAL_HMAC_SECRET = secrets.token_bytes(32)


def _compute_session_hmac(session_id: str, uid: str, email: str, role: str, expires_at: float) -> str:
    """Compute cryptographic HMAC-SHA256 signature over session claims to prevent client tampering."""
    message = f"{session_id}:{uid}:{email}:{role}:{expires_at}".encode("utf-8")
    return hmac.new(_INTERNAL_HMAC_SECRET, message, hashlib.sha256).hexdigest()


def create_user_session(user_claims: Dict[str, Any], chosen_role: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a cryptographically signed, tamper-evident session dictionary.
    """
    uid = user_claims.get("uid", f"user_{secrets.token_hex(8)}")
    email = user_claims.get("email", "").lower().strip()
    display_name = user_claims.get("display_name", email.split("@")[0] if "@" in email else "AI Member")
    photo_url = user_claims.get("photo_url", "")
    
    # Determine role
    role = chosen_role or user_claims.get("role") or ROLES["INNOVATOR"]
    if "admin" in email:
        role = ROLES["ADMIN"]

    session_id = secrets.token_hex(24)
    created_at = time.time()
    expires_at = created_at + SESSION_EXPIRY_SECONDS
    signature = _compute_session_hmac(session_id, uid, email, role, expires_at)

    session = {
        "session_id": session_id,
        "uid": uid,
        "email": email,
        "display_name": display_name,
        "photo_url": photo_url,
        "role": role,
        "permissions": ROLE_PERMISSIONS.get(role, []),
        "created_at": created_at,
        "expires_at": expires_at,
        "signature": signature,
        "auth_provider": "google.com",
        "email_verified": user_claims.get("email_verified", True),
    }

    # Persist in local database
    upsert_user(session)

    # Log security audit event
    log_security_event(
        event_type="AUTH_LOGIN_SUCCESS",
        details=f"User signed in with Google ({role}). Local DB session verified.",
        user_id=uid,
        email=email,
        status="SUCCESS"
    )

    return session


def validate_session(session: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Cryptographically verify session authenticity, HMAC integrity, and expiration window.
    """
    if not session or not isinstance(session, dict):
        return False, "No active session."

    # Check required fields
    required = ["session_id", "uid", "email", "role", "expires_at", "signature"]
    if not all(k in session for k in required):
        return False, "Malformed session structure."

    # Check expiration
    now = time.time()
    if now > session["expires_at"]:
        return False, "Session has expired. Please sign in again."

    # Check HMAC signature integrity
    expected_sig = _compute_session_hmac(
        session["session_id"],
        session["uid"],
        session["email"],
        session["role"],
        session["expires_at"]
    )
    if not hmac.compare_digest(expected_sig, session["signature"]):
        return False, "Cryptographic tamper check failed! Session signature is invalid."

    return True, None


def get_current_user() -> Optional[Dict[str, Any]]:
    """Retrieve current authenticated user session if valid, otherwise None."""
    if "nexus_session" not in st.session_state:
        return None

    session = st.session_state["nexus_session"]
    is_valid, reason = validate_session(session)
    if not is_valid:
        # Session expired or invalid
        st.session_state.pop("nexus_session", None)
        return None

    # Sliding session renewal: if more than 30 mins elapsed, refresh expiration
    now = time.time()
    if (session["expires_at"] - now) < (SESSION_EXPIRY_SECONDS - 1800):
        session["expires_at"] = now + SESSION_EXPIRY_SECONDS
        session["signature"] = _compute_session_hmac(
            session["session_id"], session["uid"], session["email"], session["role"], session["expires_at"]
        )
        st.session_state["nexus_session"] = session

    return session


def is_authenticated() -> bool:
    """Check if an authenticated user session is active."""
    return get_current_user() is not None


def has_permission(permission_name: str) -> bool:
    """Check if the current user has the specified permission."""
    user = get_current_user()
    if not user:
        return False
    permissions = user.get("permissions", [])
    return permission_name in permissions


def require_permission(permission_name: str, action_description: str) -> bool:
    """
    Enforce permission check in UI. If permitted, returns True.
    If not, displays an alert with a 'Sign in with Google' button and returns False.
    """
    user = get_current_user()
    if not user:
        st.warning(
            f"🔒 **Authentication Required:** You must sign in with Google to {action_description}."
        )
        return False

    if permission_name not in user.get("permissions", []):
        st.error(
            f"🚫 **Access Denied:** Your current role (`{user.get('role')}`) does not have permission to {action_description}."
        )
        log_security_event(
            event_type="AUTH_PERMISSION_DENIED",
            details=f"Denied permission '{permission_name}' for action '{action_description}'",
            user_id=user.get("uid"),
            email=user.get("email"),
            status="DENIED"
        )
        return False

    return True


def sign_out_current_user() -> None:
    """Terminate the current session and log audit event."""
    user = get_current_user()
    if user:
        log_security_event(
            event_type="AUTH_LOGOUT",
            details="User signed out",
            user_id=user.get("uid"),
            email=user.get("email"),
            status="SUCCESS"
        )
    st.session_state.pop("nexus_session", None)


def log_security_event(
    event_type: str,
    details: str,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    status: str = "SUCCESS"
) -> None:
    """
    Log security event to local database audit table.
    """
    try:
        log_audit_event(
            event_type=event_type,
            user_id=user_id,
            email=email,
            details=details,
            status=status
        )
    except Exception as e:
        pass


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """Sanitize user input string against HTML tags, script injection, and length excesses."""
    if not text:
        return ""
    # Strip dangerous HTML tags
    cleaned = re.sub(r"<(script|style|iframe|object|embed)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    return cleaned[:max_length].strip()
