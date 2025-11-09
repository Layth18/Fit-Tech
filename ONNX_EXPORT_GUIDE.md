# Export AI Model to ONNX Format - Guide

## What is ONNX?

ONNX (Open Neural Network Exchange) is an open format for machine learning models that allows you to:
- Deploy models across different platforms (Python, C++, JavaScript, etc.)
- Use optimized inference engines (ONNX Runtime)
- Share models between different frameworks
- Deploy to edge devices, mobile, and cloud

---

## Prerequisites

### 1. Install Required Packages

```bash
pip install tf2onnx onnx onnxruntime
```

Or update requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. TensorFlow Must Be Installed

ONNX export **requires TensorFlow**. The fallback linear regression model cannot be exported to ONNX.

---

## How to Export

### Method 1: Using the Export Script (Recommended)

```bash
# Export model for a specific player
python export_to_onnx.py --player "Player Name" --output player_model.onnx

# With position specification
python export_to_onnx.py --player "Ahmed Al-Nakhli" --position midfielder --output ahmed_model.onnx
```

**Example:**
```bash
python export_to_onnx.py --player "Yousef Al-Shammari" --output yousef_model.onnx
```

### Method 2: Using Python Code

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

# Initialize and train
predictor = CycleToPeakPredictor()
predictor.load_all_data()
predictor.prepare_player_data("Player Name", position="midfielder")
predictor.train_model("Player Name")

# Export to ONNX
lstm_predictor = predictor.lstm_predictor
input_shape = (15, 20)  # (sequence_length, n_features)
lstm_predictor.export_to_onnx("model.onnx", input_shape=input_shape)
```

### Method 3: Direct from LSTMPredictor

```python
from lstm_predictor import LSTMPredictor
import numpy as np

# Create and train predictor
predictor = LSTMPredictor(sequence_length=15, n_features=20)
# ... train the model ...

# Export
predictor.export_to_onnx("model.onnx", input_shape=(15, 20))
```

---

## Export Process

1. **Train the model** - Model must be trained first
2. **Convert to ONNX** - Uses tf2onnx to convert TensorFlow/Keras model
3. **Save file** - Saves as `.onnx` file

---

## Using the Exported ONNX Model

### In Python with ONNX Runtime

```python
import onnxruntime as ort
import numpy as np

# Load the ONNX model
session = ort.InferenceSession("model.onnx")

# Prepare input data
# Shape: (batch_size, sequence_length, n_features)
# Example: (1, 15, 20)
input_data = np.random.randn(1, 15, 20).astype(np.float32)

# Get input name
input_name = session.get_inputs()[0].name

# Run inference
outputs = session.run(None, {input_name: input_data})

# Get prediction
prediction = outputs[0][0][0]  # Single value
print(f"Predicted performance rating: {prediction}")
```

### In C++

```cpp
#include <onnxruntime_cxx_api.h>

// Load model
Ort::Env env;
Ort::Session session(env, "model.onnx", Ort::SessionOptions{nullptr});

// Prepare input
std::vector<float> input_data(1 * 15 * 20);
// ... fill input_data ...

// Run inference
auto output = session.Run(...);
```

### In JavaScript/Node.js

```javascript
const ort = require('onnxruntime-node');

// Load model
const session = await ort.InferenceSession.create('./model.onnx');

// Prepare input
const inputTensor = new ort.Tensor('float32', inputData, [1, 15, 20]);

// Run inference
const results = await session.run({ input: inputTensor });
const prediction = results.output.data[0];
```

---

## Model Information

### Input Shape
- **Format:** `(batch_size, sequence_length, n_features)`
- **Default:** `(1, 15, 20)`
- **Meaning:**
  - `batch_size`: Usually 1 for single prediction
  - `sequence_length`: 15 days of training data
  - `n_features`: 20 features per day

### Output Shape
- **Format:** `(batch_size, 1)`
- **Value:** Single float (performance rating 1-10)

### Data Preprocessing

**Important:** The ONNX model expects **scaled/normalized** input data. You need to:
1. Use the same feature scaler used during training
2. Scale your input data before inference

```python
# Example: Scale input data
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Assuming you saved the scaler during training
scaler = MinMaxScaler()
# ... fit scaler on training data ...

# Scale new data
input_data = np.array([...])  # Shape: (15, 20)
scaled_data = scaler.transform(input_data)
reshaped = scaled_data.reshape(1, 15, 20).astype(np.float32)

# Run ONNX model
outputs = session.run(None, {input_name: reshaped})
```

---

## Troubleshooting

### Error: "TensorFlow not available"
- **Solution:** Install TensorFlow: `pip install tensorflow`
- ONNX export requires TensorFlow/Keras models

### Error: "tf2onnx not installed"
- **Solution:** `pip install tf2onnx onnx`

### Error: "Model not trained"
- **Solution:** Train the model first before exporting

### Error: "Input shape mismatch"
- **Solution:** Ensure input shape matches training shape
- Default: `(1, 15, 20)` for sequence_length=15, n_features=20

### Model file is large
- **Normal:** ONNX models can be 1-10 MB depending on architecture
- **Optimization:** Use ONNX Runtime optimizations for deployment

---

## Advanced: Model Optimization

### Quantization (Reduce Size)

```python
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

# Load model
model_fp32 = "model.onnx"
model_quant = "model_quantized.onnx"

# Quantize to INT8
quantize_dynamic(model_fp32, model_quant, weight_type=QuantType.QUInt8)
```

### Optimization for Inference

```python
import onnx
from onnxruntime.transformers import optimizer

# Optimize model
model = onnx.load("model.onnx")
optimized_model = optimizer.optimize_model(model)
optimized_model.save_model_to_file("model_optimized.onnx")
```

---

## Example: Complete Workflow

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
import onnxruntime as ort
import numpy as np

# 1. Train and export
predictor = CycleToPeakPredictor()
predictor.load_all_data()
predictor.prepare_player_data("Player Name", position="midfielder")
predictor.train_model("Player Name")

# Export
lstm_predictor = predictor.lstm_predictor
input_shape = lstm_predictor.model.input_shape[1:]
lstm_predictor.export_to_onnx("player_model.onnx", input_shape=input_shape)

# 2. Use exported model
session = ort.InferenceSession("player_model.onnx")
input_name = session.get_inputs()[0].name

# Prepare input (scaled data)
input_data = np.random.randn(1, 15, 20).astype(np.float32)

# Predict
output = session.run(None, {input_name: input_data})
prediction = output[0][0][0]
print(f"Prediction: {prediction}")
```

---

## Summary

✅ **Export:** `python export_to_onnx.py --player "Name" --output model.onnx`  
✅ **Use:** Load with ONNX Runtime in Python/C++/JavaScript  
✅ **Input:** Shape `(1, 15, 20)` - scaled features  
✅ **Output:** Single float value (performance rating)  

**Your model is now portable and deployable!** 🚀

