import pandas as pd
import model.investor_views as views
from model.model import Model


def get_nrcapital_forecast(filepath, min_long_return=0.15, max_short_return=0.0):
    """
    :description: Get equity ETF data and filter ETFs by expected return

    :param filepath: Filepath to nrcapital forecasts
    :type filepath: str, required
    :param min_long_return: Minimum required long return, default is 0.15
    :type min_long_return: float, optional
    :param max_short_return: Maximum tolerable short return, default is 0.0
    :type max_short_return: float, optional
    :return: Selected equity ETFs
    :rtype: pd.DataFrame
    """
    equity_etf_csv = pd.read_csv(r'{}'.format(filepath))

    df = equity_etf_csv[
        (equity_etf_csv['FWD_RETURN_FORECAST'] >= min_long_return) |
        (equity_etf_csv['FWD_RETURN_FORECAST'] <= max_short_return)
        ]

    return df


def strategy(etf_path):
    """
    :description: Strategy
    """
    etf_path = 'https://raw.githubusercontent.com/nathanramoscfa/nrcapital/main/data/etf_cape_return_forecast.csv'
    selected_equity_etfs = get_nrcapital_forecast(etf_path)
    symbols = list(selected_equity_etfs.TICKER)

    model = Model(
        symbols,
        num_years=100,  # years
        bounds=(-0.3, 1.0),  # percent
        gamma=0.0,  # decimal
        min_weight=0.05,  # percent
        margin_rate=0.132,  # percent
        long_weight=1.3,  # percent
        short_weight=0.3,  # percent, must be positive
        frequency=252,  # periods per year
        period='max',  # '1d', '5d', '7d', '60d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
        api_source='bloomberg',  # yahoo or bloomberg
    )

    historical_prices = model.get_historical_prices()
    risk_free_rate = model.get_risk_free_rate(prints=True)
    market_caps = model.get_market_caps(prints=True)

    vif_symbols = model.vif_filter(historical_prices, market_caps, threshold=50, prints=True)
    investor_views, confidences = views.investor_views_confidences(selected_equity_etfs, vif_symbols, prints=True)

    market_symbol, market_name, market_prices = model.get_market_prices(historical_prices, symbols, prints=True)
    market_implied_risk_aversion = model.market_implied_risk_aversion(market_prices, risk_free_rate, prints=True)
    covariance_matrix = model.calculate_covariance_matrix(historical_prices, symbols, prints=False)
    posterior_covariance_matrix, posterior_expected_returns = model.calculate_black_litterman(
        covariance_matrix,
        market_prices,
        risk_free_rate,
        market_caps,
        symbols,
        investor_views,
        confidences,
        prints=True
    )
    max_sharpe_weights, max_sharpe_results = model.maximum_sharpe_portfolio(
        posterior_expected_returns, posterior_covariance_matrix, risk_free_rate, prints=True
    )

    return max_sharpe_weights
