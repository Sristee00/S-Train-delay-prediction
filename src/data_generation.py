"""
S-train Delay Data Generation Module
Generates realistic synthetic Copenhagen S-train delay data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Copenhagen S-train network data
S_TRAIN_LINES = ['A', 'B', 'C', 'E', 'F', 'H', 'Bx']

STATIONS = {
    'A': ['Ballerup', 'Skovlunde', 'Glostrup', 'Herlev', 'Rødovre', 'Vanløse', 
          'Nørrebro', 'Nørreport', 'Rådhuspladsen', 'Hovedbanegården', 'Tåsinge Plads',
          'Dybbølsbro', 'Enghave Plads', 'Vigerslev Allé', 'Isafold', 'Valby',
          'Vanløse Station', 'Åboulevarden'],
    'B': ['Hillerød', 'Helsinge', 'Birkerød', 'Holte', 'Lyngby', 'Skovshoved',
          'Ordrup', 'Charlottenlund', 'Hellerup', 'Klampenborg', 'Nørreport',
          'Hovedbanegården', 'Vesterbro', 'Vigerslev Allé', 'Tåsinge Plads'],
    'C': ['Farum', 'Værløse', 'Vangede', 'Virum', 'Gentofte', 'Charlottenlund',
          'Hellerup', 'Klampenborg', 'Nørreport', 'Hovedbanegården', 'Enghave Plads',
          'Isafold', 'Valby', 'Hundige'],
    'E': ['Køge', 'Taastrup', 'Albertslund', 'Hvidovre', 'Rødovre', 'Brønshøj',
          'Husum', 'Vanløse', 'Nørrebro', 'Nørreport', 'Hovedbanegården',
          'Tåsinge Plads', 'Dybbølsbro', 'Enghave Plads', 'Vigerslev Allé', 'Isafold'],
    'F': ['Køge', 'Borup', 'Holmegaard', 'Gevninge', 'Skovshoved', 'Hellerup',
          'Nørreport', 'Hovedbanegården', 'Tåsinge Plads', 'Isafold', 'Valby'],
    'H': ['Hellerup', 'Klampenborg', 'Nørreport', 'Hovedbanegården', 'Vesterbro',
          'Vigerslev Allé', 'Tåsinge Plads', 'Dybbølsbro', 'Enghave Plads', 'Isafold'],
    'Bx': ['Hillerød', 'Holte', 'Lyngby', 'Skovshoved', 'Nørreport', 'Hovedbanegården',
           'Vesterbro', 'Vigerslev Allé', 'Isafold', 'Valby']
}

WEATHER_CONDITIONS = ['Clear', 'Rainy', 'Snowy', 'Cloudy', 'Foggy', 'Windy']

def generate_weather_data(date: datetime, temperature_base: float = 10) -> dict:
    """Generate realistic weather patterns"""
    # Winter months (Nov-Mar) are colder
    month = date.month
    if month in [11, 12, 1, 2, 3]:
        temp = temperature_base - 8 + np.random.normal(0, 3)
        weather_probs = {
            'Clear': 0.2, 'Rainy': 0.3, 'Snowy': 0.4,
            'Cloudy': 0.08, 'Foggy': 0.01, 'Windy': 0.01
        }
    else:
        temp = temperature_base + np.random.normal(0, 3)
        weather_probs = {
            'Clear': 0.5, 'Rainy': 0.25, 'Snowy': 0.0,
            'Cloudy': 0.15, 'Foggy': 0.05, 'Windy': 0.05
        }
    
    weather = np.random.choice(list(weather_probs.keys()), p=list(weather_probs.values()))
    return {'weather': weather, 'temperature': max(-15, min(35, temp))}

def calculate_delay(hour: int, day_of_week: int, weather: str, 
                   passenger_load: float, is_maintenance: bool) -> int:
    """Calculate realistic delay based on multiple factors"""
    base_delay = 0
    
    # Rush hour delays (7-9 AM, 4-7 PM)
    if (7 <= hour <= 9) or (16 <= hour <= 19):
        base_delay += np.random.normal(5, 2)
    
    # Off-peak (less delays)
    elif (23 <= hour or hour <= 5):
        base_delay += np.random.normal(-1, 1)
    
    # Regular hours
    else:
        base_delay += np.random.normal(1, 1)
    
    # Weekend effect (fewer delays)
    if day_of_week >= 5:  # Saturday, Sunday
        base_delay -= 2
    
    # Weather impact
    weather_impact = {
        'Clear': 0, 'Cloudy': 0.5, 'Rainy': 3,
        'Snowy': 8, 'Foggy': 2, 'Windy': 1.5
    }
    base_delay += np.random.normal(weather_impact[weather], 1)
    
    # Passenger load impact
    base_delay += passenger_load * 3
    
    # Maintenance windows (random maintenance days)
    if is_maintenance:
        base_delay += np.random.normal(15, 5)
    
    # Random incidents (5% chance)
    if np.random.random() < 0.05:
        base_delay += np.random.normal(20, 5)
    
    return max(0, int(base_delay))

def generate_synthetic_data(
    start_date: datetime = datetime(2023, 1, 1),
    end_date: datetime = datetime(2023, 12, 31),
    records_per_day: int = 150
) -> pd.DataFrame:
    """
    Generate synthetic S-train delay data
    
    Parameters:
    -----------
    start_date : datetime
        Start date for data generation
    end_date : datetime
        End date for data generation
    records_per_day : int
        Number of records to generate per day
    
    Returns:
    --------
    pd.DataFrame : Synthetic delay data
    """
    
    logger.info(f"Generating synthetic data from {start_date} to {end_date}")
    
    records = []
    current_date = start_date
    
    while current_date <= end_date:
        day_of_week = current_date.weekday()
        
        # Decide if maintenance day (10% chance on weekdays)
        is_maintenance_day = (np.random.random() < 0.1) and (day_of_week < 5)
        
        for _ in range(records_per_day):
            # Random time of day
            hour = np.random.randint(5, 24)
            minute = np.random.randint(0, 60)
            
            # Random line and station
            line = np.random.choice(S_TRAIN_LINES)
            station = np.random.choice(STATIONS[line])
            
            # Generate weather
            weather_data = generate_weather_data(current_date)
            
            # Passenger load (0-1, higher in rush hours)
            if (7 <= hour <= 9) or (16 <= hour <= 19):
                passenger_load = np.random.beta(7, 2)  # Skewed towards high
            else:
                passenger_load = np.random.beta(2, 5)  # Skewed towards low
            
            # Calculate delay
            delay = calculate_delay(
                hour, day_of_week, weather_data['weather'],
                passenger_load, is_maintenance_day
            )
            
            # Determine if delayed (threshold: 2 minutes)
            is_delayed = 1 if delay >= 2 else 0
            
            record = {
                'datetime': current_date.replace(hour=hour, minute=minute),
                'line': line,
                'station': station,
                'day_of_week': day_of_week,
                'hour': hour,
                'minute': minute,
                'weather': weather_data['weather'],
                'temperature': round(weather_data['temperature'], 1),
                'passenger_load': round(passenger_load, 2),
                'is_maintenance': int(is_maintenance_day),
                'delay_minutes': delay,
                'is_delayed': is_delayed
            }
            records.append(record)
        
        current_date += timedelta(days=1)
    
    df = pd.DataFrame(records)
    logger.info(f"Generated {len(df)} records")
    
    return df

def save_synthetic_data(df: pd.DataFrame, filepath: str) -> None:
    """Save synthetic data to CSV"""
    df.to_csv(filepath, index=False)
    logger.info(f"Data saved to {filepath}")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"\nFirst 5 rows:\n{df.head()}")
    logger.info(f"\nData info:\n{df.info()}")
    logger.info(f"\nDelay statistics:\n{df['delay_minutes'].describe()}")

if __name__ == "__main__":
    # Generate data
    df = generate_synthetic_data(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        records_per_day=150
    )
    
    # Save to file
    save_synthetic_data(df, 'data/raw/s_train_delays.csv')