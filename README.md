## Plataforma para análise de dados da produção acadêmica do PPgECC

Platform for vi and analyzing academic production data developed by Programa de Pós-graduação em Engenharia Elétrica (PPgECC).

## Set up the workspace

[Clone](https://github.com/rafagarcia2/dashboard_ppgecc/forking/#clone) the project, configure the remotes and install the dependencies:

```bash
# Clone the repo into the current directory
git clone https://github.com/rafagarcia2/dashboard_ppgecc

# Navigate to the newly cloned directory
cd dashboard_ppgecc

# Create local settings
cp .env-example .env

# Set up the virtual environment
python -m venv venv

# Activate the virtual environment (Unix)
source venv/bin/activate

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Install the dependencies
pip install -U -r requirements.txt
poetry install

# Set up pre-commit hooks
pre-commit install
```

## Running

#### Debugging

To run the project for debugging, Streamlit can be used by adding settings in `.vscode/launch.json` file:

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "${file}"],
            "justMyCode": true
        }
    ]
}
```

After that, just start the application on your VS Code and it should start a local server.
