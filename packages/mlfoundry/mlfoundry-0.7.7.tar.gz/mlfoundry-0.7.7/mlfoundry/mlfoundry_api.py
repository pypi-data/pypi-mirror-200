"""
# TO independently test this module, you can run the example in the path
python examples/sklearn/iris_train.py

Besides running pytest
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Generator, Iterator, List, Optional, Sequence, Union

import coolname
import mlflow
import pandas as pd
from mlflow.entities import ArtifactType
from mlflow.store.tracking import SEARCH_MAX_RESULTS_DEFAULT
from mlflow.tracking import MlflowClient

from mlfoundry import amplitude, constants, env_vars
from mlfoundry.enums import ViewType
from mlfoundry.env_vars import TRACKING_HOST_GLOBAL
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.internal_namespace import NAMESPACE
from mlfoundry.log_types.artifacts.artifact import ArtifactVersion
from mlfoundry.log_types.artifacts.model import ModelVersion
from mlfoundry.logger import logger
from mlfoundry.mlfoundry_run import MlFoundryRun
from mlfoundry.monitoring.entities import Actual, Prediction
from mlfoundry.monitoring.store import MonitoringClient
from mlfoundry.session import Session, init_session


def _get_internal_env_vars_values() -> Dict[str, str]:
    env = {}
    for env_var_name in env_vars.INTERNAL_ENV_VARS:
        value = os.getenv(env_var_name)
        if value:
            env[env_var_name] = value

    return env


def get_client(disable_analytics: bool = False) -> MlFoundry:
    """Initializes and returns the mlfoundry client.

    Args:
        disable_analytics (bool, optional): To turn off usage analytics collection, pass `True`.
            By default, this is set to `False`.

    Returns:
        MlFoundry: Instance of `MlFoundry` class which represents a `run`.

    Examples:
    ### Get client
    ```python
    import mlfoundry

    client = mlfoundry.get_client()
    ```
    """
    # TODO (chiragjn): Will potentially need to make MlFoundry (and possibly MlFoundryRun) a Singleton instance.
    #                  Since this sets the tracking URI in global namespace, if someone were to call
    #                  get_client again with different tracking uri, the ongoing run's data will start getting
    #                  pushed to another datastore. Or we should not allow passing in tracking URI and just have
    #                  fixed online and offline clients

    user_id = amplitude.NO_USER

    session = None

    # NOTE: hack to run tests
    if os.getenv(TRACKING_HOST_GLOBAL, "").startswith("file:"):
        tracking_uri = os.getenv(TRACKING_HOST_GLOBAL)
        tracking_uri = os.path.join(tracking_uri, constants.MLRUNS_FOLDER_NAME)
        mlflow.set_tracking_uri(tracking_uri)
    else:
        session = init_session()
        user_id = session.user_info.user_id

    amplitude.init(user_id=user_id, disable_analytics=disable_analytics)
    amplitude.track(amplitude.Event.GET_CLIENT)
    return MlFoundry(session=session)


def resolve_project_name(
    ml_repo: Optional[str] = None,
    project_name: Optional[str] = None,
) -> str:
    if project_name and ml_repo:
        raise MlFoundryException(
            f"Only one of field project_name or ml_repo should be passed"
        )
    if not project_name and not ml_repo:
        raise MlFoundryException(f"ml_repo must be string type and cannot be empty")
    if ml_repo:
        project_name = ml_repo
    if project_name == "" or (not isinstance(project_name, str)):
        raise MlFoundryException(
            f"ml_repo must be string type and not empty. "
            f"Got {type(project_name)} type with value {project_name!r}"
        )
    return project_name


class MlFoundry:
    """MlFoundry."""

    def __init__(self, session: Optional[Session] = None):
        """__init__.

        Args:
            tracking_uri (Optional[str], optional): tracking_uri
        """
        self.mlflow_client = MlflowClient()
        if session:
            self.monitoring_client = MonitoringClient(session=session)

    def _get_or_create_project(self, project_name: str) -> str:
        """_get_or_create_experiment.

        Args:
            project_name (str): The name of the project.

        Returns:
            str: The id of the project.
        """
        experiment_name = project_name
        try:
            experiment = self.mlflow_client.get_experiment_by_name(experiment_name)
            if experiment is not None:
                return experiment.experiment_id
            else:
                logger.info(
                    f"project {experiment_name} does not exist. Creating {experiment_name}."
                )
                return self.mlflow_client.create_experiment(experiment_name)

        except MlflowException as e:
            err_msg = (
                f"Error happened in creating or getting project based on project name: "
                f"{experiment_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def get_all_projects(self) -> List[str]:
        """Returns a list of project ids accessible by the current user.

        Returns:
            List[str]: A list of project ids.
        """
        amplitude.track(amplitude.Event.GET_ALL_PROJECTS)
        try:
            experiments = self.mlflow_client.list_experiments(view_type=ViewType.ALL)
        except MlflowException as e:
            err_msg = (
                f"Error happened in fetching project names. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        projects = []
        for e in experiments:
            # Experiment ID 0 represents default project which we are removing.
            if e.experiment_id != "0":
                projects.append(e.name)

        return projects

    def create_run(
        self,
        project_name: Optional[str] = None,
        ml_repo: Optional[str] = None,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> MlFoundryRun:
        """Initialize a `run`.

        In a machine learning experiment `run` represents a single experiment
        conducted under a project.
        Args:
            ml_repo (str): The name of the project under which the run will be created.
                ml_repo should only contain alphanumerics (a-z,A-Z,0-9) or hyphen (-).
                The user must have `ADMIN` or `WRITE` access to this project.
            run_name (Optional[str], optional): The name of the run. If not passed, a randomly
                generated name is assigned to the run. Under a project, all runs should have
                a unique name. If the passed `run_name` is already used under a project, the
                `run_name` will be de-duplicated by adding a suffix.
                run name should only contain alphanumerics (a-z,A-Z,0-9) or hyphen (-).
            tags (Optional[Dict[str, Any]], optional): Optional tags to attach with
                this run. Tags are key-value pairs.
            kwargs:

        Returns:
            MlFoundryRun: An instance of `MlFoundryRun` class which represents a `run`.

        Examples:
        ### Create a run under current user.
        ```python
        import mlfoundry

        client = mlfoundry.get_client()

        tags = {"model_type": "svm"}
        run = client.create_run(
            ml_repo="my-classification-project", run_name="svm-with-rbf-kernel", tags=tags
        )

        run.end()
        ```

        ### Creating a run using context manager.
        ```python
        import mlfoundry

        client = mlfoundry.get_client()
        with client.create_run(
            ml_repo="my-classification-project", run_name="svm-with-rbf-kernel"
        ) as run:
            # ...
            # Model training code
            ...
        # `run` will be automatically marked as `FINISHED` or `FAILED`.
        ```

        ### Create a run in a project owned by a different user.
        ```python
        import mlfoundry

        client = mlfoundry.get_client()

        tags = {"model_type": "svm"}
        run = client.create_run(
            ml_repo="my-classification-project",
            run_name="svm-with-rbf-kernel",
            tags=tags,
        )
        run.end()
        ```
        """
        amplitude.track(amplitude.Event.CREATE_RUN)

        if not run_name:
            run_name = coolname.generate_slug(2)
            logger.info(
                f"No run_name given. Using a randomly generated name {run_name}."
                " You can pass your own using the `run_name` argument"
            )
        project_name = resolve_project_name(ml_repo=ml_repo, project_name=project_name)

        experiment_id = self._get_or_create_project(project_name)

        if tags is not None:
            NAMESPACE.validate_namespace_not_used(tags.keys())
        else:
            tags = {}

        tags.update(_get_internal_env_vars_values())
        run = self.mlflow_client.create_run(experiment_id, name=run_name, tags=tags)
        mlf_run_id = run.info.run_id

        mlf_run = MlFoundryRun(experiment_id, mlf_run_id, **kwargs)
        # TODO(Rizwan): Revisit this once run lifecycle is formalised
        mlf_run._add_git_info()
        mlf_run._add_python_mlf_version()
        logger.info(f"Run {run.info.fqn!r} has started.")
        return mlf_run

    def get_run(self, run_id: str) -> MlFoundryRun:
        """Get an existing `run` by the `run_id`.

        Args:
            run_id (str): run_id or fqn of an existing `run`.

        Returns:
            MlFoundryRun: An instance of `MlFoundryRun` class which represents a `run`.
        """
        amplitude.track(amplitude.Event.GET_RUN)
        if run_id == "" or (not isinstance(run_id, str)):
            raise MlFoundryException(
                f"run_id must be string type and not empty. "
                f"Got {type(run_id)} type with value {run_id}"
            )
        if "/" in run_id:
            return self.get_run_by_fqn(run_id)

        run = self.mlflow_client.get_run(run_id)
        return MlFoundryRun(
            experiment_id=run.info.experiment_id,
            run_id=run.info.run_id,
        )

    def get_run_by_fqn(self, run_fqn: str) -> MlFoundryRun:
        """Get an existing `run` by `fqn`.

        `fqn` stands for Fully Qualified Name. A run `fqn` has the following pattern:
        tenant_name/ml_repo/run_name

        If  a run `svm` under the project `cat-classifier` in `truefoundry` tenant,
        the `fqn` will be `truefoundry/cat-classifier/svm`.

        Args:
            run_fqn (str): `fqn` of an existing run.

        Returns:
            MlFoundryRun: An instance of `MlFoundryRun` class which represents a `run`.
        """
        run = self.mlflow_client.get_run_by_fqn(run_fqn)
        return MlFoundryRun(
            experiment_id=run.info.experiment_id,
            run_id=run.info.run_id,
        )

    def get_all_runs(
        self,
        project_name: Optional[str] = None,
        ml_repo: Optional[str] = None,
    ) -> pd.DataFrame:
        """Returns all the run name and id present under a project.

        The user must have `READ` access to the project.
        Args:
            ml_repo (str): Name of the project.
        Returns:
            pd.DataFrame: dataframe with two columns- run_id and run_name
        """
        amplitude.track(amplitude.Event.GET_ALL_RUNS)
        resolve_project_name(ml_repo=ml_repo, project_name=project_name)
        experiment = self.mlflow_client.get_experiment_by_name(project_name)
        if experiment is None:
            return pd.DataFrame(
                columns=[constants.RUN_ID_COL_NAME, constants.RUN_NAME_COL_NAME]
            )

        experiment_id = experiment.experiment_id

        try:
            all_run_infos = self.mlflow_client.list_run_infos(
                experiment_id, run_view_type=ViewType.ALL
            )
        except MlflowException as e:
            err_msg = f"Error happened in while fetching runs for project {project_name}. Error details: {e.message}"
            raise MlFoundryException(err_msg) from e

        runs = []

        for run_info in all_run_infos:
            try:
                run = self.mlflow_client.get_run(run_info.run_id)
                run_name = run.info.name or run.data.tags.get(
                    constants.RUN_NAME_COL_NAME, ""
                )
                runs.append((run_info.run_id, run_name))
            except MlflowException as e:
                logger.warning(
                    f"Could not fetch details of run with run_id {run_info.run_id}. "
                    f"Skipping this one. Error details: {e.message}. "
                )

        return pd.DataFrame(
            runs, columns=[constants.RUN_ID_COL_NAME, constants.RUN_NAME_COL_NAME]
        )

    def search_runs(
        self,
        project_name: Optional[str] = None,
        ml_repo: Optional[str] = None,
        filter_string: str = "",
        run_view_type: str = "ACTIVE_ONLY",
        order_by: Sequence[str] = ("attribute.start_time DESC",),
    ) -> Generator[MlFoundryRun, None, None]:
        """
        The user must have `READ` access to the project.
        Returns an Generator that returns a MLFoundryRun on each next call.
        All the runs under a project which matches the filter string and the run_view_type are returned.

        Args:
            ml_repo (str): Name of the project.
            filter_string (str, optional):
                Filter query string, defaults to searching all runs. Identifier required in the LHS of a search expression.
                Signifies an entity to compare against. An identifier has two parts separated by a period: the type of the entity and the name of the entity.
                The type of the entity is metrics, params, attributes, or tags. The entity name can contain alphanumeric characters and special characters.
                You can search using two run attributes : status and artifact_uri. Both attributes have string values.
                When a metric, parameter, or tag name contains a special character like hyphen, space, period, and so on,
                enclose the entity name in double quotes or backticks, params."model-type" or params.`model-type`

            run_view_type (str, optional): one of the following values "ACTIVE_ONLY", "DELETED_ONLY", or "ALL" runs.
            order_by (List[str], optional):
                List of columns to order by (e.g., "metrics.rmse"). Currently supported values
                are metric.key, parameter.key, tag.key, attribute.key. The ``order_by`` column
                can contain an optional ``DESC`` or ``ASC`` value. The default is ``ASC``.
                The default ordering is to sort by ``start_time DESC``.

        Examples:
            ```python
            import mlfoundry as mlf

            client = mlf.get_client()
            with client.create_run(ml_repo="my-project", run_name="run-1") as run1:
                run1.log_metrics(metric_dict={"accuracy": 0.74, "loss": 0.6})
                run1.log_params({"model": "LogisticRegression", "lambda": "0.001"})

            with client.create_run(ml_repo="my-project", run_name="run-2") as run2:
                run2.log_metrics(metric_dict={"accuracy": 0.8, "loss": 0.4})
                run2.log_params({"model": "SVM"})

            # Search for the subset of runs with logged accuracy metric greater than 0.75
            filter_string = "metrics.accuracy > 0.75"
            runs = client.search_runs(ml_repo="my-project", filter_string=filter_string)

            # Search for the subset of runs with logged accuracy metric greater than 0.7
            filter_string = "metrics.accuracy > 0.7"
            runs = client.search_runs(ml_repo="my-project", filter_string=filter_string)

            # Search for the subset of runs with logged accuracy metric greater than 0.7 and model="LogisticRegression"
            filter_string = "metrics.accuracy > 0.7 and params.model = 'LogisticRegression'"
            runs = client.search_runs(ml_repo="my-project", filter_string=filter_string)

            # Search for the subset of runs with logged accuracy metric greater than 0.7 and order by accuracy in Descending  order
            filter_string = "metrics.accuracy > 0.7"
            order_by = ["metric.accuracy DESC"]
            runs = client.search_runs(
                ml_repo="my-project", filter_string=filter_string, order_by=order_by
            )

            ```

        Returns:
            Genarator[MlFoundryRun, None, None]: MLFoundryRuns matching the search query.
        """
        resolve_project_name(ml_repo=ml_repo, project_name=project_name)
        try:
            run_view_type = ViewType.from_string(run_view_type.lower())
        except Exception as e:
            raise MlFoundryException(e) from e

        try:
            experiment = self.mlflow_client.get_experiment_by_name(project_name)
        except MlflowException as e:
            raise MlFoundryException(e) from e  # user doesnot have READ permission

        if experiment is None:
            logger.warning(f"Project with name {project_name} does not exist")
            return

        experiment_id = experiment.experiment_id

        page_token = None
        done = False
        while not done:
            all_runs = self.mlflow_client.search_runs(
                experiment_ids=[experiment_id],
                filter_string=filter_string,
                run_view_type=run_view_type,
                max_results=SEARCH_MAX_RESULTS_DEFAULT,
                order_by=order_by,
                page_token=page_token,
            )
            page_token = all_runs.token
            for run in all_runs:
                yield MlFoundryRun(run.info.experiment_id, run.info.run_id)
            done = page_token is None

    @staticmethod
    def get_tracking_uri():
        """get_tracking_uri."""
        return mlflow.tracking.get_tracking_uri()

    def get_model(self, fqn: str) -> ModelVersion:
        """
        Get the model version to download contents or load it in memory

        Args:
            fqn (str): Fully qualified name of the model version.

        Examples:

            ```python
            import tempfile
            import mlfoundry

            client = mlfoundry.get_client()
            model_version = client.get_model(fqn="model:truefoundry/user/my-classification-project/my-sklearn-model:1")

            # load the model into memory
            clf = model_version.load()

            # download the model to disk
            temp = tempfile.TemporaryDirectory()
            download_info = model_version.download(path=temp.name)
            print(download_info)
            ```
        """
        # TODO (chiragjn): This API is called get_model and it returns ModelVersion
        #   This will cause confusion later when we have to eventually introduce APIs to get the parent Model class
        return ModelVersion.from_fqn(fqn)

    def list_model_versions(self, model_fqn: str) -> Iterator[ModelVersion]:
        """
        List versions for a given model

        Args:
            model_fqn: FQN of the Model to list versions for.
                A model_fqn looks like `model:{org}/{user}/{project}/{artifact_name}`
                or `model:{user}/{project}/{artifact_name}`

        Returns:
            Iterator[ModelVersion]: An iterator that yields non deleted model versions
                under the given model_fqn sorted reverse by the version number

        Yields:
            ModelVersion: An instance of `mlfoundry.ModelVersion`

        Examples:

            ```python
            import mlfoundry

            mlfoundry.login(tracking_uri=https://your.truefoundry.site.com")
            client = mlfoundry.get_client()
            model_fqn = "model:org/user/my-project/my-model"
            for mv in client.list_model_versions(model_fqn=model_fqn):
                print(mv.name, mv.version, mv.description)
            ```
        """
        model = self.mlflow_client.get_model_by_fqn(fqn=model_fqn)
        max_results = 10
        page_token = None
        done = False
        while not done:
            model_versions = self.mlflow_client.list_model_versions(
                model_id=model.id, max_results=max_results, page_token=page_token
            )
            page_token = model_versions.token
            for model_version in model_versions:
                yield ModelVersion(model_version=model_version, model=model)
            if not model_versions or not page_token:
                done = True

    def get_artifact(self, fqn: str) -> ArtifactVersion:
        """
        Get the artifact version to download contents

        Args:
            fqn (str): Fully qualified name of the artifact version.

        Examples:

            ```python
            import tempfile
            import mlfoundry

            client = mlfoundry.get_client()
            artifact_version = client.get_artifact(fqn="artifact:truefoundry/user/my-classification-project/sklearn-artifact:1")

            # download the artifact to disk
            temp = tempfile.TemporaryDirectory()
            download_info = artifact_version.download(path=temp.name)
            print(download_info)
            ```
        """
        # TODO (chiragjn): This API is called get_artifact and it returns ArtifactVersion
        #   This will cause confusion later when we have to eventually introduce APIs to get the parent Artifact class
        return ArtifactVersion.from_fqn(fqn)

    def list_artifact_versions(self, artifact_fqn: str) -> Iterator[ArtifactVersion]:
        """
        List versions for a given artifact

        Args:
            artifact_fqn: FQN of the Artifact to list versions for.
                An artifact_fqn looks like `{artifact_type}:{org}/{user}/{project}/{artifact_name}`
                or `{artifact_type}:{user}/{project}/{artifact_name}`

                where artifact_type can be on of ("model", "image", "plot")

        Returns:
            Iterator[ArtifactVersion]: An iterator that yields non deleted artifact versions
                under the given artifact_fqn sorted reverse by the version number

        Yields:
            ArtifactVersion: An instance of `mlfoundry.ArtifactVersion`

        Examples:

            Examples:

            ```python
            import mlfoundry

            mlfoundry.login(tracking_uri=https://your.truefoundry.site.com")
            client = mlfoundry.get_client()
            artifact_fqn = "artifact:org/user/my-project/my-artifact"
            for av in client.list_artifact_versions(artifact_fqn=artifact_fqn):
                print(av.name, av.version, av.description)
            ```
        """
        artifact = self.mlflow_client.get_artifact_by_fqn(fqn=artifact_fqn)
        max_results = 10
        page_token = None
        done = False
        while not done:
            artifact_versions = self.mlflow_client.list_artifact_versions(
                artifact_id=artifact.id, max_results=max_results, page_token=page_token
            )
            page_token = artifact_versions.token
            for artifact_version in artifact_versions:
                yield ArtifactVersion(
                    artifact_version=artifact_version, artifact=artifact
                )
            if not artifact_versions or not page_token:
                done = True

    def log_predictions(
        self, model_version_fqn: str, predictions: List[Union[Prediction, Dict]]
    ):
        """log_predictions.

        Args:
            model_version_fqn (str): fqn of model_version where data needs to be logged
            predictions (List[mlf.Prediction]): List of prediction packets of class mlf.Prediction or dictionary

        example:
            ```python
            import mlfoundry as mlf
            client = mlf.get_client()

            client.log_predictions(
                model_version_fqn = "",
                predictions = [
                    mlf.Prediction(
                        data_id = uuid.uuid4().hex,
                        features = {
                            "feature1": "class1",
                            "feature2": 3.33,
                        },
                        prediction_data = {
                            "value": "pred_class1",
                            "probabilities": {
                                "pred_class1": 0.2,
                                "pred_class2": 0.8
                            },
                            "shap_values": {}
                        },
                        occurred_at = datetime.utcnow(),
                        raw_data = {"data": "any_data"}
                    )
                ]
            )
            ```

        """

        self.monitoring_client.log_predictions(
            model_version_fqn=model_version_fqn, predictions=predictions
        )

    def log_actuals(self, model_version_fqn: str, actuals: List[Union[Actual, Dict]]):
        """log_actuals.

        Args:
            model_version_fqn (str): fqn of model_version where data needs to be logged
            actuals: (List[mlf.Actual]): List of actual packets of class mlf.Actual or a dictionary

        example:
            ```python
            import mlfoundry as mlf
            client = mlf.get_client()
            data_id = uuid.uuid4().hex
            client.log_predictions(
                model_version_fqn = "",
                predictions = [
                    mlf.Prediction(
                        data_id = data_id,
                        features = {
                            "feature1": "class1",
                            "feature2": 3.33,
                        },
                        prediction_data = {
                            "value": "pred_class1",
                            "probabilities": {
                                "pred_class1": 0.2,
                                "pred_class2": 0.8
                            },
                            "shap_values": {}
                        },
                        occurred_at = datetime.utcnow(),
                        raw_data = {"data": "any_data"}
                    )
                ]
            )
            client.log_actuals(
                model_version_fqn = "",
                actuals = [
                    mlf.Actual(
                        data_id = data_id,
                        value = "pred_class2"
                    )
                ]
            )
            ```
        """

        self.monitoring_client.log_actuals(
            model_version_fqn=model_version_fqn, actuals=actuals
        )

    def generate_hash_from_data(
        self, features: Dict, timestamp: Optional[datetime] = None
    ):
        """generate_hash_from_data.

        Args:
            features (Dict): features for which you want to generate a unique hash
            timestamp (Optional[datetime]): Optionally pass a timestamp to generate unique has for features and a timestamp

        example:
            ```python
            import mlfoundry as mlf
            client = mlf.get_client()
            data_id = mlf.generate_hash_from_data(
                features = {
                    "features1": 1.22,
                    "feature2" : "class2"
                }
            )
            ```
        """
        return self.monitoring_client.generate_hash_from_data(
            features=features, timestamp=timestamp
        )

    def get_inference_dataset(
        self,
        model_fqn: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        actual_value_required: bool = False,
    ):
        """get_inference_dataset.
        Args:
            model_fqn(str): fqn of model for which inference data is required
            start_time(Optional[datetime]): start_time for "occurred_at" field of the prediction
            end_time(Optional[datetime]): start_time for "occurred_at" field of the prediction
            actual_value_required (Optional[bool]): if true, returns inference data rows with both predictions and actuals logged, default false
        example:
            ```python
            import mlfoundry as mlf
            client = mlf.get_client()
            inference_data = client.get_inference_dataset(model_fqn="")
            ```
        """

        # ToDo (@nikp1172) add better logging, consider edge cases for timezones for start_time/end_time
        if not end_time:
            end_time = datetime.now(tz=timezone.utc)
        if not start_time:
            start_time = end_time - timedelta(days=7)
            logger.info(f"start_time not passed, initializing to {start_time}")
        return self.monitoring_client.get_inference_dataset(
            model_fqn=model_fqn,
            start_time=start_time,
            end_time=end_time,
            actual_value_required=actual_value_required,
        )
