import ast

import click
import matplotlib.pyplot as plt
from numpy import atleast_1d
from scipy.stats import truncnorm, uniform
from scipy.stats._distn_infrastructure import rv_continuous_frozen

from merph.data import IVESPA, Aubry, Mastin, Sparks

# try:
#     from merph.app import make_dashboard
# except ImportError:
#     _has_app = False
# else:
#     _has_app = True

try:
    from merph.notebooks import launch_jupyter_example
except ImportError:
    _has_nb = False
else:
    _has_nb = True


# def has_app_dependencies(func):
#     if not _has_app:
#         raise ImportError("app has dependencies, try: pip install merph[app]")


# def has_nb_dependencies(func):
#     if not _has_nb:
#         raise ImportError("notebook has dependencies, try: pip install merph[nb]")


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


class ObservableValues(click.Option):
    def type_cast_value(self, ctx, value):
        if "uniform" in value:
            try:
                range_str = value[value.find("(") + 1 : value.find(")")]
                lower, upper = range_str.split(",")
                lower = float(lower)
                upper = float(upper)
                return uniform(loc=lower, scale=upper - lower)
            except:
                raise click.BadParameter(value)
        elif "truncnorm" in value:
            try:
                param_str = value[value.find("(") + 1 : value.find(")")]
                mu, sigma, lower, upper = param_str.split(",")
                mu = float(mu)
                sigma = float(sigma)
                lower = float(lower)
                upper = float(upper)
                a = (lower - mu) / sigma
                b = (upper - mu) / sigma
                return truncnorm(loc=mu, scale=sigma, a=a, b=b)
            except:
                raise click.BadParameter(value)
        else:
            try:
                return ast.literal_eval(value)
            except:
                raise click.BadParameter(value)


# @has_app_dependencies
# def run_app(ctx, param, value):
#     if not _has_app:
#         raise ImportError("app has dependencies, try: pip install merph[app]")

#     if not value or ctx.resilient_parsing:
#         return
#     make_dashboard()
#     ctx.exit()


# @has_nb_dependencies
# def run_example(ctx, param, value):
#     """Run a MERPH jupyter notebook example.

#     n is the example number; choices are 1, 2"""

#     if not _has_nb:
#         raise ImportError("notebook has dependencies, try: pip install merph[nb]")

#     if not value or ctx.resilient_parsing:
#         return

#     if value not in ["1", "2"]:
#         return

#     msg = "Running MERPH Example " + value
#     click.echo(msg)

#     launch_jupyter_example(value)
#     ctx.exit()


@click.command()
# @click.option(
#     "--app", is_flag=True, callback=run_app, expose_value=False, is_eager=True
# )
# @click.option(
#     "--example",
#     prompt=False,
#     type=click.Choice(["1", "2"]),
#     default=None,
#     callback=run_example,
#     expose_value=True,
#     is_eager=True,
# )
@click.option(
    "-data",
    "--dataset",
    type=click.Choice(["Mastin", "Sparks", "Aubry", "IVESPA"], case_sensitive=False),
    prompt="Select dataset",
    help="Select dataset.  Options are:\n"
    + "  - Mastin\n"
    + "  - Sparks\n"
    + "  - Aubry\n"
    + "  - IVESPA\n",
    required=True,
)
@click.option(
    "-x",
    "--xvar",
    type=click.Choice(["H", "Q", "MER"], case_sensitive=False),
    prompt="Set observed variable",
    help="Set observed variable",
    required=True,
)
@click.option(
    "-obs",
    "--observation",
    cls=ObservableValues,
    default='"15."',
    prompt="Set observations \n"
    + "  options are: \n"
    + "  - single value e.g. '10.0,'\n"
    + "  - list of values e.g. '10., 15., 20.'\n"
    + "  - uniform distribution uniform(a,b) e.g. uniform(10, 20)\n"
    + "  - truncated normal distribution truncnorm(mu, sigma, lower, upper) e.g. truncnorm(11, 1.0, 10, 15)",
    help="Set observation"
    + "  options are: \n"
    + "  - single value e.g. '10.0,'\n"
    + "  - list of values e.g. '10., 15., 20.'\n"
    + "  - uniform distribution uniform(a,b) e.g. uniform(10, 20)\n"
    + "  - truncated normal distribution truncnorm(mu, sigma, lower, upper) e.g. truncnorm(11, 1.0, 10, 15)",
    required=True,
)
@click.option(
    "-s",
    "--samples",
    type=int,
    default=1000,
    prompt="Set number of samples to draw from the posterior predictive distribution",
    help="Number of samples to draw from the posterior predictive distribution",
    required=True,
)
def run_merph(
    dataset: str, xvar: str, observation: float, samples: int, **kwargs
) -> None:
    print("Running MERPH")
    if xvar == "H":
        yvar = "Q"
    else:
        yvar = "H"
    print(f"{dataset} {yvar}|{xvar}")

    if dataset == "Mastin":
        data = Mastin
    elif dataset == "Sparks":
        data = Sparks
    elif dataset == "Aubry":
        data = Aubry
    else:  # args.dataset == 'IVESPA':
        data = IVESPA

    data.set_vars(xvar=xvar, yvar=yvar)  # sets independent and variables

    data.mle(plot=True)  # maximum likelihood estimator (Mastin curve)

    data.posterior_plot()  # Now plot the curve.

    if isinstance(observation, rv_continuous_frozen):
        obs = observation.rvs(samples)
        data.set_obs(obs)
        data.posterior_simulate(1, as_dataframe=True, plot=True, split_x=False)
    else:
        if isinstance(observation, str):
            observation = float(observation)
        elif isinstance(observation, tuple):
            observation = [float(obs) for obs in observation]
        observation = atleast_1d(observation)

        data.set_obs(observation)

        data.posterior_simulate(
            samples, plot=True, split_x=(True if len(observation) > 1 else False)
        )  # Sample from the posterior distribution (get MER values) for 1000 samples, and plot it

    plt.show()
