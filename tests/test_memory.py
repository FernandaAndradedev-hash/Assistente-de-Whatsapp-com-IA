import time
import pytest
from unittest.mock import patch

from memory import (
    Session,
    _sessions,
    add_message,
    clear_session,
    get_history,
    get_session_count,
)


class TestMemory:

    def setup_method(self):
        """Limpa sessões antes de cada teste."""
        _sessions.clear()

    def test_historico_vazio_para_numero_novo(self):
        assert get_history("5511111111111") == []

    def test_adiciona_e_recupera_mensagem(self):
        add_message("5511222222222", "user", "Quero agendar")
        history = get_history("5511222222222")
        assert len(history) == 1
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Quero agendar"

    def test_historico_mantem_ordem(self):
        add_message("5511333333333", "user", "Primeira")
        add_message("5511333333333", "assistant", "Resposta")
        add_message("5511333333333", "user", "Segunda")
        history = get_history("5511333333333")
        assert history[0]["content"] == "Primeira"
        assert history[1]["content"] == "Resposta"
        assert history[2]["content"] == "Segunda"

    def test_limpa_sessao(self):
        add_message("5511444444444", "user", "teste")
        clear_session("5511444444444")
        assert get_history("5511444444444") == []

    def test_sessao_expirada_retorna_vazio(self):
        add_message("5511555555555", "user", "teste")
        # Simula sessão expirada modificando o last_activity
        _sessions["5511555555555"].last_activity = time.time() - 9999
        assert get_history("5511555555555") == []

    def test_limite_de_mensagens_respeitado(self):
        """Histórico não deve exceder MAX_HISTORY_MESSAGES."""
        import config
        phone = "5511666666666"
        for i in range(config.MAX_HISTORY_MESSAGES + 5):
            add_message(phone, "user", f"msg {i}")
        history = get_history(phone)
        assert len(history) <= config.MAX_HISTORY_MESSAGES

    def test_numeros_diferentes_isolados(self):
        add_message("5511777777777", "user", "msg A")
        add_message("5511888888888", "user", "msg B")
        assert get_history("5511777777777")[0]["content"] == "msg A"
        assert get_history("5511888888888")[0]["content"] == "msg B"