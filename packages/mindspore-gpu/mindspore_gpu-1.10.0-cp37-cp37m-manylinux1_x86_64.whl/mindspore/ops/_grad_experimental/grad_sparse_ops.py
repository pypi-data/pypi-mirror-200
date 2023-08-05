# Copyright 2022 Huawei Technologies Co., Ltd
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

"""bprop primitives"""
from mindspore.ops.operations.sparse_ops import CSRSparseMatrixToSparseTensor
from mindspore.ops.operations.sparse_ops import SparseReorder
from mindspore.ops.operations.sparse_ops import SparseTensorToCSRSparseMatrix
from mindspore.ops.operations.sparse_ops import SparseToDenseV2
from mindspore.ops.operations.sparse_ops import SparseSoftmax
from mindspore.ops.operations.sparse_ops import SparseDenseCwiseAdd
from mindspore.ops.operations.sparse_ops import SparseSegmentSum
from mindspore.ops.operations.sparse_ops import SparseSegmentSumWithNumSegments
from mindspore.ops.operations.sparse_ops import SparseSegmentSqrtN
from mindspore.ops.operations.sparse_ops import SparseSegmentSqrtNWithNumSegments
from mindspore.ops.operations.sparse_ops import SparseSegmentMeanWithNumSegments
from mindspore.common import dtype as mstype
from mindspore import Tensor
from mindspore.ops.primitive import constexpr
from mindspore.ops import functional as F
from mindspore.ops import operations as P
from mindspore.ops.composite.multitype_ops.zeros_like_impl import zeros_like
from mindspore.ops.operations import _grad_ops as G
from mindspore.ops._grad.grad_base import bprop_getters
from mindspore.ops._utils.utils import is_shape_unknown

# Unused parameters are placeholders.
dyn_shape_op = P.TensorShape()


@constexpr
def _create_tensor(data, dtype):
    return Tensor(data, dtype=dtype)


@bprop_getters.register(SparseSoftmax)
def get_bprop_sparse_softmax(self):
    """Generate bprop for SparseSoftmax"""
    sparse_to_dense = SparseToDenseV2()
    sparse_dense_cwise_add = SparseDenseCwiseAdd()
    reduce_sum = P.ReduceSum(keep_dims=True)
    mul = P.Mul()

    def bprop(indices, values, shape, out, dout):
        default_values = _create_tensor(0, values.dtype)
        out_dout = mul(out, dout)
        sp_product = sparse_to_dense(indices, shape, out_dout, default_values)
        sum_reduced = -reduce_sum(sp_product, -1)
        sp_sum = sparse_dense_cwise_add(indices, dout, shape, sum_reduced)
        grad_x = mul(sp_sum, out)
        return zeros_like(indices), grad_x, zeros_like(shape)

    return bprop


@bprop_getters.register(SparseTensorToCSRSparseMatrix)
def get_bprop_sparse_tensor_to_csr_sparse_matrix(self):
    """Grad definition for 'SparseTensorToCSRSparseMatrix' operation"""
    op = CSRSparseMatrixToSparseTensor()

    def bprop(x_indices, x_values, x_dense_shape, out, dout):
        dx = op(dout[0], dout[1], dout[2], dout[3], dout[4])
        dx_all = (dx[0], dx[1], dx[2])
        return dx_all

    return bprop


@bprop_getters.register(CSRSparseMatrixToSparseTensor)
def get_bprop_csr_sparse_matrix_to_sparse_tensor(self):
    """Grad definition for 'CSRSparseMatrixToSparseTensor' operation"""
    op = SparseTensorToCSRSparseMatrix()

    def bprop(x_dense_shape, x_batch_pointers, x_row_pointers, x_col_indices, x_values, out, dout):
        dx = op(dout[0], dout[1], dout[2])
        dx_all = (dx[0], dx[1], dx[2], dx[3], dx[4])
        return dx_all

    return bprop


@bprop_getters.register(SparseToDenseV2)
def get_bprop_sparse_to_dense_v2(self):
    """Generate bprop for SparseToDenseV2"""

    def bprop(indices, output_shape, values, default_value, out, dout):
        sparse_values_grad = F.gather_nd(dout, indices)
        default_value_grad = F.reduce_sum(dout) - F.reduce_sum(sparse_values_grad)
        result_all = (zeros_like(indices), zeros_like(output_shape), sparse_values_grad, default_value_grad)
        return result_all

    return bprop


@bprop_getters.register(SparseSegmentSqrtN)
def get_bprop_sparse_segment_sqrt_n(self):
    """Grad definition for `SparseSegmentSqrtN` operation."""
    input_grad = G.SparseSegmentSqrtNGrad()
    shape = P.Shape()

    def bprop(x, indices, segment_ids, out, dout):
        shape_x = shape(x)
        if is_shape_unknown(shape_x):
            shape_x = dyn_shape_op(x)
        output_dim0 = P.Cast()(shape_x[0], mstype.int32)
        indices = F.cast(indices, mstype.int32)
        segment_ids = F.cast(segment_ids, mstype.int32)
        dx = input_grad(dout, indices, segment_ids, output_dim0)
        all_d = (dx, zeros_like(indices), zeros_like(segment_ids))
        return all_d

    return bprop


@bprop_getters.register(SparseSegmentSqrtNWithNumSegments)
def get_bprop_sparse_segment_sqrt_n_with_num_segments(self):
    """Grad definition for `SparseSegmentSqrtNWithNumSegments` operation."""
    input_grad = G.SparseSegmentSqrtNGrad()
    shape = P.Shape()

    def bprop(x, indices, segment_ids, num_segments, out, dout):
        shape_x = shape(x)
        if is_shape_unknown(shape_x):
            shape_x = dyn_shape_op(x)
        output_dim0 = P.Cast()(shape_x[0], mstype.int32)
        indices = F.cast(indices, mstype.int32)
        segment_ids = F.cast(segment_ids, mstype.int32)
        dx = input_grad(dout, indices, segment_ids, output_dim0)
        all_d = (dx, zeros_like(indices), zeros_like(segment_ids), zeros_like(num_segments))
        return all_d

    return bprop


@bprop_getters.register(SparseSegmentSum)
def get_bprop_sparse_segment_sum(self):
    """Grad definition for `SparseSegmentSum` operation."""
    input_grad = G.SparseSegmentSumGrad()
    shape = P.Shape()

    def bprop(x, indices, segment_ids, out, dout):
        shape_x = shape(x)
        if is_shape_unknown(shape_x):
            shape_x = dyn_shape_op(x)
        output_dim0 = P.Cast()(shape_x[0], mstype.int32)
        indices = F.cast(indices, mstype.int32)
        segment_ids = F.cast(segment_ids, mstype.int32)
        dx = input_grad(dout, indices, segment_ids, output_dim0)
        all_d = (dx, zeros_like(indices), zeros_like(segment_ids))
        return all_d

    return bprop


@bprop_getters.register(SparseSegmentSumWithNumSegments)
def get_bprop_sparse_segment_sum_with_num_segments(self):
    """Grad definition for `SparseSegmentSumWithNumSegments` operation."""
    input_grad = G.SparseSegmentSumGrad()
    shape = P.Shape()

    def bprop(x, indices, segment_ids, num_segments, out, dout):
        shape_x = shape(x)
        if is_shape_unknown(shape_x):
            shape_x = dyn_shape_op(x)
        output_dim0 = P.Cast()(shape_x[0], mstype.int32)
        indices = F.cast(indices, mstype.int32)
        segment_ids = F.cast(segment_ids, mstype.int32)
        dx = input_grad(dout, indices, segment_ids, output_dim0)
        all_d = (dx, zeros_like(indices), zeros_like(segment_ids), zeros_like(num_segments))
        return all_d

    return bprop


@bprop_getters.register(SparseSegmentMeanWithNumSegments)
def get_bprop_sparse_segment_mean_with_num_segments(self):
    """Grad definition for `SparseSegmentMeanWithNumSegments` operation."""
    input_grad = G.SparseSegmentMeanGrad()
    shape = P.Shape()

    def bprop(x, indices, segment_ids, num_segments, out, dout):
        x_shp = shape(x)
        if is_shape_unknown(x_shp):
            x_shp = dyn_shape_op(x)
            output_dim0 = F.cast(x_shp[0], mstype.int32)
        else:
            output_dim0 = F.scalar_to_tensor(x_shp[0], mstype.int32)
        indices = F.cast(indices, mstype.int32)
        segment_ids = F.cast(segment_ids, mstype.int32)
        dx = input_grad(dout, indices, segment_ids, output_dim0)
        all_d = (dx, zeros_like(indices), zeros_like(segment_ids), zeros_like(num_segments))
        return all_d

    return bprop


@bprop_getters.register(SparseReorder)
def get_bprop_sparse_reorder(self):
    """Grad definition for `SparseReorder` operation."""
    sparse_reorder_op = SparseReorder()
    range_op = P.Range()
    gather_op = P.Gather()

    def bprop(indices, values, shape, out, dout):
        num_entries = F.shape(indices)[0]
        start = Tensor(0, dtype=mstype.int32)
        limit = Tensor(num_entries, dtype=mstype.int32)
        delta = Tensor(1, dtype=mstype.int32)
        entry_indices = range_op(start, limit, delta)
        output = sparse_reorder_op(indices, entry_indices, shape)
        inverted_permutation = F.sort(output[1].astype(mstype.float32))[1]
        axis = 0
        return None, gather_op(dout[1], inverted_permutation, axis), None
    return bprop
