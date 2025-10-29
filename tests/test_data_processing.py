import pandas as pd
from data_processing import process_data, create_plot

# Skapa exempeldata för test
sample_stock = pd.DataFrame({
    "Date": ["2025-10-27", "2025-10-26"],
    "Close": [150.0, 145.0]
})
sample_currency = pd.DataFrame({
    "Currency": ["SEK", "EUR"],
    "Rate": [10.0, 0.9]
})

def test_process_data():
    df = process_data(sample_stock, sample_currency)
    # Kontrollera att Close_SEK finns
    assert "Close_SEK" in df.columns
    # Kontrollera att procentuell förändring finns
    assert "Förändring_%" in df.columns

def test_create_plot():
    df = process_data(sample_stock, sample_currency)
    plot_html = create_plot(df)
    # Kontrollera att HTML returneras
    assert "<div" in plot_html
