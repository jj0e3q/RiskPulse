"""Basic health test for collector service."""


def test_imports():
    """Test that main modules can be imported."""
    from app.core.config import settings
    from app.kafka.consumer import create_consumer
    from app.kafka.producer import send_data_collected_event

    assert settings.SERVICE_NAME == "collector_service"


def test_config():
    """Test that configuration is loaded."""
    from app.core.config import settings

    assert settings.KAFKA_BOOTSTRAP_SERVERS
    assert settings.DATABASE_URL