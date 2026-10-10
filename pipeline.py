"""
Data Processing Pipeline - CLI

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample.csv --output clean.csv --config config.yaml
    python pipeline.py --input fixtures/sample.csv --output clean.csv --config config.yaml --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="A command-line data pipeline.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True, help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def validate_input(filepath: str) -> bool:
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info("Input file validated: %s", filepath)
        return True
    logger.error("Input file not found: %s", filepath)
    return False


def main() -> None:
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config,
    )

    # 1. 验证输入文件 + 配置文件（任一不存在就退出）
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # 2. 加载输入数据和配置（同一个 try，捕获不支持格式的 ValueError）
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # 3. 先存一份原始数据副本（用来对比、生成清洗报告）
    original = data.copy()

    # 4. 处理数据（单独的 try；process_data 内部抛的异常在这里兜底）
    try:
        cleaned = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # 5. 记录处理结果
    report = create_cleaning_report(original, cleaned)
    logger.info("Processing complete: %d → %d rows", len(original), len(cleaned))

    # 6. 保存清洗后的数据为 CSV（不带 index 行号）+ 记录保存结果
    cleaned.to_csv(args.output, index=False)
    logger.info("Saved cleaned data to %s", args.output)

    # 7. 打印清洗报告
    print(report)


if __name__ == "__main__":
    main()