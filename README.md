<h3 align="center">Dashboard</h3>

  <p align="center">
    A demo dashboard application from backend to frontend.
  </p>
</div>


## About The Project

This project is a demo showcase scenario for implementing with best practice a dashboard / small - application,  from backend to frontend. The methods and skills used in this project are:

- Python best practices.
- Data Warehousing & SQL queries.
- Data Architecture.
- Data analysis dashboard with Dash.
- Application with PyQt5.
- Project architecture.
- Automate unit tests with pipeline workflow.
- Implement makefile for common commands, linting and testing.

Under no circumnstances this code is responsible for a fair prediction of stocks. This is purely a
demo project. There has been no serious research for the scientific needs of this project.

### Built with

* [python](https://www.python.org/)
<img align="left" alt="Python" width="26px" src="https://raw.githubusercontent.com/jmnote/z-icons/master/16x16/python.png" />


* [SQL (sqlite3)](https://sqlite.org)
<img align="left" alt="SQL" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/sql/sql.png" />


## Installation

Make sure you have installed python 3.10 and git in your local machine.


Clone repository from github with:

```terminal
git clone https://github.com/Kantarelis/dashboard.git
```

Create a virtual environment with inside the downloaded project folder named 'dashboard' and inside the 
virtual environment install requirements with:


```terminal
pip install -U -r requirements.txt
```

## Setup

This project has wrapped finnhub algorithms. Hence in order to work correctly, it needs an account in 
finnhub, as well as to administrate finnhub credentials on running environment. An easy way to do this is to create a file in your project environment named as ".env" and inside it define the API key of your 
finnhub account using the keyword "FINNHUB_API_KEY".

E.g.:
FINNHUB_API_KEY="****************************************"

## Example

In order to run the `simple_example.py` located in the `examples` directory of the project, one must first install licel-file-reader package in the same virtual environment. Hence, run in virtual environment the following before running the example:

```terminal
pip install -e .
```

## License
GNU General Public License. See LICENSE file.


<p align="right">(<a href="#top">back to top</a>)</p>

