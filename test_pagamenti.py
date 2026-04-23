import pytest
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise
from pagamenti import autorizza_transazione, elabora_pagamento 


""" @pytest.mark.parametrize("metodo, saldo_attuale, importo, aspettativa, risultato, mock_value", [
    ("paypal", 1000.0, -100.0, pytest.raises(ValueError, match="L'importo deve essere maggiore di zero."), None, None),
    ("stripe", 1000.0, 100.0, pytest.raises(ValueError, match="Metodo di pagamento non supportato."), None, None),
    ("carta", 500.0, 650.0, pytest.raises(ValueError, match="Fondi insufficienti per completare la transazione."), None, None),
    ("crypto", 500.0, 70.0, pytest.raises(ValueError, match="L'importo minimo per le crypto è 100."), None, None),
    # HAPPY PATH
    ("carta", 1000.0, 50.0, does_not_raise(), "Pagamento completato con successo.", True),
    ("carta", 1000.0, 50.0, does_not_raise(), "Transazione rifiutata dalla banca.", False),
    ("carta", 5000.0, 1200.0, does_not_raise(), "Pagamento completato. Richiesta verifica anti-riciclaggio.", True)
]) """

""" def test_pagamenti(metodo, saldo_attuale, importo, aspettativa, risultato, mock_value):
    with patch("pagamenti.autorizza_transazione", return_value=mock_value) as mock_autorizza:
        with aspettativa: 
            assert elabora_pagamento(metodo, saldo_attuale, importo) == risultato
            mock_autorizza.assert_called_once_with(importo) """

@pytest.mark.parametrize("metodo, saldo_attuale, importo, aspettativa, risultato", [
    ("paypal", 1000.0, -100.0, pytest.raises(ValueError, match="L'importo deve essere maggiore di zero."), None),
    ("stripe", 1000.0, 100.0, pytest.raises(ValueError, match="Metodo di pagamento non supportato."), None),
    ("carta", 500.0, 650.0, pytest.raises(ValueError, match="Fondi insufficienti per completare la transazione."), None),
    ("crypto", 500.0, 70.0, pytest.raises(ValueError, match="L'importo minimo per le crypto è 100."), None),
    # HAPPY PATH
    ("carta", 1000.0, 50.0, patch("pagamenti.autorizza_transazione", return_value=True), "Pagamento completato con successo."),
    ("carta", 1000.0, 50.0, patch("pagamenti.autorizza_transazione", return_value=False), "Transazione rifiutata dalla banca."),
    ("carta", 5000.0, 1200.0, patch("pagamenti.autorizza_transazione", return_value=True), "Pagamento completato. Richiesta verifica anti-riciclaggio."),
    
])

def test_spedizioni(metodo, saldo_attuale, importo, aspettativa, risultato):
    with aspettativa as mock_autorizza:
        assert elabora_pagamento(metodo, saldo_attuale, importo) == risultato
        mock_autorizza.assert_called_once_with(importo)

@pytest.mark.parametrize("importo, aspettativa, risultato", [
    (100.0, patch("pagamenti.random.choice", return_value=True), True),
    (100.0, patch("pagamenti.random.choice", return_value=False), False)
])

def test_autorizza_transazione(importo, aspettativa, risultato):
    with aspettativa as mock_choice:
        assert autorizza_transazione(importo) == risultato
        mock_choice.assert_called_once_with([True, False])