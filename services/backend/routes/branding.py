"""
Branding Configuration API Routes

Provides branding configuration to the frontend for dynamic customization.
"""

from flask import Blueprint, jsonify
from branding_config import get_branding_config

# Create blueprint
branding_bp = Blueprint('branding', __name__, url_prefix='/api')


@branding_bp.route('/branding', methods=['GET'])
def get_branding():
    """
    Get branding configuration for the frontend.

    Returns:
        JSON response with branding configuration
    """
    try:
        config = get_branding_config()
        frontend_config = config.get_frontend_config()

        return jsonify({
            'success': True,
            'data': frontend_config
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load branding configuration: {str(e)}'
        }), 500


@branding_bp.route('/branding/reload', methods=['POST'])
def reload_branding():
    """
    Reload branding configuration from file.
    Useful for development when branding.yaml is updated.

    Returns:
        JSON response with reload status
    """
    try:
        config = get_branding_config()
        config.reload()

        return jsonify({
            'success': True,
            'message': 'Branding configuration reloaded successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to reload branding configuration: {str(e)}'
        }), 500
