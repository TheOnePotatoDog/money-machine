"""
Tests for authentication functionality.
"""
import pytest
from datetime import timedelta
from jose import jwt

from ai_shared.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM
)

def test_password_hashing():
    """Test that password hashing and verification works correctly."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Verify the hash is different from the original password
    assert hashed != password
    
    # Verify the password verification works
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    """Test that JWT token creation works correctly."""
    # Test data
    data = {"sub": "user@example.com"}
    expires_delta = timedelta(minutes=15)
    
    # Create token
    token = create_access_token(data, expires_delta)
    
    # Decode and verify token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Check that our data is in the token
    assert payload["sub"] == "user@example.com"
    
    # Check that expiration was added
    assert "exp" in payload
