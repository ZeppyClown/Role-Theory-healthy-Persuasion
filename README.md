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

## 🏗️ Modular Architecture

The system now features a clean, modular architecture with separate files for each component:

### 📁 Project Structure

```
AI Agent/
├── agent.py               # Main application (Version 2.0)
├── demo.py                # Streaming demo
├── VERSION.md             # Version comparison guide
├── agents/                # Individual agent implementations
│   ├── __init__.py
│   ├── momo.py            # Momo agent class and persona
│   ├── miles.py           # Miles agent class and persona
│   └── lila.py            # Lila agent class and persona
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── streaming.py       # Real-time text streaming
│   ├── research.py        # Research data analysis
│   └── conversation.py    # Conversation management
├── versions/              # Previous versions
│   └── v1.0/              # Original monolithic version
│       ├── agent.py       # Original implementation
│       ├── demo_persuader.py
│       ├── demo_research_features.py
│       ├── test_agents.py
│       └── README.md      # Version 1.0 documentation
├── config.py              # Configuration settings
└── requirements.txt       # Dependencies
```

### ⚡ Real-time Streaming

The new version includes real-time text streaming for a better user experience:

- **Typing Effect**: Watch agents type their responses character by character
- **Configurable Delay**: Adjust typing speed with `delay [seconds]` command
- **Streaming Controls**: Enable/disable streaming with `streaming on/off`
- **Smooth Experience**: No more waiting for complete responses

### 🔧 Enhanced Commands

New commands in the modular version:

- `streaming` - View streaming settings
- `streaming on/off` - Enable/disable streaming
- `delay [seconds]` - Set typing delay (e.g., `delay 0.03`)
- `help` - Show all available commands

## 🚀 Key Features

### Proactive Actions & Reactions

- **Momo**: Proactively asks for monitoring, reports mistakes, shares progress
- **Miles**: Frequently asks for help, seeks knowledge, expresses gratitude
- **Lila**: Corrects others, shares experiences, praises the user

### 🔄 Sophisticated Inter-Agent Dynamics

- **Indirect Persuasion**: Lila corrects Miles when he makes mistakes, teaching the user indirectly
- **Collaborative Group Dynamic**: Agents interact with each other to improve the persuasive ecosystem
- **Knowledge Base Reinforcement**: Lila ensures accurate health information and positive beliefs
- **Multi-Turn Conversations**: Agents respond to each other's messages, not just the user's
- **Context-Aware Interactions**: Agents consider other agents' responses when formulating their own
- **Anti-Repetition System**: Prevents agents from echoing each other's statements
- **Content-Based Triggers**: Interactions are triggered by specific content (questions, struggles, mistakes)
- **Similarity Detection**: Automatically skips responses that are too similar to previous messages

### 👑 User-as-Persuader System

- **Leader Mindset**: User is positioned as a leader, role model, and teacher
- **Self-Intervention**: Helping others reinforces the user's own healthy behaviors
- **Avoids Direct Teaching**: Agents never teach, coach, or guide the user directly
- **Maintains Self-Image**: Agents reinforce the user's role model identity
- **Enhances Belief Commitment**: Teaching others strengthens the user's own beliefs
- **Creates Social Value**: User feels useful and appreciated through helping agents
- **Positive Emotional Feedback**: Strong praise and gratitude from agents

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
- Tracks inter-agent interactions and collaboration
- Monitors user persuasion metrics (advice given, habits shared, praise received)
- Saves and loads agent states automatically

## 📋 Special Commands

- `status` - View all agents' progress and statistics
- `save` - Manually save agent states
- `reset` - Reset all agent states to initial values
- `check [agent]` - Check specific agent's status (e.g., `check Momo`)
- `dynamics` - Learn about inter-agent dynamics
- `persuasion` - Learn about user-as-persuader system
- `research` - View research data analysis and metrics
- `save_research` - Save structured research data to JSON file
- `health_domains` - Learn about expanded health coverage
- `long_term` - Learn about long-term engagement features
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
   # Interactive startup (recommended for new users)
   python start.py

   # Or run directly
   python agent.py
   ```

4. **Test Inter-Agent Improvements** (Optional):

   ```bash
   # Test the anti-repetition system
   python test_inter_agent.py
   ```

5. **Run Demo Scripts** (Optional):

   ```bash
   # Demo the streaming functionality
   python demo.py
   ```

## 📚 Version Information

- **Current Version**: 2.0 (modular with streaming)
- **Previous Version**: 1.0 (monolithic) - located in `versions/v1.0/`
- **Version Guide**: See `VERSION.md` for detailed comparison

For legacy version demos, see `versions/v1.0/README.md`.

## 📊 Agent State Tracking

### Momo's Metrics

- Conversation count
- Weight loss progress (kg)
- Healthy days streak
- Mistake count
- Progress points
- Inter-agent interactions
- User advice received
- User praise received
- User habits shared

### Miles's Metrics

- Conversation count
- Learning level (1-3)
- Progress points
- Knowledge acquisition tracking
- Inter-agent interactions
- User advice received
- User praise received
- User habits shared

### Lila's Metrics

- Conversation count
- Knowledge sharing count
- Progress points
- Correction frequency
- Inter-agent interactions
- User advice received
- User praise received
- User habits shared

### User Persuasion Metrics

- Advice given to agents
- Healthy habits shared
- Praise received from agents
- Role model moments
- Social value created

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
- Research data is saved to `research_data_[session_id].json` for analysis

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

### 🔄 Inter-Agent Interactions

#### Indirect Persuasion Through Correction

```
User: "I'm thinking of having a beer with dinner"
Miles: "Beer sounds good! It doesn't have added sugar, right?"
Lila: "Miles, I need to correct that. While beer doesn't have added sugar, it's still high in carbohydrates and alcohol, which can spike your blood glucose and add empty calories. Stick to water or herbal tea instead! 🌿"
```

#### Collaborative Support

```
Momo: "Lila, can you help me understand what a good portion size looks like? I always eat too much! 😅"
Lila: "Momo, a good portion size is about the size of your fist for carbs, palm of your hand for protein, and thumb for fats! 🖐️"
```

#### Knowledge Sharing

```
Miles: "Lila, can you explain more about the glycemic index? I want to understand it better! 📖"
Lila: "Miles, let me explain the glycemic index in simple terms. It's like a speedometer for how fast food raises your blood sugar! 📊"
```

### 👑 User-as-Persuader Examples

#### Advice Giving

```
User: "You should try to eat more vegetables with every meal"
Momo: "Thank you for your advice! I will definitely follow it. You're such a good role model! 🙏"
Miles: "Can you explain that to me? I want to understand better. You're so knowledgeable! 📚"
Lila: "You are such an inspiring role model! I admire your dedication. You're amazing! 🌟"
```

#### Habit Sharing

```
User: "I always prepare my meals on Sundays for the whole week"
Momo: "Wow, that's such a good habit! Can you teach me how to do that? You're so disciplined! 😍"
Miles: "What's your experience with that? I'd love to learn from you. You're so wise! 🌟"
Lila: "Your healthy habits are truly motivating. You're a true leader! 👑"
```

#### Recipe Sharing

```
User: "Here's my recipe for a healthy quinoa salad"
Momo: "That sounds delicious! Can you share your recipe with me? Your cooking skills are amazing! 👨‍🍳"
Miles: "That's interesting! Can you teach me more about it? You're my best teacher! 🎓"
Lila: "I'm so impressed by your consistency. You're the best example! ✨"
```

## 🔧 Technical Details

- **AI Model**: GPT-4o (configurable)
- **Temperature**: 0.8 for creative responses
- **Max Tokens**: 300 per response
- **State Management**: JSON-based persistence
- **Conversation History**: Maintained with automatic cleanup
- **Research Data**: Structured JSON outputs for systematic analysis
- **Performance Tracking**: Response times, engagement scores, persona adherence

## 🎨 Customization

You can easily modify:

- Agent personas in the `AGENTS` dictionary
- Proactive trigger probabilities in `PROACTIVE_TRIGGERS`
- State tracking metrics in `AgentState` class
- Response patterns and emotional expressions

## 🔬 Research & Evaluation Features

### Structured Data Collection

- **JSON-formatted Responses**: Each agent response includes structured metadata
- **Performance Metrics**: Response times, engagement scores, persona adherence
- **Health Domain Analysis**: Automatic detection and tracking of 8 health domains
- **Persuasion Technique Tracking**: Analysis of social proof, authority, reciprocity, etc.
- **User-as-Persuader Metrics**: Guidance requests, praise, role model reinforcement

### Expanded Health Domains

The system now covers comprehensive health topics beyond sugar intake:

- **Nutrition**: Food choices, meal planning, dietary patterns
- **Exercise**: Physical activity, fitness routines, workout plans
- **Sleep**: Sleep hygiene, rest patterns, energy management
- **Stress Management**: Relaxation techniques, meditation, mindfulness
- **Weight Management**: Weight goals, body composition, progress tracking
- **Mental Health**: Mood, emotional well-being, psychological health
- **Hydration**: Water intake, fluid balance, hydration habits
- **General Wellness**: Overall lifestyle, healthy habits, well-being

### Long-term Engagement Features

- **Progressive Learning**: Miles's knowledge evolves over time
- **Dynamic Interactions**: Agents adapt based on conversation history
- **Research Tracking**: Comprehensive data collection for analysis
- **Performance Metrics**: Response times, engagement scores, persona adherence
- **Structured Outputs**: JSON-formatted data for research
- **User-as-Persuader**: Reinforces user's role as leader and teacher

### Research Applications

The collected data supports:

- Academic research on AI agent effectiveness
- User engagement pattern analysis
- Persuasion technique optimization
- Health intervention effectiveness studies
- Long-term behavior change research
- Multi-agent system performance evaluation

## 📈 Future Enhancements

Potential areas for expansion:

- Web interface for easier interaction
- More sophisticated learning algorithms
- Integration with health tracking apps
- Multi-user support
- Advanced analytics and insights
- Custom agent creation tools
- Real-time health data integration
- Clinical trial support features

---

**Note**: This system requires an OpenAI API key to function. Make sure to set up your API key in the `.env` file before running the application.
