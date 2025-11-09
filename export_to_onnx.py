"""
Export Trained AI Model to ONNX Format
This script trains a model and exports it to ONNX format for deployment.
"""

import os
import sys
from cycle_to_peak_predictor import CycleToPeakPredictor
from lstm_predictor import LSTMPredictor

def export_player_model_to_onnx(player_name: str, output_path: str = None, 
                                position: str = 'midfielder') -> bool:
    """
    Train a model for a player and export it to ONNX format
    
    Args:
        player_name: Name of the player
        output_path: Path to save ONNX model (default: {player_name}_model.onnx)
        position: Player position ('defender', 'midfielder', 'forward')
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 70)
    print("ONNX Model Export")
    print("=" * 70)
    
    # Check TensorFlow availability
    try:
        import tensorflow as tf
        print(f"[OK] TensorFlow version: {tf.__version__}")
    except ImportError:
        print("[ERROR] TensorFlow not available. ONNX export requires TensorFlow.")
        return False
    
    # Check tf2onnx availability
    try:
        import tf2onnx
        import onnx
        print(f"[OK] tf2onnx available")
    except ImportError:
        print("[ERROR] tf2onnx not installed.")
        print("[*] Install it with: pip install tf2onnx onnx")
        return False
    
    # Initialize predictor
    print(f"\n[*] Initializing predictor...")
    predictor = CycleToPeakPredictor()
    
    # Load data
    print(f"[*] Loading data...")
    predictor.load_all_data()
    
    # Prepare player data
    print(f"[*] Preparing data for player: {player_name}")
    player_data = predictor.prepare_player_data(player_name, position=position)
    
    if len(player_data) == 0:
        print(f"[ERROR] Failed to prepare player data")
        return False
    
    # Train model
    print(f"[*] Training model...")
    history = predictor.train_model(player_name)
    
    if len(history) == 0:
        print(f"[ERROR] Model training failed")
        return False
    
    # Get the trained LSTM predictor
    lstm_predictor = predictor.lstm_predictor
    
    if not lstm_predictor.is_trained:
        print(f"[ERROR] Model is not trained")
        return False
    
    # Determine output path
    if output_path is None:
        # Sanitize player name for filename
        safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        output_path = f"{safe_name}_model.onnx"
    
    # Export to ONNX
    print(f"\n[*] Exporting to ONNX format...")
    print(f"[*] Output file: {output_path}")
    
    # Get input shape from the model
    if lstm_predictor.model is not None:
        # Get input shape from Keras model
        input_shape = lstm_predictor.model.input_shape[1:]  # Remove batch dimension
        success = lstm_predictor.export_to_onnx(output_path, input_shape=input_shape)
    else:
        print("[ERROR] Model is None")
        return False
    
    if success:
        print("\n" + "=" * 70)
        print("EXPORT SUCCESSFUL!")
        print("=" * 70)
        print(f"ONNX model saved to: {os.path.abspath(output_path)}")
        print(f"\n[*] Model Information:")
        print(f"  - Player: {player_name}")
        print(f"  - Position: {position}")
        print(f"  - Input shape: {input_shape}")
        print(f"  - Output: Single value (performance rating 1-10)")
        print(f"\n[*] To use this model:")
        print(f"  import onnxruntime as ort")
        print(f"  session = ort.InferenceSession('{output_path}')")
        print(f"  # Prepare input: shape (1, {input_shape[0]}, {input_shape[1]})")
        print(f"  # Get output: session.run(None, {{'input': your_data}})")
        return True
    else:
        print("\n[ERROR] Export failed")
        return False


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export AI model to ONNX format')
    parser.add_argument('--player', type=str, required=True,
                       help='Player name to train and export')
    parser.add_argument('--output', type=str, default=None,
                       help='Output ONNX file path (default: {player_name}_model.onnx)')
    parser.add_argument('--position', type=str, default='midfielder',
                       choices=['defender', 'midfielder', 'forward'],
                       help='Player position (default: midfielder)')
    
    args = parser.parse_args()
    
    success = export_player_model_to_onnx(
        player_name=args.player,
        output_path=args.output,
        position=args.position
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

