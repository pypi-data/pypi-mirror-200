from .torchvault import TorchVault


def log(model, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.analyze_model(model)


def diff(sha1, sha2, log_dir="./model_log"):
    vault = TorchVault(log_dir)
    return vault.diff(sha1, sha2)
