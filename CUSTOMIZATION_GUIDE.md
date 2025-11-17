# AI Assistant Customization Guide

This guide explains how to customize your AI assistant for different use cases like medical assistant, legal advisor, customer support, maintenance support, or any other specialized purpose.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Branding Configuration](#branding-configuration)
4. [Use Case Examples](#use-case-examples)
5. [Advanced Customization](#advanced-customization)
6. [Technical Details](#technical-details)

---

## Overview

The AI assistant has been generalized and made fully customizable through a centralized configuration system. All branding, identity, and behavior settings are controlled through the `branding.yaml` file located in the project root.

### What Can Be Customized?

- **Assistant Identity**: Name, role, credentials, tagline
- **UI Elements**: Page titles, headers, labels, messages
- **Visual Branding**: Colors, gradients, logo, favicon
- **System Prompts**: Main assistant prompt, greetings, risk assessment context
- **Service Names**: Backend service names, database names
- **Features**: Enable/disable voice chat, risk assessment, etc.
- **Conversation Settings**: Temperature, max tokens, style

---

## Quick Start

### Basic Customization Steps

1. **Open the branding configuration file:**
   ```bash
   nano branding.yaml
   ```

2. **Update the assistant identity:**
   ```yaml
   assistant:
     name: "YourAssistantName"
     role: "your assistant role"
     tagline: "Your Custom Tagline"
     description: "Description of your assistant"
     credentials: "professional background"
   ```

3. **Update the system prompt:**
   ```yaml
   prompts:
     main_system: |
       You are {assistant_name}, a {credentials}...
       (customize the prompt for your use case)

     greeting: |
       Hello! I'm {assistant_name}...
       (customize the greeting message)
   ```

4. **Customize visual branding (optional):**
   ```yaml
   visual:
     colors:
       primary: "#YOUR_COLOR"
       secondary: "#YOUR_COLOR"
       gradient: "linear-gradient(...)"
   ```

5. **Restart the services** for changes to take effect:
   ```bash
   # Backend
   cd services/backend
   python app.py

   # AI Backend
   cd services/ai_backend
   python main.py
   ```

6. **Reload the frontend** in your browser to see the changes

---

## Branding Configuration

### Configuration File Structure

The `branding.yaml` file is divided into several sections:

#### 1. Assistant Identity

```yaml
assistant:
  name: "Amanda"              # The name of your AI assistant
  role: "relationship therapist"    # The role/profession
  tagline: "Your Relationship Support Companion"
  description: "A compassionate AI assistant..."
  credentials: "trained psychotherapist..."
```

**Placeholders**: You can use `{assistant_name}`, `{role}`, and `{credentials}` in prompts and UI text.

#### 2. UI Branding

```yaml
ui:
  page_title: "{assistant_name} - Relationship Support Chatbot"
  header_text: "{assistant_name}"
  welcome_message: "Welcome to {assistant_name}"

  chat:
    assistant_label: "{assistant_name}"
    user_label: "You"
    status:
      thinking: "{assistant_name} is thinking..."
      speaking: "{assistant_name} is speaking..."
      typing: "{assistant_name} is typing..."
      listening: "Listening..."
      processing: "Processing your message..."
```

#### 3. Visual Branding

```yaml
visual:
  logo:
    path: ""                    # Path to logo (e.g., "logo.png")
    alt_text: "{assistant_name} Logo"
    width: "150px"
    height: "50px"

  colors:
    primary: "#0066cc"
    secondary: "#667eea"
    accent: "#764ba2"
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    text_primary: "#333333"
    text_secondary: "#666666"
    text_light: "#ffffff"

  favicon: ""                   # Path to favicon
```

**Adding a Logo:**
1. Place your logo image in `services/frontend/static/img/`
2. Update the `visual.logo.path` to the filename (e.g., `"logo.png"`)
3. Adjust width and height as needed

#### 4. System Prompts

```yaml
prompts:
  main_system: |
    You are {assistant_name}, a {credentials}...

    Core Capabilities:
    - List your assistant's capabilities
    - Customize based on your use case

    Conversation Guidelines:
    - Define the tone and style
    - Set boundaries and limitations

  greeting: |
    Hello! I'm {assistant_name}...

  risk_assessment_context: |
    Customize how risk assessments are presented
```

#### 5. Service Configuration

```yaml
service:
  backend_name: "{assistant_name} Backend"
  ai_backend_name: "{assistant_name} AI Service"
  database_name: "amanda"      # Database filename
  session_timeout: 30          # Minutes
```

#### 6. Feature Flags

```yaml
features:
  voice_chat_enabled: true
  risk_assessment_enabled: true
  transcripts_enabled: true
  admin_dashboard_enabled: true
```

#### 7. Conversation Settings

```yaml
conversation:
  temperature: 0.7             # LLM temperature (0.0-1.0)
  max_tokens: 2048            # Maximum response length
  style: "empathetic"         # formal, casual, empathetic, professional
  language: "en"              # Default language
```

---

## Use Case Examples

### Example 1: Medical Assistant

```yaml
assistant:
  name: "MediCare AI"
  role: "medical assistant"
  tagline: "Your Personal Healthcare Companion"
  description: "An AI assistant designed to provide health information and wellness support."
  credentials: "medical information specialist with expertise in general health topics"

prompts:
  main_system: |
    You are {assistant_name}, a {credentials}. Your role is to provide
    evidence-based health information and wellness support.

    Core Capabilities:
    1. Health Information: Provide accurate, evidence-based health information
    2. Symptom Discussion: Help users articulate and understand their symptoms
    3. Wellness Guidance: Offer lifestyle and wellness recommendations
    4. Medical Navigation: Guide users on when to seek professional care

    IMPORTANT DISCLAIMERS:
    - You are NOT a doctor and cannot diagnose medical conditions
    - You cannot prescribe medications or treatments
    - Always recommend consulting healthcare professionals for medical advice
    - In emergencies, direct users to call emergency services

    Conversation Guidelines:
    - Use clear, accessible medical language
    - Be compassionate and supportive
    - Emphasize the importance of professional medical care
    - Provide reliable sources when sharing health information

  greeting: |
    Hello! I'm {assistant_name}, your medical information assistant.
    I'm here to provide general health information and wellness support.

    Please note: I'm not a substitute for professional medical advice.
    Always consult with healthcare providers for medical concerns.

    How can I assist you today?

visual:
  colors:
    primary: "#2E7D32"        # Medical green
    secondary: "#1976D2"      # Professional blue
    accent: "#00897B"
    gradient: "linear-gradient(135deg, #1976D2 0%, #2E7D32 100%)"

conversation:
  temperature: 0.5            # Lower for more factual responses
  style: "professional"
```

### Example 2: Legal Advisor

```yaml
assistant:
  name: "LegalAI Advisor"
  role: "legal information assistant"
  tagline: "Your Legal Information Resource"
  description: "An AI assistant providing general legal information and guidance."
  credentials: "legal information specialist with knowledge of common legal matters"

prompts:
  main_system: |
    You are {assistant_name}, a {credentials}. Your role is to provide
    general legal information to help users understand legal concepts.

    Core Capabilities:
    1. Legal Education: Explain legal concepts in accessible terms
    2. Process Guidance: Describe legal procedures and requirements
    3. Resource Direction: Point users to appropriate legal resources
    4. Document Understanding: Help users understand legal documents

    CRITICAL DISCLAIMERS:
    - You are NOT a licensed attorney and cannot provide legal advice
    - You cannot represent users in legal matters
    - Always recommend consulting with a licensed attorney
    - Different jurisdictions have different laws - specify this limitation

    Conversation Guidelines:
    - Use formal, professional language
    - Be precise and accurate with legal terminology
    - Always include appropriate disclaimers
    - Emphasize the importance of consulting qualified legal professionals
    - Never make definitive statements about specific legal outcomes

  greeting: |
    Hello! I'm {assistant_name}, your legal information resource.
    I provide general legal information and can help you understand
    legal concepts and processes.

    IMPORTANT: I am not a licensed attorney and this is not legal advice.
    For specific legal matters, please consult with a qualified attorney
    in your jurisdiction.

    What legal topic would you like to learn about?

visual:
  colors:
    primary: "#1A237E"        # Deep blue (trust, authority)
    secondary: "#424242"      # Professional gray
    accent: "#C62828"         # Accent red
    gradient: "linear-gradient(135deg, #1A237E 0%, #424242 100%)"

conversation:
  temperature: 0.3            # Very factual
  style: "formal"

features:
  risk_assessment_enabled: false    # May not be relevant for legal
```

### Example 3: Customer Support

```yaml
assistant:
  name: "SupportBot"
  role: "customer support agent"
  tagline: "We're Here to Help"
  description: "Your 24/7 customer support assistant for [Company Name]"
  credentials: "customer support specialist for [Company Name]"

prompts:
  main_system: |
    You are {assistant_name}, a {credentials}. Your role is to provide
    excellent customer support and resolve customer issues efficiently.

    Core Capabilities:
    1. Issue Resolution: Help customers solve problems with products/services
    2. Product Information: Answer questions about features and usage
    3. Account Support: Assist with account-related inquiries
    4. Escalation: Identify when to escalate to human support

    Company Knowledge:
    - [Add specific product/service information]
    - [Add common issues and solutions]
    - [Add company policies]

    Conversation Guidelines:
    - Be friendly, patient, and professional
    - Acknowledge customer frustration with empathy
    - Provide clear, step-by-step solutions
    - Follow up to ensure issues are resolved
    - Know when to escalate to human support

  greeting: |
    Hello! I'm {assistant_name} from [Company Name].
    I'm here to help you with any questions or issues you may have.

    How can I assist you today?

visual:
  colors:
    primary: "#FF6B00"        # Your brand color
    secondary: "#2196F3"
    accent: "#FFC107"
    gradient: "linear-gradient(135deg, #FF6B00 0%, #FFC107 100%)"

conversation:
  temperature: 0.6
  style: "casual"

features:
  risk_assessment_enabled: false
  voice_chat_enabled: true
```

### Example 4: Technical Maintenance Support

```yaml
assistant:
  name: "TechSupport AI"
  role: "technical support specialist"
  tagline: "Expert Technical Assistance"
  description: "AI-powered technical support for troubleshooting and maintenance"
  credentials: "technical support engineer with expertise in [systems/equipment]"

prompts:
  main_system: |
    You are {assistant_name}, a {credentials}. Your role is to provide
    technical troubleshooting and maintenance support.

    Core Capabilities:
    1. Diagnostics: Help identify technical issues
    2. Troubleshooting: Guide through systematic problem-solving
    3. Maintenance: Provide preventive maintenance guidance
    4. Documentation: Reference technical manuals and documentation

    Technical Approach:
    - Use systematic troubleshooting methodology
    - Request specific technical details (model numbers, error codes, etc.)
    - Provide clear, step-by-step instructions
    - Include safety warnings when relevant
    - Know when to recommend professional technicians

    Conversation Guidelines:
    - Be precise and technical when appropriate
    - Use diagrams or structured lists for complex procedures
    - Verify user understanding before moving to next steps
    - Document solutions for future reference

  greeting: |
    Hello! I'm {assistant_name}, your technical support assistant.
    I'm here to help you troubleshoot issues and maintain your equipment.

    Please provide details about your issue, including:
    - Equipment/system model
    - Error messages or symptoms
    - What you've already tried

    How can I help you today?

visual:
  colors:
    primary: "#37474F"        # Technical gray-blue
    secondary: "#00BCD4"      # Cyan (technical/modern)
    accent: "#FF9800"         # Warning orange
    gradient: "linear-gradient(135deg, #37474F 0%, #00BCD4 100%)"

conversation:
  temperature: 0.4            # Factual and precise
  style: "professional"
  max_tokens: 3000           # Longer responses for detailed instructions
```

---

## Advanced Customization

### Custom Logo Integration

1. **Prepare your logo:**
   - Recommended formats: PNG (with transparency) or SVG
   - Recommended size: 150x50px (adjust based on your design)

2. **Add logo to project:**
   ```bash
   # Create images directory if it doesn't exist
   mkdir -p services/frontend/static/img

   # Copy your logo
   cp /path/to/your/logo.png services/frontend/static/img/
   ```

3. **Update branding.yaml:**
   ```yaml
   visual:
     logo:
       path: "logo.png"
       alt_text: "YourBrand Logo"
       width: "150px"
       height: "50px"
   ```

### Custom Color Schemes

You can fully customize the color scheme to match your brand:

```yaml
visual:
  colors:
    # Primary colors
    primary: "#YOUR_PRIMARY_COLOR"
    secondary: "#YOUR_SECONDARY_COLOR"
    accent: "#YOUR_ACCENT_COLOR"

    # Background gradient
    gradient: "linear-gradient(135deg, #START_COLOR 0%, #END_COLOR 100%)"

    # Text colors
    text_primary: "#333333"      # Main text color
    text_secondary: "#666666"    # Secondary text
    text_light: "#ffffff"        # Light text (on dark backgrounds)
```

**Tips:**
- Use a color palette generator to create harmonious color schemes
- Ensure sufficient contrast for accessibility (WCAG AA compliance)
- Test colors on different screens and in different lighting

### Multi-Language Support

To add support for multiple languages:

1. **Set default language in branding.yaml:**
   ```yaml
   conversation:
     language: "en"    # or "es", "fr", etc.
   ```

2. **Customize prompts in target language:**
   ```yaml
   prompts:
     main_system: |
       Usted es {assistant_name}, un {credentials}...
       (Write your prompts in the target language)

     greeting: |
       ¡Hola! Soy {assistant_name}...
   ```

3. **Update UI text:**
   ```yaml
   ui:
     chat:
       status:
         thinking: "{assistant_name} está pensando..."
         speaking: "{assistant_name} está hablando..."
   ```

### Feature-Specific Customization

#### Disabling Features

```yaml
features:
  voice_chat_enabled: false           # Disable voice chat
  risk_assessment_enabled: false      # Disable risk assessment
  transcripts_enabled: true           # Keep transcripts
  admin_dashboard_enabled: false      # Hide admin features
```

#### Adjusting AI Behavior

```yaml
conversation:
  # Temperature controls randomness/creativity
  # Lower (0.0-0.3): More focused, factual, consistent
  # Medium (0.4-0.7): Balanced creativity and consistency
  # Higher (0.8-1.0): More creative, varied responses
  temperature: 0.7

  # Maximum length of responses
  max_tokens: 2048

  # Conversation style affects tone
  style: "empathetic"    # Options: formal, casual, empathetic, professional
```

---

## Technical Details

### Architecture Overview

The branding system consists of three main components:

1. **Branding Configuration File** (`branding.yaml`)
   - Central source of truth for all branding
   - Located in project root
   - YAML format for human readability

2. **Backend Branding Loaders**
   - `services/ai_backend/src/branding_config.py`
   - `services/backend/branding_config.py`
   - Load configuration and interpolate placeholders
   - Singleton pattern for efficiency

3. **Frontend Branding System**
   - `services/frontend/static/js/branding-config.js`
   - Fetches config from backend API
   - Dynamically updates UI elements
   - Applies CSS variables for colors

### Configuration Loading Flow

```
branding.yaml
    ↓
AI Backend Loader → System Prompts, Agent Configuration
    ↓
Backend API (/api/branding)
    ↓
Frontend JavaScript → UI Updates, CSS Variables
    ↓
User Interface
```

### API Endpoints

#### GET /api/branding
Fetches branding configuration for the frontend.

**Response:**
```json
{
  "success": true,
  "data": {
    "assistant": {
      "name": "Amanda",
      "tagline": "Your Relationship Support Companion"
    },
    "ui": { ... },
    "visual": { ... },
    "features": { ... }
  }
}
```

#### POST /api/branding/reload
Reloads branding configuration from file (useful during development).

**Response:**
```json
{
  "success": true,
  "message": "Branding configuration reloaded successfully"
}
```

### Files Modified for Customization

**Backend:**
- `branding.yaml` - Main configuration file
- `services/backend/app.py` - Loads branding for service name
- `services/backend/routes/branding.py` - Branding API endpoint
- `services/ai_backend/src/prompts.py` - Uses branding for prompts
- `services/ai_backend/src/branding_config.py` - Configuration loader

**Frontend:**
- `services/frontend/static/js/branding-config.js` - Config manager
- `services/frontend/index.html` - Landing page
- `services/frontend/dashboard/index.html` - Dashboard
- `services/frontend/auth/login.html` - Login page
- `services/frontend/auth/signup.html` - Signup page
- `services/frontend/static/js/dashboard.js` - Dashboard logic

### Troubleshooting

#### Changes Not Appearing

1. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Or clear browser cache completely

2. **Restart services:**
   ```bash
   # Restart backend
   cd services/backend
   pkill -f "python app.py"
   python app.py &

   # Restart AI backend
   cd services/ai_backend
   pkill -f "python main.py"
   python main.py &
   ```

3. **Check for YAML syntax errors:**
   ```bash
   python -c "import yaml; yaml.safe_load(open('branding.yaml'))"
   ```

#### Configuration Not Loading

1. **Check file path:**
   - Ensure `branding.yaml` is in the project root
   - Check file permissions (should be readable)

2. **Check backend logs:**
   - Look for "Loaded branding configuration" message
   - Check for any error messages

3. **Verify API endpoint:**
   - Visit http://localhost:5000/api/branding
   - Should return JSON with configuration

#### Colors Not Applying

1. **Check CSS variable syntax:**
   - Must be valid CSS color values
   - Gradients must be valid CSS gradient syntax

2. **Inspect browser console:**
   - Look for JavaScript errors
   - Check if branding config is loaded

---

## Best Practices

### 1. Backup Original Configuration
Before making changes, backup the original `branding.yaml`:
```bash
cp branding.yaml branding.yaml.backup
```

### 2. Test Changes Incrementally
Make small changes and test each one:
1. Update one section (e.g., assistant name)
2. Restart services
3. Test in browser
4. Proceed to next change

### 3. Use Version Control
Track your customizations with Git:
```bash
git add branding.yaml
git commit -m "Customize branding for medical assistant use case"
```

### 4. Document Custom Prompts
Keep notes on why you structured prompts a certain way:
```yaml
prompts:
  # NOTE: Temperature set to 0.5 for more factual medical responses
  # Emphasis on disclaimers due to medical nature
  main_system: |
    ...
```

### 5. Test Across Devices
Test your customized assistant on:
- Different browsers (Chrome, Firefox, Safari)
- Mobile devices
- Different screen sizes

### 6. Monitor Performance
After customization, monitor:
- Response quality and accuracy
- User feedback
- Error rates
- Performance metrics

---

## Support

For questions or issues with customization:

1. **Check this guide** for relevant examples
2. **Review the branding.yaml comments** for inline documentation
3. **Check the logs** for error messages
4. **Open an issue** on the project repository

---

## Summary Checklist

When customizing your assistant, use this checklist:

- [ ] Update assistant identity (name, role, tagline)
- [ ] Customize system prompts for your use case
- [ ] Update greeting message
- [ ] Customize UI text and labels
- [ ] Update color scheme (optional)
- [ ] Add logo and favicon (optional)
- [ ] Adjust conversation settings (temperature, style)
- [ ] Enable/disable relevant features
- [ ] Test all pages (login, signup, dashboard, chat)
- [ ] Test conversation quality
- [ ] Document your customizations
- [ ] Backup configuration file

---

*Last Updated: 2025*
