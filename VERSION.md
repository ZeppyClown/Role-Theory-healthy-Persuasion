# Multi-Agent System Versions

## 🎯 Current Version: 2.0 (Recommended)

**Location**: Root directory (`agent.py`)

### ✨ Features:

- **Modular Architecture**: Clean, organized code structure
- **Real-time Streaming**: Character-by-character typing effect
- **Separate Agent Files**: Each agent has its own file
- **Utility Modules**: Reusable components for streaming, research, and conversation
- **Enhanced Commands**: Streaming controls and better user experience

### 🚀 Quick Start:

```bash
python agent.py
```

### 📁 Structure:

```
AI Agent/
├── agent.py              # Main application (current version)
├── demo.py               # Streaming demo
├── agents/               # Individual agent implementations
│   ├── momo.py
│   ├── miles.py
│   └── lila.py
├── utils/                # Utility modules
│   ├── streaming.py
│   ├── research.py
│   └── conversation.py
└── versions/             # Previous versions
    └── v1.0/
```

---

## 📚 Previous Versions

### Version 1.0 (Legacy)

**Location**: `versions/v1.0/`

- **Monolithic Structure**: All code in single file (1,153 lines)
- **No Streaming**: Wait for complete responses
- **Basic Features**: Core functionality without modern enhancements

**Files**:

- `agent.py` - Original implementation
- `demo_persuader.py` - User-as-persuader demo
- `demo_research_features.py` - Research features demo
- `test_agents.py` - Agent testing

---

## 🔄 Migration Guide

### From Version 1.0 to 2.0:

1. **New Commands**:

   - `streaming` - View streaming settings
   - `streaming on/off` - Enable/disable streaming
   - `delay [seconds]` - Set typing speed
   - `help` - Show all commands

2. **Same Commands**:

   - `status` - View agent progress
   - `save` - Save agent states
   - `reset` - Reset all states
   - `research` - View research data

3. **File Changes**:
   - Agent states are compatible between versions
   - Research data format is the same
   - Configuration files work with both versions

---

## 💡 Recommendations

- **Use Version 2.0** for new projects and development
- **Version 1.0** is maintained for reference and compatibility
- **Migrate existing projects** to Version 2.0 for better experience

---

## 🆕 What's New in 2.0

### Code Organization

- ✅ Modular architecture
- ✅ Separate agent files
- ✅ Utility modules
- ✅ Clean imports

### User Experience

- ✅ Real-time streaming
- ✅ Configurable typing speed
- ✅ Better command system
- ✅ Enhanced feedback

### Maintainability

- ✅ Easy to modify agents
- ✅ Reusable components
- ✅ Better debugging
- ✅ Extensible structure
