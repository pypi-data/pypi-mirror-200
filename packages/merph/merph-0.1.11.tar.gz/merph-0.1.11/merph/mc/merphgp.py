import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist

try:
    import pymc as pm
    from pymc.gp.util import plot_gp_dist
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

from ..data import Aubry, Mastin


def requires_pymc():
    if not _has_pymc:
        raise ImportError("pymc is required for GP")


def requires_arviz():
    if not _has_arviz:
        raise ImportError("arviz is required for GP")


def GP_example():

    requires_pymc()
    requires_arviz()

    Aubry.set_vars(xvar="H", yvar="Q")

    x = Aubry._x
    y = Aubry._y

    with pm.Model() as model:
        rho = pm.HalfCauchy("rho", 0.5)
        eta = pm.HalfCauchy("eta", 3)
        b0 = pm.Normal("b0", 10)
        b1_0 = pm.Normal("b1_0", 1)
        b1 = pm.Deterministic("b1", b1_0 + 4)
        M = pm.gp.mean.Linear(coeffs=b1, intercept=b0)
        K = eta * pm.gp.cov.Matern52(1, rho)
        gp = pm.gp.Marginal(mean_func=M, cov_func=K)
        s = pm.HalfNormal("s", 50)
        gp = pm.gp.Marginal(mean_func=M, cov_func=K)
        gp.marginal_likelihood("y", X=x[:, None], y=y, sigma=s)

        trace = pm.sample(
            2000, tune=2000, cores=2, random_seed=42, return_inferencedata=True
        )

    with model:
        az.plot_trace(trace)
        plt.show()

    xp = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
    with model:
        y_pred = gp.conditional("y_pred", xp)
        y_pred_noise = gp.conditional("y_pred_noise", xp, pred_noise=True)
        y_s = pm.sample_posterior_predictive(
            trace, var_names=["y_pred", "y_pred_noise"], samples=5000, random_seed=42
        )

    fig1, ax1 = plt.subplots()
    plot_gp_dist(ax1, y_s["y_pred"], np.power(10, xp))
    ax1.scatter(np.power(10, x), y, c="k", s=50)

    fig2, ax2 = plt.subplots()
    plot_gp_dist(ax2, y_s["y_pred_noise"], np.power(10, xp), palette="Blues")
    ax2.scatter(np.power(10, x), y, c="k", s=50)

    plt.show()


def GP_heteroskedastic():

    requires_pymc()
    requires_arviz()

    SEED = 2020
    rng = np.random.default_rng(SEED)
    az.style.use("arviz-darkgrid")

    # Mastin.set_vars(xvar="H", yvar="Q")

    X = np.log10(Mastin.height)
    y = np.log10(Mastin.mer)

    X_ = X.flatten()

    y_obs = y
    y_obs_ = y_obs.T.flatten()

    X_obs = X.reshape(-1, 1)
    X_obs_ = X_obs.flatten()

    Xnew = np.linspace(0.8 * X.min(), 1.2 * X.max(), 100)[:, None]
    Xnew_ = Xnew.flatten()
    ynew = np.zeros_like(Xnew)

    plt.plot(X_obs, y_obs, "C0o")

    ℓ_μ, ℓ_σ = [stat for stat in get_ℓ_prior(X_)]

    with pm.Model() as model_hm:
        ℓ = pm.InverseGamma("ℓ", mu=ℓ_μ, sigma=ℓ_σ)
        η = pm.Gamma("η", alpha=2, beta=1)
        cov = η**2 * pm.gp.cov.ExpQuad(input_dim=1, ls=ℓ)

        gp_hm = pm.gp.Marginal(cov_func=cov)

        σ = pm.Exponential("σ", lam=1)

        ml_hm = gp_hm.marginal_likelihood("ml_hm", X=X_obs, y=y_obs_, sigma=σ)

        trace_hm = pm.sample(return_inferencedata=True, random_seed=SEED)

    with model_hm:
        mu_pred_hm = gp_hm.conditional("mu_pred_hm", Xnew=Xnew)
        noisy_pred_hm = gp_hm.conditional("noisy_pred_hm", Xnew=Xnew, pred_noise=True)
        samples_hm = pm.sample_posterior_predictive(
            trace_hm, var_names=["mu_pred_hm", "noisy_pred_hm"]
        )

    _, axs = plt.subplots(1, 3, figsize=(18, 4))
    mu_samples = samples_hm.posterior_predictive["mu_pred_hm"]
    noisy_samples = samples_hm.posterior_predictive["noisy_pred_hm"]
    plot_mean(axs[0], mu_samples)
    plot_var(axs[1], noisy_samples.var(axis=0))
    plot_total(axs[2], noisy_samples)

    with pm.Model() as model_ht:
        ℓ = pm.InverseGamma("ℓ", mu=ℓ_μ, sigma=ℓ_σ)
        η = pm.Gamma("η", alpha=2, beta=1)
        cov = η**2 * pm.gp.cov.ExpQuad(input_dim=1, ls=ℓ) + pm.gp.cov.WhiteNoise(
            sigma=1e-6
        )

        gp_ht = pm.gp.Latent(cov_func=cov)
        μ_f = gp_ht.prior("μ_f", X=X_obs)

        σ_ℓ = pm.InverseGamma("σ_ℓ", mu=ℓ_μ, sigma=ℓ_σ)
        σ_η = pm.Gamma("σ_η", alpha=2, beta=1)
        σ_cov = σ_η**2 * pm.gp.cov.ExpQuad(
            input_dim=1, ls=σ_ℓ
        ) + pm.gp.cov.WhiteNoise(sigma=1e-6)

        σ_gp = pm.gp.Latent(cov_func=σ_cov)
        lg_σ_f = σ_gp.prior("lg_σ_f", X=X_obs)
        σ_f = pm.Deterministic("σ_f", pm.math.exp(lg_σ_f))

        lik_ht = pm.Normal("lik_ht", mu=μ_f, sd=σ_f, observed=y_obs_)

        trace_ht = pm.sample(
            target_accept=0.95, chains=2, return_inferencedata=True, random_seed=SEED
        )

    with model_ht:
        μ_pred_ht = gp_ht.conditional("μ_pred_ht", Xnew=Xnew)
        lg_σ_pred_ht = σ_gp.conditional("lg_σ_pred_ht", Xnew=Xnew)
        samples_ht = pm.sample_posterior_predictive(
            trace_ht, var_names=["μ_pred_ht", "lg_σ_pred_ht"]
        )

    _, axs = plt.subplots(1, 3, figsize=(18, 4))
    μ_samples = samples_ht["μ_pred_ht"]
    σ_samples = np.exp(samples_ht["lg_σ_pred_ht"])
    plot_mean(axs[0], μ_samples)
    plot_var(axs[1], σ_samples**2)
    plot_total(axs[2], μ_samples, σ_samples**2)


def get_ℓ_prior(points):
    """Calculates mean and sd for InverseGamma prior on lengthscale"""
    distances = pdist(points[:, None])
    distinct = distances != 0
    ℓ_l = distances[distinct].min() if sum(distinct) > 0 else 0.1
    ℓ_u = distances[distinct].max() if sum(distinct) > 0 else 1
    ℓ_σ = max(0.1, (ℓ_u - ℓ_l) / 6)
    ℓ_μ = ℓ_l + 3 * ℓ_σ
    return ℓ_μ, ℓ_σ


def plot_inducing_points(ax):
    yl = ax.get_ylim()
    yu = -np.subtract(*yl) * 0.025 + yl[0]
    ax.plot(Xu, np.full(Xu.shape, yu), "xk", label="Inducing Points")
    ax.legend(loc="upper left")


def get_quantiles(samples, quantiles=[2.5, 50, 97.5]):
    return [np.percentile(samples, p, axis=0) for p in quantiles]


def plot_mean(ax, mean_samples):
    """Plots the median and 95% CI from samples of the mean

    Note that, although each individual GP exhibits a normal distribution at each point
    (by definition), we are sampling from a mixture of GPs defined by the posteriors of
    our hyperparameters. As such, we use percentiles rather than mean +/- stdev to
    represent the spread of predictions from our models.
    """
    l, m, u = get_quantiles(mean_samples)
    ax.plot(Xnew, m, "C0", label="Median")
    ax.fill_between(Xnew_, l, u, facecolor="C0", alpha=0.5, label="95% CI")

    ax.plot(Xnew, ynew, "--k", label="Mean Function")
    ax.plot(X, y_obs, "C1.", label="Observed Means")
    ax.set_title("Mean Behavior")
    ax.legend(loc="upper left")


def plot_var(ax, var_samples):
    """Plots the median and 95% CI from samples of the variance"""
    if var_samples.squeeze().ndim == 1:
        ax.plot(Xnew, var_samples, "C0", label="Median")
    else:
        l, m, u = get_quantiles(var_samples)
        ax.plot(Xnew, m, "C0", label="Median")
        ax.fill_between(Xnew.flatten(), l, u, facecolor="C0", alpha=0.5, label="95% CI")
    # ax.plot(X, y_err**2, "C1.", label="Observed Variance")
    ax.set_title("Variance Behavior")
    ax.legend(loc="upper left")


def plot_total(ax, mean_samples, var_samples=None, bootstrap=True, n_boots=100):
    """Plots the overall mean and variance of the aggregate system

    We can represent the overall uncertainty via explicitly sampling the underlying normal
    distributrions (with `bootstrap=True`) or as the mean +/- the standard deviation from
    the Law of Total Variance. For systems with many observations, there will likely be
    little difference, but in cases with few observations and informative priors, plotting
    the percentiles will likely give a more accurate representation.
    """

    if (var_samples is None) or (var_samples.squeeze().ndim == 1):
        samples = mean_samples
        l, m, u = get_quantiles(samples)
        ax.plot(Xnew, m, "C0", label="Median")
    elif bootstrap:
        # Estimate the aggregate behavior using samples from each normal distribution in the posterior
        samples = (
            rng.normal(
                mean_samples.T[:, :, None],
                np.sqrt(var_samples).T[:, :, None],
                (*mean_samples.T.shape, n_boots),
            )
            .reshape(len(Xnew_), -1)
            .T
        )
        l, m, u = get_quantiles(samples)
        ax.plot(Xnew, m, "C0", label="Median")
    else:
        m = mean_samples.mean(axis=0)
        ax.plot(Xnew, m, "C0", label="Mean")
        sd = np.sqrt(mean_samples.var(axis=0) + var_samples.mean(axis=0))
        l, u = m - 2 * sd, m + 2 * sd

    ax.fill_between(
        Xnew.flatten(),
        l,
        u,
        facecolor="C0",
        alpha=0.5,
        label="Total 95% CI",
    )

    ax.plot(Xnew, ynew, "--k", label="Mean Function")
    ax.plot(X_obs, y_obs_, "C1.", label="Observations")
    ax.set_title("Aggregate Behavior")
    ax.legend(loc="upper left")
