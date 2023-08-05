import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import pymc as pm
except ImportError:
    _has_pymc = False
else:
    _has_pymc = True

try:
    import arviz as az
except ImportError:
    _has_arviz = False
else:
    _has_arviz = True

# from ..data import IVESPA, Mastin


def requires_pymc():
    if not _has_pymc:
        raise ImportError("pymc is required for mc.simple_regression")


def requires_arviz():
    if not _has_arviz:
        raise ImportError("arviz is required for mc.simple_regression")


def ordinary_regression(
    data, xvar="H", new_obs=None, n_samples=1000, n_tune=2000, cores=1
):

    if xvar == "H":
        x = np.log10(data.height)
        y = np.log10(data.mer)
        xvar_label = "logH"
        yvar_label = "logQ"
    else:
        x = np.log10(data.mer)
        y = np.log10(data.height)
        xvar_label = "logQ"
        yvar_label = "logH"

    i = np.argsort(x)
    x = x[i]
    y = y[i]

    with pm.Model() as model_1:
        if xvar == "H":
            a = pm.TruncatedNormal("a", mu=3.0, sigma=1.0, lower=0.0)
            b = pm.TruncatedNormal("b", mu=4.0, sigma=1.0, lower=0.0)
        else:
            # a = pm.HalfNormal("a", 1.0 / 3.0)
            a = pm.TruncatedNormal("a", mu=-0.5, sigma=1.0, upper=0.0)
            b = pm.TruncatedNormal("b", mu=0.25, sigma=1.0, lower=0.0)
        pred = pm.MutableData(xvar_label, x, dims="obs_id")
        mu = pm.Deterministic("mu", a + b * pred, dims="obs_id")
        sigma = pm.Exponential("sigma", 1.0)

        likelihood = pm.Normal(
            yvar_label, mu=mu, sigma=sigma, observed=y, dims="obs_id"
        )

        idata = pm.sample_prior_predictive(samples=50)

        idata.extend(
            pm.sample(n_samples, tune=n_tune, return_inferencedata=True, cores=cores)
        )

    az.plot_trace(idata, var_names=["a", "b", "sigma"])

    if new_obs is not None:
        xnew = np.log10(new_obs)

        with model_1:
            pm.set_data({xvar_label: xnew})
            pm.sample_posterior_predictive(
                idata, extend_inferencedata=True, predictions=True
            )

    return idata


def robust_regression(
    data, xvar="H", new_obs=None, n_samples=1000, n_tune=2000, cores=1
):

    if xvar == "H":
        x = np.log10(data.height)
        y = np.log10(data.mer)
        xvar_label = "logH"
        yvar_label = "logQ"
    else:
        x = np.log10(data.mer)
        y = np.log10(data.height)
        xvar_label = "logQ"
        yvar_label = "logH"

    i = np.argsort(x)
    x = x[i]
    y = y[i]

    with pm.Model() as model_1:
        if xvar == "H":
            a = pm.TruncatedNormal("a", mu=3.0, sigma=1.0, lower=0.0)
            b = pm.TruncatedNormal("b", mu=4.0, sigma=1.0, lower=0.0)
        else:
            # a = pm.HalfNormal("a", 1.0 / 3.0)
            a = pm.TruncatedNormal("a", mu=-0.5, sigma=1.0, upper=0.0)
            b = pm.TruncatedNormal("b", mu=0.25, sigma=1.0, lower=0.0)
        pred = pm.MutableData(xvar_label, x, dims="obs_id")
        mu = pm.Deterministic("mu", a + b * pred, dims="obs_id")
        sigma = pm.Exponential("sigma", 1.0)

        nu = pm.HalfCauchy("nu", beta=2)
        likelihood = pm.StudentT(
            yvar_label, mu=mu, sigma=sigma, nu=nu, observed=y, dims="obs_id"
        )

        idata = pm.sample_prior_predictive(samples=50)

        idata.extend(
            pm.sample(n_samples, tune=n_tune, return_inferencedata=True, cores=cores)
        )

    az.plot_trace(idata, var_names=["a", "b", "sigma", "nu"])

    if new_obs is not None:
        xnew = np.log10(new_obs)

        with model_1:
            pm.set_data({xvar_label: xnew})
            pm.sample_posterior_predictive(
                idata, extend_inferencedata=True, predictions=True
            )

    return idata


def latitude_variance():

    df = Mastin.data
    x_obs = np.log10(df["Plume height"])
    y_obs = np.log10(df["MER"])
    z_obs = np.abs(df["Latitude"]) / 90.0

    with pm.Model() as model:
        a = pm.TruncatedNormal("a", mu=3.0, sigma=1.0, lower=0.0)
        b = pm.TruncatedNormal("b", mu=4.0, sigma=1.0, lower=0.0)
        logh = pm.MutableData("logh", x_obs, dims="obs_id")
        z = pm.MutableData("z", z_obs, dims="obs_id")
        mu = pm.Deterministic("mu", a + b * logh, dims="obs_id")
        sigma0 = pm.Exponential("sigma0", 1.0)
        sigma1 = pm.TruncatedNormal("sigma1", mu=0.0, sigma=1.0, lower=0.0)
        sigma = pm.Deterministic("sigma", sigma0 * (1 + sigma1 * z))
        lik = pm.Normal("y", mu=mu, sigma=sigma, observed=y_obs, dims="obs_id")
        idata = pm.sample_prior_predictive(samples=50)
        idata.extend(pm.sample(4000, tune=4000, return_inferencedata=True))


def climate_zones():
    data = Mastin.data
    data["MER"] = data["MER"].astype(float)
    climate_indxs, climate_zones = pd.factorize(data["Climate zone"])
    coords = {
        "climate_zone": climate_zones,
        "obs_id": np.arange(len(climate_indxs)),
    }

    with pm.Model(coords=coords) as hierarchical_model:
        climate_idx = pm.Data("climate_idx", climate_indxs, dims="obs_id")
        # Hyper-priors
        mu_a = pm.Normal("mu_a", mu=3.0, sigma=100.0)
        sigma_a = pm.HalfNormal("sigma_a", 5.0)
        mu_b = pm.Normal("mu_b", mu=4.0, sigma=100.0)
        sigma_b = pm.HalfNormal("sigma_b", 5.0)

        # Intercept for each climate zone, distributed with mean mu_a
        a = pm.Normal("a", mu=mu_a, sigma=sigma_a, dims="climate_zone")
        # Slope for each climate zone, distributed with mean mu_b
        b = pm.Normal("b", mu=mu_b, sigma=sigma_b, dims="climate_zone")

        # Model error
        eps = pm.HalfCauchy("eps", beta=5.0)

        # Expected value
        MER_est = a[climate_idx] + b[climate_idx] * data["Plume height"].values

        # Data likelihood
        MER_like = pm.Normal(
            "MER_like", mu=MER_est, sigma=eps, observed=data["MER"], dims="obs_id"
        )

    with hierarchical_model:
        hierarchical_trace = pm.sample(
            2000, tune=2000, target_accept=0.9, return_inferencedata=True
        )

        az.plot_trace(
            hierarchical_trace, var_names=["mu_a", "mu_b", "sigma_a", "sigma_b", "eps"]
        )

        az.plot_trace(
            hierarchical_trace,
            var_names=["a", "b"],
            coords={"climate_zone": climate_zones},
        )


def plot_posterior_predictive(trace, data):

    xnew = trace.predictions_constant_data
    ynew = trace.predictions

    xvar = list(xnew.keys())[0]
    yvar = list(ynew.keys())[0]

    yer = az.hdi(ynew)[yvar].values.T
    ymean = ynew[yvar].mean(("chain", "draw"))

    yer = np.power(10, yer)
    ymean = np.power(10, ymean)

    xnew = np.power(10, xnew[xvar])
    ynew = np.power(10, ynew[yvar])

    _, ax = plt.subplots()
    if xvar == "logH":
        ax.set_yscale("log")
        xobs = data.height
        yobs = data.mer
    else:
        ax.set_xscale("log")
        xobs = data.mer
        yobs = data.height

    ax.vlines(xnew, yer[0], yer[1], alpha=0.8)
    ax.plot(
        xnew,
        ymean,
        "o",
        ms=5,
        color="steelblue",
        alpha=0.8,
        label="Expected output",
    )
    ax.scatter(
        xobs,
        yobs,
        marker="o",
        color="darkred",
        alpha=0.8,
        label="Observations",
    )

    return ax
