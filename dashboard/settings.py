SELECTED_COUNTRY: str = "US"
COMPANY_NEWS_DATE_FORMAT: str = "%Y-%m-%d"

# ----- Database ------
# Database relative location
DATABASE_PATH: str = "dashboard/database/dashboard_database.db"


# Application Paths
INIT_PAGE_PATH: str = "/"
MAIN_PAGE_PATH: str = "/dashboard_main"
URL_ANIMATION: str = "https://assets9.lottiefiles.com/packages/lf20_YXD37q.json"

# Settings for stocks data feed
TIME_INTERVAL: int = 1  # Days
DATA_FEED_WINDOW: int = 1  # Days
TIME_INTEGRAL_OF_IN_INIT_PAGE: int = 1000  # Milliseconds
N_INTEGRALS_IN_INIT_PAGE: int = 2
TIME_INTEGRAL_OF_GRAPH_REFRESH_RATE: int = 1000  # Milliseconds
GRAPH_REFRESH_RATE: int = 5
