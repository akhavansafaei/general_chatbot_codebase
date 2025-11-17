"""
Branding Configuration Loader for Backend

This module loads branding configuration from the root branding.yaml file
and makes it available to the Flask backend.
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
        project_root = current_dir.parent.parent.parent
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
            'visual': {
                'logo': {
                    'path': '',
                    'alt_text': '{assistant_name} Logo',
                    'width': '150px',
                    'height': '50px'
                },
                'colors': {
                    'primary': '#0066cc',
                    'secondary': '#667eea',
                    'accent': '#764ba2',
                    'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'text_primary': '#333333',
                    'text_secondary': '#666666',
                    'text_light': '#ffffff'
                },
                'favicon': ''
            },
            'service': {
                'backend_name': 'AI Backend',
                'ai_backend_name': 'AI Service',
                'database_name': 'assistant',
                'session_timeout': 30
            },
            'features': {
                'voice_chat_enabled': True,
                'risk_assessment_enabled': True,
                'transcripts_enabled': True,
                'admin_dashboard_enabled': True
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

    def get_all(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self._config

    def get_frontend_config(self) -> Dict[str, Any]:
        """Get configuration formatted for frontend consumption."""
        return {
            'assistant': {
                'name': self.get('assistant.name'),
                'tagline': self.get('assistant.tagline'),
                'description': self.get('assistant.description')
            },
            'ui': {
                'pageTitle': self.get('ui.page_title'),
                'headerText': self.get('ui.header_text'),
                'welcomeMessage': self.get('ui.welcome_message'),
                'chat': {
                    'assistantLabel': self.get('ui.chat.assistant_label'),
                    'userLabel': self.get('ui.chat.user_label'),
                    'status': {
                        'thinking': self.get('ui.chat.status.thinking'),
                        'speaking': self.get('ui.chat.status.speaking'),
                        'typing': self.get('ui.chat.status.typing'),
                        'listening': self.get('ui.chat.status.listening'),
                        'processing': self.get('ui.chat.status.processing')
                    }
                }
            },
            'visual': {
                'logo': {
                    'path': self.get('visual.logo.path'),
                    'altText': self.get('visual.logo.alt_text'),
                    'width': self.get('visual.logo.width'),
                    'height': self.get('visual.logo.height')
                },
                'colors': {
                    'primary': self.get('visual.colors.primary'),
                    'secondary': self.get('visual.colors.secondary'),
                    'accent': self.get('visual.colors.accent'),
                    'gradient': self.get('visual.colors.gradient'),
                    'textPrimary': self.get('visual.colors.text_primary'),
                    'textSecondary': self.get('visual.colors.text_secondary'),
                    'textLight': self.get('visual.colors.text_light')
                },
                'favicon': self.get('visual.favicon')
            },
            'features': {
                'voiceChatEnabled': self.get('features.voice_chat_enabled', True),
                'riskAssessmentEnabled': self.get('features.risk_assessment_enabled', True),
                'transcriptsEnabled': self.get('features.transcripts_enabled', True),
                'adminDashboardEnabled': self.get('features.admin_dashboard_enabled', True)
            }
        }

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
