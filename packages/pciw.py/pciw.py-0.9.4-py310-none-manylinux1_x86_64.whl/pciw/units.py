import os
import platform

# ! Функции получения тега системы
def systag() -> str: return f"{platform.system()}-{platform.machine()}"

# ! Для функций
NONE_TYPE_EXCEPTIONS = ["To be filled", "Default", "N/A", "[Not Supported]", "[notsupported]"]

# ! Определение путей
NVIDIA_SMI_PATH_SUPPORTED = {
    "Linux-x86_64": os.path.join(os.path.dirname(__file__), "data/nsmi/Linux-x86_64/nsmi")
}
T_CPU_PATH_SUPPORTED = {}

NVIDIA_SMI_PATH: str = NVIDIA_SMI_PATH_SUPPORTED.get(systag(), None)
T_CPU_PATH: str = T_CPU_PATH_SUPPORTED.get(systag(), None)
