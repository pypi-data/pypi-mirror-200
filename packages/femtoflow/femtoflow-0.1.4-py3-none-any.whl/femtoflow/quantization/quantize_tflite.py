"""
TFLite Utilities Related Files, for converting a Tensorflow to TFLite Quantized Model 
"""
import tensorflow as tf
import numpy as np
import tempfile
from typing import Dict, Union, Callable

# Setup Logging
import logging
logging.basicConfig(level=logging.INFO)


class TFLiteUtils:
    """
    Quantization Related Utilities for TFLite Conversion.
    """

    @staticmethod
    def quantize_input_tensor(x: Union[np.ndarray, tf.Tensor], runner, name: str) -> np.ndarray:
        """
        Quantize an input tensor from float to int, using metadata from the TFLite
        SignatureRunner.

        Args:
            x (np.ndarray): Unquantized Tensor
            runner: TFLite Signature Runner
            name (str): The 'name' of the tensor corresponding to `x`
        
        Returns:
            (np.ndarray): The Quantized Tensor
        """
        details = runner.get_input_details()[name]
        scale, zero_point = details['quantization']
        return np.round(np.array(x, dtype=float) / scale) + zero_point

    @staticmethod
    def dequantize_output_tensor(x: Union[np.ndarray, tf.Tensor], runner, name: str) -> np.ndarray:
        """Dequantize an output value back to a float, using metadata from the TFLite 
        SignatureRunner.

        Args:
            x (tf.Tensor): Quantized Tensor`
            runner: TFLite Signature Runner
            name (str): The 'name' of the tensor corresponding to `x`

        Returns:
            (np.ndarray): The De-Quantized Tensor
        """
        details = runner.get_output_details()[name]
        scale, zero_point = details['quantization']
        return scale * (np.array(x, dtype=float) - zero_point)

    @staticmethod
    def quantized_predict(interpreter: tf.lite.Interpreter, signature_name: str,
                           inputs:Dict[str, np.ndarray], predict_fn: Callable) -> Dict[str, np.ndarray]:
        """
        Prediction function for quantized models. Can be used for TFLite inference, 
        depending on 'predict_fn'. Passed to __process_sequences__ during inference.

        Args:
            interpreter (tf.lite.Interpreter): TFLite Interpreter
            signature_name (str): Signature Name
            inputs (Dict[str, np.ndarray]): {'input_name': input_arr ...}
            predict_fn (Callable): Lambda Function that does a forward pass on 
                                     the Quantized Inputs
        Returns:
            (Dict[str, np.ndarray]): The Predicted De-Quantized Output
        """
        # Quantize inputs
        np_dtype = interpreter.get_input_details()[0]['dtype']
        runner = interpreter.get_signature_runner(signature_name)
        quantized_inputs = {name: TFLiteUtils.quantize_input_tensor(value, runner, name).astype(np_dtype) for name, value in inputs.items()} 
        
        # Predict
        quantized_outputs = predict_fn(quantized_inputs)
        dequantized_output = {key: TFLiteUtils.dequantize_output_tensor(value,
                                                                    runner,
                                                                    key).squeeze()
                                                for key, value in quantized_outputs.items()}
        # Dequantize outputs
        return dequantized_output


class TFLiteInt8Model:
    """
            This class provides functionality to convert a Tensorflow model 
            into its TFLite Equivalent, with INT-8 Weights and Activations Quantized.
    """

    def __init__(self, model: Union[tf.keras.Model, 
                                    tf.keras.Sequential], 
                       representative_dataset: Callable, 
                       tflite_save_path: str) -> None:
        """
        Constructor for the `TFLiteInt8Model` class

        Args:
            model (Union[tf.keras.Model, tf.keras.Sequential]): The Tensorflow Model
            representative_dataset (Callable): Lambda Function used as the Calibration dataset
                                                    for TFLite Conversion.
            tflite_save_path (str): Path to save the TFlite model file.

        Example:
    
        .. code-block:: python
        
            from femtoflow.quantization.quantize_tflite import TFLiteInt8Model
            import tensorflow as tf

            # Model Definition
            model_tf = tf.keras.Model(...) # The Tensorflow Model

            # Input Name of Model (Assume Single-Input model).
            model_input_name = 'foo_input_name'

            # Save Path of TFLite Object
            tflite_save_path = 'save_path.tflite'
            
            # Calibration Data Setup
            train_feats = ... # Input Features for Calibration
            num_samples = 50
            
            def representative_data_gen():
                for input_value in tf.data.Dataset.from_tensor_slices(train_feats).batch(batch_size).take(num_samples):
                    # Model has only one input so each data point has one element.
                    yield {model_input_name: tf.cast(input_value, dtype=tf.float32)}

            representative_dataset = representative_data_gen

            # Convert Tensorflow model to TFLite
            model_tflite = TFLiteInt8(model= model_tf, representative_dataset=representative_dataset,             
                                    tflite_save_path=tflite_save_path) 

            # Perform TFLite Inference on `input_feats`
            input_feats = ... # Input Features
            model_tflite_out = model_tflite({model_input_name: input_feats})
            print("Quantized inference output")
            
            # Check if TFLite file was actually generated
            assert os.path.exists(tflite_save_path), f"ERR: TFLite file {tflite_save_path} not saved successfully."

        

        Note: 
            For Models with Multiple Inputs/ Multiple Outputs, it is 
            recommended to supply a model of type `tf.keras.Model(inputs=inputs, outputs=outputs)`
            with the Input/Output Names/Shapes of the model explicitly defined.
            The Model supplied should also have `model.input_spec` defined.
            There could be TFLite Conversion Errors if the Inputs/Outputs 
            aren't explicitly defined.
        """
        self.tflite_model = self.tflite_convert_int8(model=model,
                                                     representative_dataset=representative_dataset,
                                                     tflite_save_path=tflite_save_path)

        self.interpreter = tf.lite.Interpreter(model_content=self.tflite_model)

        self.default_sig_name = 'serving_default' 
        self.runner = self.interpreter.get_signature_runner(self.default_sig_name)

        self.input_details = self.runner.get_input_details()
        self.output_details = self.runner.get_output_details()

        self.tflite_pred_fn = lambda inputs: TFLiteUtils.quantized_predict(interpreter=self.interpreter,
                                                                            signature_name=self.default_sig_name,
                                                                            inputs=inputs,
                                                                            predict_fn=lambda quantized_inputs: self.runner(**quantized_inputs))

    def tflite_convert_int8(self, model: Union[tf.keras.Model, 
                                               tf.keras.Sequential], 
                                  representative_dataset: Callable, 
                                  tflite_save_path: str) -> bytes:
        """
        Converts TF model into its TFLite Equivalent, with INT-8 Weights and Activations Quantized.
        Saves the TFLite File at the `tflite_save_path` specified, and returns the converted TFLite model buffer.

        Args:
            model (Union[tf.keras.Model, tf.keras.Sequential]): The Tensorflow Model
            representative_dataset (Callable): Lambda Function used as the Calibration dataset
                                                    for TFLite Conversion.
            tflite_save_path (str): Path to save the TFlite model file.
        
        Returns:
            (bytes): TFLite Binary Flatbuffer
        """
        assert model.input_spec is not None, "model.input_spec() was None. Expected to be Defined. \
                                              Please define explicit Input/Output Signatures to your model using \
                                              tf.keras.Model(inputs=inputs, outputs=outputs)"
        ip_shapes = [tf.TensorSpec(shape=x.shape, name=x.name) for x in model.input_spec]
        with tempfile.TemporaryDirectory() as dirname: 

            run_model = tf.function(lambda x: model(x))

            concrete_func = run_model.get_concrete_function(ip_shapes)
            model.save(dirname, save_format="tf", signatures=concrete_func)

            tf_dtype = tf.int8
            converter = tf.lite.TFLiteConverter.from_saved_model(dirname)
            converter.inference_input_type = tf_dtype 
            converter.inference_output_type = tf_dtype
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

            converter.representative_dataset = representative_dataset

            # Convert the inference model to TFLite
            logging.info("Converting TF model to TFLite...")
            tflite_model = converter.convert()

            with open(tflite_save_path, 'wb') as f:
                f.write(tflite_model)
        
        return tflite_model

    def __call__(self, inputs: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Do Quantized Forward Pass for TFLite model

        Args:
            inputs (Dict[str, np.ndarray]): Unquantized Dictionary Inputs

        Returns: 
            output (Dict[str, np.ndarray]): Unquantized Dictionary Outputs
        """
        output = self.tflite_pred_fn(inputs)
        return output