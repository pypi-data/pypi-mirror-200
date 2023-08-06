# Copyright 2020-2022 Huawei Technologies Co., Ltd
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

"""image_ops"""
from mindspore import context
from mindspore._checkparam import Validator as validator
from mindspore._checkparam import Rel
from mindspore.ops.primitive import prim_attr_register, Primitive
from mindspore.common import dtype as mstype


class AdjustSaturation(Primitive):
    """
    Adjust saturation of RGB images.

    Note:
        This is a convenience method that converts RGB images to float representation, converts them to HSV,
        adds an offset to the saturation channel, converts back to RGB and then back to the original data type.
        If several adjustments are chained it is advisable to minimize the number of redundant conversions.

    inputs:
        - **image** (Tensor): Images to adjust. Must be one of the following types: float16, float32.
           At least 3-D.The last dimension is interpreted as channels, and must be three.
        - **scale** (Tensor): A float scale to add to the saturation. A Tensor of type float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `image`.

    Raises:
        TypeError: If any iput is not Tensor.
        TypeError: If the type of `image` is not one of the following dtype: float16, float32.
        TypeError: If the type of `scale` is not float32.
        ValueError: If the dimension of the 'image' is less than 3, or the last dimension of the 'image' is not 3.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
      >>> x = Tensor([[[1.0, 2.0, 3.0],
      ...       [4.0, 5.0, 6.0]],
      ...     [[7.0, 8.0, 9.0],
      ...       [10.0, 11.0, 12.0]]])
      >>> scale = Tensor(float(0.5))
      >>> adjustsaturation = AdjustSaturation()
      >>> output = adjustsaturation(x, scale)
      >>> print(output)
             [[[ 2.         2.4999998  3.       ]
          [ 5.         5.5        6.       ]]
         [[ 8.         8.5        9.       ]
          [11.        11.5       12.       ]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustSaturation"""
        self.init_prim_io_names(inputs=['images', 'scale'], outputs=['y'])


class AdjustContrastv2(Primitive):
    """
    Adjust contrastv2 of images.

    Note:
        images is a tensor of at least 3 dimensions.
        The last 3 dimensions are interpreted as [height, width, channels].
        The other dimensions only represent a collection of images, such as [batch, height, width, channels].
        Contrast is adjusted independently for each channel of each image.

    inputs:
        -**images**(tensor): Images to adjust. Must be one of the following types: float16, float32.
          At least 3-D.The last dimension is interpreted as channels, and must be three.
        -**contrast_factor**(tensor): A float multiplier for adjusting contrast. A Tensor of type float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `images`.

    Raises:
        TypeError: If any input is not Tensor.
        TypeError: If the type of `images` is not one of the following dtype: float16, float32.
        TypeError: If the type of `contrast_factor` is not float32.
        ValueError: If the dimension of the 'images' is less than 3, or the last dimension of the 'images' is not 3.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
    >>> images = Tensor([[[1.0, 2.0, 3.0],
    ...       [4.0, 5.0, 6.0]],
    ...     [[7.0, 8.0, 9.0],
    ...       [10.0, 11.0, 12.0]]], mstype.float32)
    >>> contrast_factor = Tensor(2., mstype.float32)
    >>> adjustcontrastv2 = AdjustContrastv2()
    >>> output = adjustcontrastv2(images, contrast_factor)
    >>> print(output)
    [[[-3.5 -2.5 -1.5]
      [ 2.5  3.5  4.5]]
    <BLANKLINE>
     [[ 8.5  9.5 10.5]
      [14.5 15.5 16.5]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustContrastv2"""
        self.init_prim_io_names(inputs=['images', 'contrast_factor'], outputs=['y'])


class AdjustHue(Primitive):
    """
    Adjust hue of RGB images.

    Note:
        A convenience method that transform an RGB image to float representation.
        The image is adjusted by transforming the image to HSV and shifting the intensities in the hue channel,
        then transform back to original data mode.
        It is recommended to minimize the number of redundant transformations when several adjustments are chained.

    Inputs:
        - **image** (Tensor): RGB image or images. The size of the last dimension must be 3.
          the dtype is float16 or float32.  At least 3-D.
        - **delta** (Tensor): How much to add to the hue channel, the dtype is float32. Must be 0-D.

    Output:
        Adjusted image(s), same shape and dtype as `image`.

    Raises:
        TypeError: If neither `image` nor `delta` is a tensor.
        TypeError: If the dtype of image not float16 or float32.
        TypeError: If the dtype of delta not float32.
        ValueError: If image have at less than 3 dimensions.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
         >>> class AdjustHue(nn.Cell):
         ...   def __init__(self):
         ...     super(AdjustHue, self).__init__()
         ...     self.adjustHue = P.AdjustHue()
         ...   def construct(self, image, delta):
         ...     return self.adjustHue(image, delta)
         ...
         >>> image = np.array([[[1, 2, 3], [4, 5, 6]],
         ...                   [[7, 8, 9], [10, 11, 12]],
         ...                   [[13, 14, 15], [16, 17, 18]]]).astype(np.float32)
         >>> delta = 0.2
         >>> adjust_hue = AdjustHue()
         >>> output = adjust_hue(Tensor(image), Tensor(delta))
         >>> print("output", output)
         output [[[ 2.3999996  1.         3.       ]
                  [ 5.3999996  4.         6.       ]]
                 [[ 8.4        7.         9.       ]
                  [11.4       10.        12.       ]]
                 [[14.4       13.        15.       ]
                  [17.4       16.        18.       ]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize AdjustHue"""
        self.init_prim_io_names(inputs=['images', 'delta'], outputs=['y'])


class ExtractGlimpse(Primitive):
    """
    Extracts glimpse from the input image tensor and return a window.

    Note:
        If the window and input image tensor not overlap, random noise is filled.

    Args:
        centered (bool): An optional `bool`. Defaults to `True`. Indicates if the offset coordinates
            are centered relative to the image, in which case the (0, 0) offset is relative to the center of
            the center of the input images. If false, the (0, 0) offset corresponds to the upper left corner
            of the input images.
        normalized (bool): An optional `bool`. Defaults to `True`. indicates if the offset
            coordinates are normalized.
        uniform_noise (bool): An optional `bool`. Defaults to `True`. indicates if the noise should be
            generated using a uniform distribution or a Gaussian distribution.
        noise (str): An optional string that defaults to `uniform`. The value can be 'uniform', 'gaussian'
            and 'zero'. The window is determined by size and offsets.
            When the window and input image tensor not overlap, random noise is filled.
            The result is variable when noise is equal to 'uniform' and 'gaussian'.
            When noise is equal to 'zero', the value of uniform_noise must be 'False' and the
            filling noise will be zero so that the result is fixed.
            When uniform_noise is 'True', the value of noise only can be 'uniform'.
            When uniform_noise is 'False', the value of noise can be 'uniform', 'gaussian' and 'zero'.

    Inputs:
        - **x** (Tensor) - A 4-D float tensor of shape [batch_size, height, width, channels].
          Types allowed: float32.
        - **size** (Tensor) - A 1-D tensor of 2 elements containing the size of the glimpses to extract.
          The glimpse height must be specified first, following by the glimpse width. Types allowed: int32.
          The value of size must be greater than zero.
        - **offsets** (Tensor) - A 2-D integer tensor of shape [batch_size, 2] containing the y, x locations
          of the center of each window. Types allowed: float32.

    Outputs:
        A 4-D tensor of shape [batch_size, glimpse_height, glimpse_width, channels] with type: float32.

    Raises:
        TypeError: If `centered` is not a bool.
        TypeError: If `normalize` is not a bool.
        TypeError: If `uniform_noise` is not a bool.
        ValueError: If `noise` is not `uniform`, `gaussian` or `zero`.
        ValueError: If the value of `size` is not constant value.
        ValueError: If the batch_size of input is inconsistent with the batch_size of offsets.
        ValueError: If the value of offsets[1] is not 2.
        ValueError: If the input is not Tensor.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> class ExtractGlimpse(nn.Cell):
        ...         def __init__(self, size, centered, normalized, uniform_noise, noise):
        ...             super(ExtractGlimpse, self).__init__()
        ...             self.size = size
        ...             self.attribute = P.ExtractGlimpse(centered = centered, normalized = normalized,
        ...             uniform_noise = uniform_noise, noise = noise)
        ...         def construct(self, x, offsets):
        ...             return self.attribute(x, self.size, offsets);
        >>> x = Tensor(np.random.randn(1, 4, 2, 3).astype(np.float32))
        >>> size = Tensor(np.array([2, 2]).astype("int32"))
        >>> offsets = Tensor(np.array([[0, 0]]).astype("float32"))
        >>> attribute = ExtractGlimpse(size, True, True, True, "uniform")
        >>> output = attribute(x, offsets)
        >>> print(output)
        [[[[ 0.95008844 -0.1513572  -0.10321885]
           [ 0.41059852  0.14404356  1.4542735 ]]

          [[ 0.7610377   0.12167501  0.44386324]
           [ 0.33367434  1.4940791  -0.20515826]]]]
    """
    @prim_attr_register
    def __init__(self, centered=True, normalized=True, uniform_noise=True, noise="uniform"):
        self.add_prim_attr("max_length", 1000000)
        self.init_prim_io_names(inputs=['x', 'size', 'offsets'], outputs=['output'])
        self.centered = centered
        self.normalized = normalized
        self.uniform_noise = uniform_noise
        self.noise = noise
        self.add_prim_attr('centered', self.centered)
        self.add_prim_attr('normalized', self.normalized)
        self.add_prim_attr('noise', self.noise)
        self.add_prim_attr('uniform_noise', self.uniform_noise)
        validator.check_value_type("centered", centered, [bool], self.name)
        validator.check_value_type("normalized", normalized, [bool], self.name)
        validator.check_value_type("noise", noise, [str], self.name)
        validator.check_string(noise, ["uniform", "gaussian", "zero"], "noise", self.name)
        validator.check_value_type("uniform_noise", uniform_noise, [bool], self.name)
        if uniform_noise and noise != "uniform":
            raise ValueError(f"For '{self.name}', the value of 'noise' must be uniform "
                             f"when uniform_noise is True, but got {noise}.")


class CropAndResize(Primitive):
    """
    Extracts crops from the input image tensor and resizes them.

    Note:
        In case that the output shape depends on crop_size, the crop_size must be constant.
        For now, the backward of the operator only support bilinear method, for other methods, will return 0.

    Args:
        method (str, optional): An optional string that specifies the sampling method for resizing.
            It can be "bilinear", "nearest" or "bilinear_v2". The option "bilinear" stands for standard bilinear
            interpolation algorithm, while "bilinear_v2" may result in better result in some cases. Default: "bilinear"
        extrapolation_value (float, optional): An optional float value used extrapolation, if applicable. Default: 0.0.

    Inputs:
        - **x** (Tensor) - The input image must be a 4-D tensor of shape [batch, image_height, image_width, depth].
          Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
        - **boxes** (Tensor) - A 2-D tensor of shape [num_boxes, 4].
          The i-th row of the tensor specifies the coordinates of a box in the box_ind[i] image
          and is specified in normalized coordinates [y1, x1, y2, x2]. A normalized coordinate value of y is mapped to
          the image coordinate at y * (image_height - 1), so as the [0, 1] interval of normalized image height is
          mapped to [0, image_height - 1] in image height coordinates. We do allow y1 > y2, in which case the sampled
          crop is an up-down flipped version of the original image. The width dimension is treated similarly.
          Normalized coordinates outside the [0, 1] range are allowed, in which case we use extrapolation_value to
          extrapolate the input image values. Types allowed: float32.
        - **box_index** (Tensor) - A 1-D tensor of shape [num_boxes] with int32 values in [0, batch).
          The value of box_ind[i] specifies the image that the i-th box refers to. Types allowed: int32.
        - **crop_size** (Tuple[int]) - A tuple of two int32 elements: (crop_height, crop_width).
          Only constant value is allowed. All cropped image patches are resized to this size.
          The aspect ratio of the image content is not preserved. Both crop_height and crop_width need to be positive.
    Outputs:
        A 4-D tensor of shape [num_boxes, crop_height, crop_width, depth] with type: float32.

    Raises:
        TypeError: If `method` is not a str.
        TypeError: If `extrapolation_value` is not a float.
        ValueError: If `method` is not one of 'bilinear', 'nearest', 'bilinear_v2'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> class CropAndResizeNet(nn.Cell):
        ...     def __init__(self, crop_size):
        ...         super(CropAndResizeNet, self).__init__()
        ...         self.crop_and_resize = ops.CropAndResize()
        ...         self.crop_size = crop_size
        ...
        ...     def construct(self, x, boxes, box_index):
        ...         return self.crop_and_resize(x, boxes, box_index, self.crop_size)
        ...
        >>> BATCH_SIZE = 1
        >>> NUM_BOXES = 5
        >>> IMAGE_HEIGHT = 256
        >>> IMAGE_WIDTH = 256
        >>> CHANNELS = 3
        >>> image = np.random.normal(size=[BATCH_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS]).astype(np.float32)
        >>> boxes = np.random.uniform(size=[NUM_BOXES, 4]).astype(np.float32)
        >>> box_index = np.random.uniform(size=[NUM_BOXES], low=0, high=BATCH_SIZE).astype(np.int32)
        >>> crop_size = (24, 24)
        >>> crop_and_resize = CropAndResizeNet(crop_size=crop_size)
        >>> output = crop_and_resize(Tensor(image), Tensor(boxes), Tensor(box_index))
        >>> print(output.shape)
        (5, 24, 24, 3)
    """

    @prim_attr_register
    def __init__(self, method="bilinear", extrapolation_value=0.0):
        """Initialize CropAndResize"""
        self.init_prim_io_names(inputs=['x', 'boxes', 'box_index', 'crop_size'], outputs=['y'])
        validator.check_value_type("method", method, [str], self.name)
        validator.check_string(method, ["bilinear", "nearest", "bilinear_v2"], "method", self.name)
        self.method = method
        validator.check_value_type("extrapolation_value", extrapolation_value, [float], self.name)
        self.extrapolation_value = extrapolation_value
        self.is_ge = context.get_context("enable_ge")


class NonMaxSuppressionV3(Primitive):
    r"""
        Greedily selects a subset of bounding boxes in descending order of score.

    .. warning::
        When input "max_output_size" is negative, it will be treated as 0.

    Note:
        This algorithm is agnostic to where the origin is in the coordinate system.
        This algorithm is invariant to orthogonal transformations and translations of the coordinate system;
        thus translating or reflections of the coordinate system result in the same boxes being
        selected by the algorithm.

    Inputs:
        - **boxes** (Tensor) - A 2-D Tensor of shape [num_boxes, 4].
        - **scores** (Tensor) - A 1-D Tensor of shape [num_boxes] representing a single score
          corresponding to each box (each row of boxes), the num_boxes of "scores" must be equal to
          the num_boxes of "boxes".
        - **max_output_size** (Union[Tensor, Number.Int]) - A scalar integer Tensor representing the maximum
          number of boxes to be selected by non max suppression.
        - **iou_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding whether boxes overlap too much with respect to IOU, and iou_threshold must be equal or greater
          than 0 and be equal or smaller than 1.
        - **score_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding when to remove boxes based on score.

    Outputs:
        A 1-D integer Tensor of shape [M] representing the selected indices from the boxes tensor,
        where M <= max_output_size.

    Raises:
        TypeError: If the dtype of `boxes` and `scores` is different.
        TypeError: If the dtype of `iou_threshold` and `score_threshold` is different.
        TypeError: If `boxes` is not tensor or its dtype is not float16 or float32.
        TypeEroor: If `scores` is not tensor or its dtype is not float16 or float32.
        TypeError: If `max_output_size` is not tensor or scalar.If `max_output_size` is not int32 or int64.
        TypeError: If `iou_threshold` is not tensor or scalar. If its type is not float16 or float32.
        TypeError: If `score_threshold` is not tensor or scalar. If its type is not float16 or float32.
        ValueError: If the size of shape of `boxes` is not 2 or the second value of its shape is not 4.
        ValueError: If the size of shape of `scores` is not 1.
        ValueError: If each of the size of shape of `max_output_size`, `iou_threshold`, `score_threshold` is not 0.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> boxes = Tensor(np.array([[1, 2, 3, 4], [1, 3, 3, 4], [1, 3, 4, 4],
        ...                          [1, 1, 4, 4], [1, 1, 3, 4]]), mstype.float32)
        >>> scores = Tensor(np.array([0.4, 0.5, 0.72, 0.9, 0.45]), mstype.float32)
        >>> max_output_size = Tensor(5, mstype.int32)
        >>> iou_threshold = Tensor(0.5, mstype.float32)
        >>> score_threshold = Tensor(0, mstype.float32)
        >>> nonmaxsuppression = ops.NonMaxSuppressionV3()
        >>> output = nonmaxsuppression(boxes, scores, max_output_size, iou_threshold, score_threshold)
        >>> print(output)
        [3 2 0]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize NonMaxSuppressionV3"""


class NonMaxSuppressionWithOverlaps(Primitive):
    """
    Greedily selects a subset of bounding boxes in descending order of score.

    Note:
        This algorithm is agnostic to where the origin is in the coordinate system.
        This algorithm is invariant to orthogonal transformations and translations of the coordinate system;
        thus translating or reflections of the coordinate system result in the same boxes being
        selected by the algorithm.

    Inputs:
        - **overlaps** (Tensor) - A 2-D Tensor of shape [num_boxes, num_boxes].
          Types allowed:float32.
        - **scores** (Tensor) - A 1-D Tensor of shape [num_boxes] representing a single score
          corresponding to each box (each row of boxes),the num_boxes of "scores" must be equal to
          the num_boxes of "overlaps".
          Types allowed:float32.
        - **max_output_size** (Union[Tensor, Number.Int]) - A scalar integer Tensor representing the maximum
          number of boxes to be selected by non max suppression, and max_output_size must be equal to or greater
          than 0.
          Types allowed:int32.
        - **overlap_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding whether boxes overlap too much.
          Types allowed:float32.
        - **score_threshold** (Union[Tensor, Number.Float]) - A 0-D float tensor representing the threshold for
          deciding when to remove boxes based on score.
          Types allowed:float32.

    Outputs:
        An int32 tensor. A 1-D integer Tensor of shape [M] representing the selected indices from the boxes tensor,
        where M <= max_output_size.

    Raises:
        TypeError: If the dtype of `overlaps` and `scores` is not float32.
        TypeError: If the dtype of `overlap_threshold` and `score_threshold` is not float32.
        TypeError: If `overlaps` is not tensor or its dtype is not float32.
        TypeError: If `scores` is not tensor or its dtype is not float32.
        TypeError: If `max_output_size` is not tensor or scalar.If `max_output_size` is not int32.
        TypeError: If `overlap_threshold` is not tensor or scalar. If its type is not float32.
        TypeError: If `score_threshold` is not tensor or scalar. If its type is not float32.
        ValueError: If the size of shape of `overlaps` is not 2 or the second value of its shape
                    is not equal to the first value of its shape.
        ValueError: If the size of shape of `scores` is not 1.
        ValueError: If each of the size of shape of `max_output_size`, `overlap_threshold`, `score_threshold` is not 0.
        ValueError: If `max_output_size` is negative.
        ValueError: If the shape of `scores` is not equal to the shape of the dim0 or dim1 of `overlaps`.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU

    Examples:
        >>> overlaps = Tensor(np.array([[0.6964692, 0.28613934, 0.22685145, 0.5513148],
                                [0.71946895, 0.42310646, 0.9807642, 0.6848297],
                                [0.4809319, 0.39211753, 0.343178, 0.7290497],
                                [0.43857226, 0.059677895, 0.39804426, 0.7379954]
                                ]), mstype.float32)
        >>> scores = Tensor(np.array([0.18249173, 0.17545176, 0.53155136, 0.53182757]), mstype.float32)
        >>> max_output_size = Tensor(4, mstype.int32)
        >>> overlap_threshold = Tensor(0.1, mstype.float32)
        >>> score_threshold = Tensor(0.2, mstype.float32)
        >>> nonmaxsuppression = ops.NonMaxSuppressionWithOverlaps()
        >>> output = nonmaxsuppression(overlaps, scores, max_output_size, overlap_threshold, score_threshold)
        >>> print(output)
        [3]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize NonMaxSuppressionWithOverlaps"""
        self.init_prim_io_names(inputs=['overlaps', 'scores', 'max_output_size',
                                        'overlap_threshold', 'score_threshold'], outputs=['selected_indices'])


class HSVToRGB(Primitive):
    """
    Convert one or more images from HSV to RGB. The format of the image(s) should be NHWC.

    Inputs:
        - **x** (Tensor) - The input image must be a 4-D tensor of shape [batch, image_height, image_width, channel].
          Number of channel must be 3.
          Types allowed: float16, float32, float64.
    Outputs:
        A 4-D tensor of shape [batch, image_height, image_width, channel] with same type of input.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If the dtype of `x` is not float16, float32, float64.
        ValueError: If rank of the `x` is not equal to 4.
        ValueError: If the last dimension of `x` is not equal to 3.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> image = np.array([0.5, 0.5, 0.5]).astype(np.float32).reshape([1, 1, 1, 3])
        >>> hsv_to_rgb = P.HSVToRGB()
        >>> output = hsv_to_rgb(Tensor(image))
        >>> print(output)
        [[[[0.25 0.5  0.5 ]]]]
    """
    @prim_attr_register
    def __init__(self):
        pass


class CropAndResizeGradBoxes(Primitive):
    """
    Computes the gradient of the CropAndResize op with respect to the input boxes tensor.

    Note:
        Input images and grads must be a 4-D tensor.

    Args:
        method (str): A string specifying the interpolation method. Only "bilinear" is supported for now.
            Default: "bilinear".

    Inputs:
        - **grads** (Tensor) - A 4-D tensor of shape [num_boxes, crop_height, crop_width, depth].
          The format must be NHWC. Types allowed: float32, float64.
        - **images** (Tensor) - A 4-D tensor of shape [batch, image_height, image_width, depth].
          The format must be NHWC. Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
          Both image_height and image_width need to be positive.
        - **boxes** (Tensor) - A 2-D tensor of shape [num_boxes, 4].
          The i-th row of the tensor specifies the coordinates of a box in the box_index[i] image
          and is specified in normalized coordinates [y1, x1, y2, x2]. A normalized coordinate value of y is mapped to
          the image coordinate at y * (image_height - 1), so as the [0, 1] interval of normalized image height is
          mapped to [0, image_height - 1] in image height coordinates. We do allow y1 > y2, in which case the sampled
          crop is an up-down flipped version of the original image. The width dimension is treated similarly.
          Normalized coordinates outside the [0, 1] range are allowed, in which case we use extrapolation_value to
          extrapolate the input image values. Types allowed: float32, float64.
        - **box_index** (Tensor) - A 1-D tensor of shape [num_boxes] with int32 values in [0, batch).
          The value of box_index[i] specifies the image that the i-th box refers to. Types allowed: int32.

    Outputs:
        A 2-D tensor of shape [num_boxes, 4] with type: float32 or float64.

    Raises:
        TypeError: If `method` is not a str.
        TypeError: If `grads` is not tensor or its dtype is not float32 or float64.
        TypeError: If `images` is not tensor or its dtype is incorrect.
        TypeError: If `boxes` is not tensor or its dtype is not float32 or float64.
        TypeError: If `box_index` is not tensor or its dtype is not int32.
        ValueError: If `method` is not 'bilinear'.
        ValueError: If the size of `grads` tensor shape is not equal to 4.
        ValueError: If the size of `images` tensor shape is not equal to 4.
        ValueError: If the value of image_height or image_width of `image` tensor shape is not positive.
        ValueError: If the size of `boxes` tensor shape is not equal to 2.
        ValueError: If the length of the second dimension of `boxes` is not equal to 4.
        ValueError: If the size of `box_index` tensor shape is not equal to 1.
        ValueError: If the length of `box_index` is not equal to num_boxes.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> crop_and_resize_grad_boxes = ops.CropAndResizeGradBoxes(method = "bilinear")
        >>> grads = Tensor(np.array([[[[2.0], [5.0]], [[1.0], [4.0]]]]), mindspore.float32)
        >>> image = Tensor(np.array([[[[9.0], [5.0], [2.0], [1.0]],
        ...                           [[6.0], [1.0], [9.0], [7.0]],
        ...                           [[6.0], [0.0], [2.0], [9.0]],
        ...                           [[1.0], [2.0], [6.0], [7.0]]]]), mindspore.float32)
        >>> boxes = Tensor(np.array([[0.3, 0.8, 0.3, 0.8]]), mindspore.float32)
        >>> box_index = Tensor(np.array([0]), mindspore.int32)
        >>> output = crop_and_resize_grad_boxes(grads, image, boxes, box_index)
        >>> print(output.asnumpy())
        [138.6,-17.1,99.0,-51.300003]
    """

    @prim_attr_register
    def __init__(self, method="bilinear"):
        """Initialize CropAndResizeGradBoxes"""
        self.init_prim_io_names(inputs=['grads', 'images', 'boxes', 'box_index'], outputs=['y'])
        validator.check_value_type("method", method, [str], self.name)
        validator.check_string(method, ["bilinear"], "method", self.name)
        self.method = method


class RGBToHSV(Primitive):
    """
    Convert one or more images from RGB to HSV.
    Outputs a tensor of the same shape as the images tensor, containing the HSV value of the pixels.
    The output is only well defined if the value in images are in [0,1].

    Note:
        Last dimension of input images must be size 3.

    Inputs:
        **images** (Tensor) - Must be one of the following types: float16, float32, float64. 1-D or higher rank.
        RGB data to convert. Last dimension must be size 3.

    Outputs:
        A Tensor, has the same type and shape as input `images`.

    Raises:
        TypeError: If `images` is not tensor or its dtype is not float or double.
        ValueError: If the size of shape of `images` is less than 1.
        ValueError: If the last value of shape of `images` is not 3.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> images =  np.array([0.25, 0.5, 0.5]).astype(np.float32).reshape([1, 1, 1, 3])
        >>> rgb_to_hsv = ops.RGBToHSV()
        >>> output = rgb_to_hsv(Tensor(images))
        >>> print(output)
        [[[[0.5, 0.5, 0.5]]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize RGBToHSV"""
        self.init_prim_io_names(inputs=['images'], outputs=['y'])


class ResizeLinear1D(Primitive):
    r"""
    Using the linear interpolate method resize the input tensor 'x'.

    For general resize, refer to :func:`mindspore.ops.interpolate` for more detail.

    .. warning::
        This is an experimental feature and is subjected to change.

    Args:
        coordinate_transformation_mode (string): Default is 'align_corners'. Describes how to transform the coordinate
            in the resized tensor to the coordinate in the original tensor. Other optional: 'half_pixel', 'asymmetric'.

    Inputs:
        - **x** (Tensor) - A 3-D tensor which to resize, with shape [batch, channel, width]. Must be one of the
          following types: uint8, int8, int16, int32, int64, float16, float32, double.
        - **size** (Tensor) - A 1-D int64 Tensor, describes the size of the output tensor.

    Outputs:
        A 3-D tensor which shape is [batch, channel, new_width] with the same type as `x`.

    Raises:
        TypeError: If dtype of `x` is not in the support list.
        TypeError: If `size` is not a 1-D int64_t tensor.
        TypeError: If `coordinate_transformation_mode` is not a string.
        TypeError: If `coordinate_transformation_mode` is not in the support list.

    Supported Platforms:
        ``CPU`` ``GPU``

    Examples:
        >>> input = Tensor([[[1, 2, 3], [4, 5, 6]]], mindspore.float32)
        >>> size = Tensor([6], mindspore.int32)
        >>> resize_linear_1d = ops.ResizeLinear1D(coordinate_transformation_mode="align_corners")
        >>> output = resize_linear_1d(x=input, size=size)
        >>> print(output)
        [[[1. 1.4 1.8 2.2 2.6 3.]
          [4. 4.4 4.8 5.2 5.6 6.]]]
    """

    @prim_attr_register
    def __init__(self, coordinate_transformation_mode="align_corners"):
        """Initialize ResizeLinear1D."""
        self.init_prim_io_names(inputs=["x", "sizes"], outputs=["output"])
        validator.check_value_type(
            "coordinate_transformation_mode", coordinate_transformation_mode, [str], self.name)
        validator.check_string(coordinate_transformation_mode, ["align_corners", "half_pixel", "asymmetric"],
                               "coordinate_transformation_mode", self.name)


class ResizeBilinearV2(Primitive):
    r"""
    Resizes an image to a certain size using the bilinear interpolation.

    The resizing only affects the lower two dimensions which represent the height and width.

    Args:
        align_corners (bool): If true, rescale input by :math:`(new\_height - 1) / (height - 1)`,
                       which exactly aligns the 4 corners of images and resized images. If false,
                       rescale by :math:`new\_height / height`. Default: False.
        half_pixel_centers (bool): Whether half pixel center. If set to True, `align_corners` should be False.
                           Default: False.

    Inputs:
        - **x** (Tensor): Image to be resized. Input images must be a 4-D tensor with shape
          :math:`(batch, channels, height, width)`, with data type of float32 or float16.
        - **size** (Union[tuple[int], list[int], Tensor]): The new size of the images.
          A tuple or list or Tensor of 2 int elements :math:`(new\_height, new\_width)`.

    Outputs:
        Tensor, resized image. 4-D with shape :math:`(batch, channels, new\_height, new\_width)`,
        with the same data type as input `x`.

    Raises:
        TypeError: If `align_corners` is not a bool.
        TypeError: If `half_pixel_centers` is not a bool.
        TypeError: If `align_corners` and `half_pixel_centers` are all True.
        ValueError: If `half_pixel_centers` is True and device_target is CPU.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> x = Tensor([[[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]], mindspore.float32)
        >>> output = ResizeBilinearV2(x, (5, 5))
        >>> print(output)
        [[[[1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]]]]
    """

    @prim_attr_register
    def __init__(self, align_corners=False, half_pixel_centers=False):
        """Initialize ResizeBilinear."""
        super().__init__(name="ResizeBilinearV2")
        self.init_prim_io_names(inputs=['x', 'size'], outputs=['y'])
        self.align_corners = validator.check_value_type("align_corners", align_corners, [bool], self.name)
        self.half_pixel_centers = validator.check_value_type("half_pixel_centers",
                                                             half_pixel_centers, [bool], self.name)
        if half_pixel_centers and align_corners:
            raise ValueError(f"If half_pixel_centers is True, align_corners must be False, but got {align_corners}")
        target = context.get_context("device_target")
        if half_pixel_centers and target == "CPU":
            raise ValueError(f"Currently `half_pixel_centers`=True is not supported in CPU device_target")


class ResizeBicubic(Primitive):
    """
    Resize images to size using bicubic interpolation.

    .. warning::
        The max output length is 1000000.

    Args:
        align_corners (bool):If true, the centers of the 4 corner pixels of the input
            and output tensors are aligned, preserving the values at the corner pixels.Default: False.
        half_pixel_centers (bool): An optional bool. Default: False.

    Inputs:
        - **images** (Tensor) - The input image must be a 4-D tensor of shape [batch, height, width, channels].
          The format must be NHWC.
          Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
        - **size** (Tensor) - A 1-D tensor of shape [2], with 2 elements: new_height, new_width.
          Types allowed: int32.
    Outputs:
        A 4-D tensor of shape [batch, new_height, new_width, channels] with type: float32.

    Raises:
        TypeError: If `images` type is not allowed.
        TypeError: If `size` type is not allowed.
        TypeError: If `align_corners` type is not allowed.
        TypeError: If `half_pixel_centers` type is not allowed.
        ValueError: If `images` dim is not 4.
        ValueError: If `size` dim is not 1.
        ValueError: If `size` size is not 2.
        ValueError: If `size` value is not positive.
        ValueError: If `align_corners` and `half_pixel_centers` value are both true.


    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> class NetResizeBicubic(nn.Cell):
        ...     def __init__(self):
        ...         super(NetResizeBicubic, self).__init__()
        ...         align_corners = False
        ...         half_pixel_centers = False
        ...         self.resize = P.ResizeBicubic(align_corners, half_pixel_centers)
        ...
        ...     def construct(self, images, size):
        ...         return self.resize(images, size)
        ...
        >>> images = Tensor(np.array([1, 2, 3, 4]).reshape(1, 2, 2, 1).astype(np.float32))
        >>> size = Tensor([1, 4], mindspore.int32)
        >>> resizebicubic = NetResizeBicubic()
        >>> output = resizebicubic(images, size)
        >>> print(output)
            [[[[1.     ]
            [1.5    ]
            [2.     ]
            [2.09375]]]]
    """

    @prim_attr_register
    def __init__(self, align_corners=False, half_pixel_centers=False):
        """Initialize"""
        self.add_prim_attr("max_length", 1000000)
        validator.check_value_type('align_corners', align_corners, bool, self.name)
        validator.check_value_type('half_pixel_centers', half_pixel_centers, bool, self.name)
        self.init_prim_io_names(inputs=['images', 'size'], outputs=['y'])

    def __infer__(self, images, size):
        # get shape
        images_shape = list(images['shape'])
        size_shape = list(size['shape'])
        # get value
        if images['value'] is None:
            raise ValueError(f"For '{self.name}', the 'images' cannot be None, but got {images['value']}.")
        if size['value'] is None:
            raise ValueError(f"For '{self.name}', the 'size' cannot be None, but got {size['value']}.")
        size_value = size['value']
        # get dtype
        images_dtype = images['dtype']
        size_dtype = size['dtype']
        # check dytpe
        validator.check_tensor_dtype_valid("images", images_dtype,
                                           [mstype.int8, mstype.int16, mstype.int32, mstype.int64, mstype.float16,
                                            mstype.float32, mstype.uint8, mstype.uint16, mstype.double], self.name)
        validator.check_tensor_dtype_valid("size", size_dtype, [mstype.int32], self.name)
        # check input shape rank
        validator.check("images rank", len(images_shape), "expected", 4, Rel.EQ, self.name)
        validator.check("size rank", len(size_shape), "expected", 1, Rel.EQ, self.name)
        validator.check("size dim_0", size_shape[0], "expected", 2, Rel.EQ, self.name)
        # check size_value
        validator.check("size[0]", size_value[0], "minimum", 0, Rel.GT, self.name)
        validator.check("size[1]", size_value[1], "minimum", 0, Rel.GT, self.name)

        batch_size = images_shape[0]
        height = size_value[0]
        width = size_value[1]
        channel = images_shape[3]
        out_shape = (batch_size, height, width, channel)
        return {'shape': out_shape,
                'dtype': mstype.float32,
                'value': None}


class ResizeArea(Primitive):
    """
    Resize images to a certain size using area interpolation.

    The resizing process only changes the two dimensions of images, which represent the width and height of images.

    .. warning::
        The values of "size" must be greater than zero.

    Args:
        align_corners (bool): If true, the centers of the 4 corner pixels of the input and output tensors are aligned,
            preserving the values at the corner pixels. Defaults： False.

    Inputs:
        - **images** (Tensor) -  Input images must be a 4-D tensor with shape which is [batch, height, width, channels].
          The format must be NHWC.
          Types allowed: int8, int16, int32, int64, float16, float32, float64, uint8, uint16.
        - **size** (Tensor) - Input size must be a 1-D tensor of 2 elements: new_height, new_width.
          The new size of output image.
          Types allowed: int32.

    Outputs:
        A 4-D tensor of shape [batch, new_height, new_width, channels] with type: float32.

    Raises:
        TypeError: If dtype of `images` is not supported.
        TypeError: If dtype of `size` is not int32.
        TypeError: If dtype of `align_corners` is not bool.
        ValueError: If the num of inputs is not 2.
        ValueError: If the dimension of `images` shape is not 4.
        ValueError: If the dimension of `size` shape is not 1.
        ValueError: If the element num of `size` is not [new_height, new_width].
        ValueError: The size is not positive.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> images = Tensor([[[[2], [4], [6], [8]], [[10], [12], [14], [16]]]], mindspore.float16)
        >>> size = Tensor([1, 2], mindspore.int32)
        >>> resizearea = ops.ResizeArea()
        >>> output = resizearea(images, size)
        >>> print(output.asnumpy())
            [[[[ 7.]
               [11.]]]]
    """

    @prim_attr_register
    def __init__(self, align_corners=False):
        """Initialize ResizeArea"""
        self.init_prim_io_names(inputs=['images', 'size'], outputs=['y'])
        validator.check_value_type("align_corners", align_corners, [bool], self.name)
        self.align_corners = align_corners


class CropAndResizeGradImage(Primitive):
    """
    Computes the gradient of the CropAndResize op with respect to the input images tensor.

    Note:
        Input grads must be a 4-D tensor.

    Args:
        method (str): A string specifying the interpolation method. "bilinear", "nearest" and "bilinear_v2" are
            supported for now. Default: "bilinear".
        T (mindspore.dtype): T is a required attribute. The value range of T is {mindspore.float16, mindspore.float32,
            mindspore.float64}.

    Inputs:
        - **grads** (Tensor) - A 4-D tensor of shape [num_boxes, crop_height, crop_width, depth].
          The format must be NHWC. Types allowed: float32, float64.
        - **boxes** (Tensor) - A 2-D tensor of shape [num_boxes, 4].
          The i-th row of the tensor specifies the coordinates of a box in the box_index[i] image
          and is specified in normalized coordinates [y1, x1, y2, x2]. A normalized coordinate value of y is mapped to
          the image coordinate at y * (image_height - 1), so as the [0, 1] interval of normalized image height is
          mapped to [0, image_height - 1] in image height coordinates. We do allow y1 > y2, in which case the sampled
          crop is an up-down flipped version of the original image. The width dimension is treated similarly.
          Normalized coordinates outside the [0, 1] range are allowed, in which case we use extrapolation_value to
          extrapolate the input image values. Types allowed: float32, float64.
        - **box_index** (Tensor) - A 1-D tensor of shape [num_boxes] with int32 values in [0, batch).
          The value of box_index[i] specifies the image that the i-th box refers to. Types allowed: int32.
        - **image_size** (Tensor) - A 1-D tensor with value [batch, image_height, image_width, depth]
          containing the original image size. Both image_height and image_width need to be positive.
          Types allowed: int32.

    Outputs:
        A 4-D tensor of shape [batch, image_height, image_width, depth]. Output type depends on input attribute T.
        Types allowed: mindspore.float16, mindspore.float32, mindspore.float64.

    Raises:
        TypeError: If `method` is not a str.
        TypeError: If `grads` is not tensor or its dtype is not float32 or float64.
        TypeError: If `boxes` is not tensor or its dtype is not float32 or float64.
        TypeError: If `box_index` is not tensor or its dtype is not int32.
        TypeError: If `image_size` is not tensor or its dtype is not int32.
        TypeError: If the value of `T` is not a number dtype in mindspore.
        ValueError: If `method` is not "bilinear".
        ValueError: If `T` is not in {mindspore.float16, mindspore.float32, mindspore.float64}.
        ValueError: If the size of `grads` tensor shape is not equal to 4.
        ValueError: If the size of `boxes` tensor shape is not equal to 2.
        ValueError: If the length of the second dimension of `boxes` is not equal to 4.
        ValueError: If the size of `image_size` or `box_index` tensor shape is not equal to 1.
        ValueError: If the length of `box_index` is not equal to num_boxes.
        ValueError: If the length of `image_size` is not equal to 4.
        ValueError: If the value of image_height or image_width of `image_size` is not positive.

    Supported Platforms:
        ``GPU``

    Examples:
        >>> crop_and_resize_grad_image = ops.CropAndResizeGradImage(T = mindspore.float32, method = "bilinear")
        >>> grads = Tensor(np.array([[[[1.0], [2.0]], [[3.0], [4.0]]]]), mindspore.float32)
        >>> boxes = Tensor(np.array([[0.1, 0.2, 0.3, 0.4]]), mindspore.float32)
        >>> box_index = Tensor(np.array([0]), mindspore.int32)
        >>> image_size = Tensor(np.array([1, 4, 4, 1]), mindspore.int32)
        >>> output = crop_and_resize_grad_image(grads, boxes, box_index, image_size)
        >>> print(output.asnumpy())
        [[[[0.39999992]
           [2.0399997 ]
           [0.36000004]
           [0.        ]]
          [[1.1999999 ]
           [5.16      ]
           [0.8400003 ]
           [0.        ]]
          [[0.        ]
           [0.        ]
           [0.        ]
           [0.        ]]
          [[0.        ]
           [0.        ]
           [0.        ]
           [0.        ]]]]
    """

    @prim_attr_register
    def __init__(self, T, method="bilinear"):
        """Initialize CropAndResizeGradImage"""
        self.init_prim_io_names(inputs=['grads', 'boxes', 'box_index', 'image_size'], outputs=['y'])
        validator.check_value_type("method", method, [str], self.name)
        validator.check_string(method, ["bilinear", "nearest", "bilinear_v2"], "method", self.name)
        self.method = method
        valid_values = (mstype.float16, mstype.float32, mstype.float64)
        if T in mstype.number_type:
            validator.check("T", T, "expected", valid_values, Rel.IN, self.name)
        else:
            validator.check_type_name("T", T, valid_values, self.name)
        self.add_prim_attr("max_Byte", int(2e9))  # Maximum bytes of image gradient


class ScaleAndTranslate(Primitive):
    """
    Scale And Translate the input image tensor.

    Note:
        Input images must be a 4-D tensor.
        Input size, scale and translation must be a 1-D tensor with two elements.

    Args:
        kernel_type (str): An optional string. Deciding which image filtering algorithm to choose. Default: "lanczos3".
        antialias (bool): An optional bool. Deciding whether to use the antialias. Default: True.

    Inputs:
        - **images** (Tensor) - A 4-D tensor of shape (batch, image_height, image_width, channel).
        - **size** (Tensor) - The size of the output image after scale and translate operations. A 1-D tensor with two
          positive elements whose dtype is int32 and shape must be (2,).
        - **scale** (Tensor) - Indicates the zoom factor. A 1-D tensor with two positive elements whose dtype is float32
          and shape must be (2,).
        - **translation** (Tensor) - Translate the pixel value. A 1-D tensor with two elements whose dtype is
          float32 and shape must be (2,).

    Outputs:
        A 4-D tensor with type: float32 and shape: [batch, size[0], size[1], channel].

    Raises:
        TypeError: If `kernel_type` is not str.
        TypeError: If `antialias` is not bool.
        TypeError: If `images` is not tensor with valid dtype.
        TypeError: If `size` is not a tensor of int32.
        TypeError: If `scale` is not a tensor of float32.
        TypeError: If `translation` is not a tensor of float32.
        ValueError: If `kernel_type` is not in ["lanczos1", "lanczos3", "lanczos5", "gaussian", "box", "triangle",
                    "keyscubic", "mitchellcubic"].
        ValueError: If the rank of `images` is not 4.
        ValueError: If  the shape of `size` is not (2,).
        ValueError: If  the shape of `scale` is not (2,).
        ValueError: If the shape of `translation`  is not (2,).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> op = ScaleAndTranslate()
        >>> image = Tensor(np.array([[[[9.0], [5.0], [2.0], [1.0]],
        ...                           [[6.0], [1.0], [9.0], [7.0]]]]), mindspore.float32)
        >>> size = Tensor(np.array([2, 2]).astype(np.int32))
        >>> scale = Tensor(np.array([1, 1]).astype(np.float32))
        >>> translation = Tensor(np.array([1, 1]).astype(np.float32))
        >>> output = op(image, size, scale, translation)
        >>> print(output)
        [[[[0.]
           [0.]]
          [[0.]
           [9.]]]]
    """

    @prim_attr_register
    def __init__(self, kernel_type="lanczos3", antialias=True):
        """Initialize ScaleAndTranslate"""
        validator.check_value_type("kernel_type", kernel_type, [str], self.name)
        validator.check_string(kernel_type, ["lanczos1", "lanczos3", "lanczos5", "gaussian", "box", "triangle",
                                             "keyscubic", "mitchellcubic"], "kernel_type", self.name)
        validator.check_value_type("antialias", antialias, [bool], self.name)
