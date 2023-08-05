# import numbers
from math import log10
from typing import IO, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib import is_interactive
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from scipy.stats import invgamma, multivariate_normal, norm, t
from seaborn import color_palette

from ..utilities.number_tools import sci_string
from ..utilities.plot_tools import plotTitle

# from .QHData import QHdata


class QHstats(object):
    name: Optional[str]
    height_column: str
    mer_column: str
    height: npt.NDArray[np.float64]
    mer: npt.NDArray[np.float64]
    data: pd.DataFrame

    sigma2: np.float64
    residual: np.float64

    n: int
    df: int

    _set_vars: bool

    _x: npt.NDArray[np.float64]
    _y: npt.NDArray[np.float64]
    _matX: npt.NDArray[np.float64]
    _matV: npt.NDArray[np.float64]

    xp: Optional[npt.NDArray[np.float64]]

    def __init__(
        self,
        data: pd.DataFrame,
        name: Optional[str] = None,
        Height: str = "H",
        MER: str = "Q",
    ):
        self.name = name

        self.set_data(data)

        self.height_column = Height
        self.mer_column = MER

        self.height = data[Height].to_numpy(dtype="float", copy=True, na_value=np.nan)  # type: ignore
        self.mer = data[MER].to_numpy(dtype="float", copy=True, na_value=np.nan)  # type: ignore

        if len(self.height) != len(self.mer):
            raise RuntimeError("In QHstats object, the length of Q and H must be equal")

        self.size = len(self.height)

        self._set_vars = False

    def __str__(self):
        return "QHstats object with {} entries".format(self.size)

    def set_data(self, data: pd.DataFrame):
        """Setup the observational data passed as a pandas DataFrame

        Args:
            data (pd.DataFrame): Pandas dataframe containing the data
        """
        units = {}
        cols: List[str] = []
        data_cols: List[str] = data.columns.tolist()
        for col in data_cols:
            if "(" in col:
                name, unit = col.split("(")
                name = name[:-1]
                unit = unit[:-1]
            else:
                name = col
                unit = None
            units[name] = unit
            cols.append(name)
        if "References" in cols:
            cols.remove("References")
            data.drop(["References"], axis=1, inplace=True)  # type: ignore
        if "Comments" in cols:
            cols.remove("Comments")
            data.drop(["Comments"], axis=1, inplace=True)  # type: ignore
        if "VEI" in cols:
            data["VEI"] = data["VEI"].fillna(0).astype(int)
        if "Climate zone" in cols:
            data["Climate zone"] = pd.Categorical(
                data["Climate zone"],  # type: ignore
                categories=["Cold", "Temperate", "Subtropics", "Tropical"],
            )
        data.columns = cols
        self.data = data
        self.data_columns = cols
        self.data_units = units

    def check_vars_set(self):
        if not self._set_vars:
            raise RuntimeError("Variables are not set.  First run set_vars.")

    def set_vars(self, xvar: str, yvar: str):
        """Specify the observed variable (x-variable) and inferred variable (y-variable)

        Args:
            xvar (str): The explanatory variable.  Can be "H" for column height. Can be "Q" or "MER" for mass eruption rate.
            yvar (str): The predicted variable.  Can be "H" for column height.  Can be "Q" or "MER" for mass eruption rate.

        Raises:
            ValueError: if xvar is not "H" or "Q" or "MER".
            ValueError: if yvar is not "H" or "Q" or "MER".
            ValueError: if xvar == yvar.
            RuntimeError: if there are not sufficient data points in the data set to make predictions based on the explantory variable.
        """

        if xvar not in ["H", "Q", "MER"]:
            raise ValueError(f"xvar must be either H or Q or MER, received {xvar}")
        if yvar not in ["H", "Q", "MER"]:
            raise ValueError(f"yvar must be either H or Q or MER, received {yvar}")

        if xvar == yvar:
            raise ValueError(
                f"xvar must not be the same as yvar, received {xvar}, {yvar}"
            )

        self.xvar = xvar
        self.yvar = yvar

        x: npt.NDArray[np.float64]
        x = np.log10(self.height) if xvar == "H" else np.log10(self.mer)
        self.xvar_unit = "km" if xvar == "H" else "kg/s"

        y: npt.NDArray[np.float64]
        y = np.log10(self.height) if yvar == "H" else np.log10(self.mer)
        self.yvar_unit = "km" if yvar == "H" else "kg/s"

        # Cut out NaNs
        x_nans = np.isnan(x)  # Logical array with True corresponding to NaN
        y_nans = np.isnan(y)

        x = x[~x_nans & ~y_nans]  # Select values where both x and y are not NaNs
        y = y[~x_nans & ~y_nans]

        self._x = x
        self._y = y

        if x.size != y.size:
            raise RuntimeError(
                f"Data is not properly sized.  _x has size {x.size}, _y has size {y.size}"
            )

        self._set_vars = True

        n = x.size
        self.n = n

        matX: npt.NDArray[np.float64]
        matX = np.ones([n, 2], dtype=np.float64)  # type: ignore
        matX[:, 1] = x

        self._matX = matX
        self._matV = np.linalg.inv(np.matmul(matX.T, matX))  # type: ignore

        self.df = n - 2

        if self.df <= 0:
            raise RuntimeError("Too little data for statistics")

        self.xp = None

        self.mle()

    def mle_trace(self) -> pd.DataFrame:

        self.check_vars_set()

        x: npt.NDArray[np.float64]
        if self.xvar == "H":
            x = np.linspace(-1, 1.7, num=100, dtype=np.float64)  # type: ignore
        else:
            x = np.linspace(-1, 11, num=100, dtype=np.float64)  # type: ignore

        y = self.beta_vec[0] + self.beta_vec[1] * x

        if self.xvar == "H":
            height = np.power(10, x)
            mer = np.power(10, y)
        else:
            mer = np.power(10, x)
            height = np.power(10, y)

        df = pd.DataFrame(columns=["x", "y", self.mer_column, self.height_column])

        df["x"] = x
        df["y"] = y
        df[self.mer_column] = mer
        df[self.height_column] = height

        return df

    def mle(self, plot: bool = False):

        self.check_vars_set()

        self.beta_vec = np.matmul(np.matmul(self._matV, self._matX.T), self._y)

        a = self._y - np.matmul(self._matX, self.beta_vec)
        self.sigma2 = np.dot(a, a) / float(self.n - 2)  # type: ignore

        self.residual = self._y - np.matmul(self._matX, self.beta_vec)

        if plot:
            if self.xvar == "H":
                x = np.linspace(0, np.log10(50), num=100)  # type: ignore
            else:
                x = np.linspace(1, 11, num=100)  # type: ignore
            y = self.beta_vec[0] + self.beta_vec[1] * x
            mlefig, axs = plt.subplots(nrows=1, ncols=2)
            axs[0].scatter(self._x, self._y)  # type: ignore
            axs[0].plot(x, y)  # type: ignore
            axs[0].set_xlabel(r"$\log_{10}(" + self.xvar + ")$")  # type: ignore
            axs[0].set_ylabel(r"$\log_{10}(" + self.yvar + ")$")  # type: ignore
            if self.xvar == "H":
                axs[1].scatter(np.power(10, self._x), self._y)  # type: ignore
                axs[1].plot(np.power(10, x), y)  # type: ignore
            else:
                axs[1].scatter(self._x, np.power(10, self._y))  # type: ignore
                axs[1].plot(x, np.power(10, y))  # type: ignore
            axs[1].set_xlabel(r"${xvar}$".format(xvar=self.xvar))  # type: ignore
            axs[1].set_ylabel(r"$\log_{10}(" + self.yvar + ")$")  # type: ignore
            title = plotTitle(
                r"Maximum likelihood estimator for linear"
                + r" trend in log-transformed data"
            )
            plt.suptitle(title)
            mlefig.tight_layout(rect=[0, 0.03, 1, 0.95])
            if not is_interactive():
                mlefig.show()

    def set_obs(self, xp: npt.NDArray[np.float64], logscale: bool = False):

        self.check_vars_set()

        if logscale:
            self.xp = np.float64(np.atleast_1d(xp))  # type: ignore
        else:
            self.xp = np.log10(np.atleast_1d(xp), dtype=np.float64)  # type: ignore

        self.params()

    def params(self):
        # s2 = self.n * self.sigma2 / float(self.n - 2)

        Xp = np.ones([np.size(self.xp), 2])  # type: ignore
        Xp[:, 1] = self.xp

        mu = np.matmul(Xp, self.beta_vec)
        Id = np.identity(np.size(self.xp), dtype=np.float64)  # type: ignore
        Sigma2 = self.sigma2 * (Id + np.matmul(np.matmul(Xp, self._matV), Xp.T))  # type: ignore

        self.mu = mu
        self.Sigma = np.sqrt(np.diag(Sigma2))  # type: ignore

    def posterior_probability(
        self, yp: Union[np.float_, npt.NDArray[np.float_]]
    ) -> Dict[str, npt.NDArray[np.float64]]:

        self.check_vars_set()

        pz = t.pdf(yp, self.df, loc=self.mu, scale=self.Sigma)  # type: ignore
        cz = t.cdf(yp, self.df, loc=self.mu, scale=self.Sigma)  # type: ignore

        return {"cdf": cz, "pdf": pz}

    def posterior_point(
        self, pp: Union[np.float_, npt.NDArray[np.float_]]
    ) -> Union[np.float_, npt.NDArray[np.float_]]:

        self.check_vars_set()

        ppf = t.ppf(pp, self.df, loc=self.mu, scale=self.Sigma)  # type: ignore

        return ppf  # type: ignore

    def posterior_mean(self) -> npt.NDArray[np.float64]:
        # ONLY WORKS FOR SINGLE OBSERVATION

        self.check_vars_set()

        mean = t.mean(self.df, loc=self.mu, scale=self.Sigma)  # type: ignore

        return mean  # type: ignore

    def posterior_median(self) -> npt.NDArray[np.float64]:
        # ONLY WORKS FOR SINGLE OBSERVATION

        self.check_vars_set()

        median = t.median(self.df, loc=self.mu, scale=self.Sigma)  # type: ignore

        return median  # type: ignore

    def posterior_simulate(
        self,
        Nsamples: int,
        plot: bool = False,
        split_x: bool = False,
        as_dataframe: bool = False,
    ) -> Union[pd.DataFrame, npt.NDArray[np.float64]]:

        self.check_vars_set()

        if self.xp is None:
            raise ValueError(
                "No observation set.  Set observations with method set_obs before posterior_simulate."
            )

        alph = 0.5 * (self.n - 2)
        bet = 0.5 * (self.n - 2) * self.sigma2

        # Sample the posterior variance, sigma^2 | data
        sig2 = invgamma.rvs(alph, scale=bet, size=Nsamples)  # type: ignore

        Nx = len(self.xp)

        y: npt.NDArray[np.float64]
        if split_x:
            y = np.empty([Nsamples, Nx])  # type: ignore
        else:
            y = np.empty([Nsamples * Nx])  # type: ignore

        # Sample the posterior parameters, beta | sigma^2, data
        # and sample the posterior prediction y | beta, sigma^2, data
        for j in range(0, Nsamples):
            beta_vec = multivariate_normal.rvs(self.beta_vec, self._matV * sig2[j])  # type: ignore

            m = beta_vec[0] + beta_vec[1] * self.xp  # type: ignore

            y_pred = np.atleast_1d(norm.rvs(m, sig2[j]))  # type: ignore
            if split_x:
                y[j, :] = y_pred[:]
            else:
                y[j * Nx : (j + 1) * Nx] = y_pred.flatten()

        if plot:
            if self.yvar == "H":
                yy = np.power(10, y)
                xlab = "${}$".format(self.yvar)
                if split_x:
                    title = plotTitle(
                        r"Histogram of posterior predictive"
                        + r" distribution of $H$ with observation of $Q$"
                    )
                else:
                    if Nx > 3:
                        title = plotTitle(
                            r"Histogram of posterior predictive"
                            + r" distribution of $H$ with observation"
                            + r" {}".format(
                                sci_string(
                                    np.power(10, self.xp.min()), precision=1, latex=True
                                )
                            )
                            + r"$ \leq Q \leq $"
                            + " {}".format(
                                sci_string(
                                    np.power(10, self.xp.max()), precision=1, latex=True
                                )
                            )
                            + r" {}".format(self.xvar_unit)
                        )
                    else:
                        title_str = [
                            "Histogram of posterior predictive"
                            + r" distribution of $H$ with observation"
                            + r" $Q = $"
                        ]
                        for j in range(Nx):
                            title_str += sci_string(
                                np.power(10, self.xp[j]), latex=True
                            )
                            title_str += (
                                r", " if j < Nx - 1 else r" {}".format(self.xvar_unit)
                            )
                        title = plotTitle(title_str)
            else:  # self.yvar == "Q":
                yy = y
                xlab = r"$\log_{10}" + "{}$".format(self.yvar)
                if split_x:
                    title = plotTitle(
                        r"Histogram of posterior predictive"
                        + r" distribution of $Q$ with observation of $H$."
                    )
                else:
                    if Nx > 3:
                        title = plotTitle(
                            r"Histogram of posterior predictive"
                            + r" distribution of $Q$ with observation"
                            + r" ${:.1f} \leq H \leq {:.1f}$".format(
                                np.power(10, self.xp.min()), np.power(10, self.xp.max())
                            )
                            + r" {}".format(self.xvar_unit)  # type: ignore
                        )
                    else:
                        title = plotTitle(
                            r"Histogram of posterior predictive"
                            + r" distribution of $Q$ with observation"
                            + r" $H = {}$ {}".format(
                                np.power(10, self.xp), self.xvar_unit
                            )
                        )
            histfig, ax1 = plt.subplots()
            if split_x:
                cmap: List[str]
                cmap = color_palette("deep", n_colors=Nx, as_cmap=True)  # type: ignore
                for j in range(Nx):
                    if self.xvar == "H":
                        label = r"$H = {:.1f}$ {}".format(
                            np.power(10, self.xp[j]), self.xvar_unit
                        )
                    else:
                        label = (
                            r"$Q = $"
                            + sci_string(np.power(10, self.xp[j]), latex=True)
                            + r" {}".format(self.xvar_unit)
                        )
                    ax1.hist(  # type: ignore
                        yy[:, j],
                        50,
                        density=True,
                        facecolor=cmap[j],
                        alpha=0.75,
                        label=label,
                    )
            else:
                ax1.hist(  # type: ignore
                    yy, 50, density=True, facecolor="#005c8d", alpha=0.75
                )
            ax1.set_xlabel(xlab)
            ax1.set_ylabel("Probability")
            if split_x:
                ax1.legend()
            histfig.suptitle(title)
            ax1.grid(True)  # type: ignore
            if not is_interactive():
                histfig.show()

        if as_dataframe:
            if split_x:
                y_df = pd.DataFrame(
                    columns=[
                        f"log {self.xvar}",
                        f"log {self.yvar}",
                        self.xvar,
                        self.yvar,
                    ]
                )
                for j, x in enumerate(self.xp):  # (variable) x: np.float64
                    tmp_df = pd.DataFrame(
                        columns=[f"log {self.xvar}", f"log {self.yvar}"]
                    )
                    logy_col = f"log {self.yvar}"
                    tmp_df[logy_col] = np.float64(y[:, j])
                    logx_col = f"log {self.xvar}"
                    tmp_df[logx_col] = np.float64(x)
                    tmp_df[self.yvar] = np.float64(np.power(10, y[:, j]))
                    tmp_df[self.xvar] = np.float64(np.power(10, x))

                    y_df = pd.concat([y_df, tmp_df], ignore_index=True)
            else:
                y_df = pd.DataFrame(
                    columns=[
                        f"log {self.xvar}",
                        f"log {self.yvar}",
                        self.xvar,
                        self.yvar,
                    ]
                )
                if len(self.xp) == 1:
                    xp = self.xp * np.ones_like(y.flatten())
                    y_df[f"log {self.xvar}"] = np.float64(xp)
                else:
                    y_df[f"log {self.xvar}"] = np.float64(np.repeat(self.xp, Nsamples))
                y_df[self.xvar] = np.float64(np.power(10, y_df[f"log {self.xvar}"]))
                y_df[f"log {self.yvar}"] = np.float64(y.flatten())
                y_df[self.yvar] = np.float64(np.power(10, y_df[f"log {self.yvar}"]))

            y_df = y_df.astype("float64")
            return y_df

        return y

    def posterior_distribution(
        self,
        *,
        pscale: str = "Linear",
        xscale: str = "Log",
        N: int = 200,
        ylow: Optional[np.float64] = None,
        yhigh: Optional[np.float64] = None,
    ):

        self.check_vars_set()

        if self.xp is None:
            raise ValueError(
                "No observation set.  Set observations with method set_obs before posterior_simulate."
            )

        scale_allowed = {"Linear", "Log"}
        if pscale not in scale_allowed:
            raise ValueError(
                f"posterior_probability: pscale must be one of {scale_allowed}; received {pscale}"
            )
        if xscale not in scale_allowed:
            raise ValueError(
                f"posterior_probability: xscale must be one of {scale_allowed}; received {xscale}"
            )

        if ylow is None:
            ylow = 3.0 if self.xvar == "H" else 0.0  # type: ignore
        if yhigh is None:
            yhigh = 12.0 if self.xvar == "H" else log10(30.0)

        logx: npt.NDArray[np.float64]
        logx = np.linspace(ylow, yhigh, N)  # type: ignore
        df = self.posterior_probability(yp=logx)

        if xscale == "Log":
            xx = logx
        else:
            xx = np.power(10, logx)

        ypfig, ax1 = plt.subplots()
        if pscale == "Linear":
            ax1.plot(xx, df["cdf"], label="Cumulative distribution function")
            ax1.plot(xx, df["pdf"], label="Probabiltiy density function")
            ax1.set_ylabel(r"$p$")
        else:
            ax1.plot(xx, np.log10(df["cdf"]), label="Cumulative distribution function")
            ax1.plot(xx, np.log10(df["pdf"]), label="Probabiltiy density function")
            ax1.set_ylabel(r"$\log_{10}(p)$")
        ax1.legend()
        if xscale == "Log":
            ax1.set_xlabel(r"$\log_{10}" + "({})$".format(self.yvar))
        else:
            ax1.set_xlabel(r"${}$".format(self.yvar))
        if self.xvar == "H":
            title = plotTitle(
                r"Probability density functions for"
                + r" posterior prediction of ${}$ with observation".format(self.yvar)
                + r" ${}={}$ {}".format(
                    self.xvar, np.power(10, self.xp), self.xvar_unit
                )
            )
        else:  # self.xvar == "Q":
            title = plotTitle(
                r"Probability density functions for"
                + r" posterior prediction of ${}$".format(self.yvar)
                + r" with observation $Q = $"
                + r" {}".format(sci_string(np.power(10, self.xp[0]), latex=True))
                + r" {}".format(self.xvar_unit)
            )

        plt.suptitle(title)
        if not is_interactive():
            ypfig.show()

    def posterior_ppf(
        self, pp: Union[np.float_, npt.NDArray[np.float64]]
    ) -> Union[np.float64, npt.NDArray[np.float64]]:

        self.check_vars_set()

        ppf = t.ppf(pp, self.df, loc=self.mu, scale=self.Sigma)  # type: ignore

        return ppf  # type: ignore

    def posterior_ppf_plot(self, *, plow: float = 0.01, phigh: float = 0.99):

        self.check_vars_set()

        if self.xp is None:
            raise ValueError(
                "No observation set.  Set observations with method set_obs before posterior_simulate."
            )

        pp = npt.NDArray[np.float64]
        pp = np.linspace(plow, phigh, 100, dtype=np.float64)  # type: ignore

        ppf = self.posterior_ppf(pp)

        ppfig, ax1 = plt.subplots()
        ax1.plot(pp, ppf)
        if self.xvar == "H":
            ax1.set_xlabel(
                r"$p(\log_{10} Q < \log_{10} q | \log_{10} H = "
                + r" {})$".format(self.xp)
            )
            ax1.set_ylabel(r"$\log_{10} (q)$")
            title = plotTitle(
                r"Probability point function for"
                + r" posterior prediction of ${}$ with observation".format(self.yvar)
                + r" ${}={}$ {}".format(
                    self.xvar, np.power(10, self.xp), self.xvar_unit
                )
            )
        else:  # self.xvar == "Q"
            ax1.set_xlabel(
                r"$p(\log_{10} H < \log_{10} h | \log_{10} Q = "
                + r" {})$".format(self.xp)
            )
            ax1.set_ylabel(r"$\log_{10} (h)$")
            title = plotTitle(
                r"Probability point function for"
                + r" posterior prediction of ${}$ with observation ${} = $".format(
                    self.yvar, self.xvar
                )
                + r" {}".format(sci_string(self.xp, latex=True))
                + r" {}".format(self.xvar_unit)
            )
        plt.suptitle(title)
        if not is_interactive():
            ppfig.show()

    def posterior_data(self) -> Dict[str, npt.NDArray[np.float64]]:

        self.check_vars_set()

        if self.xp is not None:
            xp = self.xp
        else:
            xp = None

        n_q: int = 100
        n_h: int = 200

        qq: npt.NDArray[np.float64]
        qq = np.linspace(  # type: ignore
            np.amin(np.log10(self.mer)) - 1,  # type: ignore
            np.amax(np.log10(self.mer)) + 1,  # type: ignore
            n_q,
        )
        hh: npt.NDArray[np.float64]
        hh = np.linspace(-1, log10(50), n_h)  # type: ignore

        logparr = np.zeros([n_h, n_q])  # type: ignore
        parr = np.zeros([n_h, n_q])  # type: ignore

        if self.xvar == "H":
            for j in range(0, n_h):
                self.set_obs(hh[j], logscale=True)
                prob = self.posterior_probability(yp=qq)
                parr[j, :] = prob["pdf"]
                logparr[j, :] = np.log10(prob["pdf"])
        else:  # self.xvar == "Q":
            for j in range(0, n_q):
                self.set_obs(qq[j], logscale=True)
                prob = self.posterior_probability(yp=hh)
                parr[:, j] = prob["pdf"]
                logparr[:, j] = np.log10(prob["pdf"])

        if xp is not None:
            self.set_obs(xp, logscale=True)
        else:
            self.xp = None

        return {
            "logQ": qq,
            "Q": np.power(10, qq),
            "logH": hh,
            "H": np.power(10, hh),
            "logp": logparr,
            "p": parr,
        }

    def posterior_plot(self):

        self.check_vars_set()

        if self.xp is not None:
            xp = self.xp
        else:
            xp = None

        pdata = self.posterior_data()

        if self.xvar == "H":
            ppcfig, ax1 = plt.subplots()
            cntrs = plt.contourf(
                pdata["H"], pdata["logQ"], pdata["logp"].T, [-5, -4, -3, -2, -1, 0, 1]
            )
            cbar = plt.colorbar(cntrs)
            cbar.ax.set_ylabel("probability density", labelpad=15, rotation=270)
            cbar.ax.set_yticklabels(
                [
                    r"$10^{-5}$",
                    r"$10^{-4}$",
                    r"$10^{-3}$",
                    r"$10^{-2}$",
                    r"$10^{-1}$",
                    r"$1$",
                    r"$10$",
                ]
            )
            ax1.scatter(self.height, np.log10(self.mer), color="r")  # type: ignore

            y = self.beta_vec[0] + self.beta_vec[1] * pdata["logH"]
            ax1.plot(pdata["H"], y, color="r")

            ax1.set_xlabel(r"Plume height $H$ (km)")
            ax1.set_ylabel(r"Mass Eruption Rate $MER$ (kg/s)")
            yticks = np.arange(np.floor(pdata["logQ"][0]), np.ceil(pdata["logQ"][-1]), dtype=int)  # type: ignore
            ax1.set_yticks(yticks)
            ax1.set_yticklabels([r"$10^{yy}$".format(yy=y) for y in yticks])
            ax1.set_ylim([pdata["logQ"][0], pdata["logQ"][-1]])

            title = plotTitle(
                r"Posterior distribution for MER|H and observational data"
            )

        else:  # self.xvar == "Q":
            ppcfig, ax1 = plt.subplots()
            cntrs = plt.contourf(
                pdata["logQ"],
                pdata["H"],
                pdata["logp"],
                [-3, -2, -1, 0, 1, 2, 3],
            )
            cbar = plt.colorbar(cntrs)
            cbar.ax.set_ylabel("probability density", labelpad=15, rotation=270)
            cbar.ax.set_yticklabels(
                [
                    r"$10^{-3}$",
                    r"$10^{-2}$",
                    r"$10^{-1}$",
                    r"$1$",
                    r"$10$",
                    r"$100$",
                    r"$1000$",
                ]
            )
            ax1.scatter(np.log10(self.mer), self.height, color="r")  # type: ignore
            ax1.set_xlabel(r"$\log_{10} Q$")
            ax1.set_ylabel(r"$H$")
            title = plotTitle(r"Posterior distribution for H|Q and observational data")

        plt.suptitle(title)
        if not is_interactive():
            ppcfig.show()

        if xp is not None:
            self.set_obs(xp, logscale=True)
        else:
            self.xp = None
        return ax1

    def posterior_quantiles_plot(self):

        self.check_vars_set()

        if self.xp is not None:
            xp = self.xp
        else:
            xp = None

        alphas = 10.0 ** (np.arange(-5, 0, 1))
        alphas = np.concatenate([alphas, np.array([0.05, 0.25, 0.45, 0.495])])
        alphas = np.concatenate([alphas, 1 - alphas])
        alphas = np.sort(alphas)
        n_alphas = alphas.size
        n_ints = n_alphas // 2

        n_steps: int = 100
        if self.xvar == "H":

            h0: npt.NDArray[np.float64]
            h0 = np.linspace(0, log10(50), n_steps)  # type: ignore
            q_intervals = np.zeros((n_steps, n_alphas))

            q0 = np.zeros((n_steps))

            for j, hh in enumerate(h0):
                self.set_obs(hh, logscale=True)
                q0[j] = self.mu
                q_intervals[j, :] = self.posterior_point(alphas)

            colormap = color_palette("flare", n_ints)
            sm = LinearSegmentedColormap.from_list("p", colormap, N=n_ints)
            ppcfig, ax1 = plt.subplots()
            for j in range(n_alphas - 1):
                k = j if j < n_ints else n_ints - j - 1
                ax1.fill_betweenx(
                    10**h0,
                    10 ** q_intervals[:, j],
                    10 ** q_intervals[:, j + 1],
                    facecolor=colormap[k],
                    edgecolor=colormap[k],
                    alpha=1,
                )
            ax1.plot(10**q0, 10**h0, color=(0.266, 0.075, 0.290))
            ax1.set_xscale("log")

            fig2, ax2 = plt.subplots()
            sc = ax2.scatter(
                np.arange(n_ints),
                np.arange(n_ints),
                c=np.arange(n_ints),
                cmap=sm,
            )
            ax1_divider = make_axes_locatable(ax1)
            cbar_ax = ax1_divider.append_axes("right", size="7%", pad="2%")
            ppcfig.colorbar(sc, cax=cbar_ax)
            tick_locs = (np.arange(n_ints) + 0.5) * (n_ints - 1) / n_ints
            cbar_ax.set_yticks(tick_locs)
            clabels = [sci_string(p, precision=2, latex=True) for p in alphas[:n_ints]]
            cbar_ax.set_yticklabels(clabels)
            plt.close(fig2)

            ax1.scatter(self.mer, self.height, color="darkgrey")  # type: ignore

            ax1.set_xlim([0.75 * self.mer.min(), 1.25 * self.mer.max()])
            ax1.set_ylim([0.75 * self.height.min(), 1.25 * self.height.max()])

            ax1.set_xlabel(r"$Q$")
            ax1.set_ylabel(r"$H$")
            title = plotTitle(
                r"Posterior predictive distribution for MER|H and observational data"
            )

        else:  # self.xvar == "Q":
            q0: npt.NDArray[np.float64]
            q0 = np.linspace(1, 9, n_steps)  # type: ignore
            h_intervals = np.zeros((n_steps, n_alphas))

            h0 = np.zeros((n_steps))

            for j, qq in enumerate(q0):
                self.set_obs(qq, logscale=True)
                h0[j] = self.mu
                h_intervals[j, :] = self.posterior_point(alphas)

            colormap = color_palette("flare", n_ints)
            sm = LinearSegmentedColormap.from_list("p", colormap, N=n_ints)
            ppcfig, ax1 = plt.subplots()
            for j in range(n_alphas - 1):
                k = j if j < n_ints else n_ints - j - 1
                ax1.fill_between(
                    10**q0,
                    10 ** h_intervals[:, j],
                    10 ** h_intervals[:, j + 1],
                    facecolor=colormap[k],
                    edgecolor=colormap[k],
                    alpha=1,
                )
            ax1.plot(10**q0, 10**h0, color=(0.266, 0.075, 0.290))
            ax1.set_xscale("log")

            fig2, ax2 = plt.subplots()
            sc = ax2.scatter(
                np.arange(n_ints),
                np.arange(n_ints),
                c=np.arange(n_ints),
                cmap=sm,
            )
            ax1_divider = make_axes_locatable(ax1)
            cbar_ax = ax1_divider.append_axes("right", size="7%", pad="2%")
            ppcfig.colorbar(sc, cax=cbar_ax)
            tick_locs = (np.arange(n_ints) + 0.5) * (n_ints - 1) / n_ints
            cbar_ax.set_yticks(tick_locs)
            clabels = [sci_string(p, precision=2, latex=True) for p in alphas[:n_ints]]
            cbar_ax.set_yticklabels(clabels)
            plt.close(fig2)

            ax1.scatter(self.mer, self.height, color="darkgrey")  # type: ignore

            ax1.set_xlim([0.75 * self.mer.min(), 1.25 * self.mer.max()])
            ax1.set_ylim([0.75 * self.height.min(), 1.25 * self.height.max()])
            ax1.set_xlabel(r"$Q$")
            ax1.set_ylabel(r"$H$")
            title = plotTitle(
                r"Posterior predictive distribution for H|Q and observational data"
            )

        plt.suptitle(title)
        if not is_interactive():
            ppcfig.show()

        if xp is not None:
            self.set_obs(xp, logscale=True)
        else:
            self.xp = None
        return ax1


def read_excel(
    xls: IO,  # Union[str, TextIO, BinaryIO],
    name: Optional[str] = None,
    Height: str = "H",
    MER: str = "Q",
    skiprows: int = 0,
) -> QHstats:
    df = pd.read_excel(xls, skiprows=skiprows)  # type: ignore

    return QHstats(df, name=name, Height=Height, MER=MER)


def read_csv(
    csv: IO, name: Optional[str] = None, Height: str = "H", MER: str = "Q"
) -> QHstats:
    df = pd.read_csv(csv)  # type: ignore

    return QHstats(df, name=name, Height=Height, MER=MER)
