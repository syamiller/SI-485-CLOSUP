# SI-485-CLOSUP

Instructions for running code to produce the dashboard locally:

*Ensure that Python is installed on your machine (NOTE: dashboard created in v3.11.8)*

1. Create a new virtual environment for this project (*suggested*) and install the dependencies in `requirements.txt` (*required*).
2. Run all cells in `get_data.ipynb`.
   -  Enter your XBRL username, password, clientID, and Secret when prompted.
   -  This should produce a CSV file named `xbrl_data.csv` when run successfully.
2. Ensure that the `xbrl_functions.py` file is stored in the same folder as `xbrl_data.csv` *AND* `app.py`.
3. Run `app.py`.
   - This will deploy the dashboard locally.
   - The terminal should provide a link to view the dashboard locally. Follow the link (or paste 'http://127.0.0.1:8080/' into your browser) to view the dashboard.