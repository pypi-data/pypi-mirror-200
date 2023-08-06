

import tensorflow as tf
import os
import numpy as np
from femtoflow.quantization.quantize_tflite import TFLiteInt8Model


def test_TFLiteInt8Model():
    """
    Quantizes a Tensorflow Model with Dense/Conv2D Layers 
    to INT-8 Activations and Weights using `TFLiteInt8Model`.
    
    Further, confirm forward pass of the TF Model, TFLite Model
    gives roughly the same output on validation data.
    """
    batch_size = 256
    train_samples = 1024
    val_samples = 512

    # Generate random data for training and validation
    train_data = np.random.rand(train_samples, 28, 28, 3) # 1024 images of size 28x28 with 3 channels
    train_labels = np.random.randint(0, 10, size=(train_samples,)) # 1024 random labels between 0 and 9
    train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels)).batch(batch_size, drop_remainder=True)

    val_data = np.random.rand(val_samples, 28, 28, 3) # 1024 images of size 28x28 with 3 channels
    val_labels = np.random.randint(0, 10, size=(val_samples,)) # 1024 random labels between 0 and 9
    val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels)).batch(batch_size, drop_remainder=True)

    # Define the model architecture
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    # Compile the model with appropriate loss and metrics
    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    input_name = model.input_names[0]
    output_name =  'output_0'
    def representative_data_gen(num_samples=5):
        for feats, labels in train_dataset.take(num_samples):
            # Model has only one input so each data point has one element.
            yield {input_name: tf.cast(feats, dtype=tf.float32)}
        
    tflite_save_path = 'tflite_unittest.tflite'
    model_tflite = TFLiteInt8Model(model=model,
                                    representative_dataset=representative_data_gen,
                                    tflite_save_path=tflite_save_path)

    assert os.path.exists(tflite_save_path), f"ERR: TFLite file not found at {tflite_save_path}"

    for feats, _ in val_dataset:
        input_dict = {input_name: feats}
        tf_fwd = model(input_dict)
        tflite_fwd = model_tflite(input_dict)[output_name]

        tolerance = 0.1
        assert np.allclose(tf_fwd, tflite_fwd, atol=tolerance)