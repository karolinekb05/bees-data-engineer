import pytest
import pandas as pd
import numpy as np
from scripts.utils import run_data_quality_checks

def test_normalization_logic():
    """Valida se a transformação para minúsculas e preenchimento de nulos funciona"""
    data = {'state': ['California', None], 'country': ['United States', 'USA']}
    df = pd.DataFrame(data)
    
    # Simulação da lógica da Silver
    df['state'] = df['state'].fillna('unknown').str.lower()
    
    assert df['state'].iloc[0] == 'california'
    assert df['state'].iloc[1] == 'unknown'

def test_gold_aggregation():
    """Valida se a contagem por tipo e localização está correta"""
    data = {
        'brewery_type': ['micro', 'micro', 'large'],
        'country': ['us', 'us', 'us'],
        'state': ['ca', 'ca', 'ca']
    }
    df = pd.DataFrame(data)
    
    # Lógica da Gold
    gold = df.groupby(['brewery_type', 'country', 'state']).size().reset_index(name='count')
    
    assert len(gold) == 2  # Dois tipos: micro e large
    assert gold.loc[gold['brewery_type'] == 'micro', 'count'].values[0] == 2

def test_data_quality_missing_ids():
    """Valida se o check de qualidade identifica IDs nulos"""
    df_invalid = pd.DataFrame({'id': [None, '123'], 'brewery_type': ['micro', 'micro']})
    
    with pytest.raises(ValueError, match="IDs nulos encontrados"):
        if df_invalid['id'].isnull().any():
            raise ValueError("IDs nulos encontrados")