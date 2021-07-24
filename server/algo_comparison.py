from dataclasses import dataclass
from typing import List

from server.statistics.stats_reporter import StatsReporter, ComparisonData


@dataclass
class ComparisonListData:
    total_waiting_time: List[int]
    total_neg_acc_time: List[int]
    avg_car_waiting: List[float]
    median_car_waiting: List[float]
    var_car_waiting: List[float]
    car_num: int
    # total_waiting_df: DataFrame
    # cars_waiting_df: DataFrame
    avg_car_neg_acc: List[float]
    median_car_neg_acc: List[float]
    var_car_neg_acc: List[float]
    # total_neg_acc_df: DataFrame
    # cars_neg_acc_df: DataFrame


def collect_reports(reporters: List[StatsReporter]):
    for reporter in reporters:
        data: ComparisonData = reporter.report_compare()

