"""
Project Constants
"""

# Data paths
RAW_DATA_PATH = 'data/raw/s_train_delays.csv'
PROCESSED_DATA_PATH = 'data/processed/s_train_delays_processed.csv'
ARTIFACTS_PATH = 'data/artifacts/'

# S-train network
S_TRAIN_LINES = ['A', 'B', 'C', 'E', 'F', 'H', 'Bx']

# Delay threshold (minutes)
DELAY_THRESHOLD = 2

# Train-test split
TRAIN_TEST_SPLIT = 0.8
RANDOM_STATE = 42

# Model parameters
MODEL_RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Features
CATEGORICAL_FEATURES = ['line', 'weather', 'day_of_week']
NUMERICAL_FEATURES = ['hour', 'minute', 'temperature', 'passenger_load', 'is_maintenance']
TARGET_FEATURE = 'is_delayed'

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'