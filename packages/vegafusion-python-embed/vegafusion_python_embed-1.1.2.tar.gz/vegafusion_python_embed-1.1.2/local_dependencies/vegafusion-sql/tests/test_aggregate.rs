#[macro_use]
extern crate lazy_static;

mod utils;
use datafusion_expr::{avg, col, count, expr, lit, max, min, round, sum, AggregateFunction, Expr};
use rstest::rstest;
use rstest_reuse::{self, *};
use serde_json::json;
use std::ops::{Div, Mul};
use utils::{check_dataframe_query, dialect_names, make_connection, TOKIO_RUNTIME};
use vegafusion_common::data::table::VegaFusionTable;
use vegafusion_sql::dataframe::SqlDataFrame;

#[cfg(test)]
mod test_simple_aggs {
    use crate::*;

    #[apply(dialect_names)]
    async fn test(#[case] dialect_name: &str) {
        println!("{dialect_name}");
        let (conn, evaluable) = TOKIO_RUNTIME.block_on(make_connection(dialect_name));

        let table = VegaFusionTable::from_json(
            &json!([
                {"a": 1, "b": 2, "c": "A"},
                {"a": 3, "b": 2, "c": "BB"},
                {"a": 5, "b": 3, "c": "CCC"},
                {"a": 7, "b": 3, "c": "DDDD"},
                {"a": 9, "b": 3, "c": "EEEEE"},
                {"a": 11, "b": 3, "c": "FFFFFF"},
            ]),
            1024,
        )
        .unwrap();

        let df = SqlDataFrame::from_values(&table, conn, Default::default()).unwrap();
        let df = df
            .aggregate(
                vec![col("b")],
                vec![
                    min(col("a")).alias("min_a"),
                    max(col("a")).alias("max_a"),
                    avg(col("a")).alias("avg_a"),
                    sum(col("a")).alias("sum_a"),
                    count(col("a")).alias("count_a"),
                ],
            )
            .await
            .unwrap();
        let df_result = df
            .sort(
                vec![Expr::Sort(expr::Sort {
                    expr: Box::new(col("b")),
                    asc: true,
                    nulls_first: true,
                })],
                None,
            )
            .await;

        check_dataframe_query(
            df_result,
            "aggregate",
            "simple_aggs",
            dialect_name,
            evaluable,
        );
    }

    #[test]
    fn test_marker() {} // Help IDE detect test module
}

#[cfg(test)]
mod test_median_agg {
    use crate::*;

    #[apply(dialect_names)]
    async fn test(dialect_name: &str) {
        println!("{dialect_name}");
        let (conn, evaluable) = TOKIO_RUNTIME.block_on(make_connection(dialect_name));

        let table = VegaFusionTable::from_json(
            &json!([
                {"a": 1, "b": 2},
                {"a": 3, "b": 2},
                {"a": 5.5, "b": 3},
                {"a": 7.5, "b": 3},
                {"a": 100, "b": 3},
            ]),
            1024,
        )
        .unwrap();

        let df = SqlDataFrame::from_values(&table, conn, Default::default()).unwrap();
        let df_result = df
            .aggregate(
                vec![],
                vec![
                    count(col("a")).alias("count_a"),
                    Expr::AggregateFunction(expr::AggregateFunction {
                        fun: AggregateFunction::Median,
                        args: vec![col("a")],
                        distinct: false,
                        filter: None,
                    })
                    .alias("median_a"),
                ],
            )
            .await;

        check_dataframe_query(
            df_result,
            "aggregate",
            "median_agg",
            dialect_name,
            evaluable,
        );
    }

    #[test]
    fn test_marker() {} // Help IDE detect test module
}

#[cfg(test)]
mod test_variance_aggs {
    use crate::*;

    #[apply(dialect_names)]
    async fn test(dialect_name: &str) {
        println!("{dialect_name}");
        let (conn, evaluable) = TOKIO_RUNTIME.block_on(make_connection(dialect_name));

        let table = VegaFusionTable::from_json(
            &json!([
                {"a": 1, "b": 2},
                {"a": 3, "b": 2},
                {"a": 5, "b": 3},
                {"a": 7, "b": 3},
                {"a": 9, "b": 3},
            ]),
            1024,
        )
        .unwrap();

        let df = SqlDataFrame::from_values(&table, conn, Default::default()).unwrap();
        let df_result = df
            .aggregate(
                vec![col("b")],
                vec![
                    round(
                        Expr::AggregateFunction(expr::AggregateFunction {
                            fun: AggregateFunction::Stddev,
                            args: vec![col("a")],
                            distinct: false,
                            filter: None,
                        })
                        .mul(lit(100)),
                    )
                    .div(lit(100))
                    .alias("stddev_a"),
                    round(
                        Expr::AggregateFunction(expr::AggregateFunction {
                            fun: AggregateFunction::StddevPop,
                            args: vec![col("a")],
                            distinct: false,
                            filter: None,
                        })
                        .mul(lit(100)),
                    )
                    .div(lit(100))
                    .alias("stddev_pop_a"),
                    round(
                        Expr::AggregateFunction(expr::AggregateFunction {
                            fun: AggregateFunction::Variance,
                            args: vec![col("a")],
                            distinct: false,
                            filter: None,
                        })
                        .mul(lit(100)),
                    )
                    .div(lit(100))
                    .alias("var_a"),
                    round(
                        Expr::AggregateFunction(expr::AggregateFunction {
                            fun: AggregateFunction::VariancePop,
                            args: vec![col("a")],
                            distinct: false,
                            filter: None,
                        })
                        .mul(lit(100)),
                    )
                    .div(lit(100))
                    .alias("var_pop_a"),
                ],
            )
            .await;
        let df_result = if let Ok(df) = df_result {
            df.sort(
                vec![Expr::Sort(expr::Sort {
                    expr: Box::new(col("b")),
                    asc: true,
                    nulls_first: true,
                })],
                None,
            )
            .await
        } else {
            df_result
        };

        check_dataframe_query(
            df_result,
            "aggregate",
            "variance_aggs",
            dialect_name,
            evaluable,
        );
    }

    #[test]
    fn test_marker() {} // Help IDE detect test module
}
