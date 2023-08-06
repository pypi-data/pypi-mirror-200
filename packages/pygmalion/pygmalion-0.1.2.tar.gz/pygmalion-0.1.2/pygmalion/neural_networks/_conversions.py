import torch
import pandas as pd
import numpy as np
from typing import List, Iterable, Optional, Union
from warnings import warn
from pygmalion.tokenizers._utilities import Tokenizer


def named_to_tensor(data: Union[pd.DataFrame, dict, Iterable],
                    names: List[str], device: Optional[torch.device]=None
                    ) -> torch.Tensor:
    """converts named variables to tensors"""
    if isinstance(data, dict):
        data = {k: v if hasattr(v, "__iter__") else [v] for k, v in zip(names, (data[n] for n in names))}
        data = pd.DataFrame.from_dict(data)
    if isinstance(data, pd.DataFrame):
        data = data[names].to_numpy()
    data = floats_to_tensor(data, device=device)
    if len(data.shape) == 1:
        data = data.unsqueeze(-1)
    return data


def floats_to_tensor(arr: Iterable, device: Optional[torch.device] = None) -> torch.Tensor:
    """converts an array of numerical values to a tensor of floats"""
    if isinstance(arr, pd.Series):
        arr = arr.to_numpy()
    t = torch.tensor(arr, dtype=torch.float, device=device,
                     requires_grad=False)
    return t


def tensor_to_floats(tensor: torch.Tensor) -> np.ndarray:
    """converts a torch.Tensor to a numpy.ndarray of doubles"""
    assert tensor.dtype == torch.float
    return tensor.detach().cpu().numpy()


def longs_to_tensor(arr: Iterable, device: Optional[torch.device] = None) -> torch.Tensor:
    """converts an array of numerical values to a tensor of longs"""
    if isinstance(arr, pd.Series):
        arr = arr.to_numpy()
    t = torch.tensor(arr, dtype=torch.long, device=device,
                     requires_grad=False)
    return t


def tensor_to_longs(tensor: torch.Tensor) -> list:
    """converts a tensor of longs to numpy"""
    assert tensor.dtype == torch.long
    return tensor.detach().cpu().numpy()


def images_to_tensor(images: Iterable[np.ndarray],
                     device: Optional[torch.device] = None) -> torch.Tensor:
    """Converts a list of images to a tensor"""
    assert ((isinstance(images, np.ndarray) and images.dtype == np.uint8)
            or all(im.dtype == np.uint8 for im in images))
    images = floats_to_tensor(images, device)/255
    if len(images.shape) == 3:  # Grayscale images
        images = images.unsqueeze(1)  # (N, H, W) --> (N, 1, H, W)
    else:  # RGB/RGBA images
        images = images.permute(0, 3, 1, 2)  # (N, H, W, C) --> (N, C, H, W)
    return images


def tensor_to_images(tensor: torch.Tensor,
                     colors: Union[np.ndarray, None] = None
                     ) -> np.ndarray:
    """
    Converts a tensor of long to a list of images
    If 'colors' is not None, tensor must contain indexes to the
    color for each pixel.
    Otherwise it must be a tensor of float valued images between 0. and 255.
    """
    if colors is None:
        arr = np.round(tensor_to_floats(tensor))
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        if arr.shape[1] == 1:  # grayscale images
            return arr[:, 0, :, :]
        elif arr.shape[1] in [3, 4]:  # RGB or RGBA image
            return np.moveaxis(arr, 1, -1)
        else:
            raise ValueError(f"Unexpected number of channels {tensor.shape[1]}"
                             " for tensor representing a list of images")
    else:
        assert tensor.dtype == torch.long
        return colors[tensor_to_longs(tensor)]


def tensor_to_index(tensor: torch.tensor, dim=1) -> np.ndarray:
    """Converts a tensor to an array of category index"""
    return tensor_to_longs(torch.argmax(tensor, dim=dim))


def classes_to_tensor(input: Iterable[Union[str, int]],
                      classes: Iterable[str],
                      device: Optional[torch.device] = None) -> torch.Tensor:
    """
    converts a list of classes to tensor
    'classes' must be a list of unique possible classes.
    The tensor contains for each input the index of the category.
    """
    indexes = {c: i for i, c in enumerate(classes)}
    return longs_to_tensor([indexes[c] if isinstance(c, str) else int(c) for c in input],
                           device=device)


def tensor_to_classes(tensor: torch.Tensor,
                      classes: List[str]) -> List[str]:
    """Converts a tensor of category indexes to str category"""
    indexes = tensor_to_index(tensor)
    return [classes[i] for i in indexes]


def tensor_to_dataframe(tensor: torch.Tensor,
                        names: List[str]) -> pd.DataFrame:
    """converts a tensor to dataframe with named columns"""
    return pd.DataFrame(data=tensor_to_floats(tensor), columns=names)


def tensor_to_probabilities(tensor: torch.Tensor,
                            classes: List[str]) -> pd.DataFrame:
    """
    Converts the raw output of a classifier neural network
    to a dataframe of class probability for each observation
    """
    return tensor_to_dataframe(torch.softmax(tensor, dim=-1), classes)


def segmented_to_tensor(images: np.ndarray, colors: Iterable,
                        device: torch.device) -> torch.Tensor:
    """
    Converts a segmented image to a tensor of long
    """
    if len(images.shape) == 4:  # Color image
        assert all(hasattr(c, "__iter__") for c in colors)
    elif len(images.shape) == 3:  # Grayscale image
        assert all(isinstance(c, int) for c in colors)
        images = np.expand_dims(images, -1)
        colors = [[c] for c in colors]
    else:
        raise RuntimeError("Unexpected shape of segmented images")
    masks = np.stack([np.all(images == c, axis=3) for c in colors])
    if not masks.any(axis=0).all():
        raise RuntimeError("Found color associated to no class")
    return longs_to_tensor(np.argmax(masks, axis=0), device)


def strings_to_tensor(strings: Iterable[str],
                      tokenizer: Tokenizer,
                      device: torch.device,
                      max_sequence_length: Optional[int] = None,
                      raise_on_longer_sequences: bool = False,
                      add_start_end_tokens: bool = False,
                      **kwargs) -> torch.Tensor:
    """
    converts a list of sentences to tensor

    Parameters
    ----------
    strings : iterable of str
        a list of strings
    tokenizer : Tokenizer
        the tokenizer to segment strings
    device : torch.device
        the device to host the tensor on
    max_sequence_length : int or None
        Sentences are stored in a tensor with one dimension corresponding to
        the max token sequence's length, and strings shorter are padded.
        If max_sequence_length is specified, the size of this dimension is
        fixed and strings that are longer are droped.
        Otherwise this dimension is defined by the longest encoded string.
    raise_on_longer_sequences : bool
        If True, raise a ValueError if any sequence
        is longer than max_sequence_length once tokenized
    add_start_end_token : bool
        If True, the <START> and <END> special token are appended around each
        encoded string, before padding with <PAD>
    **kwargs : dict
        dict of kwargs passed to the tokenizer when encoding


    Returns
    -------
    torch.Tensor :
        a tensor of shape (N, L) of longs, where:
        * N is the number of strings
        * L is the length of longest sentence
        and each scalar is the index of a word in the lexicon
    """
    pad = tokenizer.PAD
    strings = [tokenizer.encode(s, **kwargs) for s in strings]
    if add_start_end_tokens:
        start, end = tokenizer.START, tokenizer.END
        strings = [[start] + s + [end] for s in strings]
    if max_sequence_length is None:
        L_max = max(len(s) for s in strings)
    else:
        n = sum(1 for s in strings if len(s) > max_sequence_length)
        if n > 0:
            error = f"Found {n:,}/{len(strings):,} sequences with tokenized length superior to {max_sequence_length}".replace(",", " ")
            if raise_on_longer_sequences:
                raise ValueError(error)
            else:
                warn(error)
        strings = [s if len(s) <= max_sequence_length else [] for s in strings]
        L_max = max_sequence_length
    data = [s + [pad]*(L_max - len(s)) for s in strings]
    return longs_to_tensor(data, device)


def tensor_to_sentences(tensor: torch.Tensor, tokenizer: Tokenizer) -> List[str]:
    """
    converts a tensor to a list of sentences

    Parameters
    ----------
    tensor : torch.Tensor
        a tensor of shape (N, L) where:
        * N is the number of sentences
        * L is the length of longest sentence
    tokenizer : Tokenizer
        a tokenizer with a 'decode' method

    Returns
    -------
    list of str :
        a list of sentences,
        each sentence is a set of words separated by whitespaces
    """
    sentences = tensor_to_longs(tensor)[:, 1:-1]
    return [tokenizer.decode(s) for s in sentences]


# def bounding_boxes_to_tensor(bboxes: List[dict], image_size: Tuple[int, int],
#                              cell_size: Tuple[int, int], classes: List[str],
#                              device: torch.device) -> Tuple[torch.Tensor]:
#     """
#     Converts a list of bounding boxes to a tuple of tensors
#     (multiple bounding boxes for each image)
#     * The 'boxe_coords', a tensor of shape (N, 2, H, W) of (x, y)
#       of the bounding boxe falling in the given grid cell.
#     * The 'boxe_size', a tensor of shape (N, 2, H, W) of (width, height)
#       of the bounding boxe falling in the given grid cell.
#     * The 'object_mask', a tensor of shape (N, H, W) which is True when there
#       is an object in the grid cell and False otherwise
#     * The 'class_index', a tensor of shape (N, H, W) of class indexes present
#       in each grid cell.
#       0 by default for empty cells
#     * The 'weights", either None or a tensor of shape (N, H, W) of floats.
#       In which case the value are the weighting in the loss function of each
#       object to detect.

#     Parameters
#     ----------
#     bboxes : list of dict
#         A dict for each image with the keys
#             * x1, x2, y1, y2 : list of int
#                 the x/y positions of the two corners of the boxe (in pixels)
#             * class : list of str
#                 the classes of the detected objects
#             * [weights : optional, list of floats]
#                 the weighting of each object in the loss function
#     image_size : tupe of int
#         the (height, width) of the images
#     cell_size : tuple of int
#         the (height, width) of the anchor grid's cells (in pixels)
#     classes : list of str
#         list of the unique class names
#     device : torch.device
#         the device the tensors should be stored on

#     Return
#     ------
#     tuple of torch.Tensor :
#         (boxe_coords, boxe_size, object_mask, class_index, weights)
#     """
#     h_image, w_image = image_size
#     h_cell, w_cell = cell_size
#     h_grid, w_grid = h_image // h_cell, w_image // w_cell
#     object_mask = np.zeros((len(bboxes), h_grid, w_grid), dtype=np.bool)
#     class_index = np.zeros((len(bboxes), h_grid, w_grid), dtype=np.long)
#     boxe_coords = np.zeros((len(bboxes), 2, h_grid, w_grid), dtype=np.float)
#     boxe_size = np.zeros((len(bboxes), 2, h_grid, w_grid), dtype=np.float)
#     data = [(img, int(0.5*(y1+y2)/h_cell), int(0.5*(x1+x2)/w_cell),
#              0.5*(y1+y2)/h_cell % 1, 0.5*(x1+x2)/w_cell % 1,
#              abs(y1-y2)/h_cell, abs(x1-x2)/w_cell, classes.index(c))
#             for img, bb in enumerate(bboxes)
#             for x1, x2, y1, y2, c
#             in zip(bb["x1"], bb["x2"], bb["y1"], bb["y2"], bb["class"])]
#     img, row, column, y, x, h, w, c = zip(*data)
#     object_mask[img, row, column] = True
#     boxe_coords[img, :, row, column] = list(zip(x, y))
#     boxe_size[img, :, row, column] = list(zip(w, h))
#     class_index[img, row, column] = c
#     weights = [bb.get("weights", None) for bb in bboxes]
#     if not(None in weights):
#         weights = sum(weights, [])
#         cell_weights = np.zeros((len(bboxes), h, w), dtype=np.float)
#         cell_weights[img, row, column] = weights
#     else:
#         cell_weights = None
#     boxe_coords = torch.tensor(boxe_coords, dtype=torch.float, device=device)
#     boxe_size = torch.tensor(boxe_size, dtype=torch.float, device=device)
#     object_mask = torch.tensor(object_mask, dtype=torch.bool, device=device)
#     class_index = torch.tensor(class_index, dtype=torch.long, device=device)
#     if cell_weights is not None:
#         cell_weights = torch.tensor(cell_weights, dtype=torch.float,
#                                     device=device)
#     return boxe_coords, boxe_size, object_mask, class_index, cell_weights


# def tensor_to_bounding_boxes(tensors: Tuple[torch.Tensor],
#                              cell_size: Tuple[int, int],
#                              classes: List[str]) -> List[dict]:
#     """
#     Converts the (boxe_size, object_proba, class_proba) tensors
#     to a bounding boxes dict for each image.

#     Parameters
#     ----------
#     tensors : tuple of tensors
#         A tuple of ('boxe_coords', 'boxe_size', 'object_proba', 'class_proba')
#         * 'boxe_coords' : torch.Tensor
#             A tensor of shape (N, B, 2, H, W) of (x, y) boxe coordinates
#             x/y is the center of the boxe in relative cell coordinate
#             (between 0 and 1)
#         * 'boxe_size' : torch.Tensor
#             A tensor of shape (N, B, 4, H, W) of (w, h) boxe coordinates
#             h/w is the height/width of the boxe divided by the grid cell size
#         * 'object_proba' : torch.Tensor
#             A tensor of shape (N, B, H, W) of probability of object presence
#         * 'class_proba' : torch.Tensor
#             A tensor of shape (N, B, C, H, W) of class probabilities of the
#             detected objects
#         where N is the number of images, B the number of bounding boxes
#         predicted per cell of the anchor grid, C the number of classes,
#         H/W the height/width of the anchor grid.
#     cell_size : tuple of int
#         The (height, width) of a cell in the anchor grid
#     classes : list of str
#         The list of unique classes


#     Returns
#     -------
#     list of dict:
#         the bounding boxes of each image as a dictionnary of keys:
#         - x1, y1, x2, y2 : list of int
#             coordinates of the corners of each bounding boxe
#         - class : list of str
#             the class of each detected object
#         - confidence : list of float
#             the confidence of presence of an object of given class
#             (probability from 0 to 1)
#     """
#     cpu_tensors = [t.detach().cpu() for t in tensors]
#     boxe_coords, boxe_size, object_proba, class_proba = cpu_tensors
#     N, H, W = object_proba.shape
#     h, w = cell_size
#     # Converting boxes coordinates from (x, y, h, w) to (x1, y1, x2, y2)
#     steps = [torch.tensor([i*dl for i in range(L)], dtype=torch.float)
#              for dl, L in zip([h, w], [H, W])]
#     grid_y, grid_x = torch.meshgrid(*steps)
#     x1 = (boxe_coords[:, 0, ...] - 0.5*boxe_size[:, 0, ...])*w + grid_x
#     y1 = (boxe_coords[:, 1, ...] - 0.5*boxe_size[:, 1, ...])*h + grid_y
#     x2 = (boxe_coords[:, 0, ...] + 0.5*boxe_size[:, 0, ...])*w + grid_x
#     y2 = (boxe_coords[:, 1, ...] + 0.5*boxe_size[:, 1, ...])*h + grid_y
#     boxes = torch.stack([x1, y1, x2, y2], dim=-1).view(N, -1, 4)
#     # Getting the class index and confidence of each bounding boxe found
#     class_proba = torch.softmax(class_proba, dim=1)
#     class_proba, class_index = torch.max(class_proba, dim=1)
#     class_proba = class_proba.view(N, -1)
#     class_index = class_index.view(N, -1)
#     object_proba = object_proba.view(N, -1)
#     confidence = object_proba * class_proba
#     # filtering boxes with confidence too low
#     mask = (confidence >= 0.5)
#     # Performing non max suppression
#     kept = [ops.batched_nms(boxes[i, mask[i]], confidence[i, mask[i]],
#                             class_index[i, mask[i]], 0.5) for i in range(N)]
#     # returning the list of boxes found
#     res = [{"x1": [int(round(x.item())) for k in kept
#                    for x in boxes[i, mask[i]][k, 0]],
#             "y1": [int(round(y.item())) for k in kept
#                    for y in boxes[i, mask[i]][k, 1]],
#             "x2": [int(round(x.item())) for k in kept
#                    for x in boxes[i, mask[i]][k, 2]],
#             "y2": [int(round(y.item())) for k in kept
#                    for y in boxes[i, mask[i]][k, 3]],
#             "class": [classes[c] for k in kept
#                       for c in class_index[i, mask[i]][k]],
#             "confidence": [c.item() for k in kept
#                            for c in confidence[i, mask[i]][k]]}
#            for i in range(N)]
#     return res