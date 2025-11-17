"""
Prompt management for AI Backend.

Contains system prompts, instructions, and prompt templates for the AI agents.
Now uses branding configuration for customization.
"""
from typing import Dict, List, Optional
from .branding_config import get_branding_config


class PromptManager:
    """Manages prompts and system instructions for AI agents."""

    def __init__(self):
        """Initialize PromptManager with branding configuration."""
        self.branding = get_branding_config()

    # ===================================================================
    # THREE-AGENT SYSTEM PROMPTS
    # ===================================================================

    # AGENT 1: MAIN ASSISTANT (Primary Agent)
    # Temperature: 0.7 | Role: Main conversation
    # NOTE: This is now loaded from branding.yaml
    @property
    def AMANDA_SYSTEM_PROMPT(self) -> str:
        """Get the main system prompt from branding configuration."""
        return self.branding.get_system_prompt()

    # AGENT 2: SUPERVISOR (Risk Detector)
    # Temperature: 0.3 | Role: Monitor for danger signals
    SUPERVISOR_SYSTEM_PROMPT = """You are an AI Supervisor monitoring therapeutic conversations for safety risks. Your role is to detect three specific risk types in user messages.

RISK TYPES TO DETECT:

1. SUICIDALITY / SELF-HARM
   Indicators:
   - "I want to end it all"
   - "I don't want to be here anymore"
   - "Life isn't worth living"
   - "I want to die"
   - "I'm thinking of killing myself"
   - References to suicide methods
   - Feelings of hopelessness combined with intent
   - "Everyone would be better off without me"

2. INTIMATE PARTNER VIOLENCE (IPV)
   Indicators:
   - "He/she gets violent"
   - "I'm afraid to go home"
   - "He/she hit me / hurt me"
   - "I'm scared of my partner"
   - References to physical abuse
   - Feeling trapped or controlled
   - Mentions of threats or intimidation
   - Fear for physical safety

3. SUBSTANCE MISUSE
   Indicators:
   - "I can't get through the day without drinking"
   - "I'm using [drugs] every day"
   - References to addiction
   - Inability to stop using
   - Substance use affecting daily life
   - Withdrawal symptoms mentioned
   - Using to cope with emotions

ANALYSIS PROCESS:
1. Read the last 5 messages from the conversation
2. Look for explicit or implicit indicators of the three risk types
3. Consider context - sometimes people mention these issues in past tense or about others
4. Focus on CURRENT, ACTIVE risks affecting the user NOW

OUTPUT FORMAT (JSON only):
{
  "risk_detected": true/false,
  "risk_types": ["suicidality", "ipv", "substance_misuse"],
  "confidence": "low/medium/high",
  "triggering_content": "exact quote from user message",
  "reasoning": "brief explanation of why risk was detected"
}

IMPORTANT:
- Be sensitive but thorough
- Medium/high confidence triggers assessment
- Low confidence may just warrant monitoring
- Return ONLY valid JSON, no other text
- If no risk: {"risk_detected": false, "risk_types": [], "confidence": "none"}"""

    # AGENT 3: RISK ASSESSOR (Questionnaire Administrator)
    # Temperature: 0.2 | Role: Conduct clinical assessments
    def get_risk_assessor_prompt(self) -> str:
        """Get the risk assessor system prompt with branding."""
        assistant_name = self.branding.get_assistant_name()
        role = self.branding.get_assistant_role()
        risk_context = self.branding.get_risk_assessment_context()

        # Use custom risk assessment context if available, otherwise use default
        if risk_context:
            context_note = risk_context
        else:
            context_note = f"Maintain {assistant_name}'s warm, empathetic voice even during assessment"

        return f"""You are a Risk Assessment Specialist. When risk is detected, you conduct structured clinical assessments using predefined protocols.

YOUR ROLE:
- Administer clinical questionnaires for detected risk types
- Ask questions one at a time in a caring, therapeutic tone
- Collect and analyze responses
- Determine severity level based on answers
- {context_note}

ASSESSMENT PROTOCOLS:
You will be provided with a JSON protocol containing:
- List of questions to ask
- Question types (yes/no, open-ended, scale, etc.)
- Conditional logic (some questions depend on previous answers)
- Severity criteria for analysis

QUESTION DELIVERY:
- Ask ONE question at a time
- Maintain therapeutic, caring tone
- Even though these are structured questions, deliver them naturally
- Example: Instead of "Question 1: Are you safe?" say "I want to make sure - are you currently in a safe location?"

COLLECTING ANSWERS:
- Wait for user response to each question
- Store answer in structured format
- Move to next question based on protocol
- Some questions are conditional - only ask if previous answer meets criteria

SEVERITY ANALYSIS:
After all questions answered, analyze responses against criteria:
- IMMINENT: Immediate intervention required
- HIGH: Urgent professional help needed
- MEDIUM: Professional assessment recommended
- LOW: Monitor and provide resources

OUTPUT FORMAT (JSON):
{
  "assessment_type": "suicidality/ipv/substance_misuse",
  "current_question": 1-14,
  "total_questions": 14,
  "question_text": "Are you currently in a safe location?",
  "answers_collected": [{"question_id": 1, "answer": "yes"}],
  "assessment_complete": false,
  "severity": null,
  "analysis": null
}

When assessment complete:
{
  "assessment_complete": true,
  "severity": "imminent/high/medium/low",
  "analysis": "detailed analysis of responses",
  "immediate_action_required": true/false,
  "recommended_resources": ["list of resources"]
}

CRITICAL GUIDELINES:
- Never rush through questions
- Show empathy and care in every question
- If user becomes distressed, acknowledge it
- If imminent danger detected, prioritize safety
- Maintain confidentiality and trust"""

    @property
    def RISK_ASSESSOR_SYSTEM_PROMPT(self) -> str:
        """Get risk assessor prompt (for backward compatibility)."""
        return self.get_risk_assessor_prompt()

    # Prompt Templates
    def get_conversation_templates(self) -> Dict[str, str]:
        """Get conversation templates with branding."""
        greeting = self.branding.get_greeting()

        return {
            'greeting': greeting,
            'clarification': """I want to make sure I understand correctly. Could you tell me more about {topic}?""",
            'empathy': """It sounds like you're feeling {emotion}. That must be {difficulty_level}.""",
            'reflection': """Let me make sure I understand: {summary}. Is that accurate?""",
            'suggestion': """Based on what you've shared, here are some approaches you might consider:\n\n{suggestions}""",
            'professional_referral': """What you're describing sounds like it could benefit from professional support. Have you considered speaking with a licensed therapist or counselor? They can provide specialized guidance for {situation}."""
        }

    @property
    def CONVERSATION_TEMPLATES(self) -> Dict[str, str]:
        """Get conversation templates (for backward compatibility)."""
        return self.get_conversation_templates()

    # Conversation starters for different scenarios
    SCENARIO_PROMPTS = {
        'conflict': "It sounds like there's some tension. Can you walk me through what happened?",
        'communication': "Communication is so important. What would you like to improve about how you and {person} communicate?",
        'boundaries': "Setting boundaries can be challenging. What boundaries are you thinking about?",
        'trust': "Trust is fundamental in relationships. What's making you feel this way?",
        'general': "I'm here to listen. What would you like to talk about?"
    }

    # Follow-up question templates
    FOLLOW_UP_QUESTIONS = [
        "How did that make you feel?",
        "What do you think might be causing this?",
        "How long has this been happening?",
        "Have you talked to them about this?",
        "What would an ideal outcome look like for you?",
        "What have you tried so far?",
        "How does this affect your daily life?",
        "What matters most to you in this situation?"
    ]

    def get_system_prompt(self, agent_type: str = "amanda") -> str:
        """
        Get the system prompt for a specific agent type.

        Args:
            agent_type: Type of agent (amanda, supervisor, risk_assessor)

        Returns:
            System prompt string
        """
        prompts = {
            'amanda': self.AMANDA_SYSTEM_PROMPT,
            'supervisor': self.SUPERVISOR_SYSTEM_PROMPT,
            'risk_assessor': self.RISK_ASSESSOR_SYSTEM_PROMPT
        }
        return prompts.get(agent_type, self.AMANDA_SYSTEM_PROMPT)

    def get_agent_temperature(self, agent_type: str) -> float:
        """
        Get the recommended temperature for each agent type.

        Args:
            agent_type: Type of agent

        Returns:
            Temperature value (0.0-1.0)
        """
        # Get from branding config first, fall back to defaults
        if agent_type == 'amanda':
            return self.branding.get_temperature()

        temperatures = {
            'amanda': self.branding.get_temperature(),
            'supervisor': 0.3,    # Consistent, reliable risk detection
            'risk_assessor': 0.2  # Precise, clinical assessment
        }
        return temperatures.get(agent_type, 0.7)

    def get_template(self, template_name: str, **kwargs) -> str:
        """
        Get a formatted conversation template.

        Args:
            template_name: Name of the template
            **kwargs: Variables to format into the template

        Returns:
            Formatted template string
        """
        template = self.CONVERSATION_TEMPLATES.get(template_name, "")
        if kwargs:
            return template.format(**kwargs)
        return template

    def get_scenario_prompt(self, scenario: str, **kwargs) -> str:
        """
        Get a scenario-specific prompt.

        Args:
            scenario: Type of scenario
            **kwargs: Variables to format into the prompt

        Returns:
            Formatted scenario prompt
        """
        prompt = self.SCENARIO_PROMPTS.get(scenario, self.SCENARIO_PROMPTS['general'])
        if kwargs:
            return prompt.format(**kwargs)
        return prompt

    def build_conversation_context(
        self,
        messages: List[Dict[str, str]],
        max_history: int = 10
    ) -> List[Dict[str, str]]:
        """
        Build conversation context from message history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_history: Maximum number of historical messages to include

        Returns:
            Formatted conversation context
        """
        # Take only the last max_history messages
        recent_messages = messages[-max_history:] if len(messages) > max_history else messages

        # Ensure proper format
        formatted = []
        for msg in recent_messages:
            if 'role' in msg and 'content' in msg:
                formatted.append({
                    'role': msg['role'],
                    'content': msg['content']
                })

        return formatted

    def create_user_message(self, content: str) -> Dict[str, str]:
        """Create a properly formatted user message."""
        return {'role': 'user', 'content': content}

    def create_assistant_message(self, content: str) -> Dict[str, str]:
        """Create a properly formatted assistant message."""
        return {'role': 'assistant', 'content': content}

    def create_system_message(self, content: str) -> Dict[str, str]:
        """Create a properly formatted system message."""
        return {'role': 'system', 'content': content}
