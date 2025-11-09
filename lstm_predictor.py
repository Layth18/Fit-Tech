"""
LSTM-based Performance Predictor
Predicts future match performance using time-series LSTM model
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import MinMaxScaler separately (needed even without TensorFlow)
try:
    from sklearn.preprocessing import MinMaxScaler
except ImportError:
    # Fallback if sklearn not available
    MinMaxScaler = None
    print("scikit-learn not available. Using simplified rating calculation.")

try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. Using simplified model.")


class LSTMPredictor:
    """LSTM model for predicting match performance"""
    
    def __init__(self, sequence_length: int = 15, n_features: int = 20):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        # Initialize scalers only if available
        if MinMaxScaler is not None:
            self.scaler = MinMaxScaler()
            self.feature_scaler = MinMaxScaler()
        else:
            self.scaler = None
            self.feature_scaler = None
        self.is_trained = False
        self.TENSORFLOW_AVAILABLE = TENSORFLOW_AVAILABLE
        
    def prepare_sequences(self, data: pd.DataFrame, 
                         target_col: str = 'performance_rating',
                         feature_cols: List[str] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for LSTM training
        Returns (X, y) where X is sequences and y is targets
        """
        if feature_cols is None:
            # Select numeric columns excluding target
            feature_cols = [col for col in data.select_dtypes(include=[np.number]).columns 
                          if col != target_col]
        
        # Sort by date if available
        if 'date' in data.columns:
            data = data.sort_values('date')
        
        # Extract features and target
        features = data[feature_cols].values
        target = data[target_col].values if target_col in data.columns else None
        
        # Scale features
        if self.feature_scaler is not None:
            features_scaled = self.feature_scaler.fit_transform(features)
        else:
            # Simple normalization if scaler not available
            features_scaled = (features - features.min(axis=0)) / (features.max(axis=0) - features.min(axis=0) + 1e-6)
        
        # Create sequences
        X, y = [], []
        
        for i in range(self.sequence_length, len(features_scaled)):
            # Input sequence: previous sequence_length days
            X.append(features_scaled[i - self.sequence_length:i])
            
            # Target: performance rating at current time
            if target is not None:
                y.append(target[i])
            else:
                y.append(0)  # Placeholder
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> Optional[object]:
        """Build LSTM model architecture"""
        if not self.TENSORFLOW_AVAILABLE:
            print("TensorFlow not available. Using simple linear predictor.")
            return None
        
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        
        return model
    
    def train(self, X: np.ndarray, y: np.ndarray, 
             validation_split: float = 0.2, epochs: int = 50, 
             batch_size: int = 32, verbose: int = 1) -> Dict:
        """
        Train the LSTM model
        """
        if not self.TENSORFLOW_AVAILABLE:
            # Simple linear regression fallback
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error, mean_absolute_error
            
            # Flatten sequences for linear model
            X_flat = X.reshape(X.shape[0], -1)
            
            split_idx = int(len(X_flat) * (1 - validation_split))
            X_train, X_val = X_flat[:split_idx], X_flat[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)
            
            history = {
                'loss': [mean_squared_error(y_train, train_pred)],
                'val_loss': [mean_squared_error(y_val, val_pred)],
                'mae': [mean_absolute_error(y_train, train_pred)],
                'val_mae': [mean_absolute_error(y_val, val_pred)]
            }
            
            self.model = model
            self.is_trained = True
            
            return history
        
        # Build model
        input_shape = (X.shape[1], X.shape[2])
        self.model = self.build_model(input_shape)
        
        if self.model is None:
            return {}
        
        # Scale target
        if self.scaler is not None:
            y_scaled = self.scaler.fit_transform(y.reshape(-1, 1)).flatten()
        else:
            # Simple normalization if scaler not available
            y_min, y_max = y.min(), y.max()
            y_scaled = (y - y_min) / (y_max - y_min + 1e-6)
        
        # Train
        history = self.model.fit(
            X, y_scaled,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose
        )
        
        self.is_trained = True
        
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict performance ratings
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if not self.TENSORFLOW_AVAILABLE:
            # Linear model prediction
            X_flat = X.reshape(X.shape[0], -1)
            predictions = self.model.predict(X_flat)
            return predictions.flatten()
        
        # LSTM prediction
        predictions_scaled = self.model.predict(X, verbose=0)
        if self.scaler is not None:
            predictions = self.scaler.inverse_transform(predictions_scaled.reshape(-1, 1))
        else:
            # Simple denormalization if scaler not available
            predictions = predictions_scaled
        
        return predictions.flatten()
    
    def predict_next_match(self, recent_data: pd.DataFrame,
                          feature_cols: List[str] = None) -> float:
        """
        Predict performance rating for next match given recent training cycle data
        """
        if feature_cols is None:
            feature_cols = [col for col in recent_data.select_dtypes(include=[np.number]).columns]
        
        # Get last sequence_length days
        if len(recent_data) < self.sequence_length:
            # Pad with last available data
            padding_needed = self.sequence_length - len(recent_data)
            last_row = recent_data.iloc[-1:].copy()
            padding = pd.concat([last_row] * padding_needed, ignore_index=True)
            recent_data = pd.concat([padding, recent_data], ignore_index=True)
        
        # Prepare sequence
        features = recent_data[feature_cols].values[-self.sequence_length:]
        if self.feature_scaler is not None:
            features_scaled = self.feature_scaler.transform(features)
        else:
            # Simple normalization if scaler not available
            features_scaled = (features - features.min(axis=0)) / (features.max(axis=0) - features.min(axis=0) + 1e-6)
        sequence = features_scaled.reshape(1, self.sequence_length, len(feature_cols))
        
        # Predict
        prediction = self.predict(sequence)
        
        # Ensure prediction is in valid range (1-10)
        prediction = np.clip(prediction[0], 1.0, 10.0)
        
        return float(prediction)
    
    def export_to_onnx(self, output_path: str, input_shape: Tuple[int, int] = None) -> bool:
        """
        Export trained TensorFlow/Keras model to ONNX format
        
        Args:
            output_path: Path to save the ONNX model (e.g., 'model.onnx')
            input_shape: Input shape (sequence_length, n_features). 
                        If None, uses self.sequence_length and self.n_features
        
        Returns:
            True if export successful, False otherwise
        """
        if not self.TENSORFLOW_AVAILABLE:
            print("[ERROR] TensorFlow not available. Cannot export to ONNX.")
            print("ONNX export requires TensorFlow/Keras model.")
            return False
        
        if not self.is_trained or self.model is None:
            print("[ERROR] Model not trained. Train the model first.")
            return False
        
        try:
            import tf2onnx
            import onnx
        except ImportError:
            print("[ERROR] tf2onnx not installed. Install it with: pip install tf2onnx")
            return False
        
        try:
            # Determine input shape
            if input_shape is None:
                input_shape = (self.sequence_length, self.n_features)
            
            # Create a dummy input for shape specification
            dummy_input = np.random.randn(1, *input_shape).astype(np.float32)
            
            # Convert to ONNX
            print(f"[*] Converting model to ONNX format...")
            print(f"[*] Input shape: {input_shape}")
            
            # Use tf2onnx to convert Keras model to ONNX
            # Try different API approaches for compatibility
            try:
                # Method 1: Using TensorSpec (newer API)
                from tf2onnx import convert
                spec = (convert.TensorSpec(dummy_input.shape, dtype=dummy_input.dtype, name="input"),)
                onnx_model, _ = convert.from_keras(
                    self.model,
                    input_signature=spec,
                    opset=13
                )
            except (AttributeError, ImportError):
                # Method 2: Using older API
                import tf2onnx
                spec = (tf2onnx.TensorSpec(dummy_input.shape, dtype=dummy_input.dtype, name="input"),)
                onnx_model, _ = tf2onnx.convert.from_keras(
                    self.model,
                    input_signature=spec,
                    opset=13
                )
            
            # Save ONNX model
            onnx.save_model(onnx_model, output_path)
            print(f"[OK] Model exported to ONNX: {output_path}")
            print(f"[*] Model input shape: {input_shape}")
            print(f"[*] Model output: single value (performance rating)")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to export to ONNX: {e}")
            import traceback
            traceback.print_exc()
            return False

