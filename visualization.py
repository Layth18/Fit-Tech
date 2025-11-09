"""
Visualization Module for Cycle-to-Peak Predictor
Creates charts and visualizations for performance analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('default')

sns.set_palette("husl")


class PerformanceVisualizer:
    """Creates visualizations for performance analysis"""
    
    def __init__(self):
        self.figsize = (12, 6)
    
    def plot_performance_evolution(self, evolution_data: pd.DataFrame, 
                                  predicted_rating: Optional[float] = None,
                                  save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot performance evolution over time with predicted rating
        """
        if len(evolution_data) == 0:
            print("No evolution data to plot")
            return None
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot historical ratings
        ax.plot(evolution_data['date'], evolution_data['performance_rating'],
                marker='o', linewidth=2, markersize=8, label='Historical Performance', color='#2E86AB')
        
        # Add predicted rating if provided
        if predicted_rating is not None:
            last_date = evolution_data['date'].max()
            next_date = last_date + pd.Timedelta(days=7)  # Assume next match in 7 days
            ax.scatter([next_date], [predicted_rating], 
                      marker='*', s=300, color='#A23B72', 
                      label=f'Predicted Rating: {predicted_rating:.2f}', zorder=5)
            ax.plot([last_date, next_date], 
                   [evolution_data['performance_rating'].iloc[-1], predicted_rating],
                   '--', color='#A23B72', alpha=0.5, linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Performance Rating (1-10)', fontsize=12, fontweight='bold')
        ax.set_title('Player Performance Evolution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        ax.set_ylim(0, 10.5)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_training_cycle(self, cycle_data: pd.DataFrame,
                           save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot training cycle showing daily physical load
        """
        if len(cycle_data) == 0:
            print("No cycle data to plot")
            return None
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Filter to training days only
        training_days = cycle_data[cycle_data['event_type'] == 'Training Day'].copy()
        
        if len(training_days) > 0:
            # Sort by J_minus (days until match)
            training_days = training_days.sort_values('J_minus', ascending=False)
            
            # Create bar chart
            colors = plt.cm.viridis(np.linspace(0, 1, len(training_days)))
            bars = ax.barh(training_days['J_minus'], training_days['player_load'],
                          color=colors, alpha=0.7, edgecolor='black', linewidth=1)
            
            # Add value labels
            for i, (j_minus, load) in enumerate(zip(training_days['J_minus'], training_days['player_load'])):
                if load > 0:
                    ax.text(load, j_minus, f'{load:.0f}', 
                           va='center', ha='left', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Player Load', fontsize=12, fontweight='bold')
        ax.set_ylabel('Days Until Match (J-)', fontsize=12, fontweight='bold')
        ax.set_title('Training Cycle - Physical Load Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_match_readiness_dashboard(self, predictions: List[Dict],
                                         save_path: Optional[str] = None) -> plt.Figure:
        """
        Create dashboard showing match readiness scores for multiple players
        """
        if len(predictions) == 0:
            print("No predictions to plot")
            return None
        
        df = pd.DataFrame(predictions)
        df = df.sort_values('match_readiness_score', ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(df) * 0.5)))
        
        # Color code by readiness
        colors = ['#E63946' if score < 5 else '#F77F00' if score < 7 else '#06A77D' 
                 for score in df['match_readiness_score']]
        
        bars = ax.barh(df['player_name'], df['match_readiness_score'],
                      color=colors, alpha=0.7, edgecolor='black', linewidth=1)
        
        # Add value labels
        for i, (name, score) in enumerate(zip(df['player_name'], df['match_readiness_score'])):
            ax.text(score, i, f' {score:.2f}', 
                   va='center', ha='left', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Match Readiness Score (1-10)', fontsize=12, fontweight='bold')
        ax.set_title('Team Match Readiness Overview', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10.5)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#06A77D', label='Ready (7-10)'),
            Patch(facecolor='#F77F00', label='Moderate (5-7)'),
            Patch(facecolor='#E63946', label='At Risk (<5)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_summary_report(self, player_name: str, prediction: Dict,
                             evolution_data: pd.DataFrame,
                             cycle_data: pd.DataFrame,
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Create comprehensive summary report for a player
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Performance Evolution
        ax1 = fig.add_subplot(gs[0, :])
        if len(evolution_data) > 0:
            self._plot_evolution_subplot(ax1, evolution_data, prediction.get('predicted_rating'))
        
        # 2. Training Cycle
        ax2 = fig.add_subplot(gs[1, 0])
        if len(cycle_data) > 0:
            self._plot_cycle_subplot(ax2, cycle_data)
        
        # 3. Key Metrics
        ax3 = fig.add_subplot(gs[1, 1])
        self._plot_metrics_subplot(ax3, prediction)
        
        fig.suptitle(f'Performance Analysis: {player_name}', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def _plot_evolution_subplot(self, ax, evolution_data: pd.DataFrame, predicted_rating: Optional[float]):
        """Helper for evolution subplot"""
        ax.plot(evolution_data['date'], evolution_data['performance_rating'],
               marker='o', linewidth=2, markersize=6, label='Historical', color='#2E86AB')
        if predicted_rating:
            last_date = evolution_data['date'].max()
            next_date = last_date + pd.Timedelta(days=7)
            ax.scatter([next_date], [predicted_rating], marker='*', s=200,
                      color='#A23B72', label=f'Predicted: {predicted_rating:.2f}')
        ax.set_title('Performance Evolution', fontweight='bold')
        ax.set_ylabel('Rating (1-10)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_cycle_subplot(self, ax, cycle_data: pd.DataFrame):
        """Helper for cycle subplot"""
        training_days = cycle_data[cycle_data['event_type'] == 'Training Day'].copy()
        if len(training_days) > 0:
            training_days = training_days.sort_values('J_minus', ascending=False)
            ax.barh(training_days['J_minus'], training_days['player_load'],
                   color='#F18F01', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Player Load')
            ax.set_ylabel('Days Until Match (J-)')
            ax.set_title('Training Cycle', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
    
    def _plot_metrics_subplot(self, ax, prediction: Dict):
        """Helper for metrics subplot"""
        metrics = {
            'Match Readiness': prediction.get('match_readiness_score', 0),
            'Days Until Match': prediction.get('days_until_match', 0) or 'N/A',
            'Training Load': prediction.get('recent_training_load', 0)
        }
        
        # Create gauge-style visualization
        score = prediction.get('match_readiness_score', 0)
        colors_gauge = ['#E63946', '#F77F00', '#06A77D']
        if score < 5:
            color = colors_gauge[0]
        elif score < 7:
            color = colors_gauge[1]
        else:
            color = colors_gauge[2]
        
        # Simple bar representation
        ax.barh([0], [score], color=color, alpha=0.7, height=0.5)
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Score')
        ax.set_title(f'Match Readiness: {score:.2f}/10', fontweight='bold')
        ax.text(score/2, 0, f'{score:.2f}', ha='center', va='center',
               fontsize=20, fontweight='bold', color='white')
        ax.axis('off')


def main():
    """Example usage"""
    print("Visualization module loaded successfully!")
    print("Use PerformanceVisualizer to create charts and reports.")


if __name__ == "__main__":
    main()


