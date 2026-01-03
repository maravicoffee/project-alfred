"""
Project Alfred - Security & Input Validation
Protects against common security vulnerabilities
"""

import re
from typing import Any, Dict, Optional
import html
import json


class SecurityValidator:
    """Security validation and sanitization"""
    
    def __init__(self):
        # Dangerous patterns to block
        self.sql_injection_patterns = [
            r"(\bUNION\b.*\bSELECT\b)",
            r"(\bDROP\b.*\bTABLE\b)",
            r"(\bINSERT\b.*\bINTO\b)",
            r"(\bDELETE\b.*\bFROM\b)",
            r"(--)",
            r"(;.*--)",
            r"(\bEXEC\b)",
            r"(\bEXECUTE\b)"
        ]
        
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe",
            r"<object",
            r"<embed"
        ]
        
        self.command_injection_patterns = [
            r"[;&|`$]",
            r"\$\(",
            r"``",
            r">\s*/",
            r"<\s*/"
        ]
    
    def sanitize_input(self, text: str, allow_html: bool = False) -> str:
        """Sanitize user input"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Escape HTML if not allowed
        if not allow_html:
            text = html.escape(text)
        
        # Limit length
        max_length = 10000
        if len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    def validate_sql_safe(self, text: str) -> bool:
        """Check if text is safe from SQL injection"""
        text_upper = text.upper()
        
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return False
        
        return True
    
    def validate_xss_safe(self, text: str) -> bool:
        """Check if text is safe from XSS"""
        text_lower = text.lower()
        
        for pattern in self.xss_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False
        
        return True
    
    def validate_command_safe(self, text: str) -> bool:
        """Check if text is safe from command injection"""
        for pattern in self.command_injection_patterns:
            if re.search(pattern, text):
                return False
        
        return True
    
    def validate_user_input(self, text: str, context: str = "general") -> Dict[str, Any]:
        """
        Comprehensive input validation
        
        Args:
            text: Input text to validate
            context: Context of input ("general", "code", "sql", "command")
        
        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "sanitized": text,
            "warnings": []
        }
        
        # Sanitize
        results["sanitized"] = self.sanitize_input(text)
        
        # Context-specific validation
        if context == "sql":
            if not self.validate_sql_safe(text):
                results["valid"] = False
                results["warnings"].append("Potential SQL injection detected")
        
        elif context == "command":
            if not self.validate_command_safe(text):
                results["valid"] = False
                results["warnings"].append("Potential command injection detected")
        
        elif context == "general":
            if not self.validate_xss_safe(text):
                results["valid"] = False
                results["warnings"].append("Potential XSS attack detected")
        
        # Check for excessive length
        if len(text) > 10000:
            results["warnings"].append("Input exceeds maximum length")
        
        return results
    
    def validate_json(self, data: str) -> Optional[Dict]:
        """Safely parse and validate JSON"""
        try:
            parsed = json.loads(data)
            return parsed
        except json.JSONDecodeError:
            return None
    
    def validate_user_id(self, user_id: str) -> bool:
        """Validate user ID format"""
        # Allow alphanumeric, hyphens, underscores
        pattern = r'^[a-zA-Z0-9_-]{1,64}$'
        return bool(re.match(pattern, user_id))
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def rate_limit_check(self, user_id: str, action: str, limit: int = 100, window: int = 60) -> bool:
        """
        Check rate limiting (simplified version)
        In production, use Redis or similar for distributed rate limiting
        """
        # This is a placeholder - implement with Redis in production
        return True
    
    def sanitize_file_path(self, path: str) -> str:
        """Sanitize file path to prevent directory traversal"""
        # Remove directory traversal attempts
        path = path.replace('..', '')
        path = path.replace('//', '/')
        
        # Only allow filename, no directories
        import os
        path = os.path.basename(path)
        
        return path
    
    def validate_code_safety(self, code: str) -> Dict[str, Any]:
        """
        Validate Python code for dangerous operations
        """
        dangerous_imports = [
            'os.system',
            'subprocess.Popen',
            'eval',
            'exec',
            '__import__',
            'compile',
            'open(',  # File operations
            'socket',
            'urllib',
            'requests'
        ]
        
        warnings = []
        
        for dangerous in dangerous_imports:
            if dangerous in code:
                warnings.append(f"Potentially dangerous operation: {dangerous}")
        
        return {
            "safe": len(warnings) == 0,
            "warnings": warnings
        }


# Singleton instance
security_validator = SecurityValidator()


# Example usage
if __name__ == "__main__":
    validator = SecurityValidator()
    
    # Test SQL injection
    sql_test = "SELECT * FROM users WHERE id = 1; DROP TABLE users--"
    result = validator.validate_user_input(sql_test, context="sql")
    print(f"SQL Test: {result}")
    
    # Test XSS
    xss_test = "<script>alert('XSS')</script>"
    result = validator.validate_user_input(xss_test, context="general")
    print(f"XSS Test: {result}")
    
    # Test safe input
    safe_test = "Hello, this is a normal message"
    result = validator.validate_user_input(safe_test)
    print(f"Safe Test: {result}")
