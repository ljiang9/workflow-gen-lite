"""命令行：python -m workflow_gen_lite "打开冰箱然后放大象然后关门"。"""
from __future__ import annotations
import argparse, json, sys
from .parser import parse_workflow, to_json
from .llm import llm_parse


def main(argv=None):
    ap = argparse.ArgumentParser(prog="workflow-gen", description="自然语言 → 工作流 JSON")
    ap.add_argument("utterance"); ap.add_argument("--name"); ap.add_argument("--llm", action="store_true")
    args = ap.parse_args(argv)
    if args.llm:
        llm_result = llm_parse(args.utterance)
        if llm_result:
            print(json.dumps(llm_result, ensure_ascii=False, indent=2)); return 0
        print("（无 OPENAI_API_KEY 或 LLM 失败，降级为规则解析）", file=sys.stderr)
    print(to_json(parse_workflow(args.utterance, name=args.name)))
    return 0


if __name__ == "__main__": raise SystemExit(main())
