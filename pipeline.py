"""
Data Processing Pipeline - CLI

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="A command-line data pipeline.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True, help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def main() -> None:
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config,
    )

    # 1. 验证输入文件 + 配置文件
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # 2. 加载输入数据和配置
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # 3. 从配置读取验证所需的列设置
    validation = config["validation"]
    required_columns = validation["required_columns"]
    numeric_columns = validation["numeric_columns"]

    # 4. 验证数据（单独的 try；validate_dataframe 抛的异常在这里兜底）
    try:
        validated = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d → %d rows", len(data), len(validated))

    # 5. 处理数据（用验证后的 validated）
    original = validated.copy()
    try:
        cleaned = process_data(validated, config)
    except ValueError:
        sys.exit(1)
    logger.info("Processing complete: %d → %d rows", len(original), len(cleaned))

    # 6. 保存清洗后的数据
    save_data(cleaned, args.output)
    logger.info("Saved cleaned data to %s", args.output)

    # 7. 生成并打印清洗报告（放在 main 最后）
    report = create_cleaning_report(original, cleaned)
    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()