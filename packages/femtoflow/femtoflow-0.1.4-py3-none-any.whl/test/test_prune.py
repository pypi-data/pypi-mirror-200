import unittest
import pytest
import tensorflow as tf
import numpy as np
import random
from parameterized import parameterized
import tensorflow_model_optimization as tfmot
from femtoflow.sparsity.prune import PruneHelper
from femtoflow.utils.metrics import calculate_sparsity

class TestPruneHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """
        Set of Testcases to test the PruneHelper()
        class in prune.py 
        """
        super(TestPruneHelper, self).__init__(*args, **kwargs)
        self.supported_pencil_sizes = (4, 8)

    def base_prune_helper(self, pencil_size=4, pencil_pooling_type='AVG', prune_scheduler='poly_decay',
                          min_parameter_thresh=0):
        """
        Returns an object of `PruneHelper()` with the arguments specifed.
            The default arguments can be overridden if we want a `PruneHelper()` object with
            different arguments
        """
        return PruneHelper(**{'pencil_size': pencil_size, 'pencil_pooling_type': pencil_pooling_type,
                              'prune_scheduler': prune_scheduler, 'min_parameter_thresh': min_parameter_thresh})

    def base_scheduler_args(self, begin_step=0, end_step=100, prune_frequency=5, 
                               power=2, initial_sparsity=0.3, final_sparsity=0.6, frequency=3):
        """ 
        Returns the Arguments to-be-passed to `PruneHelper._get_scheduler_params()`
            Default Arguments can be overwritten if we want to pass different arguments to `PruneHelper._get_scheduler_params()`
        """
        return  {'begin_step': begin_step, 'end_step': end_step, 'prune_frequency': prune_frequency, 'power': power, 
                 'initial_sparsity': initial_sparsity, 'final_sparsity': final_sparsity}

    @parameterized.expand([
        (tf.keras.layers.Conv2D, False),
        (tf.keras.layers.Conv1D, False),
        (tf.keras.layers.Dense,   True),
        (tf.keras.layers.RNN,     True),
        (tf.keras.layers.LSTM,    True)
    ])
    def test_is_pencil_pruning_supported(self, layer, is_supported):
        """
        Test to check if Pencil Pruning is Supported.
            Expectation: Conv1D/ Conv2D do not have Pencil Pruning Supported.
                         Other layers (Linear, LSTN, etc.) have Pencil Pruning Supported. 

        :params layer (tf.layers.layer.keras) - Tensorflow Layer
        :params is_supported (bool) - Expected Is-Supported Results
        """
        prune_wrapper = self.base_prune_helper()
        assert prune_wrapper._is_block_pruning_supported(layer) is is_supported

    @parameterized.expand([
        (1, [tf.keras.layers.Conv1D, tf.keras.layers.Conv2D],  True),
        (6, [tf.keras.layers.Dense, tf.keras.layers.RNN],      True),
        (4, [tf.keras.layers.Dense, tf.keras.layers.Conv2D],  False),
        (4, [tf.keras.layers.Dense, tf.keras.layers.Conv1D],  False),
        (8, [tf.keras.layers.Dense, tf.keras.layers.RNN],      True),
    ])
    def test_is_pruning_supported(self, pencil_size, layers_to_prune, is_supported):
        """
        Test to check if Pruning is Supported, given `pencil_size` and `layers_to_prune`.
            Expectation: 1)  Pruning Conv2D/Conv1D layers are not supported.
                             If Conv2D/Conv1D are specified in `layers_to_prune`,
                             `_is_pruning_supported()` should return False
                         2) Specifying Pencil Size other than 4, 8 should raise an assertion.

        :params pencil_size (int) - The Pencil Size
        :params layers_to_prune (List[tf.keras.layers.Layer]) - List of TF Layers to prune
        :params is_supported (bool) - Expected Is-Supported Results
        """
        if pencil_size not in self.supported_pencil_sizes:
            with pytest.raises(AssertionError):
                prune_wrapper = self.base_prune_helper(pencil_size=pencil_size)
            return                
        prune_wrapper = self.base_prune_helper(pencil_size=pencil_size)
        assert prune_wrapper._is_pruning_supported(layers_to_prune=layers_to_prune) is is_supported

    def test_get_scheduler_params_polynomial_decay(self):
        """
        Test to check if `prune_wrapper._get_scheduler_params()` returns 
        the correct arguments for `prune_scheduler='poly_decay'`
        """
        prune_wrapper = self.base_prune_helper(prune_scheduler='poly_decay')
        scheduler_args   = self.base_scheduler_args()
        scheduler_params = prune_wrapper._get_scheduler_params(**scheduler_args)
        self.assertEqual(scheduler_params, {'begin_step': 0, 'end_step': 100, 'frequency': 5, 'power': 2, 'initial_sparsity': 0.3, 'final_sparsity': 0.6})

    def test_get_scheduler_params_constant_sparsity(self):
        """
        Test to check if `prune_wrapper._get_scheduler_params()` returns 
        the correct arguments for `prune_scheduler='constant'`
        """
        prune_wrapper = self.base_prune_helper(prune_scheduler='constant')
        scheduler_args   = self.base_scheduler_args()
        scheduler_params = prune_wrapper._get_scheduler_params(**scheduler_args)
        self.assertEqual(scheduler_params, {'begin_step': 0, 'end_step': 100, 'frequency': 5, 'target_sparsity': 0.6})

    # Define the model with LSTM, Conv1D, Dense Layers
    model_time_series = tf.keras.Sequential([
        tf.keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(None, 1)),
        tf.keras.layers.LSTM(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])

    # Define the model with Conv2D and Dense layers
    model_mnist = tf.keras.Sequential([
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    @parameterized.expand([
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.LSTM], [], 0),
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.LSTM], [], 1000),
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.LSTM], [], 10000000),
        (model_mnist, [tf.keras.layers.Dense], [], 0),
        (model_mnist, [tf.keras.layers.Dense], [], 1000),
        (model_mnist, [tf.keras.layers.Dense], [], 10000000),
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.LSTM], ['dense_1/kernel:0', 'dense/kernel:0'], 0),
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.LSTM], ['dense_1/kernel:0', 'lstm/lstm_cell_1/kernel:0'], 0),
        (model_mnist, [tf.keras.layers.Dense], ['dense/kernel:0'], 0)
    ])
    def test_model_add_prune_wrappers(self, model, layers_to_prune, force_skip_layers, min_parameter_thresh):
        """
        Test to check if `PruneHelper.model_add_prune_wrappers()` work as expected
            Expectation: 1) Model Layer's specified in `layers_to_prune` get wrapped with 
                            instances of `prune_low_magnitude()` wrapper layer.
                         2) For layers unspecified in `layer_to_prune`, there should
                            be no change.

            Exceptions: 1) Supported Layers with Weight-Matrix size < `min_parameter_thresh`,
                           should NOT be pruned.
                         2) Layer's whose weights are included in `force_skip_layers`
                            should NOT be pruned

        :params model (tf.keras.Sequential) - The Tensorflow Model
        :params layers_to_prune (List[tf.keras.layers.Layer]) - List of TF Layers to prune
        :params force_skip_layers (List[str]) - TF Layers to skip Pruning
        """
        # Clone the Model for this testcase
        model = tf.keras.models.clone_model(model)
        
        # Setup required Variables to Define `prune_wrapper()`
        prune_wrapper = self.base_prune_helper(min_parameter_thresh=min_parameter_thresh)
        scheduler_args   = self.base_scheduler_args()


        # Add the `prune_low_magnitude()` Pruning Wrappers to the layers to be pruned
        model_with_prune_wrappers = prune_wrapper(model=model, layers_to_prune=layers_to_prune, 
                                                  force_skip_layers=force_skip_layers, **scheduler_args)

        def _min_parameter_thresh_check(layer):
            """
            Helper function to check if any of the Weights of Layer `layer`
            has a size (or number of parameters) > `min_parameter_thresh`.

            Generally, a Dense Layer will have 2 Weights: The 2-D Weights and Biases
            Returns:
                True: If the layer has a weight of size > `min_parameter_thresh`
                False: If none of the weights of the layer has size > `min_parameter_thresh`
            """
            return any(tf.size(weight) > min_parameter_thresh for weight in layer.trainable_weights)
        
        def _layer_in_skip_list(layer):
            """
            Checks if the Layer's weights are included in `force_skip_layers`
            Returns:
                True: If layer's weights is included in `force_skip_layers`
                False otherwise
            """
            return any(weight.name in force_skip_layers for weight in layer.trainable_weights)

        # Get Layers we expect to be Pruned
        # 1) Layers should be present in `layers_to_prune`
        # 2) Layers should have weights with Size (number of params) > `min_parameter_thresh`
        # 3) Layer weights should not be included in `force_skip_layers`  
        model_ref_pruned_layers = [any(isinstance(layer, layer_type) and 
                                   _min_parameter_thresh_check(layer) and
                                   not _layer_in_skip_list(layer)  for layer_type in layers_to_prune) for layer in model.layers]
        
        # Assert only Layers in `layers_to_prune` have the Prune Wrapper `prune_low_magnitude` applied 
        for bool_prune_layer, layer in zip(model_ref_pruned_layers, model_with_prune_wrappers.layers):
            if bool_prune_layer:
                # prune_low_magnitude() wrapper applied as expected for layer to be pruned
                assert 'prune_low_magnitude' in layer.name
            else:
                # prune_low_magnitude() wrapper not applied to layer not being pruned
                assert 'prune_low_magnitude' not in layer.name

    @parameterized.expand([
        (model_time_series, [tf.keras.layers.Dense, tf.keras.layers.Conv1D], 4),
        (model_mnist, [tf.keras.layers.Dense, tf.keras.layers.Conv2D], 8),
    ])
    def test_unsupported_conv_layers(self, model, layers_to_prune, pencil_size):
        """
        Test to check if specifying Conv2D/ Conv1D in `layers_to_prune` raises an
        `AssertionError` exception, when trying to prune with `pencil_size = 4/ 8`.
            Expectation: An Exception will be raised, as Conv2D/ Conv1D layers are not
                        supported

        :params model (tf.keras.Sequential) - The Tensorflow Model
        :params layers_to_prune (List[tf.keras.layers.Layer]) - List of TF Layers to prune
        """
        # Clone the Model for this testcase
        model = tf.keras.models.clone_model(model)

        # Pencil Size = 4/8, implies Conv1D/ Conv2D Layers are unsupported        
        prune_wrapper = self.base_prune_helper(pencil_size=pencil_size)
        scheduler_args   = self.base_scheduler_args()

        # layers_to_prune has Conv1D layer. Expect prune_wrapper(..) to fail.
        # as Conv1D/Conv2D layers are not supported with `pencil_size > 1`
        with pytest.raises(AssertionError):
            model_with_prune_wrappers = prune_wrapper(model=model, layers_to_prune=layers_to_prune, **scheduler_args)
        
    """
    Utility Functions for `test_pencil_sparsity_pattern()`
    """
    def select_random_indices(self, array_1d, num_indices):
        """
        Returns `num_indices` random indices that can be sampled
        from a 1-D `array_1d` array (or list)

        :params - array_1d : 1-D Numpy array
        :num_indices (int) : Number of Indices to Return
        """
        return random.sample(range(len(array_1d)), num_indices)
        
    def find_contiguous_blocks(self, arr, val):
        """
        Find's contiguous block lengths of `val` in 1-D array `arr`
        Example:
            arr = [1, 1, 1, 2, 2, 3, 3, 2, 2, 2, 3, 3, 3, 3]
            val = 3
            Output = [2, 4] # There are 2 contiguous blocks of `val=3` 
                              of lengths 2, 4 respectively
        
        :params arr - 1-D np.ndarray or List
        :params val - The Element whose contiguous blocks we want to search
        """
        block_lengths = []
        current_length = 0
        for i in range(arr.size):
            if arr[i] == val:
                current_length += 1
            else:
                if current_length > 0:
                    block_lengths.append(current_length)
                current_length = 0
        if current_length > 0:
            block_lengths.append(current_length)
        return block_lengths

    def find_pencil_size_from_dense_arr(self, arr: np.ndarray,
                                              expected_pencil_size,
                                              num_cols_to_inspect=5):
        """
        Determine's the Pencil Size from the numpy array `arr`.
        
        Procedure:
            1) Select `num_cols_to_inspect` random columns to inspect
            2) Find smallest number of contiguous zeros in each column, i.e.:
               len_zeroes_one, len_zeroes_two ....... len_zeroes_five
            3) The Pencil Size can be estimated to be:
               `pencil_size = min(len_zeroes_one, len_zeroes_two ....... len_zeroes_five) 

        :params arr (np.ndarray) - The weight matrix whose pencil size we want to determine
        :params num_cols_to_inspect (int) - Number of Rows to sample
        """
        # Flatten the weight matrix, to get a Dense Matrix        
        num_rows, num_cols = arr.shape
        cols_to_sample = self.select_random_indices(array_1d=range(0, num_cols), 
                                                    num_indices=num_cols_to_inspect)

        pencil_size = num_rows # Initialize to max-possible pencil size
        for col_id in cols_to_sample:
            # Work with row length, where `len_row % pencil_size == 0`
            arr_col = arr[:num_rows - num_rows % expected_pencil_size, col_id]

            # Get Contiguous Blocks of "Zeros"
            # Find length of all contiguous zeros in each column (`prune_mask_lens`)
            prune_mask_lens = self.find_contiguous_blocks(arr=arr_col, val=0)
            if not prune_mask_lens:
                continue

            # Find the smallest contiguous zero block (or pencil) `prune_mask_min_len`
            prune_mask_min_len = min(prune_mask_lens)
            pencil_size = min(pencil_size, prune_mask_min_len)
        return pencil_size


    @parameterized.expand([
        ((4, 'poly_decay')),
        ((4, 'sine')),
        ((8, 'linear')),
        ((8, 'constant')),
    ])
    def test_pencil_sparsity_pattern(self, pencil_size, prune_scheduler):
        """
        Test to check:
            1) The Sparse Pattern Induced had the expected `pencil_size`
            2) We reached the `final_sparsity` level of 0.7 as expected after
               performing pruning.

            @note: We prune only Dense Layers for simplicity

            :params pencil_size (int) - The Pencil Size
            :params prune_scheduler (str) - The Scheduler Type
        """
        """
        # Generate random data for training and validation
        """
        train_data = np.random.rand(1024, 28, 28, 3) # 1024 images of size 28x28 with 3 channels
        train_labels = np.random.randint(0, 10, size=(1024,)) # 1024 random labels between 0 and 9
        val_data = np.random.rand(512, 28, 28, 3) # 512 images of size 28x28 with 3 channels
        val_labels = np.random.randint(0, 10, size=(512,)) # 512 random labels between 0 and 9

        batch_size=256
        train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels)).batch(batch_size, drop_remainder=True)

        """
        # Define the model architecture
        """
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(10)
        ])

        # Compile the model with appropriate loss and metrics
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])

        # Train the model on the random data
        num_epochs = 2
        model.fit(train_dataset, epochs=num_epochs, validation_data=(val_data, val_labels))

        """
        Prune the Model
        """
        final_sparsity = 0.7
        prune_wrapper = self.base_prune_helper(pencil_size=pencil_size, prune_scheduler=prune_scheduler)
        scheduler_args = self.base_scheduler_args(**{'initial_sparsity': 0.3, 
                                                     'final_sparsity': final_sparsity,
                                                     'end_step': num_epochs*len(train_dataset),
                                                     'begin_step': 2,
                                                     'prune_frequency': 2})

        layers_to_prune = [tf.keras.layers.Dense] # Layers we want to prune 

        # Add the `prune_low_magnitude()` Pruning Wrappers to the layers to be pruned
        model_to_prune = prune_wrapper(model=model,
                                      layers_to_prune=layers_to_prune,
                                      **scheduler_args)

        # Perform Training With Sparsity
        model_to_prune.compile(optimizer='adam',
                               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                               metrics=['accuracy'])
        model_to_prune.fit(train_dataset, epochs=num_epochs, validation_data=(val_data, val_labels), 
                           callbacks=[tfmot.sparsity.keras.UpdatePruningStep()])

        # Remove Pruned Wrappers and Inspect Sparse weights: 
        model_pruned_stripped = tfmot.sparsity.keras.strip_pruning(model_to_prune)

        for layer in model_pruned_stripped.trainable_weights:
            if 'bias' in layer.name:
                # We dont prune 'bias's' so skip checking
                continue

            if 'dense' not in layer.name:
                # layers_to_prune only had Dense Layer, skip check
                # for other layers
                continue

            """
            Sparsity Level Check - Only Dense Layers expected to have sparsity
            """
            layer_spu = layer.numpy().T # Default Shape: `IP_CHANNELS x OP_CHANNELS` (TF does x.W)
                                        # SPU Shape: `OP_CHANNELS x IP_CHANNELS` (SPU does W.x)
            sparsity_level = calculate_sparsity(layer_spu)
            eps = 0.08
            assert  sparsity_level - eps <= final_sparsity <= sparsity_level + eps
 
            """
            Pencil Pattern Checker. Assert Dense Layers induced 
            sparsity with expected pencil size.
            """
            pred_pencil_size = self.find_pencil_size_from_dense_arr(layer_spu, expected_pencil_size=pencil_size)
             # Make Requirement Easier
             # Generally, we should be asserting pred_pencil_size == pencil_size
             # But, there are cases when there are `always` 2 or more adjacent blocks of size `pencil_size` (unlikeley but does happen)  
            assert pred_pencil_size % pencil_size == 0