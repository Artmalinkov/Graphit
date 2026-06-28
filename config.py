# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


class Config:
    """Центральная конфигурация проекта Graphite"""

    # ============================================================
    # PostgreSQL
    # ============================================================
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'graphite_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    @property
    def DATABASE_URL(self) -> str:
        """URL для подключения к PostgreSQL (синхронный)"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """URL для асинхронного подключения (для будущих задач)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # ============================================================
    # Пути
    # ============================================================
    PROJECT_ROOT = Path(__file__).parent.resolve()

    # Путь к хранилищу Obsidian
    OBSIDIAN_PATH = Path(os.getenv(
        'OBSIDIAN_PATH',
        r'D:/00.Основное/02.Obsidian/My_mind/Obsidian_socnet'
    ))

    # Директории проекта
    DATA_DIR = PROJECT_ROOT / 'data'
    DATA_RAW = DATA_DIR / 'raw'
    DATA_PROCESSED = DATA_DIR / 'processed'
    OUTPUT_DIR = PROJECT_ROOT / 'output'
    LOGS_DIR = PROJECT_ROOT / 'logs'
    DOCS_DIR = PROJECT_ROOT / 'docs'
    SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
    SRC_DIR = PROJECT_ROOT / 'src'

    # ============================================================
    # Настройки приложения
    # ============================================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))

    # ============================================================
    # Настройки визуализации
    # ============================================================
    GRAPH_WIDTH = int(os.getenv('GRAPH_WIDTH', 1400))
    GRAPH_HEIGHT = int(os.getenv('GRAPH_HEIGHT', 900))
    GRAPH_BG_COLOR = os.getenv('GRAPH_BG_COLOR', '#ffffff')
    GRAPH_FONT_COLOR = os.getenv('GRAPH_FONT_COLOR', '#000000')

    # ============================================================
    # Настройки парсинга
    # ============================================================
    MAX_NOTES_LENGTH = int(os.getenv('MAX_NOTES_LENGTH', 1000))
    SKIP_EMPTY_FILES = os.getenv('SKIP_EMPTY_FILES', 'True').lower() == 'true'

    # ============================================================
    # Методы
    # ============================================================
    @classmethod
    def ensure_directories(cls) -> None:
        """Создает все необходимые папки, если их нет"""
        dirs = [
            cls.DATA_RAW,
            cls.DATA_PROCESSED,
            cls.OUTPUT_DIR,
            cls.LOGS_DIR,
            cls.DOCS_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            # Создаем .gitkeep чтобы папки не пропадали в репозитории
            gitkeep = d / '.gitkeep'
            if not gitkeep.exists():
                gitkeep.touch()

    @classmethod
    def info(cls) -> str:
        """Возвращает строку с информацией о конфигурации"""
        return f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                         G R A P H I T E                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║  📁 Проект:        {cls.PROJECT_ROOT}                                
║  📂 Obsidian:      {cls.OBSIDIAN_PATH}                               
║  🗄️  База:         {cls.DB_NAME}@{cls.DB_HOST}:{cls.DB_PORT}         
║  📤 Выход:         {cls.OUTPUT_DIR}                                 
║  📊 LOG_LEVEL:     {cls.LOG_LEVEL}                                  
║  📦 BATCH_SIZE:    {cls.BATCH_SIZE}                                 
╚═══════════════════════════════════════════════════════════════════════╝
"""


# Создаем экземпляр конфигурации для удобного импорта
config = Config()

# При импорте сразу создаем все папки
config.ensure_directories()

# ============================================================
# Тестирование (запустите python config.py для проверки)
# ============================================================
if __name__ == '__main__':
    print(config.info())
    print("\n📊 Детали подключения:")
    print(f"   DATABASE_URL: {config.DATABASE_URL}")
    print(f"   DATABASE_URL_ASYNC: {config.DATABASE_URL_ASYNC}")
    print("\n📁 Директории:")
    print(f"   DATA_RAW: {config.DATA_RAW}")
    print(f"   DATA_PROCESSED: {config.DATA_PROCESSED}")
    print(f"   OUTPUT_DIR: {config.OUTPUT_DIR}")
    print(f"   LOGS_DIR: {config.LOGS_DIR}")
    print("\n🎨 Настройки графа:")
    print(f"   GRAPH_WIDTH: {config.GRAPH_WIDTH}")
    print(f"   GRAPH_HEIGHT: {config.GRAPH_HEIGHT}")
    print("\n✅ Все директории созданы")