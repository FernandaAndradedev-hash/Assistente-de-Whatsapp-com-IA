import os
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake")
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")
os.environ.setdefault("EVOLUTION_API_KEY", "test-key")

from unittest.mock import MagicMock, patch

from memory import _sessions


class TestAgent:

    def setup_method(self):
        _sessions.clear()

    @patch("agent._client")
    @patch("agent.retrieve")
    def test_resposta_normal(self, mock_retrieve, mock_client):
        mock_retrieve.return_value = [
            {"text": "Aceitamos Unimed.", "title": "Convênios", "category": "convenios", "score": 0.90}
        ]
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Aceitamos Unimed e outros planos.")]
        mock_client.messages.create.return_value = mock_response

        from agent import process_message
        result = process_message("5511999999999", "Quais convênios aceitam?")

        assert "Unimed" in result
        assert isinstance(result, str)

    @patch("agent._client")
    @patch("agent.retrieve")
    def test_historico_salvo_apos_resposta(self, mock_retrieve, mock_client):
        mock_retrieve.return_value = []
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Olá! Como posso ajudar?")]
        mock_client.messages.create.return_value = mock_response

        from agent import process_message
        from memory import get_history

        process_message("5511888888888", "Olá")
        history = get_history("5511888888888")

        assert len(history) == 2  # user + assistant
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

    def test_comando_sair_limpa_sessao(self):
        from agent import process_message
        from memory import add_message, get_history

        add_message("5511777777777", "user", "mensagem anterior")
        result = process_message("5511777777777", "sair")

        assert get_history("5511777777777") == []
        assert "prazer" in result.lower() or "vida+" in result.lower()

    def test_pedido_de_humano_retorna_telefone(self):
        from agent import process_message
        result = process_message("5511666666666", "quero falar com um humano")
        assert "3456-7890" in result or "atendente" in result.lower() or "equipe" in result.lower()