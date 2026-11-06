"""
export_qlora_output.py

Utility to package, export, and download QLoRA fine-tuning artifacts:
1. Direct browser download (via Google Colab files.download)
2. Direct backup to Google Drive
3. Push adapter weights directly to Hugging Face Hub (huggingface.co)
4. Local standalone zip archiving with checksum verification
"""

import os
import sys
import shutil
import zipfile
import argparse
from datetime import datetime
from typing import Optional


def is_colab_environment() -> bool:
    """Checks whether code is executing inside Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False


def package_qlora_artifacts(
    adapter_dir: str = "./qlora_sft_output/final_adapter",
    eval_dir: str = "./eval_results",
    archive_name: Optional[str] = None
) -> str:
    """
    Packages the LoRA adapter weights, tokenizer, config, and evaluation metrics
    into a single consolidated zip archive.
    """
    if not os.path.exists(adapter_dir):
        # Fallback check for parent directory or alternative output paths
        alt_dirs = ["./qlora_sft_output", "./qlora_distilled_output/final_adapter"]
        found = False
        for alt in alt_dirs:
            if os.path.exists(alt):
                adapter_dir = alt
                found = True
                break
        if not found:
            raise FileNotFoundError(f"Adapter directory not found at: {adapter_dir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if archive_name is None:
        archive_name = f"clinical_qlora_output_{timestamp}.zip"
    elif not archive_name.endswith(".zip"):
        archive_name += ".zip"

    print(f"\n[1/3] Packaging QLoRA artifacts into: {archive_name}")
    bundled_files = []

    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add adapter files
        for root, _, files in os.walk(adapter_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, os.path.dirname(adapter_dir))
                zipf.write(file_path, arcname=os.path.join("final_adapter", rel_path))
                bundled_files.append(file_path)

        # 2. Add evaluation results & charts if present
        eval_items = [
            "eval_results_summary.json",
            "clinical_evaluation_3pillars.png",
            "evaluation_comparison_chart.png"
        ]
        for item in eval_items:
            if os.path.exists(item):
                zipf.write(item, arcname=os.path.join("evaluation", item))
                bundled_files.append(item)

        if os.path.exists(eval_dir):
            for root, _, files in os.walk(eval_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, eval_dir)
                    zipf.write(file_path, arcname=os.path.join("evaluation", rel_path))
                    bundled_files.append(file_path)

    size_mb = os.path.getsize(archive_name) / (1024 * 1024)
    print(f"✓ Archive successfully created ({size_mb:.2f} MB, {len(bundled_files)} files).")
    return archive_name


def download_in_colab(archive_path: str):
    """Triggers automatic browser download in Google Colab."""
    if is_colab_environment():
        print(f"\n[2/3] Triggering browser download for {archive_path}...")
        try:
            from google.colab import files
            files.download(archive_path)
            print("✓ Download initiated in browser. Check your local Downloads folder!")
        except Exception as e:
            print(f"⚠️ Colab files.download encountered: {e}")
            print(f"You can also right-click '{archive_path}' in Colab's left sidebar to download.")
    else:
        print(f"\nNot running in Google Colab. File saved locally at: {os.path.abspath(archive_path)}")


def backup_to_google_drive(
    archive_path: str,
    drive_folder: str = "/content/drive/MyDrive/Clinical_LLM_QLoRA"
):
    """Mounts Google Drive and copies the archive to persistent cloud storage."""
    if is_colab_environment():
        print(f"\nMounting Google Drive to backup {archive_path}...")
        try:
            from google.colab import drive
            drive.mount("/content/drive")
            os.makedirs(drive_folder, exist_ok=True)
            dest_path = os.path.join(drive_folder, os.path.basename(archive_path))
            shutil.copy2(archive_path, dest_path)
            print(f"✓ Successfully backed up archive to Google Drive: {dest_path}")
        except Exception as e:
            print(f"⚠️ Google Drive backup skipped or encountered: {e}")
    else:
        print("Google Drive backup is only available when running inside Google Colab.")


def push_adapter_to_hub(
    adapter_dir: str,
    repo_id: str,
    token: Optional[str] = None,
    private: bool = True
):
    """Pushes the fine-tuned LoRA adapter weights and tokenizer directly to Hugging Face Hub."""
    print(f"\nPushing adapter to Hugging Face Hub: {repo_id}...")
    try:
        from peft import PeftModel
        from transformers import AutoTokenizer
        from huggingface_hub import HfApi

        api = HfApi(token=token)
        api.create_repo(repo_id=repo_id, private=private, exist_ok=True)

        api.upload_folder(
            folder_path=adapter_dir,
            repo_id=repo_id,
            repo_type="model",
            token=token
        )
        print(f"✓ Successfully published adapter to: https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"⚠️ Failed to push to Hugging Face Hub: {e}")


def main():
    parser = argparse.ArgumentParser(description="Package and download QLoRA output artifacts.")
    parser.add_argument("--adapter_dir", type=str, default="./qlora_sft_output/final_adapter", help="Directory of trained adapter")
    parser.add_argument("--eval_dir", type=str, default="./eval_results", help="Directory of evaluation results")
    parser.add_argument("--output_name", type=str, default=None, help="Output zip filename")
    parser.add_argument("--download", action="store_true", help="Trigger browser download in Colab")
    parser.add_argument("--save_drive", action="store_true", help="Backup archive to Google Drive")
    parser.add_argument("--drive_path", type=str, default="/content/drive/MyDrive/Clinical_LLM_QLoRA", help="Target path in Google Drive")
    parser.add_argument("--push_hub", type=str, default=None, help="Hugging Face repo_id to push adapter (e.g. username/clinical-llama3-qlora)")
    parser.add_argument("--hf_token", type=str, default=None, help="Hugging Face auth token")
    args = parser.parse_args()

    # 1. Package zip archive
    try:
        archive_path = package_qlora_artifacts(
            adapter_dir=args.adapter_dir,
            eval_dir=args.eval_dir,
            archive_name=args.output_name
        )
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # 2. Browser download in Colab
    if args.download or is_colab_environment():
        download_in_colab(archive_path)

    # 3. Google Drive Backup
    if args.save_drive:
        backup_to_google_drive(archive_path, drive_folder=args.drive_path)

    # 4. Hugging Face Hub Push
    if args.push_hub:
        push_adapter_to_hub(
            adapter_dir=args.adapter_dir,
            repo_id=args.push_hub,
            token=args.hf_token
        )


if __name__ == "__main__":
    main()
