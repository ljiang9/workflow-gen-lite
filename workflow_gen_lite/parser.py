"""规则解析自然语言 → 工作流 JSON。"""
from __future__ import annotations
import json, re
from dataclasses import dataclass, asdict, field


@dataclass
class Step:
    id: str
    action: str
    mode: str = "sequential"


@dataclass
class Workflow:
    name: str
    steps: list = field(default_factory=list)
    def to_dict(self):
        return {"name": self.name, "steps": [asdict(s) for s in self.steps]}


SEQ_CONNECTORS = ["然后", "接着", "之后", "再然后", "再", "接下来", "随后"]
PAR_CONNECTORS = ["同时", "并行", "一起", "与此同时", "并且"]


def _split_utterance(utterance):
    s = utterance.strip().rstrip("。.!！\n")
    chunks = [c.strip() for c in re.split(r"[\n；;]", s) if c.strip()]
    cleaned = []
    for c in chunks:
        c = re.sub(r"^\s*\d+\s*[.、)）]\s*", "", c).strip()
        if c: cleaned.append(c)
    out = []
    for c in cleaned:
        par_split = None
        for conn in PAR_CONNECTORS:
            if conn in c:
                par_split = [p.strip() for p in c.split(conn, 1)]; break
        if par_split and len(par_split) == 2:
            out.append((par_split[0], "sequential"))
            out.append((par_split[1], "parallel")); continue
        seq_split = None
        for conn in SEQ_CONNECTORS:
            if conn in c:
                seq_split = [p.strip() for p in c.split(conn)]; break
        if seq_split and len(seq_split) > 1:
            for p in seq_split:
                if p: out.append((p, "sequential"))
        else:
            out.append((c, "sequential"))
    return out


def parse_workflow(utterance, name=None):
    parts = _split_utterance(utterance)
    steps = []
    for i, (action, mode) in enumerate(parts, 1):
        action = re.sub(r"^(然后|接着|之后|同时|并行|并且|再)\s*", "", action).strip()
        steps.append(Step(id=f"step_{i}", action=action, mode=mode))
    wf_name = name or (utterance[:20].replace("\n", " ") + ("..." if len(utterance) > 20 else ""))
    return Workflow(name=wf_name, steps=steps)


def to_json(wf):
    return json.dumps(wf.to_dict(), ensure_ascii=False, indent=2)
