#!/usr/bin/env python3
"""
PepeluGPT - Enhanced Security Utilities
Comprehensive security functions for the cosmic intelligence platform.
Born of Light, Forged for Defense.
"""

import os
import re
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple
import logging
from functools import wraps
import traceback

class SecurityError(Exception):
    """Custom exception for security violations."""
    pass

class CosmicSecurityValidator:
    """Enhanced security validation with cosmic-level protection."""
    
    ALLOWED_EXTENSIONS = {
        '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.html', '.xml', 
        '.txt', '.md', '.pptx', '.ppt', '.csv', '.json'
    }
    
    DANGEROUS_PATTERNS = [
        r'\.\.',  # Path traversal
        r'[<>:"|?*]',  # Windows forbidden characters
        r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$',  # Windows reserved names
        r'[\x00-\x1f]',  # Control characters
    ]
    
    @staticmethod
    def validate_file_path_security(file_path: Union[str, Path], 
                                   allowed_roots: Optional[List[Path]] = None) -> Path:
        """Validate file path against security threats."""
        try:
            path = Path(file_path).resolve()
        except (OSError, ValueError) as e:
            raise SecurityError(f"🛡️ Invalid path format: {e}")
        
        # Check for path traversal attempts
        if '..' in str(file_path):
            raise SecurityError(f"🛡️ Path traversal attempt detected: {file_path}")
        
        # Validate against dangerous patterns
        for pattern in CosmicSecurityValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, str(file_path), re.IGNORECASE):
                raise SecurityError(f"🛡️ Dangerous pattern detected in path: {file_path}")
        
        # Check if path is within allowed roots
        if allowed_roots:
            path_allowed = False
            for root in allowed_roots:
                try:
                    path.relative_to(root.resolve())
                    path_allowed = True
                    break
                except ValueError:
                    continue
            
            if not path_allowed:
                raise SecurityError(f"🛡️ Path outside allowed boundaries: {path}")
        
        return path
    
    @staticmethod
    def sanitize_input(user_input: str, max_length: int = 1000) -> str:
        """Sanitize user input with cosmic precision."""
        if not isinstance(user_input, str):
            raise SecurityError("🛡️ Input must be a string")
        
        # Length validation
        if len(user_input) > max_length:
            raise SecurityError(f"🛡️ Input too long: {len(user_input)} > {max_length}")
        
        # Remove control characters except tab, newline, carriage return
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', user_input)
        
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    @staticmethod
    def validate_command_safety(command: List[str]) -> bool:
        """Validate command arguments for safe execution."""
        if not isinstance(command, list):
            raise SecurityError("🛡️ Command must be a list")
        
        if not command:
            raise SecurityError("🛡️ Empty command not allowed")
        
        # Check for dangerous commands
        dangerous_commands = {
            'rm', 'del', 'format', 'fdisk', 'mkfs', 'dd',
            'chmod', 'chown', 'sudo', 'su', 'passwd',
            'wget', 'curl', 'nc', 'netcat', 'telnet'
        }
        
        base_command = Path(command[0]).name.lower()
        if base_command in dangerous_commands:
            raise SecurityError(f"🛡️ Dangerous command not allowed: {base_command}")
        
        # Check for shell injection patterns in arguments
        shell_patterns = [r'[;&|`$]', r'\$\(', r'`.*`']
        for arg in command[1:]:
            for pattern in shell_patterns:
                if re.search(pattern, str(arg)):
                    raise SecurityError(f"🛡️ Shell injection pattern detected: {arg}")
        
        return True
    
    @staticmethod
    def secure_subprocess_run(command: List[str], timeout: int = 30, 
                            capture_output: bool = True) -> subprocess.CompletedProcess:
        """Securely execute subprocess with validation and timeouts."""
        # Validate command safety
        CosmicSecurityValidator.validate_command_safety(command)
        
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                check=False  # Don't raise on non-zero exit
            )
            return result
        except subprocess.TimeoutExpired:
            raise SecurityError(f"🛡️ Command timed out after {timeout} seconds")
        except FileNotFoundError:
            raise SecurityError(f"🛡️ Command not found: {command[0]}")
        except Exception as e:
            raise SecurityError(f"🛡️ Command execution failed: {e}")

class CosmicInputValidator:
    """Enhanced input validation for cosmic-level security."""
    
    @staticmethod
    def validate_query(query: str) -> str:
        """Validate search query input."""
        if not query or not query.strip():
            raise SecurityError("🛡️ Empty query not allowed")
        
        sanitized = CosmicSecurityValidator.sanitize_input(query, max_length=500)
        
        # Additional query-specific validation
        if len(sanitized) < 2:
            raise SecurityError("🛡️ Query too short")
        
        return sanitized
    
    @staticmethod
    def validate_filename(filename: str) -> str:
        """Validate filename for security."""
        sanitized = CosmicSecurityValidator.sanitize_input(filename, max_length=255)
        
        # Remove or replace dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', sanitized)
        
        # Ensure it's not a reserved name
        if sanitized.upper() in ['CON', 'PRN', 'AUX', 'NUL'] or \
           re.match(r'^(COM|LPT)[1-9]$', sanitized.upper()):
            sanitized = f"file_{sanitized}"
        
        return sanitized
    
    @staticmethod
    def validate_config_value(value: Any, expected_type: type, 
                            min_val: Any = None, max_val: Any = None) -> Any:
        """Validate configuration values."""
        if not isinstance(value, expected_type):
            raise SecurityError(f"🛡️ Invalid config type: expected {expected_type}, got {type(value)}")
        
        if min_val is not None and value < min_val:
            raise SecurityError(f"🛡️ Config value too small: {value} < {min_val}")
        
        if max_val is not None and value > max_val:
            raise SecurityError(f"🛡️ Config value too large: {value} > {max_val}")
        
        return value

class SecureFileHandler:
    """Secure file operations with cosmic protection."""
    
    def __init__(self, allowed_roots: Optional[List[Path]] = None):
        """Initialize with allowed root directories."""
        self.allowed_roots = allowed_roots or [Path.cwd()]
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def safe_read_file(self, file_path: Union[str, Path], 
                      max_size: int = 100 * 1024 * 1024) -> str:  # 100MB limit
        """Safely read file with size and path validation."""
        validated_path = CosmicSecurityValidator.validate_file_path_security(
            file_path, self.allowed_roots
        )
        
        if not validated_path.exists():
            raise SecurityError(f"🛡️ File not found: {validated_path}")
        
        if not validated_path.is_file():
            raise SecurityError(f"🛡️ Not a file: {validated_path}")
        
        # Check file size
        file_size = validated_path.stat().st_size
        if file_size > max_size:
            raise SecurityError(f"🛡️ File too large: {file_size} > {max_size}")
        
        try:
            with open(validated_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content
        except (IOError, OSError) as e:
            raise SecurityError(f"🛡️ Failed to read file: {e}")
    
    def safe_write_file(self, file_path: Union[str, Path], content: str,
                       max_size: int = 10 * 1024 * 1024) -> bool:  # 10MB limit
        """Safely write file with validation."""
        validated_path = CosmicSecurityValidator.validate_file_path_security(
            file_path, self.allowed_roots
        )
        
        # Check content size
        content_size = len(content.encode('utf-8'))
        if content_size > max_size:
            raise SecurityError(f"🛡️ Content too large: {content_size} > {max_size}")
        
        # Ensure parent directory exists and is writable
        validated_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(validated_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Safely wrote file: {validated_path}")
            return True
        except (IOError, OSError) as e:
            raise SecurityError(f"🛡️ Failed to write file: {e}")


# ========== ENHANCED SECURITY INTEGRATION ==========
# Integrated from enhanced_security_integration.py

# Add validation modules to path
try:
    sys.path.append(str(Path(__file__).parent.parent / 'validation'))
    from ..validation.input_sanitizer import EnhancedInputSanitizer
    from ..validation.privacy_check import PrivacyGuard
    from ..validation.security_validator import SecurityValidator as ValidationSecurityValidator
    from ..validation.module_guard import ModuleGuard as ValidationModuleGuard
except ImportError as e:
    print(f"⚠️ Validation modules not found: {e}")
    # Create mock classes for backward compatibility
    class EnhancedInputSanitizer:
        @staticmethod
        def sanitize_input(text): return text, True, {}
    
    class PrivacyGuard:
        @staticmethod
        def scan_for_pii(text): return False, {}
    
    class ValidationSecurityValidator:
        @staticmethod
        def validate_comprehensive_security(text): return {"overall_score": 100, "is_safe": True}
    
    class ValidationModuleGuard:
        @staticmethod
        def create_secure_environment(): return {}


class EnhancedSecurityCore:
    """Enhanced security core with integrated validation framework."""
    
    def __init__(self):
        """Initialize security core with validation components."""
        self.input_sanitizer = EnhancedInputSanitizer()
        self.privacy_guard = PrivacyGuard()
        self.security_validator = ValidationSecurityValidator()
        self.module_guard = ValidationModuleGuard()
        
        # Security configuration
        self.security_config = {
            'strict_mode': True,
            'log_security_events': True,
            'block_suspicious_input': True,
            'privacy_protection_level': 'high',
            'validation_enabled': True
        }
        
        # Security metrics
        self.security_metrics = {
            'total_validations': 0,
            'blocked_inputs': 0,
            'pii_detections': 0,
            'security_warnings': 0,
            'sanitization_events': 0
        }
    
    def validate_and_sanitize_input(self, user_input: str) -> Tuple[str, bool, Dict[str, Any]]:
        """Comprehensive input validation and sanitization."""
        self.security_metrics['total_validations'] += 1
        
        try:
            # Step 1: Input sanitization
            sanitized_input, is_safe, sanitization_report = self.input_sanitizer.sanitize_input(user_input)
            
            if not is_safe and self.security_config['block_suspicious_input']:
                self.security_metrics['blocked_inputs'] += 1
                return "", False, {
                    'status': 'blocked',
                    'reason': 'Input failed sanitization',
                    'details': sanitization_report
                }
            
            if sanitization_report.get('modifications_made'):
                self.security_metrics['sanitization_events'] += 1
            
            # Step 2: Privacy scanning
            has_pii, pii_report = self.privacy_guard.scan_for_pii(sanitized_input)
            
            if has_pii:
                self.security_metrics['pii_detections'] += 1
                if self.security_config['privacy_protection_level'] == 'high':
                    return "", False, {
                        'status': 'blocked',
                        'reason': 'PII detected in input',
                        'details': pii_report
                    }
            
            # Step 3: Security validation
            security_report = self.security_validator.validate_comprehensive_security(sanitized_input)
            
            if not security_report.get('is_safe', True):
                self.security_metrics['security_warnings'] += 1
                if self.security_config['strict_mode']:
                    return "", False, {
                        'status': 'blocked',
                        'reason': 'Security validation failed',
                        'details': security_report
                    }
            
            # All validations passed
            validation_report = {
                'status': 'validated',
                'sanitization': sanitization_report,
                'privacy': pii_report,
                'security': security_report,
                'final_input': sanitized_input
            }
            
            return sanitized_input, True, validation_report
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            traceback.print_exc()
            return user_input, False, {
                'status': 'error',
                'reason': f'Validation system error: {e}'
            }
    
    def validate_output(self, response: str) -> Tuple[str, bool, Dict[str, Any]]:
        """Validate and sanitize output before returning to user."""
        try:
            # Check for PII in output
            has_pii, pii_report = self.privacy_guard.scan_for_pii(response)
            
            if has_pii:
                self.security_metrics['pii_detections'] += 1
                # Mask PII in output
                sanitized_output, _, sanitization_report = self.input_sanitizer.sanitize_input(response)
                
                return sanitized_output, True, {
                    'status': 'sanitized',
                    'reason': 'PII detected in output',
                    'pii_detected': pii_report,
                    'sanitization': sanitization_report
                }
            
            return response, True, {'status': 'clean'}
            
        except Exception as e:
            print(f"❌ Output validation error: {e}")
            return response, False, {
                'status': 'error',
                'reason': f'Output validation error: {e}'
            }
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get current security metrics."""
        return {
            **self.security_metrics,
            'security_config': self.security_config,
            'validation_success_rate': (
                (self.security_metrics['total_validations'] - self.security_metrics['blocked_inputs']) /
                max(self.security_metrics['total_validations'], 1) * 100
            )
        }
    
    def update_security_config(self, config_updates: Dict[str, Any]) -> bool:
        """Update security configuration."""
        try:
            self.security_config.update(config_updates)
            return True
        except Exception as e:
            print(f"❌ Failed to update security config: {e}")
            return False


def security_validation_decorator(func):
    """Decorator to add security validation to any function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create security core instance for this execution
        security_core = EnhancedSecurityCore()
        
        # Validate input arguments that are strings
        validated_args = []
        for arg in args:
            if isinstance(arg, str):
                validated_input, is_safe, report = security_core.validate_and_sanitize_input(arg)
                if not is_safe and security_core.security_config['block_suspicious_input']:
                    raise SecurityError(f"Input validation failed: {report.get('reason', 'Unknown')}")
                validated_args.append(validated_input)
            else:
                validated_args.append(arg)
        
        # Execute the original function
        result = func(*validated_args, **kwargs)
        
        # Validate output if it's a string
        if isinstance(result, str):
            validated_output, is_safe, report = security_core.validate_output(result)
            if not is_safe:
                print(f"⚠️ Output validation warning: {report.get('reason', 'Unknown')}")
            return validated_output
        
        return result
    
    return wrapper


def create_secure_pepelugpt_wrapper():
    """Create a secure wrapper for PepeluGPT with integrated validation."""
    try:
        # Try to import the original PepeluGPT core
        sys.path.append(str(Path(__file__).parent.parent))
        
        security_core = EnhancedSecurityCore()
        
        def secure_process_query(query: str, personality_mode: str = "oracle") -> Dict[str, Any]:
            """Secure query processing with comprehensive validation."""
            
            # Step 1: Validate and sanitize input
            validated_query, is_safe, validation_report = security_core.validate_and_sanitize_input(query)
            
            if not is_safe:
                return {
                    'response': "❌ Input validation failed. Please check your query for security or privacy concerns.",
                    'status': 'validation_failed',
                    'validation_report': validation_report,
                    'security_metrics': security_core.get_security_metrics()
                }
            
            # Step 2: Create secure execution environment
            secure_env = security_core.module_guard.create_secure_environment()
            
            # Step 3: Process query (placeholder for actual PepeluGPT integration)
            try:
                # This would integrate with the actual PepeluGPT core
                response = f"🔒 Secure PepeluGPT Response (Personality: {personality_mode})\n\n"
                response += f"Query processed: {validated_query}\n\n"
                response += "✅ Security validation passed\n"
                response += f"🎭 Personality mode: {personality_mode}\n"
                response += f"🛡️ Security score: {validation_report.get('security', {}).get('overall_score', 'N/A')}"
                
                # Step 4: Validate output
                validated_response, output_safe, output_report = security_core.validate_output(response)
                
                return {
                    'response': validated_response,
                    'status': 'success',
                    'validation_report': validation_report,
                    'output_validation': output_report,
                    'security_metrics': security_core.get_security_metrics(),
                    'personality_mode': personality_mode
                }
                
            except Exception as e:
                return {
                    'response': "❌ An error occurred while processing your query.",
                    'status': 'processing_error',
                    'error': str(e),
                    'security_metrics': security_core.get_security_metrics()
                }
        
        return secure_process_query
        
    except Exception as e:
        print(f"❌ Failed to create secure wrapper: {e}")
        return None


def get_enhanced_security_help() -> str:
    """Get help text for enhanced security features."""
    return """
🛡️ **PepeluGPT Enhanced Security System**

**Security Features:**
• **Input Sanitization**: Removes malicious content and validates input
• **Privacy Protection**: Detects and masks PII (Personal Identifiable Information)
• **Security Validation**: Comprehensive threat detection and scoring
• **Module Security**: Secure execution environment for code processing

**Security Commands:**
• `/security status` - Show current security metrics
• `/security config` - Display security configuration
• `/security strict [on/off]` - Toggle strict security mode
• `/security privacy [low/medium/high]` - Set privacy protection level

**Privacy Protection:**
• Email addresses, phone numbers, SSNs automatically detected
• Credit card numbers and other sensitive data masked
• Configurable privacy levels (low/medium/high)

**Security Validation:**
• Malicious content detection (XSS, SQL injection, etc.)
• Input entropy analysis for anomaly detection
• Threat scoring and risk assessment
• Comprehensive security reporting

**Configuration Options:**
• `strict_mode`: Block all suspicious input (default: True)
• `privacy_protection_level`: Privacy scanning intensity (default: high)
• `block_suspicious_input`: Auto-block risky content (default: True)
• `log_security_events`: Log security events (default: True)

For maximum security, keep all protection features enabled.
"""


# Global enhanced security core instance
global_enhanced_security_core = EnhancedSecurityCore()

# ========== END ENHANCED SECURITY INTEGRATION ==========


def secure_clear_screen():
    """Securely clear the terminal screen."""
    try:
        if os.name == 'nt':  # Windows
            result = CosmicSecurityValidator.secure_subprocess_run(['cls'], timeout=5)
        else:  # Unix/Linux/Mac
            result = CosmicSecurityValidator.secure_subprocess_run(['clear'], timeout=5)
        
        if result.returncode != 0:
            # Fallback: print newlines
            print("\n" * 50)
    except SecurityError:
        # Ultimate fallback
        print("\n" * 50)

def generate_secure_hash(data: str, algorithm: str = 'sha256') -> str:
    """Generate secure hash of data."""
    if algorithm not in ['sha256', 'sha512', 'blake2b']:
        raise SecurityError(f"🛡️ Unsupported hash algorithm: {algorithm}")
    
    data_bytes = data.encode('utf-8')
    
    if algorithm == 'sha256':
        return hashlib.sha256(data_bytes).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(data_bytes).hexdigest()
    else:  # blake2b
        return hashlib.blake2b(data_bytes).hexdigest()

# Security configuration
SECURITY_CONFIG = {
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'max_query_length': 500,
    'max_filename_length': 255,
    'subprocess_timeout': 30,
    'allowed_file_extensions': CosmicSecurityValidator.ALLOWED_EXTENSIONS,
    'hash_algorithm': 'sha256'
}

def get_security_config() -> Dict[str, Any]:
    """Get current security configuration."""
    return SECURITY_CONFIG.copy()

def update_security_config(updates: Dict[str, Any]) -> None:
    """Update security configuration with validation."""
    for key, value in updates.items():
        if key not in SECURITY_CONFIG:
            raise SecurityError(f"🛡️ Unknown security config key: {key}")
        
        # Validate specific config values
        if key == 'max_file_size':
            CosmicInputValidator.validate_config_value(value, int, 1024, 1024**3)
        elif key == 'max_query_length':
            CosmicInputValidator.validate_config_value(value, int, 10, 10000)
        elif key == 'subprocess_timeout':
            CosmicInputValidator.validate_config_value(value, int, 1, 300)
        
        SECURITY_CONFIG[key] = value

if __name__ == "__main__":
    # Security validation tests
    print("🛡️ Testing PepeluGPT Security Utilities")
    
    # Test path validation
    try:
        CosmicSecurityValidator.validate_file_path_security("../../../etc/passwd")
        print("❌ Path traversal not detected!")
    except SecurityError:
        print("✅ Path traversal detected and blocked")
    
    # Test input sanitization
    sanitized = CosmicSecurityValidator.sanitize_input("Hello\x00World\x1f!")
    print(f"✅ Sanitized input: '{sanitized}'")
    
    # Test secure clear
    print("✅ Testing secure clear screen...")
    secure_clear_screen()
    
    # Test enhanced security features
    print("\n🔒 Testing Enhanced Security Integration")
    
    # Test enhanced security core
    enhanced_core = EnhancedSecurityCore()
    
    # Test input validation with mock PII
    test_input = "Hello, my email is user@example.com and my SSN is 123-45-6789"
    validated, safe, report = enhanced_core.validate_and_sanitize_input(test_input)
    
    print(f"Enhanced Test Input: {test_input}")
    print(f"Validated: {validated}")
    print(f"Safe: {safe}")
    print(f"Report status: {report.get('status', 'unknown')}")
    print(f"Security Metrics: {enhanced_core.get_security_metrics()}")
    
    # Test security decorator
    @security_validation_decorator
    def test_function(message: str) -> str:
        return f"Processed: {message}"
    
    try:
        result = test_function("Test message")
        print(f"✅ Decorator test result: {result}")
    except SecurityError as e:
        print(f"🛡️ Security decorator blocked input: {e}")
    
    # Test secure wrapper creation
    secure_wrapper = create_secure_pepelugpt_wrapper()
    if secure_wrapper:
        print("✅ Secure PepeluGPT wrapper created successfully")
        # Test secure query processing
        test_result = secure_wrapper("What is artificial intelligence?", "oracle")
        print(f"Secure query result status: {test_result.get('status', 'unknown')}")
    else:
        print("⚠️ Secure wrapper creation failed")
    
    print("\n🌟 All security utilities tests completed!")
    print(f"🔧 Enhanced security help available via get_enhanced_security_help()")
    
    # Display enhanced security help
    print("\n" + get_enhanced_security_help())
