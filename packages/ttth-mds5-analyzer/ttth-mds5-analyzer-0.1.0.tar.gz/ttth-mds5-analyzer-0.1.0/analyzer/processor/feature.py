import warnings

warnings.filterwarnings('ignore')


class FeatureProcessor:

    def __init__(self):
        pass

    @staticmethod
    def handle_missing_values_by_mode(variable_name, df):
        print(f'{variable_name} before fill missing values: {df[variable_name].isna().sum()}')
        mode = df[variable_name].mode()[0]
        missing_index = df[df[variable_name].isna()].index
        df.loc[missing_index, variable_name] = mode
        print(f'{variable_name} after fill missing values: {df[variable_name].isna().sum()}')

    @staticmethod
    def handle_missing_values_by_median(variable_name, df):
        print(f'{variable_name} before fill missing values: {df[variable_name].isna().sum()}')
        median = df[variable_name].median()
        missing_index = df[df[variable_name].isna()].index
        df.loc[missing_index, variable_name] = median
        print(f'{variable_name} after fill missing values: {df[variable_name].isna().sum()}')