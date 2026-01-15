import pytest
from app.services.bedrock_service import BedrockService

def test_bedrock_init():
    service = BedrockService()
    assert service.model_id is not None
    assert service.client is not None

# Mock test for response generation (to avoid actual API calls during tests if needed)
def test_generate_response_mock(mocker):
    service = BedrockService()
    mocker.patch.object(service.client, 'invoke', return_value=type('obj', (object,), {'content': 'Mocked answer'})())
    response = service.generate_response("You are a bot", "Hello")
    assert response == "Mocked answer"
