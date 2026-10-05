"""workflow_gen_lite: 自然语言 → 工作流定义 JSON。"""
from .parser import parse_workflow, Workflow
from .llm import llm_parse

__all__ = ["parse_workflow", "Workflow", "llm_parse"]
__version__ = "0.1.0"
