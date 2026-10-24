#!/usr/bin/env python3
"""
Interactive & CLI Query Script for RAG-Anything / LightRAG Knowledge Graph.
Supports local, global, hybrid, and naive search modes on persisted rag_storage.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Ensure active python's bin directory is in PATH for subprocesses
env_bin = os.path.join(sys.prefix, "bin")
if env_bin not in os.environ.get("PATH", "").split(os.pathsep):
    os.environ["PATH"] = f"{env_bin}{os.pathsep}{os.environ.get('PATH', '')}"

from config import (
    DEFAULT_EMBEDDING_DIM,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_VISION_MODEL,
    LOCAL_LLM_API_KEY,
    LOCAL_LLM_BASE_URL,
    RAG_STORAGE_DIR,
)
from ingest_rag import setup_rag_anything_engine
from lightrag import QueryParam


async def run_query(
    query_text: str,
    mode: str = "hybrid",
    top_k: int = 20,
    storage_dir: Path = RAG_STORAGE_DIR,
    base_url: str = LOCAL_LLM_BASE_URL,
    llm_model: str = DEFAULT_LLM_MODEL,
):
    """
    Executes a query against the persisted LightRAG knowledge graph.
    """
    if not storage_dir.exists() or not (storage_dir / "graph_chunk_entity_relation.graphml").exists():
        print(f"❌ Error: RAG storage directory or graph not found at {storage_dir}")
        print("Please run ingest_rag.py --execute first.")
        sys.exit(1)

    print(f"\n🧠 Initializing RAG Engine from: {storage_dir}")
    print(f"   Model: {llm_model} | Mode: {mode.upper()} | Top-K: {top_k}")

    rag = setup_rag_anything_engine(
        base_url=base_url,
        llm_model=llm_model,
        storage_dir=storage_dir,
    )

    # Ensure LightRAG is ready (parser check not needed for querying)
    rag._parser_installation_checked = True
    await rag._ensure_lightrag_initialized()

    param = QueryParam(
        mode=mode,
        top_k=top_k,
    )

    print(f"\n🔍 Query: \"{query_text}\"")
    print("-" * 60)

    try:
        response = await rag.lightrag.aquery(query_text, param=param)
        print("\n📝 Response:\n")
        print(response)
        print("-" * 60)
        return response
    except Exception as e:
        print(f"\n❌ Query failed: {e}")
        return None


async def interactive_mode(
    mode: str = "hybrid",
    storage_dir: Path = RAG_STORAGE_DIR,
    base_url: str = LOCAL_LLM_BASE_URL,
    llm_model: str = DEFAULT_LLM_MODEL,
):
    """
    Interactive shell for querying the knowledge graph continuously.
    """
    print("=" * 60)
    print(" 🏥 MEDICAL RAG-ANYTHING INTERACTIVE QUERY SHELL")
    print(f"   Storage: {storage_dir}")
    print(f"   Model:   {llm_model}")
    print(f"   Default Mode: {mode}")
    print("   Type 'exit' or 'quit' to stop.")
    print("   Change mode anytime by typing: /mode <local|global|hybrid|naive>")
    print("=" * 60)

    rag = setup_rag_anything_engine(
        base_url=base_url,
        llm_model=llm_model,
        storage_dir=storage_dir,
    )
    # Parser check not needed for querying
    rag._parser_installation_checked = True
    await rag._ensure_lightrag_initialized()

    current_mode = mode

    while True:
        try:
            user_input = input(f"\n[{current_mode.upper()}] Ask a clinical question > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting query shell. Goodbye!")
                break

            if user_input.startswith("/mode"):
                parts = user_input.split()
                if len(parts) > 1 and parts[1].lower() in ("local", "global", "hybrid", "naive", "mix"):
                    current_mode = parts[1].lower()
                    print(f"Switched query mode to: {current_mode.upper()}")
                else:
                    print("Usage: /mode <local|global|hybrid|naive|mix>")
                continue

            param = QueryParam(mode=current_mode)
            print(f"\n⏳ Searching Knowledge Graph ({current_mode})...")
            response = await rag.lightrag.aquery(user_input, param=param)
            print("\n" + "=" * 50)
            print(response)
            print("=" * 50)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting query shell.")
            break
        except Exception as e:
            print(f"\n❌ Error processing query: {e}")


def main():
    parser = argparse.ArgumentParser(description="Query the Medical RAG-Anything Knowledge Graph.")
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Question to query. If omitted, enters interactive mode.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="hybrid",
        choices=["local", "global", "hybrid", "naive", "mix"],
        help="Query mode: local (entity focus), global (community themes), hybrid (both), naive (vector only).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=20,
        help="Number of top chunks/entities to retrieve.",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default=DEFAULT_LLM_MODEL,
        help=f"Local LLM model name (default: {DEFAULT_LLM_MODEL}).",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=LOCAL_LLM_BASE_URL,
        help=f"Local OpenAI-compatible API URL (default: {LOCAL_LLM_BASE_URL}).",
    )
    args = parser.parse_args()

    if args.query:
        asyncio.run(
            run_query(
                query_text=args.query,
                mode=args.mode,
                top_k=args.top_k,
                llm_model=args.llm_model,
                base_url=args.base_url,
            )
        )
    else:
        asyncio.run(
            interactive_mode(
                mode=args.mode,
                llm_model=args.llm_model,
                base_url=args.base_url,
            )
        )


if __name__ == "__main__":
    main()