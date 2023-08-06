from itertools import repeat
from typing import Any, Iterable, Mapping, Optional

from pyspark.sql import DataFrame
from pyspark.sql.types import Row

from aporia.core.errors import AporiaError
from aporia.inference.inference_model import InferenceModel
from aporia.pyspark.experimental.batch_api import log_batch_prediction, log_streaming_prediction


class PySparkPrediction:
    """PySpark prediction representation."""

    def __init__(
        self,
        id: Optional[Row] = None,
        features: Optional[Row] = None,
        predictions: Optional[Row] = None,
        raw_inputs: Optional[Row] = None,
        actuals: Optional[Row] = None,
    ):
        """Initializes a PySparkPrediction.

        Args:
            id: Prediction ID.
            features: Prediction features.
            predictions: Prediction results.
            raw_inputs: Prediction raw inputs.
            actuals: Prediction actual results.
        """
        self.id = id[0] if id is not None else None
        self.features = None
        if features is not None:
            self.features = features.asDict()

        self.predictions = None
        if predictions is not None:
            self.predictions = predictions.asDict()

        self.raw_inputs = None
        if raw_inputs is not None:
            self.raw_inputs = raw_inputs.asDict()

        self.actuals = None
        if actuals is not None:
            self.actuals = actuals.asDict()


class PySparkInferenceModel:
    """Model object for reporting PySpark dataframes."""

    def __init__(self, inference_model: InferenceModel):
        """Initliazes a PySparkInferenceModel.

        Args:
            inference_model: An inference model object, which will be used to
                report the actual predictions.
        """
        self._inference_model = inference_model

    def log_batch_pyspark_raw_inputs(self, ids: DataFrame, raw_inputs: DataFrame):
        """See aporia.model.Model."""
        with self._inference_model.handle_error(
            "Logging PySpark raw_inputs batch failed, error: {}"
        ):
            self._validate_pyspark_dataframes(ids=ids, dataframes=[raw_inputs])

            for prediction in self._iter_pyspark_prediction_dataframes(
                ids=ids, raw_inputs=raw_inputs
            ):
                self._inference_model.log_raw_inputs(
                    id=prediction.id, raw_inputs=prediction.raw_inputs
                )

    def log_batch_pyspark_actuals(self, ids: DataFrame, actuals: DataFrame):
        """See aporia.model.Model."""
        with self._inference_model.handle_error("Logging PySpark actuals batch failed, error: {}"):
            self._validate_pyspark_dataframes(ids=ids, dataframes=[actuals])

            for prediction in self._iter_pyspark_prediction_dataframes(ids=ids, actuals=actuals):
                self._inference_model.log_actuals(id=prediction.id, actuals=prediction.actuals)

    def log_batch_pyspark_prediction(
        self,
        version_id: str,
        data: DataFrame,
        model: Any,
        id_column: Optional[str] = None,
        features: Optional[Mapping[str, str]] = None,
        predictions: Optional[Mapping[str, str]] = None,
        timestamp_column: Optional[str] = None,
        raw_inputs: Optional[Mapping[str, str]] = None,
        labels: Optional[Mapping[str, str]] = None,
        spark_options: Optional[Mapping[str, str]] = None,
        date_format: Optional[str] = None,
    ):
        """See aporia.model.Model."""
        with self._inference_model.handle_error(
            "Logging PySpark prediction batch failed, error: {}"
        ):
            log_batch_prediction(
                version_id=version_id,
                apr_model=model,
                data=data,
                id_column=id_column,
                features=features,
                predictions=predictions,
                timestamp_column=timestamp_column,
                raw_inputs=raw_inputs,
                labels=labels,
                spark_options=spark_options,
                date_format=date_format,
            )

    def log_streaming_pyspark_prediction(
        self,
        version_id: str,
        data: DataFrame,
        model: Any,
        id_column: Optional[str] = None,
        features: Optional[Mapping[str, str]] = None,
        predictions: Optional[Mapping[str, str]] = None,
        timestamp_column: Optional[str] = None,
        raw_inputs: Optional[Mapping[str, str]] = None,
        labels: Optional[Mapping[str, str]] = None,
        spark_options: Optional[Mapping[str, str]] = None,
        date_format: Optional[str] = None,
    ):
        """See aporia.model.Model."""
        with self._inference_model.handle_error(
            "Logging PySpark prediction batch failed, error: {}"
        ):
            log_streaming_prediction(
                version_id=version_id,
                apr_model=model,
                data=data,
                id_column=id_column,
                features=features,
                predictions=predictions,
                timestamp_column=timestamp_column,
                raw_inputs=raw_inputs,
                labels=labels,
                spark_options=spark_options,
                date_format=date_format,
            )

    @staticmethod
    def _validate_pyspark_dataframes(
        ids: DataFrame,
        dataframes: Iterable[Optional[DataFrame]],
    ):
        if ids is None:
            return

        expected_count = ids.count()
        for dataframe in dataframes:
            if dataframe is None:
                continue

            if dataframe.count() != expected_count:
                raise AporiaError("PySpark dataframe sizes do not match.")

        if len(ids.columns) != 1:
            raise AporiaError("Ids dataframe must contain exactly one column.")

    @staticmethod
    def _iter_pyspark_prediction_dataframes(
        ids: Optional[DataFrame] = None,
        features: Optional[DataFrame] = None,
        predictions: Optional[DataFrame] = None,
        raw_inputs: Optional[DataFrame] = None,
        actuals: Optional[DataFrame] = None,
    ) -> Iterable[PySparkPrediction]:

        ids_iter = repeat(None)
        if ids is not None:
            ids_iter = ids.toLocalIterator()  # type: ignore

        features_iter = repeat(None)
        if features is not None:
            features_iter = features.toLocalIterator()  # type: ignore

        predictions_iter = repeat(None)
        if predictions is not None:
            predictions_iter = predictions.toLocalIterator()  # type: ignore

        raw_inputs_iter = repeat(None)
        if raw_inputs is not None:
            raw_inputs_iter = raw_inputs.toLocalIterator()  # type: ignore

        actuals_iter = repeat(None)
        if actuals is not None:
            actuals_iter = actuals.toLocalIterator()  # type: ignore

        for id_row, features_row, predictions_row, raw_inputs_row, actuals_row in zip(
            ids_iter,
            features_iter,
            predictions_iter,
            raw_inputs_iter,
            actuals_iter,
        ):
            yield PySparkPrediction(
                id=id_row,
                features=features_row,
                predictions=predictions_row,
                raw_inputs=raw_inputs_row,
                actuals=actuals_row,
            )
