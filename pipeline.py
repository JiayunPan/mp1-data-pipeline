"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""
from data_loaders import load_data
import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the pipeline."""
    # 根据 verbose 决定门槛(level)：True→DEBUG(显示全部)，False→INFO(挡住DEBUG)
    level = logging.DEBUG if verbose else logging.INFO

    # 配置日志系统：设定门槛 + 每条消息的排版格式
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",  # 时间 等级 消息
        datefmt="%H:%M:%S",  # 时间只显示 时:分:秒
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    # 创建一个"点单员"，description 是这个程序的简介
    parser = argparse.ArgumentParser(description="A command-line data pipeline.")

    # --input / -i：必填，输入文件路径
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file",
    )

    # --output / -o：必填，输出文件路径
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file",
    )

    # --format：可选，只能填 csv 或 json，默认 csv
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format: csv or json (default: csv)",
    )

    # --verbose / -v：可选开关，写了就是 True，不写就是 False
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    # 让点单员真正去读用户敲的参数，把结果打包返回
    return parser.parse_args()


def validate_input(filepath: str) -> bool:
    """Check whether the input path exists and is a file."""
    # 问一句：这个路径是不是一个真实存在的文件？
    if Path(filepath).is_file():
        # 是 → 记一条 INFO 日志，返回 True
        logger.info("Input file validated: %s", filepath)
        return True
    # 不是 → 记一条 ERROR 日志，返回 False
    logger.error("Input file not found: %s", filepath)
    return False


def main() -> None:
    """Main pipeline function."""
    # 1. 读命令行参数，拿到那张"订单卡"
    args = parse_arguments()

    # 2. 根据 --verbose 配置日志系统
    setup_logging(args.verbose)

    # 3. 把读到的参数用 DEBUG 级别记下来（方便排查）
    logger.debug(
        "Arguments parsed: input=%s, output=%s, format=%s",
        args.input, args.output, args.format,
    )

    # 4. 验证输入文件是否存在
    # 5. 无效就以状态码 1 退出
    if not validate_input(args.input):
        sys.exit(1)
    try:
        data = load_data(args.input)
    except ValueError:
        sys.exit(1)


if __name__ == "__main__":
    main()