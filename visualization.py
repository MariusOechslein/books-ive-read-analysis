"""Module for creating visualizations and plots."""

import logging
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from config import (
    PLOTS_DIR,
    FIGURE_SIZE_LARGE,
    FIGURE_SIZE_MEDIUM,
    ROTATION_ANGLE,
    ANALYSIS_YEARS,
    COLUMN_YEAR,
    COLUMN_CATEGORIES,
)

logger = logging.getLogger(__name__)


def ensure_plots_directory() -> None:
    """Ensure the plots directory exists."""
    PLOTS_DIR.mkdir(exist_ok=True)


def plot_books_per_year(books_pd: pd.DataFrame) -> None:
    """
    Create a bar plot showing the number of books read per year.
    
    Args:
        books_pd: DataFrame containing books data with a 'year' column.
    """
    try:
        ensure_plots_directory()
        
        books_per_year = books_pd[COLUMN_YEAR].value_counts().sort_index()
        
        plt.figure(figsize=FIGURE_SIZE_MEDIUM)
        plt.bar(books_per_year.index, books_per_year.values)
        plt.xlabel('Year')
        plt.ylabel('Number of Books')
        plt.title('Books Read Per Year')
        plt.xticks(rotation=ROTATION_ANGLE)
        
        output_path = PLOTS_DIR / 'books_per_year.png'
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Saved plot to {output_path}")
        print(f"Plot saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Error creating books per year plot: {e}")
        raise


def plot_books_per_column(
    books_extended_pd: pd.DataFrame,
    column: str = COLUMN_CATEGORIES,
    save_file_name_suffix: str = ''
) -> None:
    """
    Create a bar plot showing the number of books per category/column.
    
    This function handles columns that contain comma-separated values by
    splitting them and counting each value separately.
    
    Args:
        books_extended_pd: DataFrame containing the column to plot.
        column: Name of the column to plot (default: 'categories').
        save_file_name_suffix: Optional suffix to add to the output filename.
    """
    try:
        ensure_plots_directory()
        
        # Split comma-separated values and flatten
        column_series = books_extended_pd[column].dropna().apply(lambda x: x.split(', '))
        all_values = [value for sublist in column_series for value in sublist]
        
        # Count occurrences
        value_counts = pd.Series(all_values).value_counts()
        
        # Create plot
        plt.figure(figsize=FIGURE_SIZE_LARGE)
        value_counts.plot(kind='bar')
        plt.xlabel(column.capitalize())
        plt.ylabel('Number of Books')
        plt.title(f'Books per {column.capitalize()}')
        plt.xticks(rotation=ROTATION_ANGLE, ha='right')
        
        # Save plot
        output_filename = f'books_per_{column}{save_file_name_suffix}.png'
        output_path = PLOTS_DIR / output_filename
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Saved plot to {output_path}")
        print(f"Plot saved to {output_path}")
    
    except KeyError:
        logger.error(f"Column '{column}' not found in DataFrame")
        raise
    except Exception as e:
        logger.error(f"Error creating plot for column '{column}': {e}")
        raise


def plot_books_per_column_per_year(
    books_extended_pd: pd.DataFrame,
    books_pd: pd.DataFrame,
    column: str = COLUMN_CATEGORIES
) -> None:
    """
    Create plots showing book distribution by column for each year.
    
    Creates individual plots for each year and a combined subplot figure.
    
    Args:
        books_extended_pd: Extended DataFrame containing the column to plot.
        books_pd: Original DataFrame containing the 'year' column.
        column: Name of the column to plot (default: 'categories').
    """
    try:
        ensure_plots_directory()
        
        # Add year column to extended DataFrame
        if len(books_extended_pd) != len(books_pd):
            error_msg = "Error: Length of books_extended_pd and books_pd do not match"
            logger.error(error_msg)
            print(error_msg)
            raise ValueError(error_msg)
        
        books_extended_pd[COLUMN_YEAR] = books_pd[COLUMN_YEAR]
        
        # Create individual plots for each year
        for year in ANALYSIS_YEARS:
            books_year = books_extended_pd[books_extended_pd[COLUMN_YEAR] == year]
            if not books_year.empty:
                plot_books_per_column(
                    books_year,
                    column=column,
                    save_file_name_suffix=f"_{year}"
                )
        
        # Create combined subplot figure
        plt.figure(figsize=FIGURE_SIZE_LARGE)
        
        for i, year in enumerate(ANALYSIS_YEARS):
            plt.subplot(3, 3, i + 1)
            
            books_year = books_extended_pd[books_extended_pd[COLUMN_YEAR] == year]
            
            if not books_year.empty and column in books_year.columns:
                # Split comma-separated values and flatten
                column_series = books_year[column].dropna().apply(lambda x: x.split(', '))
                all_values = [value for sublist in column_series for value in sublist]
                
                if all_values:
                    value_counts = pd.Series(all_values).value_counts()
                    value_counts.plot(kind='bar')
            
            plt.xlabel(column.capitalize())
            plt.ylabel('Number of Books')
            plt.title(f'Books per {column.capitalize()} in {year}')
            plt.xticks(rotation=ROTATION_ANGLE, ha='right')
        
        plt.tight_layout()
        
        output_path = PLOTS_DIR / f'books_per_{column}_per_year.png'
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Saved combined plot to {output_path}")
        print(f"Combined plot saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Error creating plots per year for column '{column}': {e}")
        raise
