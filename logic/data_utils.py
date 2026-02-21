"""
Data Utilities
Reusable pandas functions for data cleaning, normalization, and validation.
"""
import pandas as pd
from typing import List

def clean_email_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Очистка и нормализация колонки с email-адресами (нижний регистр, удаление пробелов)."""
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.strip().str.lower()
    return df

def clean_string_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Удаление пробелов по краям строковых данных в указанной колонке."""
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.strip()
    return df

def filter_valid_grades(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Удаление пустых, NaN и невалидных значений оценок из колонки."""
    if column_name in df.columns:
        df = df[df[column_name].notna()]
        df = df[df[column_name].astype(str).str.strip() != '']
        df = df[df[column_name].astype(str).str.strip().str.lower() != 'nan']
    return df

def extract_missing_columns(df: pd.DataFrame, required_columns: List[str]) -> List[str]:
    """Возвращает список колонок, которых не хватает в DataFrame."""
    return [col for col in required_columns if col not in df.columns]
