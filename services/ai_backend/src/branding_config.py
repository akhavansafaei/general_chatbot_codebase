"""
Branding Configuration Loader

This module loads and provides access to branding configuration from branding.yaml.
It allows easy customization of the AI assistant's identity, appearance, and behavior.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class BrandingConfig:
    """Loads and manages branding configuration."""

    _instance: Optional['BrandingConfig'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Singleton pattern to ensure single config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """Load branding configuration from branding.yaml."""
        # Try to find branding.yaml in project root
        current_dir = Path(__file__).resolve()
        project_root = current_dir.parent.parent.parent.parent
        branding_file = project_root / "branding.yaml"

        if not branding_file.exists():
            print(f"Warning: branding.yaml not found at {branding_file}")
            print("Using default configuration")
            self._config = self._get_default_config()
            return

        try:
            with open(branding_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            print(f"Loaded branding configuration from {branding_file}")
        except Exception as e:
            print(f"Error loading branding.yaml: {e}")
            print("Using default configuration")
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if branding.yaml is not found."""
        return {
            'assistant': {
                'name': 'Assistant',
                'role': 'AI assistant',
                'tagline': 'Your AI Companion',
                'description': 'An AI assistant ready to help.',
                'credentials': 'AI assistant'
            },
            'ui': {
                'page_title': '{assistant_name} - AI Assistant',
                'header_text': '{assistant_name}',
                'welcome_message': 'Welcome to {assistant_name}',
                'chat': {
                    'assistant_label': '{assistant_name}',
                    'user_label': 'You',
                    'status': {
                        'thinking': '{assistant_name} is thinking...',
                        'speaking': '{assistant_name} is speaking...',
                        'typing': '{assistant_name} is typing...',
                        'listening': 'Listening...',
                        'processing': 'Processing your message...'
                    }
                }
            },
            'prompts': {
                'main_system': 'You are an AI assistant.',
                'greeting': 'Hello! How can I help you today?',
                'risk_assessment_context': ''
            },
            'service': {
                'backend_name': 'AI Backend',
                'ai_backend_name': 'AI Service',
                'database_name': 'assistant',
                'session_timeout': 30
            },
            'conversation': {
                'temperature': 0.7,
                'max_tokens': 2048,
                'style': 'professional',
                'language': 'en'
            }
        }

    def _interpolate(self, text: str) -> str:
        """Replace placeholders in text with actual values."""
        if not isinstance(text, str):
            return text

        replacements = {
            '{assistant_name}': self.get('assistant.name', 'Assistant'),
            '{role}': self.get('assistant.role', 'AI assistant'),
            '{credentials}': self.get('assistant.credentials', 'AI assistant'),
            '{tagline}': self.get('assistant.tagline', 'Your AI Companion')
        }

        result = text
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            key: Configuration key in dot notation (e.g., 'assistant.name')
            default: Default value if key is not found

        Returns:
            Configuration value with placeholders replaced
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        # Interpolate placeholders if value is a string
        if isinstance(value, str):
            return self._interpolate(value)

        return value

    def get_assistant_name(self) -> str:
        """Get the assistant name."""
        return self.get('assistant.name', 'Assistant')

    def get_assistant_role(self) -> str:
        """Get the assistant role."""
        return self.get('assistant.role', 'AI assistant')

    def get_assistant_tagline(self) -> str:
        """Get the assistant tagline."""
        return self.get('assistant.tagline', 'Your AI Companion')

    def get_system_prompt(self) -> str:
        """Get the main system prompt with interpolated values."""
        return self.get('prompts.main_system', 'You are an AI assistant.')

    def get_greeting(self) -> str:
        """Get the greeting message with interpolated values."""
        return self.get('prompts.greeting', 'Hello! How can I help you today?')

    def get_risk_assessment_context(self) -> str:
        """Get the risk assessment context prompt."""
        return self.get('prompts.risk_assessment_context', '')

    def get_temperature(self) -> float:
        """Get the default conversation temperature."""
        return float(self.get('conversation.temperature', 0.7))

    def get_max_tokens(self) -> int:
        """Get the default max tokens."""
        return int(self.get('conversation.max_tokens', 2048))

    def get_all(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self._config

    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()


# Global instance
_branding_config = None


def get_branding_config() -> BrandingConfig:
    """Get the global branding configuration instance."""
    global _branding_config
    if _branding_config is None:
        _branding_config = BrandingConfig()
    return _branding_config


def get_assistant_name() -> str:
    """Convenience function to get assistant name."""
    return get_branding_config().get_assistant_name()


def get_system_prompt() -> str:
    """Convenience function to get system prompt."""
    return get_branding_config().get_system_prompt()


def get_greeting() -> str:
    """Convenience function to get greeting."""
    return get_branding_config().get_greeting()
