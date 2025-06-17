def generate_framework(story_info):
    """
    Generate a formatted story framework from the story_info dictionary using a table format
    """
    # Title as heading
    framework = f"""# 📖 {story_info['title'] or 'Your Amazing Story'}

| Story Element | Description |
|--------------|-------------|
| 🌍 Setting | {story_info['setting'] or '[Where does your story take place?]'} |
| 👤 Main Character | {story_info['character_main'] or '[Who is your story about?]'} |
| 🎯 Goal | {story_info['goal'] or '[What does your character want to achieve?]'} |
| ⚔️ Conflict | {story_info['conflict'] or '[What\'s stopping them?]'} |
| 👥 Helpers | {story_info['helpers'] or '[Who helps your main character?]'} |
| 👥 Villains | {story_info['villains'] or '[Who causes trouble?]'} |
| 🌟 Climax | {story_info['climax'] or '[What\'s the most exciting part?]'} |
| ✨ Ending | {story_info['ending'] or '[How does it all work out?]'} |
| 🎨 Theme | {story_info['theme'] or '[What\'s the main message of your story?]'} |
"""
    return framework 