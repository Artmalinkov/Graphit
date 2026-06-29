# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


class Config:
    PROJECT_ROOT = Path(__file__).parent.resolve()

    # === SQLite ===
    DB_NAME = os.getenv('DB_NAME', 'graphite_db.db.sqlite')

    # Формируем путь: папка db/ + имя файла
    DB_DIR = PROJECT_ROOT / 'db'
    DB_PATH = os.getenv('DB_PATH', str(DB_DIR / f'{DB_NAME}.sqlite'))

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///{self.DB_PATH}"

    # === Пути к данным ===
    OBSIDIAN_PATH = Path(os.getenv(
        'OBSIDIAN_PATH',
        r'D:/00.Основное/02.Obsidian/My_mind/Obsidian_socnet'
    ))

    DATA_DIR = PROJECT_ROOT / 'data'
    DATA_RAW = DATA_DIR / 'raw'
    DATA_PROCESSED = DATA_DIR / 'processed'
    OUTPUT_DIR = PROJECT_ROOT / 'output'
    LOGS_DIR = PROJECT_ROOT / 'logs'

    # === Настройки ===
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))

    # === Настройки визуализации ===
    GRAPH_WIDTH = int(os.getenv('GRAPH_WIDTH', 1400))
    GRAPH_HEIGHT = int(os.getenv('GRAPH_HEIGHT', 900))

    # === Методы ===
    @classmethod
    def ensure_directories(cls) -> None:
        """Создаёт все необходимые папки"""
        dirs = [
            cls.DATA_RAW,
            cls.DATA_PROCESSED,
            cls.OUTPUT_DIR,
            cls.LOGS_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    @classmethod
    def info(cls) -> str:
        """Информация о конфигурации"""
        return f"""
╔═══════════════════════════════════════════════════════════╗
║                    G R A P H I T E                       ║
╠═══════════════════════════════════════════════════════════╣
║  📁 Проект:        {cls.PROJECT_ROOT}                    
║  📂 Obsidian:      {cls.OBSIDIAN_PATH}                   
║  🗄️  База:         {cls.DB_PATH}                         
║  📤 Выход:         {cls.OUTPUT_DIR}                     
╚═══════════════════════════════════════════════════════════╝
"""


# Создаём экземпляр для удобного импорта
config = Config()

# При импорте создаём папки
config.ensure_directories()

# ============================================================
# Тестирование (запустите python config.py для проверки)
# ============================================================
if __name__ == '__main__':
    print(config.info())
    print(f"\n📊 DATABASE_URL: {config.DATABASE_URL}")
    print(f"✅ Все директории созданы")