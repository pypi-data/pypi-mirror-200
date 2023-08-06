# Copyright 2023 OctoML, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .protos import remote_inference_pb2 as pb
import numpy as np

_pb_to_numpy_dtype = {
    pb.TENSOR_DTYPE_F16: np.dtype('float16'),
    pb.TENSOR_DTYPE_F32: np.dtype('float32'),
    pb.TENSOR_DTYPE_F64: np.dtype('float64'),
    pb.TENSOR_DTYPE_I8: np.dtype('int8'),
    pb.TENSOR_DTYPE_I16: np.dtype('int16'),
    pb.TENSOR_DTYPE_I32: np.dtype('int32'),
    pb.TENSOR_DTYPE_I64: np.dtype('int64'),
    pb.TENSOR_DTYPE_UINT8: np.dtype('uint8'),
    pb.TENSOR_DTYPE_UINT16: np.dtype('uint16'),
    pb.TENSOR_DTYPE_UINT32: np.dtype('uint32'),
    pb.TENSOR_DTYPE_UINT64: np.dtype('uint64'),
    pb.TENSOR_DTYPE_BOOL: np.dtype('bool')
}

_numpy_to_pb_dtype = {n: p for p, n in _pb_to_numpy_dtype.items()}


def tensor_to_numpy(tensor: pb.Tensor):
    dtype = _pb_to_numpy_dtype[tensor.dtype]
    data = np.frombuffer(tensor.data, dtype)
    return data.reshape(tensor.shape)


def proto_to_numpy(value: pb.Value):
    return tensor_to_numpy(value.tensor)


def numpy_to_proto(array) -> pb.Value:
    data = array.tobytes()
    dtype = _numpy_to_pb_dtype[array.dtype]
    tensor_proto = pb.Tensor(dtype=dtype, shape=array.shape, data=data)
    return pb.Value(tensor=tensor_proto)
