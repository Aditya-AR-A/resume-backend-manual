import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.schemas import AppConfig, Settings, DatabaseConfig, CacheConfig, AIConfig, LLMConfig, LLMProvider


class AppSettings(BaseSettings):
    """
    Application settings with structured configuration
    """

    # Application Configuration
    app_name: str = "Portfolio Fast API Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    reload: bool = True
    port: int = 8000

    # Security
    secret_key: str  # required, loaded from .env/.env.local

    # Database Config
    db_url: Optional[str] = None
    db_pool_size: int = 10
    db_timeout: float = 0.5

    # Cache Configuration
    cache_enabled: bool = True
    cache_backend: str = "redis"   # redis | memcached | memory | file | none
    cache_url: Optional[str] = None
    cache_ttl: int = 300           # default 5 minutes

    # Data Directory
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = Path(os.getenv("DATA_DIR", base_dir / "data"))

    # CORS
    cors_origins: list[str] = ["*"]

    # Logging Configuration
    log_dir: Path = Path(__file__).parent.parent / "logs"
    log_level: str = "DEBUG"   # could be "INFO" / "WARNING" / "ERROR"
    log_complete_file: str = "complete.log"
    log_session_prefix: str = "session"

    # Config for env files 
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


    def print_settings_summary(self):
        print("Application Settings Summary:")
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")


    def get_app_config(self) -> AppConfig:
        """Get application configuration"""
        return AppConfig(
            name=self.app_name,
            version=self.app_version,
            debug=self.debug,
            host=self.host,
            port=self.port
        )


    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration"""
        return DatabaseConfig(
            url=self.database_url
        )


    def get_cache_config(self) -> CacheConfig:
        """Get cache configuration"""
        return CacheConfig(
            enabled=self.cache_enabled,
            ttl=self.cache_ttl,
            max_size=self.cache_max_size
        )


    def get_ai_config(self) -> AIConfig:
        """Get AI configuration with provider settings"""
        providers = {}

        # Configure Groq provider
        if self.groq_api_key:
            providers[LLMProvider.GROQ] = LLMConfig(
                provider=LLMProvider.GROQ,
                api_key=self.groq_api_key,
                model=self.groq_model,
                temperature=self.groq_temperature,
                max_tokens=self.groq_max_tokens
            )

        # Configure OpenAI provider
        if self.openai_api_key:
            providers[LLMProvider.OPENAI] = LLMConfig(
                provider=LLMProvider.OPENAI,
                api_key=self.openai_api_key,
                model=self.openai_model,
                temperature=self.openai_temperature,
                max_tokens=self.openai_max_tokens
            )

        # Configure Anthropic provider
        if self.anthropic_api_key:
            providers[LLMProvider.ANTHROPIC] = LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                api_key=self.anthropic_api_key,
                model=self.anthropic_model,
                temperature=self.anthropic_temperature,
                max_tokens=self.anthropic_max_tokens
            )

        return AIConfig(
            primary_provider=self.primary_llm_provider,
            providers=providers,
            enable_caching=self.ai_cache_enabled,
            cache_ttl=self.ai_cache_ttl,
            max_retries=self.ai_max_retries,
            timeout=self.ai_timeout
        )

    def get_structured_settings(self) -> Settings:
        """Get structured settings object"""
        return Settings(
            app=self.get_app_config(),
            database=self.get_database_config(),
            cache=self.get_cache_config(),
            ai=self.get_ai_config()
        )




# Create global settings instance
app_settings = AppSettings()

# Create structured settings for use throughout the app
settings = app_settings.get_structured_settings()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_settings() -> bool:
    """Validate that all required settings are properly configured"""
    errors = []

    # Check if at least one LLM provider is configured
    if not any([
        app_settings.groq_api_key,
        app_settings.openai_api_key,
        app_settings.anthropic_api_key
    ]):
        errors.append("No LLM provider API keys configured")

    # Check data directory exists
    if not app_settings.data_dir.exists():
        errors.append(f"Data directory does not exist: {app_settings.data_dir}")

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


def print_settings_summary():
    """Print a summary of current settings"""
    print("=== Application Settings Summary ===")
    print(f"App Name: {app_settings.app_name}")
    print(f"Version: {app_settings.app_version}")
    print(f"Debug Mode: {app_settings.debug}")
    print(f"Host: {app_settings.host}:{app_settings.port}")
    print(f"Data Directory: {app_settings.data_dir}")

    print("\n=== AI Configuration ===")
    print(f"Primary Provider: {app_settings.primary_llm_provider.value}")
    print(f"Cache Enabled: {app_settings.ai_cache_enabled}")

    providers = []
    if app_settings.groq_api_key:
        providers.append("Groq")
    if app_settings.openai_api_key:
        providers.append("OpenAI")
    if app_settings.anthropic_api_key:
        providers.append("Anthropic")

    print(f"Available Providers: {', '.join(providers) if providers else 'None'}")
    print("=" * 40)


# Validate settings on import
if not validate_settings():
    print("Warning: Some settings are not properly configured!")
    print_settings_summary()

