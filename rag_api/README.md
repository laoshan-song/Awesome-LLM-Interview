# RAG API

这是 `cheatsheet.html` 的后端 RAG 服务，负责把 55 个授权公开 PDF 的静态 chunk 索引升级为标准检索增强问答流程。

## 流程

1. 读取 `assets/local_pdf_rag_index.json` 中的 PDF chunk、标题、主题、页码和 PDF 链接。
2. 使用 `BAAI/bge-small-zh-v1.5` 生成 chunk embedding，并缓存到 `rag_api/data/`。
3. 查询时使用同一个 embedding 模型生成 query embedding。
4. 执行 hybrid retrieval：向量 cosine similarity + BM25 风格关键词分数。
5. 可选使用 `BAAI/bge-reranker-v2-m3` 对候选片段重排。
6. 可选调用 OpenAI 模型生成带引用答案；未配置 `OPENAI_API_KEY` 时返回抽取式证据回答。

## 本地启动

```bash
cd rag_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

首次启动会下载 embedding 模型并构建向量缓存。模型默认是 `BAAI/bge-small-zh-v1.5`；如果机器内存和下载条件允许，可以改成 `BAAI/bge-m3`。

`bge-small-zh-v1.5` 查询侧默认使用 `QUERY_PREFIX=为这个句子生成表示以用于检索相关文章：`，用于贴近 BGE 的检索式 embedding 用法。

Windows 注意：如果 `python` 指向 `C:\Users\<你>\AppData\Local\Microsoft\WindowsApps\python.exe`，那只是 Microsoft Store 的 App Execution Alias，不是真正的 Python。建议安装 python.org 的标准 CPython，并用真实路径创建虚拟环境；本项目已验证 Python 3.11 可运行。

验证命令：

```bash
python -m py_compile app.py
python -c "import fastapi, sentence_transformers, numpy; print('imports ok')"
```

## API

```bash
curl -X POST http://localhost:8000/api/rag/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Transformer 为什么比 RNN 更适合长距离依赖？\",\"top_k\":5}"
```

响应包含：

- `answer`：带引用编号的回答。
- `citations`：PDF 标题、页码、片段、PDF 直链和分数。
- `embedding_model`：当前 embedding 模型。
- `mode`：`extractive` 或 `llm`。

## 前端接入

在浏览器控制台或页面配置中设置：

```js
localStorage.setItem('awesome_llm_rag_api_url', 'http://localhost:8000')
```

之后网页 PDF RAG 会优先调用后端 API；API 不可用时自动回退到浏览器端轻量检索。

## 部署建议

- 小型 CPU 机器：`BAAI/bge-small-zh-v1.5`，关闭 reranker。
- 更高质量：`BAAI/bge-m3` + `BAAI/bge-reranker-v2-m3`。
- 生产环境：把 `ALLOW_ORIGINS` 限制为 GitHub Pages 域名和你的 API 域名。

Docker 构建建议在仓库根目录执行：

```bash
docker build -f rag_api/Dockerfile -t awesome-llm-rag-api .
docker run --rm -p 8000:8000 awesome-llm-rag-api
```
