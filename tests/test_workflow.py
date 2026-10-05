import json, os, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from workflow_gen_lite.parser import parse_workflow, to_json
from workflow_gen_lite.llm import llm_parse


class TestWorkflowGen(unittest.TestCase):
    def test_sequential_connectors(self):
        wf = parse_workflow("打开冰箱然后放大象然后关门", name="装大象")
        self.assertEqual(wf.name, "装大象"); self.assertEqual(len(wf.steps), 3)
        self.assertEqual(wf.steps[0].action, "打开冰箱"); self.assertEqual(wf.steps[1].action, "放大象")
        for s in wf.steps: self.assertEqual(s.mode, "sequential")
    def test_parallel_marker(self):
        wf = parse_workflow("打开冰箱同时拍照然后关门")
        modes = [s.mode for s in wf.steps]
        self.assertEqual(modes[0], "sequential"); self.assertEqual(modes[1], "parallel")
    def test_newline_split(self):
        wf = parse_workflow("第一步：起床\n第二步：刷牙\n第三步：出门")
        self.assertEqual(len(wf.steps), 3)
    def test_numbered_list(self):
        wf = parse_workflow("1. 写需求\n2. 评审\n3. 开发\n4. 测试")
        actions = [s.action for s in wf.steps]
        self.assertIn("写需求", actions[0]); self.assertIn("测试", actions[-1])
    def test_to_json_valid(self):
        d = json.loads(to_json(parse_workflow("A 然后 B 同时 C", name="t")))
        self.assertEqual(d["name"], "t"); self.assertGreaterEqual(len(d["steps"]), 2)
    def test_ids_unique(self):
        ids = [s.id for s in parse_workflow("X 然后 Y 然后 Z").steps]
        self.assertEqual(len(ids), len(set(ids)))
    def test_llm_no_key_returns_none(self):
        old = os.environ.pop("OPENAI_API_KEY", None)
        try: self.assertIsNone(llm_parse("随便一句"))
        finally:
            if old: os.environ["OPENAI_API_KEY"] = old


if __name__ == "__main__": unittest.main()
