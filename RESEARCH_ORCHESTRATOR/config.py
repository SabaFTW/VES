
CONFIG = {
    'model': {
        'type': 'ollama',
        'endpoint': 'http://localhost:11434/api/generate',
        'model_name': 'llama3'
    },
    'search': {
        'local_dir': '/home/saba/VES',
        'file_types': ['md', 'txt', 'pdf'],
        'brave_api_key': None,  # Optional
        'drive_enabled': False  # Optional
    },
    'output': {
        'dir': '/home/saba/research_outputs',
        'format': 'markdown'
    }
}
