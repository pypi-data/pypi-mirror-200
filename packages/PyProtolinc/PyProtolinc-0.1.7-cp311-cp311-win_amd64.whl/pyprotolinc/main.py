""" Main module. Configures the logger and provides the entry points of the command line runner. """

import time
import logging
import cProfile
import pstats
import io
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count
from typing import Optional, Union
import importlib.metadata
import gc

import numpy as np
import numpy.typing as npt
import pandas as pd
import fire  # type: ignore

from pyprotolinc.models import Model
from pyprotolinc import get_config_from_file, RunConfig
from pyprotolinc.portfolio import PortfolioLoader, Portfolio
from pyprotolinc.results import export_results
from pyprotolinc.runner import Projector, CProjector
from pyprotolinc.models.state_models import state_model_by_name
from pyprotolinc.models.model_config import get_model_by_name
from pyprotolinc.assumptions.iohelpers import AssumptionsLoaderFromConfig
from pyprotolinc.assumptions.providers import AssumptionSetWrapper
from pyprotolinc.product import product_class_lookup
from pyprotolinc.utils import download_dav_tables


# logging.basicConfig(filename='runlog.txt', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s - %(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)

# module level logger
logger = logging.getLogger(__name__)
__version__ = importlib.metadata.version("pyprotolinc")


def create_model(model_class: type[Model],
                 state_model_name: str,
                 assumptions_file: Optional[str],
                 assumption_wrapper_opt: Optional[AssumptionSetWrapper]) -> Model:
    """ Create a valuation model.

        :param model_class: The class of the model.
        :param str state_model_name: The name of the state model.
        :param assumptions_file: Path to the assumptions config file to be used.
        :param assumption_wrapper: Object of type AssumptionSetWrapper that is used directly.

        :return: The valuation model.
        :rtype: Instance of `model_class`
    """

    # try determining the state model
    state_model_class = state_model_by_name(state_model_name)

    # load the assumptions
    assumption_wrapper: AssumptionSetWrapper
    if assumptions_file is None and assumption_wrapper_opt is None:
        raise Exception("Creating a model requires either a valid assumption spec or and AssumptionSet")
    elif assumption_wrapper_opt is None and assumptions_file is not None:
        loader = AssumptionsLoaderFromConfig(assumptions_file, len(state_model_class))
        assumption_wrapper = loader.load()
    elif assumption_wrapper_opt is not None:
        assumption_wrapper = assumption_wrapper_opt
    else:
        raise Exception("Unreachable exception to silence mypy")

    # instantiate the model
    model = model_class(state_model_class, assumption_wrapper)
    # adjust_state_for_generic_model(model, state_model_name)

    return model


def project_cashflows(run_config: RunConfig,
                      df_portfolio_overwrite: Optional[pd.DataFrame] = None,
                      assumption_wrapper: Optional[AssumptionSetWrapper] = None,
                      export_to_file: bool = True) -> dict[str, npt.NDArray[np.float64]]:
    """ The main calculation rountine, can also be called as library function. If
        a dataframe is passed it will be used to build the portfolio object,
        otherwise the portfolio will be obtained from th run-config.

        :param run_config: The run configuration object.
        :param df_portfolio_overwrite: An optional dataframe that will be used instead of the configured portfolio if provided
        :param assumption_wrapper: Optionally an assumption set can be injected here directly instead of getting it via the configured paths
        :param export_to_file: Boolean flag to indicate if the results should be written to a file (as specified in the config object)

        :return: Dictionary containing the result vectors.
        :rtype: dict[str, npt.NDArray[np.float64]]
    """
    t = time.time()

    logger.info("Multistate run with config: %s", str(run_config))

    rows_for_state_recorder: Optional[tuple[int]] = None  # (0, 1, 2)
    num_timesteps = run_config.years_to_simulate * 12 * run_config.steps_per_month

    model = create_model(get_model_by_name(run_config.model_name), run_config.state_model_name, run_config.assumptions_path, assumption_wrapper)

    if df_portfolio_overwrite is None:
        if run_config.portfolio_path is None:
            raise Exception("Config parameters portfolio_path must not be None if no overwrite portfolio is provided!")
        else:
            portfolio_loader = PortfolioLoader(run_config.portfolio_path, run_config.portfolio_cache)
            portfolio = portfolio_loader.load(model.states_model)
    else:
        portfolio = Portfolio(None, model.states_model, df_portfolio_overwrite)

    # split into subportfolios - for the PyKernel we split by product and month_in year, for the CKernel
    # only by product
    if run_config.kernel_engine in ["P", "PY", "PYTHON"]:
        subportfolios = portfolio.split_by_product_and_month_in_year(chunk_size=run_config.portfolio_chunk_size)
    elif run_config.kernel_engine in ["C", "CPP", "C++"]:
        subportfolios = portfolio.split_by_product_and_month_in_year(chunk_size=run_config.portfolio_chunk_size, split_mont_in_year=False)
    else:
        raise Exception(f"Unknown kernel engine specified: {run_config.kernel_engine}")

    # container for the results of the different sub-portfolios
    results_arrays = []

    # projections
    if run_config.use_multicore and len(subportfolios) > 1:  # and run_config.kernel_engine in ["P", "PY", "PYTHON"]:

        num_processes = min(cpu_count(), len(subportfolios))

        PARAMS = [(run_config, model, num_timesteps, sub_ptf, rows_for_state_recorder, chunk_index+1, len(subportfolios))
                  for chunk_index, sub_ptf in enumerate(subportfolios)]
        logger.info("Executions in parallel wit %s processes and %s units", num_processes, len(PARAMS))
        pool = Pool(num_processes)

        for projector_results in pool.starmap(_project_subportfolio, PARAMS):
            results_arrays.append(projector_results)

    else:
        logger.info("Executions in single process for %s units", len(subportfolios))
        for sp_ind, sub_ptf in enumerate(subportfolios):

            projector_results = _project_subportfolio(run_config, model, num_timesteps, sub_ptf, rows_for_state_recorder, sp_ind + 1, len(subportfolios))
            results_arrays.append(projector_results)

            gc.collect()

    # combine the results from the subportfolios
    logger.debug("Combining results from subportfolios")
    res_combined = dict(results_arrays[0])
    for res_ind in range(1, len(results_arrays)):
        res_set = results_arrays[res_ind]
        for key, val in res_set.items():
            if key not in ("YEAR", "QUARTER", "MONTH"):
                res_combined[key] = res_combined[key] + res_set[key]

    # export result
    if export_to_file:
        export_results(res_combined, run_config.outfile)

    elapsed = time.time() - t
    logger.info("Elapsed time %s seconds.", round(elapsed, 1))

    return res_combined


def _project_subportfolio(run_config: RunConfig,
                          model: Model,
                          num_timesteps: int,
                          portfolio: Portfolio,
                          rows_for_state_recorder: Optional[tuple[int]],
                          chunk_index: int,
                          num_chunks: int) -> dict[str, Union[npt.NDArray[np.float64], npt.NDArray[np.int16]]]:

    assert portfolio.homogenous_wrt_product, "Subportfolio should have identical product in all rows"
    product_name = portfolio.products.iloc[0]
    product_class = product_class_lookup(product_name)
    assert model.states_model == product_class.STATES_MODEL, "State-Models must be consistent for the product and the run"
    product = product_class(portfolio)

    projector: Union[CProjector, Projector]
    if run_config.kernel_engine in ["C", "CPP", "C++"]:

        # not needed for the C++ call
        proj_state = None

        logger.info("Projecting subportfolio {} / {} with C++ engine".format(chunk_index, num_chunks))
        projector = CProjector(run_config,
                               portfolio,
                               model,
                               product,
                               # rows_for_state_recorder=rows_for_state_recorder,
                               chunk_index=chunk_index,
                               num_chunks=num_chunks
                               )

    elif run_config.kernel_engine in ["P", "PY", "PYTHON"]:

        proj_state = model.new_state_instance(num_timesteps, portfolio, rows_for_state_recorder=rows_for_state_recorder)
        logger.info("Projecting subportfolio {} / {} with Python engine".format(chunk_index, num_chunks))
        projector = Projector(run_config,
                              portfolio,
                              model,
                              proj_state,
                              product,
                              rows_for_state_recorder=rows_for_state_recorder,
                              chunk_index=chunk_index,
                              num_chunks=num_chunks)

    else:
        raise Exception("Unknown kernel type: {}".format(run_config.kernel_engine))

    projector.run()
    result: dict[str, Union[npt.NDArray[np.float64], npt.NDArray[np.int16]]] = projector.get_results_dict()
    return result


def project_cashflows_cli(config_file_or_object: Union[str, RunConfig] = 'config.yml',
                          multi_processing_overwrite: Optional[bool] = None) -> None:
    """ Start a projection run.

        :param str config_file_or_object: Path to the config file or a RunConfig
        :param multi_processing_overwrite: Optional boolen parameter that allows overwriting the multiprocessing setting in the config file.

        :return: None
    """

    run_config: RunConfig
    if isinstance(config_file_or_object, str):
        run_config = get_config_from_file(config_file_or_object)
    elif isinstance(config_file_or_object, RunConfig):
        run_config = config_file_or_object

    if multi_processing_overwrite is not None:
        run_config.use_multicore = multi_processing_overwrite
    project_cashflows(run_config)


def profile(config_file: str = 'config.yml',
            multi_processing_overwrite: Optional[bool] = None) -> None:
    """ Run and and export a CSV file with runtime statistics.

        :param str config_file: Path ot the config file
        :param multi_processing_overwrite: Optional boolen parameters that allows overwriting the multiprocessing setting in the config file.

        :return: None
    """

    run_config = get_config_from_file(config_file)

    if run_config.profile_out_dir is None:
        raise Exception("Config parameteter `profile_out_dir` must be provided for profile run!")

    if multi_processing_overwrite is not None:
        run_config.use_multicore = multi_processing_overwrite

    pr = cProfile.Profile()

    # here we call the program
    pr.enable()
    project_cashflows(run_config)
    pr.disable()

    result_io = io.StringIO()
    pstats.Stats(pr, stream=result_io).print_stats()
    result = result_io.getvalue()
    # chop the string into a csv-like buffer
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
    df = pd.read_csv(io.StringIO(result))

    # filter for package  methods with positive runtime
    df_filtered = df[(df["filename:lineno(function)"].str.contains("pyprotolinc")) &
                     (df.cumtime > 0)].copy()

    # shorten the location by the common prefix
    start_pos = df_filtered["filename:lineno(function)"].str.find("pyprotolinc").unique()[0]
    df_filtered["filename:lineno(function)"] = df_filtered["filename:lineno(function)"].str.slice(start_pos)

    ct = datetime.now().strftime('%d-%m-%Y_%H_%M_%S')
    output_file = os.path.join(run_config.profile_out_dir, "profile_{}.xlsx".format(ct))

    df_filtered.index = pd.Index(np.arange(1, 1 + len(df_filtered)))
    df_filtered.to_excel(output_file)
    logger.info("Statistics written to %s", output_file)


def show_docs_in_browser() -> None:
    """ Show the *readthedocs* help pages in the system browser
        :return: None
    """
    import webbrowser
    url = "https://pyprotolinc.readthedocs.io/en/latest/index.html"
    webbrowser.open(url)


def print_version():
    print(__version__)


def main() -> None:
    """ Entry point of the CLI client. Declares the following subtasks:

          - `run` to run start a run from the command line
          - `profile` to run start a run with profile information from the command line
          - `download_dav_tables` to download soem DAV tables from the R package `mortality tables`
    """
    fire.Fire({
        "run": project_cashflows_cli,
        "profile": profile,
        "download_dav_tables": download_dav_tables,
        "docs": show_docs_in_browser,
        "version": print_version,
    })


if __name__ == "__main__":
    project_cashflows_cli()
    # run_config = get_config_from_file(config_file='config.yml')
    # print(run_config)
