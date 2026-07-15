# Como executar o FinTrack Insights

## Requisitos

- Python 3.10 ou superior;
- navegador atualizado.

## Dashboard

No terminal, a partir da raiz do projeto:

```bash
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale e execute:

```bash
python -m pip install -r requirements.txt
streamlit run dashboard.py
```

Abra `http://localhost:8501` caso o navegador não seja iniciado automaticamente.

## Protótipo navegável

Abra `prototipo_fintrack.html` diretamente no navegador. Qualquer credencial permite entrar porque o fluxo é apenas uma simulação acadêmica.

## Validação da base e testes

```bash
python scripts/validar_dados.py
python -m pytest -q
```

