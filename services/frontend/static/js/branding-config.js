/**
 * Branding Configuration Manager
 *
 * Fetches and manages branding configuration from the backend.
 * Provides a centralized way to access branding settings throughout the frontend.
 */

class BrandingConfig {
    constructor() {
        this.config = null;
        this.loading = false;
        this.loadPromise = null;
    }

    /**
     * Load branding configuration from the backend API
     * @returns {Promise<Object>} The branding configuration
     */
    async load() {
        // Return existing load promise if already loading
        if (this.loading && this.loadPromise) {
            return this.loadPromise;
        }

        // Return cached config if already loaded
        if (this.config) {
            return Promise.resolve(this.config);
        }

        this.loading = true;
        this.loadPromise = this._fetchConfig();

        try {
            this.config = await this.loadPromise;
            this.loading = false;
            return this.config;
        } catch (error) {
            this.loading = false;
            this.loadPromise = null;
            throw error;
        }
    }

    /**
     * Internal method to fetch configuration from backend
     * @private
     */
    async _fetchConfig() {
        try {
            const response = await fetch('http://localhost:5000/api/branding', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch branding config: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success && data.data) {
                return data.data;
            } else {
                throw new Error('Invalid branding configuration response');
            }
        } catch (error) {
            console.error('Error loading branding configuration:', error);
            // Return default configuration on error
            return this._getDefaultConfig();
        }
    }

    /**
     * Get default configuration (fallback)
     * @private
     */
    _getDefaultConfig() {
        return {
            assistant: {
                name: 'Assistant',
                tagline: 'Your AI Companion',
                description: 'An AI assistant ready to help.'
            },
            ui: {
                pageTitle: 'AI Assistant',
                headerText: 'Assistant',
                welcomeMessage: 'Welcome to Assistant',
                chat: {
                    assistantLabel: 'Assistant',
                    userLabel: 'You',
                    status: {
                        thinking: 'Assistant is thinking...',
                        speaking: 'Assistant is speaking...',
                        typing: 'Assistant is typing...',
                        listening: 'Listening...',
                        processing: 'Processing your message...'
                    }
                }
            },
            visual: {
                logo: {
                    path: '',
                    altText: 'Assistant Logo',
                    width: '150px',
                    height: '50px'
                },
                colors: {
                    primary: '#0066cc',
                    secondary: '#667eea',
                    accent: '#764ba2',
                    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    textPrimary: '#333333',
                    textSecondary: '#666666',
                    textLight: '#ffffff'
                },
                favicon: ''
            },
            features: {
                voiceChatEnabled: true,
                riskAssessmentEnabled: true,
                transcriptsEnabled: true,
                adminDashboardEnabled: true
            }
        };
    }

    /**
     * Get a configuration value using dot notation
     * @param {string} path - Path to config value (e.g., 'assistant.name')
     * @param {*} defaultValue - Default value if path not found
     * @returns {*} Configuration value
     */
    get(path, defaultValue = null) {
        if (!this.config) {
            console.warn('Branding config not loaded yet');
            return defaultValue;
        }

        const keys = path.split('.');
        let value = this.config;

        for (const key of keys) {
            if (value && typeof value === 'object' && key in value) {
                value = value[key];
            } else {
                return defaultValue;
            }
        }

        return value;
    }

    /**
     * Get assistant name
     * @returns {string}
     */
    getAssistantName() {
        return this.get('assistant.name', 'Assistant');
    }

    /**
     * Get assistant tagline
     * @returns {string}
     */
    getTagline() {
        return this.get('assistant.tagline', 'Your AI Companion');
    }

    /**
     * Get page title
     * @returns {string}
     */
    getPageTitle() {
        return this.get('ui.pageTitle', 'AI Assistant');
    }

    /**
     * Get chat status message
     * @param {string} type - Status type (thinking, speaking, typing, etc.)
     * @returns {string}
     */
    getStatusMessage(type) {
        return this.get(`ui.chat.status.${type}`, 'Processing...');
    }

    /**
     * Get assistant label for chat messages
     * @returns {string}
     */
    getAssistantLabel() {
        return this.get('ui.chat.assistantLabel', 'Assistant');
    }

    /**
     * Get user label for chat messages
     * @returns {string}
     */
    getUserLabel() {
        return this.get('ui.chat.userLabel', 'You');
    }

    /**
     * Get primary color
     * @returns {string}
     */
    getPrimaryColor() {
        return this.get('visual.colors.primary', '#0066cc');
    }

    /**
     * Get gradient
     * @returns {string}
     */
    getGradient() {
        return this.get('visual.colors.gradient', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)');
    }

    /**
     * Apply branding to the page
     * Updates page title, favicon, CSS variables, etc.
     */
    applyBranding() {
        if (!this.config) {
            console.warn('Cannot apply branding - config not loaded');
            return;
        }

        // Update page title
        const pageTitle = this.getPageTitle();
        if (pageTitle) {
            document.title = pageTitle;
        }

        // Update favicon if specified
        const faviconPath = this.get('visual.favicon');
        if (faviconPath) {
            let link = document.querySelector("link[rel~='icon']");
            if (!link) {
                link = document.createElement('link');
                link.rel = 'icon';
                document.head.appendChild(link);
            }
            link.href = faviconPath;
        }

        // Apply CSS variables for colors
        const colors = this.get('visual.colors', {});
        const root = document.documentElement;

        if (colors.primary) root.style.setProperty('--brand-primary', colors.primary);
        if (colors.secondary) root.style.setProperty('--brand-secondary', colors.secondary);
        if (colors.accent) root.style.setProperty('--brand-accent', colors.accent);
        if (colors.gradient) root.style.setProperty('--brand-gradient', colors.gradient);
        if (colors.textPrimary) root.style.setProperty('--text-primary', colors.textPrimary);
        if (colors.textSecondary) root.style.setProperty('--text-secondary', colors.textSecondary);
        if (colors.textLight) root.style.setProperty('--text-light', colors.textLight);

        console.log('Branding applied successfully');
    }

    /**
     * Reload configuration from backend
     * @returns {Promise<Object>}
     */
    async reload() {
        this.config = null;
        this.loading = false;
        this.loadPromise = null;
        return await this.load();
    }
}

// Create global instance
const brandingConfig = new BrandingConfig();

// Auto-load configuration when script is included
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', async () => {
        try {
            await brandingConfig.load();
            brandingConfig.applyBranding();
        } catch (error) {
            console.error('Failed to load branding configuration:', error);
        }
    });
} else {
    // DOM already loaded
    brandingConfig.load().then(() => {
        brandingConfig.applyBranding();
    }).catch(error => {
        console.error('Failed to load branding configuration:', error);
    });
}

// Export for use in other scripts
window.brandingConfig = brandingConfig;
