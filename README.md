# Enhanced Healthy Habits AI Agent System

A sophisticated multi-agent AI system featuring three distinct AI companions - Momo, Miles, and Lila - each with unique personalities, proactive behaviors, and dynamic learning capabilities focused on healthy lifestyle adoption.

## 🤖 Meet Your AI Companions

### Momo - The Cheerful Struggler

- **Personality**: Cheerful, thankful, but weak-willed
- **Proactive Behaviors**:
  - Asks for monitoring and reminders
  - Reports mistakes and asks for inspection
  - Shares progress (weight loss, healthy days)
  - Requests specific reminders to be better
- **Emotional Traits**: Always cheerful, expresses genuine remorse, shows excitement about progress

### Miles - The Curious Learner

- **Personality**: Knowledge-hungry, innocent, grateful
- **Proactive Behaviors**:
  - Asks frequent questions about food choices
  - Seeks specific knowledge about nutrition
  - Expresses gratitude for corrections
  - Celebrates learning moments
- **Learning Progression**: Questions evolve from basic to advanced as knowledge grows

### Lila - The Knowledgeable Motivator

- **Personality**: Knowledgeable, emotionally expressive, takes initiative
- **Proactive Behaviors**:
  - Corrects wrong information from others
  - Shares positive experiences
  - Strongly praises the user
  - Takes initiative when others are quiet
- **Emotional Traits**: Passionate, admiring, concerned for others' health

## 🚀 Key Features

### Proactive Actions & Reactions

- **Momo**: Proactively asks for monitoring, reports mistakes, shares progress
- **Miles**: Frequently asks for help, seeks knowledge, expresses gratitude
- **Lila**: Corrects others, shares experiences, praises the user

### Dynamic Behavior & Progress

- **Learning Progression**: Miles's questions become more sophisticated over time
- **Progress Tracking**: Momo reports tangible progress like weight loss
- **State Persistence**: All agent states are saved and loaded between sessions

### Enhanced Emotional Expression

- Each agent maintains consistent emotional traits
- Responses reflect their unique personalities
- Emotional expressions evolve with their progress

### Agent State Management

- Tracks conversation counts, progress points, learning levels
- Monitors mistakes, weight loss, healthy days
- Saves and loads agent states automatically

## 📋 Special Commands

- `status` - View all agents' progress and statistics
- `save` - Manually save agent states
- `reset` - Reset all agent states to initial values
- `check [agent]` - Check specific agent's status (e.g., `check Momo`)
- `exit` or `quit` - Stop the chat and save states

## 🛠️ Installation & Setup

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python agent.py
   ```

## 📊 Agent State Tracking

### Momo's Metrics

- Conversation count
- Weight loss progress (kg)
- Healthy days streak
- Mistake count
- Progress points

### Miles's Metrics

- Conversation count
- Learning level (1-3)
- Progress points
- Knowledge acquisition tracking

### Lila's Metrics

- Conversation count
- Knowledge sharing count
- Progress points
- Correction frequency

## 🔄 Dynamic Learning System

### Miles's Learning Progression

- **Level 1**: Basic questions (coke vs beer, what's healthy)
- **Level 2**: Intermediate questions (GI of foods, portion sizes)
- **Level 3**: Advanced questions (nutritional timing, meal planning)

### Proactive Trigger System

Each agent has specific probabilities for different proactive behaviors:

- **Momo**: 30% monitoring requests, 20% mistake reports, 25% progress reports
- **Miles**: 40% question asking, 30% knowledge seeking, 20% gratitude expression
- **Lila**: 25% corrections, 30% user praise, 20% experience sharing

## 💾 Data Persistence

- Agent states are automatically saved to `agent_states.json`
- States are loaded when the application starts
- Manual save/load functionality available
- Conversation history is maintained during sessions

## 🎯 Example Interactions

### Momo's Proactive Monitoring Request

```
Momo: "Hi! I'm feeling motivated today! Could you remind me to prepare a healthy breakfast before sleep? I want to start tomorrow strong! Thank you for always supporting me! 💪"
```

### Miles's Learning Question

```
Miles: "I'm confused about fruits again! Which should I take? Durian or apple? I heard durian is high in calories but apple has sugar too. Can you help me understand which is better for my health goals?"
```

### Lila's Correction

```
Lila: "Miles, do not take beer. Though it contains no added sugar, the high carbohydrate will increase your blood glucose. You're doing great asking questions though! Keep learning! 🌟"
```

## 🔧 Technical Details

- **AI Model**: GPT-4o (configurable)
- **Temperature**: 0.8 for creative responses
- **Max Tokens**: 300 per response
- **State Management**: JSON-based persistence
- **Conversation History**: Maintained with automatic cleanup

## 🎨 Customization

You can easily modify:

- Agent personas in the `AGENTS` dictionary
- Proactive trigger probabilities in `PROACTIVE_TRIGGERS`
- State tracking metrics in `AgentState` class
- Response patterns and emotional expressions

## 📈 Future Enhancements

Potential areas for expansion:

- Web interface for easier interaction
- More sophisticated learning algorithms
- Integration with health tracking apps
- Multi-user support
- Advanced analytics and insights
- Custom agent creation tools

---

**Note**: This system requires an OpenAI API key to function. Make sure to set up your API key in the `.env` file before running the application.
