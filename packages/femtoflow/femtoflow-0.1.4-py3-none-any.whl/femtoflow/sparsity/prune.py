"""
Pruning Utilities, for Inducing Sparsity into Tensorflow Models 
"""
import tensorflow as tf
import tensorflow_model_optimization as tfmot
from typing import Union, List, Callable, Any, Tuple
from femtoflow.sparsity.pruning_schedulers.linear_scheduler import LinearPruningSchedule
from femtoflow.sparsity.pruning_schedulers.sine_scheduler import QuadrantSinePruningSchedule

# Setup Logging
import logging
logging.basicConfig(level=logging.INFO)


class PruneHelper:
    """
    Pruning related utilities for Tensorflow Models.
    """

    def __init__(self, 
                 pencil_size: int=4,
                 pencil_pooling_type: str='AVG',
                 prune_scheduler: str='polynomial_decay',
                 min_parameter_thresh: int=200
                 ) -> None:
        """This class adds Prune Wrappers (`tfmot.sparsity.keras.prune_low_magnitude`)
        to the layers specified in `layers_to_prune` to the tensorflow model `model`.

        We can perform Training, while inducing sparsity to `model-with-prune-wrappers()`
        by calling instances of `tfmot.sparsity.keras.UpdatePruningStep()` at specific points 
        in the training loop, to successfully induce sparsity.
        See: https://www.tensorflow.org/model_optimization/guide/pruning/comprehensive_guide.md

        We can also pass `tfmot.sparsity.keras.UpdatePruningStep()` to `model.fit()`
        as an additional callback() instead to induce sparsity (See Example Below).

        We can Prune model's with "Pencil Sparsity" to induce Sparsity Patterns 
        that can take advantage of Femtosense's Sparse Accelerator.        
        As an example, say we have a Dense Matrix of shape `(INPUT_CHANNEL, OUTPUT_CHANNEL)`
        we force sparse blocks to be in chucks of shape `(Pencil_Size, 1)`

        Note: 
            `Conv1D` and `Conv2D` layers only support `pencil_size=1`.
            However, pruning with `pencil_size=1` will not give performance boost
            when using Femtosense's SPU. 
            Hence, we say `pencil_size=1` is not supported, and raise an assertion above

            Other Layers (Dense, LSTM, RNN, etc.) support pruning with `pencil_size > 1`

        Example:
        
        .. code-block:: python

            # Define the PruneHelper Class
            prune_helper = PruneHelper(pencil_size=4,
                                        pencil_pooling_type='AVG',
                                        prune_scheduler='poly_decay',
                                        min_parameter_thresh=200)

            model = ... # The Tensorflow Model
            train_dataset = ...  # Optional - used to calculate end_step)
            num_epochs = ... # Optional - used to calculate end_step

            # Get the Model with `tfmot.sparsity.keras.prune_low_magnitude`
            # Wrappers Applied to Layers we want to prune.
            model_to_prune = prune_helper(model=model,
                                          layers_to_prune=[tf.keras.layers.Dense, 
                                                           tf.keras.layers.RNN],
                                          initial_sparsity=0.2,
                                          final_sparsity=0.6,
                                          begin_step=0,
                                          end_step=len(train_dataset) * num_epochs,
                                          prune_frequency=100,
                                          force_skip_layers=['dense_1/kernel:0', 'dense/kernel:0'])

            model_to_prune.compile(optimizer=optimizer, loss=loss_fn, metrics=metrics)
            model_to_prune.fit(train_dataset,
                               epochs=epochs, 
                               callbacks=[tfmot.sparsity.keras.UpdatePruningStep()])

            # Perform Sparse Evaluation
            model_to_prune.evaluate(...)
            
            # Remove Sparse Wrappers, and apply Prune Mask to obtain the Sparse Weights.
            model_pruned_stripped = tfmot.sparsity.keras.strip_pruning(model_to_prune)

            # Visualize Sparse Weights
            sparse_weights = model_pruned_stripped.trainable_weights
        
        Args:
            pencil_size (int): The Pencil Size 
                Default: 1
                The weight matrix is pruned in a pencil-sparse manner (along input dimension)
            pencil_pooling_type (str): Computes Pencil-Wise (or block-wise) L1-Norm Scores.
                All elements in the Pencil (or Block) with lowest L1-Norm Scores are set to 0 
                Options: ['AVG', 'MAX']
                Default: 'AVG'
            prune_scheduler (str): Pruning Scheduler (to set the prune level after every step)
                Options: ['poly_decay', 'constant', 'linear', 'sine']
            min_parameter_thresh (int): A Weight Matix Tensor will be pruned only if the 
                                        weight has more than `min_parameter_thresh` parameters. 
                                        Default: 200
        """
        assert pencil_size in (4, 8), f"Femtosense's SPU currently supports only Sparse Pencil Size of 4 or 8."
        self.pencil_size = pencil_size
        self.block_size  = (1, self.pencil_size) # We use Only Row-Major Blocks of Dim: (1, Pencil Size)
        self.pencil_pooling_type = pencil_pooling_type

        self.min_parameter_thresh = min_parameter_thresh

        self.prune_scheduler = prune_scheduler
        self.prune_scheduler_map = {'poly_decay': tfmot.sparsity.keras.PolynomialDecay,
                                    'constant': tfmot.sparsity.keras.ConstantSparsity,
                                    'linear': LinearPruningSchedule,
                                    'sine': QuadrantSinePruningSchedule}
        
        
    def _is_block_pruning_supported(self, layer: tf.keras.layers.Layer) -> bool:
        """Checks if Block Pruning (Pencil Sparsity) is supported for a given layer.
        Currently, Conv1D and Conv2D do not support Block Pruning (Pencil Sparsity)

        Args:
            layer (tf.keras.layers.Layer)
        
        Returns:
            (bool)
        """
        if layer in [tf.keras.layers.Conv1D, tf.keras.layers.Conv2D]:
            return False
        return True

    def _is_pruning_supported(self, layers_to_prune: List[tf.keras.layers.Layer]) -> bool:
        """
        Checks if Pruning with specified `self.pencil_size` is supported 
        for the layers passed to `self.layers_to_prune`.

        Args:
            layers_to_prune (List[tf.keras.layers.Layer])
            
        Returns:
            (bool)
        """
        bool_not_supported = any(not self._is_block_pruning_supported(layer=layer_type) for layer_type in layers_to_prune)
        return not bool_not_supported

    def _prune_selected_layers_fn(self, pruning_params: dict, 
                                        layers_to_prune: List[tf.keras.layers.Layer],
                                        force_skip_layers: List[str]=[]) -> Callable:
        """Returns a helper function  `_prune_layer` to make prune layers included 
        in `layers_to_prune` layers only.
        
        Args:
            pruning_params (dict)
            layers_to_prune (List[tf.keras.layers.Layer])
            force_skip_layers (List[str]) - Skips pruning layers included in `force_skip_layers`.
                                                User should include the `layer.trainable_weights[index].name` in this list
                                                if they explicitly want to skip pruning a given layer.
         Returns:
            _prune_layer (Callable)
        """
        def _prune_layer(layer: tf.keras.layers.Layer) -> tfmot.sparsity.keras.prune_low_magnitude:
            """
            Add `tfmot.sparsity.keras.prune_low_magnitude` wrapper to layers
            that are intended to be pruned.
            """
            prune_layer_bool = any(isinstance(layer, layer_type) for layer_type in layers_to_prune)
            if prune_layer_bool is False:
                return layer

            # Prune the Layer, only if the Number of Parameters of the Weight Matrix > `self.min_parameter_thresh`
            weight_thresh_bool = any(tf.size(weight) > self.min_parameter_thresh for weight in layer.trainable_weights)
            if weight_thresh_bool is False:
                return layer

            # Check if we want to forcibly skip pruning some layers
            force_skip_bool = any(weight.name in force_skip_layers for weight in layer.trainable_weights)
            if force_skip_bool is True:
                return layer

            return tfmot.sparsity.keras.prune_low_magnitude(layer, **pruning_params)
        return _prune_layer
    
    def _get_scheduler_params(self, begin_step: int, 
                                   end_step: int, 
                                   prune_frequency: int, 
                                   power: int, 
                                   initial_sparsity: float, 
                                   final_sparsity: float):
        """Get Scheduler Param's to be supplied to either `PolynomialDecay()`, `ConstantSparsity()`, 
        `LinearPruningSchedule()` or `QuadrantSinePruningSchedule()`, prune scheduler.

        Args:
            begin_step (int): Step at which to begin pruning.
            end_step (int): Step at which to end pruning.  
            prune_frequency (int): Only apply pruning every `prune_frequency` steps.
            power (int): Exponent to be used in the sparsity function.
                             Applicable only for `prune_scheduler == 'poly_decay'` 
            initial_sparsity (int): The Initial Sparsity Value to apply at `begin_step`
            final_sparsity (int): The Expected Final Sparsity Value at `end_step`

        Returns:
            (Dict): The Parameter Dictionary.
        """
        scheduler_params = {'begin_step': begin_step, 'end_step': end_step, 'frequency': prune_frequency}
        if self.prune_scheduler == 'poly_decay':
            scheduler_params.update({'power': power, 'initial_sparsity': initial_sparsity, 'final_sparsity': final_sparsity})
        elif  self.prune_scheduler == 'constant':
            scheduler_params.update({'target_sparsity': final_sparsity})
        elif self.prune_scheduler == 'linear' or self.prune_scheduler == 'sine':
            scheduler_params.update({'initial_sparsity': initial_sparsity, 'final_sparsity': final_sparsity})
        else:
            raise Exception(f"Unknown Prune Scheduler: {self.prune_scheduler}")
        return scheduler_params

    def _model_add_prune_wrappers(self, model: Union[tf.keras.Model, tf.keras.Sequential],
                                        layers_to_prune: List[tf.keras.layers.Layer],
                                        initial_sparsity: float,
                                        final_sparsity: float,
                                        begin_step: int,
                                        end_step: int,
                                        prune_frequency: int,
                                        power: int=3,
                                        force_skip_layers: List[str]=[],
                                        ) -> Union[tf.keras.Model, tf.keras.Sequential]:
        """Adds `tfmot.sparsity.keras.prune_low_magnitude()` Pruning Wrappers to 
        Layers of the Tensorflow Model specified in `self.layers_to_prune`.

        A layer wrapped with `tfmot.sparsity.keras.prune_low_magnitude()` can 
        be pruned via the `tfmot` library by calling instances of the 
        `tfmot.sparsity.keras.UpdatePruningStep()` callback appropriately in the 
        training loop 

        Args:
            model (Union[tf.keras.Model, tf.keras.Sequential]) - The Tensorflow model.
            layers_to_prune (List[tf.keras.layers.Layer]): List of Tensorflow Layers to Prune
                Example: [tf.keras.layers.Dense, tf.keras.layers.Conv1D]
            initial_sparsity (int): The Initial Sparsity Value to apply at `begin_step`
            final_sparsity (int): The Expected Final Sparsity Value at `end_step`
            begin_step (int): Step at which to begin pruning.
            end_step (int): Step at which to end pruning.  
            prune_frequency (int): Only apply pruning every `prune_frequency` steps.
            power (int): Exponent to be used in the sparsity function.
                             Applicable only for `prune_scheduler == 'poly_decay'` 
                             Default: 3
            force_skip_layers (List[str]) - Don't Prune layers whose names are included 
                                                in `force_skip_layers`
                                                Default: []

        Returns:
            (Union[tf.keras.Model, tf.keras.Sequential]):  
                model's prunable layers wrapped with `tfmot.sparsity.keras.prune_low_magnitude()`
        """
        assert self._is_pruning_supported(layers_to_prune) is True, f"For Pencil Size \
                            {self.pencil_size}, Conv1D/ Conv2D layers are Unsupported.\
                                                Supplied Layers: {layers_to_prune}"

        scheduler_params = self._get_scheduler_params(begin_step=begin_step, end_step=end_step, prune_frequency=prune_frequency, 
                                                      power=power, initial_sparsity=initial_sparsity, final_sparsity=final_sparsity)
        pruning_params = {
            'pruning_schedule': self.prune_scheduler_map[self.prune_scheduler](**scheduler_params),
            'block_size': self.block_size, 'block_pooling_type': self.pencil_pooling_type}
        model_to_prune = tf.keras.models.clone_model(model, clone_function=self._prune_selected_layers_fn(pruning_params, layers_to_prune, force_skip_layers))
        return model_to_prune

    def __call__(self, *args, **kwargs):
        """Wrapper Function of `PruneHelper._model_add_prune_wrappers()`
        """
        # Add tfmot.sparsity.keras.prune_low_magnitude() wrappers to the layers that will be pruned
        return self._model_add_prune_wrappers(*args, **kwargs)