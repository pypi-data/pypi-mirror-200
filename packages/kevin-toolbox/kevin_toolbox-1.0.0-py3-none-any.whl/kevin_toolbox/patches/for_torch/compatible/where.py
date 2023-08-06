import torch
import numpy as np
from kevin_toolbox.env_info import version

if version.compare(torch.__version__, "<", "1.2"):
    """
        参考 torch.where()
            在 1.1 版本及其之前的 pytorch 中的 torch.where()，
            只有 torch.where(condition, x, y) 的用法，
            而没有 torch.where(condition) 的用法，
            考虑到兼容性，在pytorch版本过低时，自动使用 numpy.where() 来替代
    """


    def where(*args):
        if len(args) == 1:
            res = np.where(args[0].cpu())
            return torch.as_tensor(res, device=args[0].device)
        else:
            return torch.where(*args)
else:
    where = torch.where
