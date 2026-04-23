# MAI IMPORTARE I MODULI O LE FUNZIONI CHE VOGLIAMO TESTARE (-- BLACK-BOX --)
import pytest
import subprocess

def generatore(argomenti: list[str]):
    comando_base = ["python", "generatore.py"]
    comando_completo = comando_base + argomenti

    risultato = subprocess.run(comando_completo, capture_output=True, text=True)
    return risultato

def test_nessun_parametro_ritorna_exit_code_1():
    risultato = generatore([])

    assert risultato.returncode == 1, f"Exit error code: {risultato.returncode}"
    
    assert "Devi fornire un nome utente" in risultato.stderr
    assert risultato.stdout == ""

def test_nessun_parametro_ritorna_exit_code_2():
    risultato = generatore(["admin"])

    assert risultato.returncode == 2
    
    assert "riservati" in risultato.stderr
    assert risultato.stdout == ""

def test_nessun_parametro_ritorna_exit_code_0():
    risultato = generatore(["matteo"])

    assert risultato.returncode == 0
    
    assert "Token di accesso generato" in risultato.stdout
    assert "MATTEO" in risultato.stdout
    assert risultato.stderr == ""
