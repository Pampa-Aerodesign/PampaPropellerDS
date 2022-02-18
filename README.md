<img src="logo.png?raw=true" width="200" height="200" />

# PampaPropellerDS

Over the years, it has been difficult to use the data provided by our propeller manufacturer Advanced Precision Composite (APC), as it is made available in a .dat format with littler standardization. To solve this problem, Pampa Aerodesign developed a crawler to download the performance data from all APC propellers and transform it to CSVs. Currently the data-set has performance data for 525 propellers for RPMs between 1000-20000. This collection was called Pampa Propeller Data-Set or PPDS.

Here you can find its associated Python library, where we hope to add a Streamlit web app to facilitate the analisis of any given propeller. We also hope to add date by more manufacturers in the future. Documentation and tests are in development.

## Local installation
To run this code locally you must clone the repository and install the lib to do so copy and paste the following commands onto your terminal:

```bash
git clone https://github.com/Pampa-Aerodesign/PampaPropellerDS.git
```

```bash
cd PampaPropellerDS
```


```bash
pip install .
```

## Roadmap
~~v0.1 - Download APC data and store files in the repo~~

~~v0.2 - Create a parser to turn APC raw data into CSVs~~

~~v0.3 - Convert all APC raw data into CSVs and store them in the repo~~

v0.4 - Show data from the APC files in the Streamlit App; build documentation and unit tests for all functions.
