# Personalized Learning Roadmap Generator

A CLI-based system that generates personalized learning roadmaps by combining AI conversation, preference analysis, and adaptive roadmap generation.

## 🎯 Overview

This project orchestrates a complete personalized learning experience:

1. **Role Selection** - User selects their target role (AI/Data Scientist, Full Stack Developer, etc.)
2. **Preset Roadmap Display** - Shows the standard learning path for that role
3. **AI Conversation** - Gemini LLM interviews the user about skills, experience, and goals
4. **Personalization** - Analyzes user profile and adjusts topic priorities, hours, and recommendations
5. **Roadmap Generation** - LLM generates a customized roadmap matching user preferences
6. **Output** - Displays and saves the personalized roadmap

## 📁 Project Structure

```
4-2-26/
├── main.py                      # Main orchestrator (entry point)
├── llm/                         # Conversation engine
│   ├── conversation_engine.py   # Manages user conversation
│   ├── gemini_client.py         # Gemini API wrapper
│   ├── role_guides.py           # Role definitions
│   ├── system_prompt.py         # LLM system prompt
│   └── user_profile.py          # User profile management
├── personalizer/                # Roadmap personalization
│   ├── service.py               # Main personalization service
│   ├── loader.py                # Load semantic roadmaps
│   ├── llm.py                   # LLM interface (mock)
│   ├── transform.py             # Apply personalization
│   ├── prompt.py                # Personalization prompts
│   └── schemas.py               # Data validation
├── roadmap_updater/             # NEW: Roadmap generation
│   ├── updater.py               # Main roadmap updater
│   └── gemini_client.py         # Gemini API client
├── fake frontend/               # Preset roadmaps (text format)
│   ├── ai-ds                    # AI & Data Scientist roadmap
│   ├── fs                       # Full Stack Developer roadmap
│   ├── ml                       # Machine Learning Engineer roadmap
│   ├── gd                       # Game Developer roadmap
│   └── sa                       # Software Architect roadmap
├── conversion/                  # Pipeline for semantic data
├── data/                        # Source roadmap data
└── output/                      # Generated personalized outputs
    ├── {role}_profile.json      # User profile
    ├── {role}_personalized.json # Personalized semantic data
    └── {role}_roadmap.txt       # Final personalized roadmap
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   cd C:\Users\Subbu\Desktop\Projects\4-2-26
   ```

2. **Install dependencies**
   ```bash
   pip install google-generativeai python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 🎮 Usage

Run the main orchestrator:

```bash
python main.py
```

### Interactive Flow

1. **Select Role** - Choose from 5 available roles (1-5)

2. **View Preset Roadmap** - See the standard learning path
   - Press Enter to continue

3. **Conversation** - Answer questions about your background
   - The AI will ask about your skills, experience, and goals
   - Type your answers naturally
   - Type `done` when finished

4. **Personalization** - System analyzes your profile
   - Automatically adjusts priorities and hours

5. **View Personalized Roadmap** - See your custom learning path
   - Tailored to your experience and goals
   - Press Enter to continue

6. **Results Saved** - Check the `output/` folder for:
   - `{role}_profile.json` - Your user profile
   - `{role}_personalized.json` - Personalized data
   - `{role}_roadmap.txt` - Your custom roadmap

## 🔧 Modules

### 1. LLM Module (`llm/`)
- **Purpose**: Conversational AI to extract user information
- **LLM**: Gemini 2.5 Flash
- **Key Files**:
  - `conversation_engine.py` - Orchestrates conversation flow
  - `gemini_client.py` - API wrapper for Gemini
  - `user_profile.py` - Stores and manages user data

### 2. Personalizer Module (`personalizer/`)
- **Purpose**: Analyze user profile and update roadmap semantics
- **Key Files**:
  - `service.py` - Main personalization pipeline
  - `transform.py` - Apply priority/hour adjustments
  - `loader.py` - Load semantic roadmap data

### 3. Roadmap Updater Module (`roadmap_updater/`) ✨ NEW
- **Purpose**: Generate updated roadmap text using LLM
- **LLM**: Gemini 2.5 Flash (same as conversation)
- **Key Files**:
  - `updater.py` - Main roadmap generation logic
  - `gemini_client.py` - Gemini API client
- **Inputs**:
  - Preset roadmap text
  - Personalized semantic data (priorities, hours)
  - User profile (skills, goals, experience)
- **Output**:
  - Updated roadmap in same tree format as preset

### 4. Main Orchestrator (`main.py`)
- **Purpose**: Coordinate all modules in sequence
- **Flow**: Selection → Display → Conversation → Personalization → Generation → Display

## 📊 Data Flow

```
User Input
    ↓
Role Selection
    ↓
Preset Roadmap (fake frontend/) ─────────┐
    ↓                                     │
LLM Conversation (llm/)                   │
    ↓                                     │
User Profile                              │
    ↓                                     ↓
Personalizer (personalizer/)         Roadmap Updater
    ↓                                (roadmap_updater/)
Personalized Semantics                    │
    ↓                                     │
    └─────────────────────────────────────┘
                   ↓
          Updated Roadmap Text
                   ↓
            Display + Save
```

## 🧪 Testing

Test individual modules:

```bash
# Test LLM conversation
cd llm
python test_gemini.py

# Test personalizer
cd personalizer
python test_run.py

# Test end-to-end
python main.py
```

## 📝 Configuration

### Available Roles

- `ai_data_scientist` - AI & Data Scientist
- `full_stack` - Full Stack Developer
- `machine_learning` - Machine Learning Engineer
- `game_developer` - Game Developer
- `software_architect` - Software Architect

### Customization

- **Add new roles**: 
  1. Add roadmap text to `fake frontend/`
  2. Update `ROLE_GUIDES` in `llm/role_guides.py`
  3. Add mapping in `main.py` `PRESET_ROADMAPS`

- **Adjust conversation length**: 
  - Modify `max_turns` in `main.py` `run_conversation()`

- **Change LLM model**:
  - Update `model="gemini-2.5-flash"` in Gemini client files

## 🔐 Environment Variables

Required in `.env`:
- `GEMINI_API_KEY` - Your Google Gemini API key

## 📦 Dependencies

- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management

## 🤝 Contributing

The project follows a modular architecture:
- Each module is independent and testable
- Use the same LLM client pattern for consistency
- Follow the orchestration pattern in `main.py`

## 📄 License

MIT License

## 🎉 Features

✅ Interactive CLI interface  
✅ AI-powered conversation  
✅ Personalized learning priorities  
✅ Adaptive roadmap generation  
✅ Multiple role support  
✅ Persistent result storage  
✅ Modular architecture  

## 🐛 Troubleshooting

**ModuleNotFoundError**:
- Ensure you're running from project root
- Check Python path includes all module folders

**API Key Error**:
- Verify `.env` file exists with `GEMINI_API_KEY`
- Check API key is valid and active

**Conversation doesn't start**:
- Type `done` to skip if needed
- Press Ctrl+C to interrupt gracefully

## 📞 Support

For issues or questions, check:
1. Terminal output for error messages
2. Generated `output/` folder for results
3. Module test scripts for debugging
