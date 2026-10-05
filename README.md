# workflow-gen-lite

零依赖的自然语言 → 工作流 JSON 小工具。把一句话切分成带顺序/并行标记的步骤列表，输出结构化 JSON。可选 LLM 解析（urllib 直连 OpenAI 兼容接口），无 key 自动降级为规则解析。

## 快速开始

```bash
python -m workflow_gen_lite "打开冰箱然后放大象，同时拍照，最后关门" --name "装大象"
```

## 无 API Key 如何运行

不加 --llm 时就是纯规则解析，完全离线，不需要任何 Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
