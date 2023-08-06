# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""ms function for mixed precision."""
from __future__ import absolute_import

from abc import ABC, abstractmethod

from ._checkparam import Validator as validator
from .common import dtype as mstype
from . import context
from . import ops
from .common.api import ms_class
from .common.parameter import Parameter
from .common.tensor import Tensor
from .train.loss_scale_manager import DynamicLossScaleManager, LossScaleManager, FixedLossScaleManager
from .train.amp import build_train_network, auto_mixed_precision

_ascend_target = context.get_context("device_target") == "Ascend"
_gpu_target = context.get_context("device_target") == "GPU"

_gpu_float_status = ops.FloatStatus()

_npu_alloc_float_status = ops.NPUAllocFloatStatus()
_npu_clear_float_status = ops.NPUClearFloatStatus()
_npu_get_float_status = ops.NPUGetFloatStatus()

if _ascend_target:
    _status = _npu_alloc_float_status()
    _ = _npu_clear_float_status(_status)
else:
    _status = None

_hypermap = ops.HyperMap()
_partial = ops.Partial()


def _grad_unscale(scale, grad):
    return grad * ops.Reciprocal()(scale).astype(grad.dtype)


def _grad_scale(scale, grad):
    return grad * scale.astype(grad.dtype)


def _is_finite(inputs):
    if _gpu_target:
        return _gpu_float_status(inputs)[0] == 0
    status = ops.isfinite(inputs)
    return status.all()


def all_finite(inputs):
    r"""
    Returns a scalar Tensor indicating whether the inputs are finite.

    Note:
        This is an experimental interface that is subject to change or deletion.

        The interface must be used in whole network training scenario to detect
        whether grads are finite, and the results may be different on different
        device targets.

    Args:
        inputs (Union(tuple(Tensor), list(Tensor))): a iterable Tensor.

    Returns:
        Tensor, a scalar Tensor and the dtype is bool.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = (Tensor(np.array([np.log(-1), 1, np.log(0)])), Tensor(np.array([1.0]))
        >>> output = all_finite(x)
    """
    if _ascend_target:
        status = ops.depend(_status, inputs)
        get_status = _npu_get_float_status(status)
        status = ops.depend(status, get_status)
        status_finite = status.sum() == 0
        _ = _npu_clear_float_status(status)
        return status_finite
    outputs = _hypermap(_partial(_is_finite), inputs)
    return ops.stack(outputs).all()


@ms_class
class LossScaler(ABC):
    r"""
    Loss scaler abstract class when using mixed precision.

    Derived class needs to implement all of its methods. During training, `scale` and `unscale` is used
    to scale and unscale the loss value and gradients to avoid overflow, `adjust` is used to update the
    loss scale value.

    Note:
        This is an experimental interface that is subject to change or deletion.
    """
    @abstractmethod
    def scale(self, inputs):
        """
        Scaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.
        """
        raise NotImplementedError

    @abstractmethod
    def unscale(self, inputs):
        """
        Unscaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.
        """
        raise NotImplementedError

    @abstractmethod
    def adjust(self, grads_finite):
        """
        Adjust the `scale_value` dependent on whether grads are finite.

        Args:
            grads_finite (Tensor): a scalar bool Tensor indicating whether the grads are finite.
        """
        raise NotImplementedError


class StaticLossScaler(LossScaler):
    r"""
    Static Loss scale class.

    Scales and unscales loss or gradients by a fixed constant.

    Note:
        This is an experimental interface that is subject to change or deletion.

    Args:
        scale_value (Union(float, int)): The initial loss scale value.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> loss_scaler = amp.StaticLossScaler(scale_value=2**10)
        >>> loss_value = Tensor([1.], mindspore.float32)
        >>> scaled_loss_value = loss_scaler.scale(loss_value)
        >>> print(scaled_loss_value)
        [1024.]
        >>> grads = (Tensor(np.array([1.5, 1.0]), mindspore.float16),
        ...      Tensor(np.array([1.2]), mindspore.float16))
        >>> unscaled_grads = loss_scaler.unscale(grads)
        >>> print(unscaled_grads)
        (Tensor(shape=[2], dtype=Float16, value= [ 1.4648e-03,  9.7656e-04]),
        Tensor(shape=[1], dtype=Float16, value= [ 1.1721e-03]))
    """
    def __init__(self, scale_value):
        scale_value = validator.check_value_type("scale_value", scale_value, [float, int])
        if scale_value < 1.0:
            raise ValueError("The argument 'scale_value' must be > 1, but got {}".format(scale_value))
        self.scale_value = Parameter(Tensor(scale_value, dtype=mstype.float32), name="scale_value")

    def scale(self, inputs):
        """
        Scaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.

        Returns:
            Union(Tensor, tuple(Tensor)), the scaled value.
        """
        return _hypermap(_partial(_grad_scale, self.scale_value), inputs)

    def unscale(self, inputs):
        """
        Unscaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.

        Returns:
            Union(Tensor, tuple(Tensor)), the unscaled value.
        """
        return _hypermap(_partial(_grad_unscale, self.scale_value), inputs)

    def adjust(self, grads_finite):
        """
        `scale_value` is fixed.

        Args:
            grads_finite (Tensor): a scalar bool Tensor indicating whether the grads are finite.
        """
        return False


class DynamicLossScaler(LossScaler):
    r"""
    Dynamic Loss scale class.

    Dynamic loss scaling tries to determine the largest loss scale value that
    will keep gradients finite. It does this by increasing the loss scale every
    `scale_window` steps by `factor` if the grads remain finite, otherwise it reduces
    the loss scale by `1 / factor` and resets the counter.

    Note:
        This is an experimental interface that is subject to change or deletion.

    Args:
        scale_value (Union(float, int)): The initial loss scale value.
        scale_factor (int): The scale factor.
        scale_window (int): Maximum continuous training steps that do not have
            overflow to increase the loss scale.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> loss_scaler = amp.DynamicLossScaler(scale_value=2**10, scale_factor=2, scale_window=1)
        >>> grads = (Tensor(np.array([np.log(-1), 1.0]), mindspore.float16),
        ...             Tensor(np.array([0.2]), mindspore.float16))
        >>> unscaled_grads = loss_scaler.unscale(grads)
        >>> grads_finite = amp.all_finite(unscaled_grads)
        >>> loss_scaler.adjust(grads_finite)
        True
        >>> print(loss_scaler.scale_value.asnumpy())
        512.0
    """
    def __init__(self, scale_value, scale_factor, scale_window):
        scale_value = validator.check_value_type("scale_value", scale_value, [float, int])
        if scale_value < 1.0:
            raise ValueError("The argument 'scale_value' must be > 1, but got {}".format(scale_value))
        self.scale_value = Parameter(Tensor(scale_value, dtype=mstype.float32), name="scale_value")
        self.scale_window = validator.check_positive_int(scale_window, "scale_window")
        self.scale_factor = validator.check_positive_int(scale_factor, "scale_factor")
        self.counter = Parameter(Tensor(0, dtype=mstype.int32), name="counter")

    def scale(self, inputs):
        """
        Scaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.

        Returns:
            Union(Tensor, tuple(Tensor)), the scaled value.
        """
        return _hypermap(_partial(_grad_scale, self.scale_value), inputs)

    def unscale(self, inputs):
        """
        Unscaling inputs by `scale_value`.

        Args:
            inputs (Union(Tensor, tuple(Tensor))): the input loss value or gradients.

        Returns:
            Union(Tensor, tuple(Tensor)), the unscaled value.
        """
        return _hypermap(_partial(_grad_unscale, self.scale_value), inputs)

    def adjust(self, grads_finite):
        """
        Adjust the `scale_value` dependent on whether grads are finite.

        Args:
            grads_finite (Tensor): a scalar bool Tensor indicating whether the grads are finite.
        """
        one = ops.ones((), self.scale_value.dtype)
        scale_mul_factor = self.scale_value * self.scale_factor
        scale_value = ops.select(
            grads_finite,
            ops.select(
                self.counter == (self.scale_window - 1),
                ops.select(_is_finite(scale_mul_factor),
                           scale_mul_factor,
                           self.scale_value),
                self.scale_value),
            ops.maximum(one, self.scale_value / self.scale_factor))
        ops.assign(self.scale_value, scale_value)

        counter = ((self.counter + 1) % self.scale_window) * grads_finite
        ops.assign(self.counter, counter)
        return True

__all__ = [
    "DynamicLossScaleManager", "LossScaleManager", "FixedLossScaleManager",
    "build_train_network", "DynamicLossScaler", "StaticLossScaler", "LossScaler",
    "auto_mixed_precision", "all_finite"
]
