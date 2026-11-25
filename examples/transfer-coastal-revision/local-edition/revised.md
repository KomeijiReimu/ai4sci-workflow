# Temporal Trends in Sea-Level Rise Acceleration Along the Dutch Coast

**Proposed local revision of the cited v1 preprint (not approved by its original authors).**

Iris Keizer, Dewi Le Bars, Cees de Valk, André Jüling, Roderik van de Wal, Sybren Drijfhout. Original discussion preprint: 10.5194/egusphere-2022-935, posted 2022-10-04. CC BY 4.0. Source: https://egusphere.copernicus.org/preprints/2022/egusphere-2022-935/egusphere-2022-935.pdf. Editable text extraction of the complete original, not a facsimile: layout, figures and mathematical typography are not preserved. Figure numbers/captions and original page references are retained.

## Original PDF page 1

     https://doi.org/10.5194/egusphere-2022-935
     Preprint. Discussion started: 4 October 2022
      c Author(s) 2022. CC BY 4.0 License.




     Temporal Trends in Sea-Level Rise Acceleration Along the Dutch Coast
     Iris Keizer1 , Dewi Le Bars1 , Cees de Valk1 , André Jüling1 , Roderik van de Wal2,3 , and
     Sybren Drijfhout1,2
     1
       Royal Netherlands Meteorological Institute (KNMI), De Bilt, The Netherlands
     2
       Institute for Marine and Atmospheric Research Utrecht, Utrecht University, Utrecht, The Netherlands
     3
       Department of Physical Geography, Utrecht University, Utrecht, The Netherlands
     Correspondence: Iris Keizer (iris.keizer@knmi.nl)

     Abstract.
While a global acceleration of sea-level rise (SLR) during the 20th century is now established, locally acceleration is more difficult to detect because additional processes play a role which sometimes mask the acceleration. Here we study the rate of SLR along the coast of the Netherlands from six tide gauge records, covering the period 1890–2020. We focus on the influence of the wind field and the nodal tide variations on the local sea-level trend. We use four generalised additive models, including different predictive variables, and a parametric bootstrap method to compute the sea-level trend. From the sea-level trend, we obtain the continuous evolution of the rate of SLR and its uncertainty over the observational period through differentiation. The 1960–2019 period shows a higher rate (2.26 mm/yr) than the 1900–1959 period (1.82 mm/yr) under the Tr model, with a fitted difference of 0.44 mm/yr (conditional spread-only band −0.26 to 1.06 mm/yr). The 1970–2019 minus 1900–1959 contrast shows a 0.55 mm/yr increase in the Tr model, with uncertainty bands crossing zero.
         A small but significant part of the long-term sea-level trend is due to wind forcing related to a strengthening and northward
     shift of the jet stream. Additionally, we detect a multidecadal mode of sea-level variability forced by the wind with an amplitude
     of around 1 cm. We argue that it is related to multi-decadal sea surface temperature variations in the North Atlantic, similar to
     the Atlantic Multidecadal Variability.




                                                                     1


## Original PDF page 2

     https://doi.org/10.5194/egusphere-2022-935
     Preprint. Discussion started: 4 October 2022
      c Author(s) 2022. CC BY 4.0 License.




     1    Introduction

     Understanding the current and past rates of sea level rise (SLR) is essential to make reliable sea-level projections and to adapt
     accordingly. In the Netherlands, the current rate of SLR is used to estimate the volume of sand that must be supplied to maintain
     the coastline and avoid a retreat of dunes. It also estimates how much salt and gas mining can be allowed under the Wadden
25   Sea. In addition, local sea-level measurements are important to evaluate sea-level projections (Vries et al., 2014) and could be
     used as an early warning indicator for adaptation measures to uncertain climate change (Haasnoot et al., 2018).
         There is now high confidence in an acceleration of global SLR in the 20th century compared to the previous three millennia
     and in the period 2006-2018 compared to 1971-2018 (Fox-Kemper et al., 2021). More recently, Walker et al. (2022) estimated
     the time when the rate of global SLR emerged from the background variability of the Common Era (0-2000CE) to the middle
30   of the 19th century. For the North-East Atlantic, they found this emergence to occur around the middle of the 20th century.
     This is in line with Dangendorf et al. (2019) who found a global acceleration of SLR from the 1960s.
         Along the coast of the Netherlands, there has been an ongoing debate about whether an acceleration of SLR takes place or not
     (Baart et al., 2011; Wahl et al., 2013; Steffelbauer et al., 2022). There are multiple lines of evidence that an acceleration should
     already be detectable or will be detectable soon. Global acceleration of SLR is driven by the increasing thermal expansion of
35   oceans and faster melting glaciers and ice sheets. These mechanisms are also expected to contribute to SLR in the North Sea.
     However, the contribution of mass loss from the Greenland Ice Sheet is much smaller than the globally averaged contribution
     due to gravitational effects (Slangen et al., 2012). Additionally, the ocean dynamic sea level is expected to rise along the North-
     East Atlantic (Lyu et al., 2020; Hermans et al., 2022) and dynamic sea-level projections based on climate models from the
     Coupled Model Intercomparison Project (CMIP5 and CMIP6) also expect an acceleration. Combined, the expectation for the
40   climate-driven sea-level change along the Dutch coast is close to the global mean changes. (Vries et al., 2014; Fox-Kemper
     et al., 2021).
         The data availability along the Dutch coast is much better than for reconstructed global sea level (Dangendorf et al., 2019;
     Frederikse et al., 2020). There are six tide gauges measuring sea level with very little missing data since at least 1890. Therefore,
     it is interesting to study the local acceleration in SLR. The issue with detecting regional acceleration of SLR comes from the
45   large interannual to multidecadal variability from atmospheric forcing, especially important for shallow seas like the North
     Sea (Gill, 1982; Hermans et al., 2020), and from similar variations in local steric sea level (Bingham and Hughes, 2012).
     Understanding and removing the interannual to multidecadal sources of variability from tide gauge records was found to be
     essential for detecting an acceleration of SLR (Haigh et al., 2014). To this end, multilinear regression models between sea levels
     and atmospheric variables like sea-level pressure gradients, zonal and meridional wind velocity and sometimes precipitation
50   as predictive variables have been used by various authors. For example, this approach was applied to Cuxhaven in the German
     Bight by Dangendorf et al. (2013) and multiple regions by Calafat and Chambers (2013). Nevertheless, there is no generally
     agreed approach for detecting an acceleration of SLR from tide gauge stations. Sometimes the observed records are extended
     by sea-level projections, and the acceleration is defined as a rate of SLR significantly larger than observed, which only allows
     for finding an acceleration in the future (Haigh et al., 2014; Dangendorf et al., 2014a). Some studies compared the rate between



                                                                      2


## Original PDF page 3

     https://doi.org/10.5194/egusphere-2022-935
     Preprint. Discussion started: 4 October 2022
      c Author(s) 2022. CC BY 4.0 License.




55   two periods (Calafat and Chambers, 2013; Steffelbauer et al., 2022) and others fitted a second-degree polynomial to the data
     (Haigh et al., 2014; Dangendorf et al., 2019). In general, the variability due to atmospheric forcing was first estimated by
     linearly detrending the time series. After that, the variability is removed from the sea level data before estimating the trend
     and acceleration. Of these previous studies of SLR in the North Sea, many studies did not find evidence of a significant
     acceleration of SLR (Calafat and Chambers, 2013; Wahl et al., 2013; Haigh et al., 2014; Ezer et al., 2016) whereas Steffelbauer
60   et al. (2022) did. To detect the acceleration of SLR in the North Sea, Steffelbauer et al. (2022) analysed the 100-year time series
     (1919-2018) of eight tide gauges and found a common breakpoint in the early 1990s. The calculated rate of mean SLR of the
     stations increases from 1.7±0.3 mm/yr before the breakpoint to 2.7 ±0.4 mm/yr after the breakpoint implying an acceleration.
     Moreover, the prior distribution adopted for the rate of SLR before and after the breakpoint assumes that the latter rate can not
     be smaller than the former rate, which implies that acceleration is assumed from the beginning.
65       In this paper, we use a new time series approach which uses a Generalised Additive Model (GAM), which allows us to
     estimate a nonlinear trend and the optimal multilinear regression model simultaneously. The zonal wind and nodal tide are
     included in the GAM as predictive variables. To reduce the uncertainty in the estimated rate of SLR, only the most important
     predictor for the atmospheric forcing, the zonal wind, is used, unlike in many previous studies. Also, other authors did not
     always include the nodal cycle as a predictive variable. Using the GAM, we avoid making strong assumptions about the shape
70   of the sea-level trend like a linear shape as was assumed by Calafat and Chambers (2013); Steffelbauer et al. (2022). The
     sea-level trend is obtained as a smooth curve representing the long-term change in the data. This trend is then differentiated
     to compute the rate of SLR. Also, using the GAM allows us to obtain an evolution of the rate of SLR over the observational
     period, as has not been obtained previously. We also apply a rigorous parametric bootstrap method to estimate the uncertainty
     in the rate of SLR, which avoids the assumption that the noise is serially uncorrelated. Furthermore, comparing estimates of the
75   rate of SLR with and without the effects of zonal wind and nodal cycle allows us to study the influence of these processes on
     SLR along the coast of the Netherlands. We also discuss the physical mechanisms driving the wind-driven sea-level variations
     in the North Sea.


     2     Data

     2.1    Tide Gauge Observations

80   Annual-mean sea-level measurements are used from the six reference tide gauges along the coast of the Netherlands: Delfzijl,
     Den Helder, Harlingen, IJmuiden, Hoek van Holland and Vlissingen. These stations are used for operational sea level moni-
     toring because of their extended temporal coverage and uniform distribution along the Dutch coast (Baart et al., 2019). The
     measurements are provided by the Permanent Service for Mean Sea Level (Holgate et al., 2013) and were retrieved on Novem-
     ber 1st, 2021 from http://www.psmsl.org/data/obtaining/. While the time series for the different stations start between 1862
85   and 1872, only 1890 to 2020 are used for the analysis. As was done for other studies, tide gauge data is limited to the period
     after 1890 to avoid the inclusion of a sea-level jump around 1885 (Frederikse and Gerkema, 2018; Baart et al., 2019). From



                                                                     3


## Original PDF page 4

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      that year, the monthly mean sea level is based on mean sea-level readings rather than mean tide level readings, which could
      result in a jump in the monthly data (Woodworth, 2017).

      2.2    Atmospheric Reanalysis

90    We use the monthly mean zonal wind at 10 m and atmospheric pressure at sea level from two atmospheric reanalysis products.
      The first product, the ERA5 reanalysis, from the Copernicus Climate Change service Climate Data Store, is available from
      1979 to 2020 with a backward extension to 1950 (Hersbach et al., 2020; Bell et al., 2021). ERA5 has a spatial resolution of
      0.25°×0.25°. The second product, the Twentieth Century Reanalysis Version 3 (20CRv3) from the National Oceanographic
      and Atmospheric Administration (NOAA), is available from 1836 to 2015 (Slivinski et al., 2019). The data from this analysis
95    has a spatial resolution of 1.0°×1.0°.


      3     Method

      3.1    Statistical Models

      Four statistical models were developed and used to unravel the influence of different factors on SLR and to extract the back-
      ground sea-level trend. All models are based on the Generalised Additive Model (GAM, Hastie and Tibshirani (2017); Wood
100   (2020)) and are estimated by penalised maximum likelihood. Compared to a multi-linear regression model, a GAM replaces
      the strict assumption of a linear or quadratic shape of the sea-level trend by a sum of many smooth functions. This offers the
      advantage that we are not required to make a priori assumptions about the shape of the sea-level trend. In our four models, the
      GAM represents the annual-mean sea level averaged over the six tide gauges as a smooth curve (a linear combination of many
      smooth cubic B-spline basis functions) plus terms representing the influence of the predictive variables. The smooth curve
105   represents the background variation in sea level to be estimated; its exact meaning depends on the choice of the predictive
      variables. Its smoothness is controlled by a penalty term subtracted from the log-likelihood, which is proportional to the time-
      integral of the squared curvature of the smooth term Wood (2020). The penalty term was assigned a weight tuned to match the
      variance of the smooth curve to the variance of a 30-year average.
          The first model estimates the sea-level trend only (Tr) without using any predictive variables. This setup is equivalent to
110   assuming we do not know anything about the drivers of SLR. We use this model as a reference to evaluate the improvements
      achieved by increasing the model complexity. In the second model, the influence of the lunar nodal tide on sea level is added
      (TrNc). Two sinusoidal waves in opposition of phase with unknown amplitude and a fixed period of 18.613 years, the period of
      the nodal tide potential, are included as a predictive variable for the nodal cycle in the GAM. There has been some debate in the
      literature about the best way to estimate the influence of the nodal cycle on sea level in the North Sea. Using linear regression
115   to estimate the effect of the nodal tide along the Dutch coast shows an increased magnitude and shift in the phase compared to
      the equilibrium tides (Baart et al., 2011). However, using a closed sea-level budget, Frederikse et al. (2016) suggested that there
      is no indication that the nodal cycle deviates from the equilibrium tide in the North Sea between 1958 and 2014. We find that



                                                                      4


## Original PDF page 5

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      assuming equilibrium tides leaves a large amount of energy in the spectrum close to the period of the nodal cycle. Therefore,
      we decide to use a linear regression model with an undetermined phase and amplitude but a fixed period as in Baart et al.
120   (2011) even though it might remove some additional variability around the period of nodal tides. Using this second model, the
      influence of the nodal cycle on the trend and variability of sea level can be studied.
        The third and fourth models combine trend, nodal cycle and wind. For the third model, wind effects are included by adding
      u|u| (TrNcZw), where u is the zonal wind from reanalysis averaged over the closest grid cell of each tide gauge (Fig. 1a). This is
      inspired by the wind stress formulation (Dangendorf et al., 2019) but simplified to keep only the zonal wind component. Along
125   the Dutch coast, the zonal wind is much more important for sea-level changes than the meridional wind (see Figs. 7 and 8 from
      Frederikse and Gerkema (2018) and Fig. 4 from Dangendorf et al. (2014a)) and both wind components are highly correlated.
      The fourth model uses a large-scale pressure gradient as a predictive variable for the wind effect on sea level (TrNcPd). As
      in Dangendorf et al. (2014b), we compute the Pearson correlation coefficient between linearly detrended sea level along the
      Dutch coast and atmospheric pressure at sea level (Fig. 1b). This shows a similar pattern as was previously obtained for the
130   German bight (Dangendorf et al., 2014b). The pattern is characterised by a region of negative correlation over Scandinavia and
      a positive correlation over southern Europe/northern Africa. Each of these regions defines a box where the average pressure is
      computed. Then, instead of using the pressure in both boxes as predictive variables as in Dangendorf et al. (2014b), we take
      the difference between the southern and northern boxes. This adds only one variable to the model and is physically motivated
      by the fact that the meridional pressure gradient is related to the zonal wind by geostrophy. To cover the period from 1836
135   to 2020, we combine the variables representing wind effects from the two reanalysis datasets using a linear bias correction
      method (Casanueva et al., 2013). The ERA5 dataset is used as reference data. The mean and standard deviation of the 20CRv3
      pressure and zonal wind time series are adjusted over the overlap period, 1950-2015, to match those of ERA5.

      3.2   Analysis of Model Output

      The wind influence on sea level can be obtained from the results of the TrNcZw and TrNcPd GAMs. Once the linear regression
140   coefficients are obtained between 1890 and 2020, the wind influence on sea level can be extended back to 1836, the beginning
      of the 20CRv3 atmospheric reanalysis. We estimate the wind-driven sea-level trend using a 3rd-degree polynomial fit to the
      annual-mean data. Also, a spectral analysis is performed on the detrended annual-mean data. The spectra are obtained using a
      multitaper method (Lees and Park, 1995). To obtain the low-frequency wind influence on sea level, the detrended annual-mean
      sea level data is smoothed using a local polynomial regression (LOWESS, Cleveland and Devlin (1988)) with a window of 21
145   years that effectively removes high-frequency variability.
        Using our four statistical models, we obtain the background sea-level trend. As a next step, the rate of SLR is obtained from
      differentiating these estimated smooth sea-level trends. The rates of SLR resulting from the different models do not include the
      same physical processes. TrNcZw and TrNcPd do not include the contribution from wind and nodal effects and TrNc does not
      include nodal effects while Tr includes all processes.




                                                                      5


## Original PDF page 6

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




150   3.3   Uncertainty Computation

      To estimate our models from the data, we use a generic method for likelihood-based estimation of GAM (Wood, 2020).
      It treats the unknown noise terms as independent identically distributed normal random variables. However, checks of the
      residuals reveal that they are serially correlated, so the independence assumption is not warranted. This does not invalidate the
      method: since only marginal parameters are estimated, the estimator is consistent under weak assumptions on the dependence;
155   see Section 2 of Cox and Reid (2004). However, serial dependence of the noise affects the covariance of the estimated model
      parameters, so for deriving confidence intervals and for testing hypotheses, we must account for it. Our estimator for the rate of
      SLR (the finite difference of the smooth spline estimate of the variation in sea level) is particularly sensitive to low-frequency
      components of the noise. Our error analysis must account for these subtle aspects of serial dependence. Therefore, we apply
      a parametric bootstrap method based on the noise spectrum, similar to the Wild Bootstrap version of the technique in Kirch
160   and Politis (2011): we estimate the noise spectrum, using the same method as described in the previous section, and generate
      random instances of the gaussian process having this spectrum. From these, we obtain instances of the sea level time series
      by adding the estimates of the non-random terms. Then we apply the GAM-based estimator for our models to each of these
      instances to obtain an estimate of the rate of SLR. This sample of estimates is used to derive the error statistics and to test
      hypotheses.

### Period comparison (revision)

To reproduce whole/pre/post and paired bands, use the fitted central-derivative rates and conditional sensitivity bands from the v1 GAM. Annual rate at year t is 10 × (fitted trend in cm at t+1 minus trend at t−1) / 2 years, in mm/yr. We averaged these rates over inclusive year labels, not level endpoints. For each of 100 author-produced realization columns, we averaged the rates within each window, then subtracted its own earlier-period mean from its later-period mean. The empirical draw centers differ from the fitted rates: e.g., for Tr over 1900–2019 the raw draw mean is 4.04 mm/yr, versus 2.04 mm/yr fitted. We therefore report the 2.5th and 97.5th percentiles of the *centered* draws translated to the fitted point as a conditional spread diagnostic only; these are not the original Figure 4 5th–95th percentile ranges, established confidence limits, or null-test p-values. No GAM was refitted.

165     However, because the estimate of the rate of SLR is sensitive to low-frequency noise, we cannot assume that the noise
      spectrum is sufficiently closely approximated by the spectrum of the residuals, as Kirch and Politis (2011) do. Therefore, we
      need to estimate the noise spectrum from the spectrum of the residuals. A simple iterative correction scheme solves this inverse
      problem. Given a guess of the noise spectrum, we simulate random instances of sea level time series as above. For each, we
      estimate the model coefficients, derive the residuals, estimate their spectrum and average these estimates. The quotient of this
170   average to the guess is the mean effect of model estimation. The spectrum of the residuals is then corrected by dividing it
      by this quotient. The result is used as a guess for the next step. The iteration is initialised with the spectrum of the residuals.
      It converges within 3 to 5 iterations. The spectrum of the residuals and the estimated noise spectrum differ only in the low
      frequencies, as some of the noise in this band is absorbed in the spline term.


      4 Results

175   4.1   Comparison of the Different GAMs

      The GAM progressively better fits the data, measured by the deviance (Tbl. 1), as the complexity of the model increases (e.g.,
      the number of predictive variables increases), measured by the number of degrees of freedom (Tbl. 1). The deviance is used to
      compare generalised linear models and is a generalisation of the sum of squares of residuals used to compare linear regression
      models (Wood, 2020). Including the nodal cycle reduces the deviance by 12%, and including the wind further reduces the
180   deviance by an additional 37% for TrNcPd to 58% for TrNcZw implying that the best fit is obtained for TrNcZw. The improved




                                                                      6


## Original PDF page 7

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




       (a)                                                                (b)




      Figure 1. (a) Location of the six tide gauges used to define the mean sea level along the Dutch coast and of the zonal wind data used from the
      atmospheric reanalyses. (b) The correlation coefficient between sea level along the Dutch coast and atmospheric pressure at sea level from
      20CRv3 reanalysis between 1890 and 2015. Both variables are linearly detrended.


                                                                                      Degrees of freedom     Deviance
                                  Statistical model

                                  Tr : Trend only                                                      4.6        1167
                                  TrNc : Trend and nodal tide                                          6.6        1031
                                  TrNcPd : Trend, nodal tide and wind (pressure)                       7.6         652
                                  TrNcZw : Trend, nodal tide and wind (velocity)                       7.6         428
      Table 1. Summary of statistical model performance. The number of degrees of freedom includes the number of predictive variables and the
      number of basis functions used by the B-spline method. The deviance is a generalisation of the sum of squares of residuals used to compare
      linear regression models.



      fit for TrNcZw could be explained by the fact that here the local zonal wind is used, whereas for TrNcPd, a simplification of
      large-scale zonal wind is used.
        The resulting fits can be seen in Fig. 2. When more predictive variables for the wind are included in the model, like the
      meridional wind or wind taken at multiple locations in the North Sea, the deviance can be further reduced. However, the
185   increased degrees of freedom increase the standard error in estimating the trend (not shown). Therefore, we find that using only
      one predictive variable for the wind is the best choice for estimating the sea-level trend.




                                                                            7


## Original PDF page 8

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




                                           20
                                           15
                                           10
                          Sea level [cm]



                                            5
                                            0
                                            5                                             Tide gauge
                                                                                          Tr
                                           10                                             TrNc
                                           15                                             TrNcZw
                                                1900 1925 1950 1975 2000 2025
                                                         Time [years]

      Figure 2. Comparison of the annual tide gauge data averaged over 6 tide gauges along the Dutch coast with three Generalised Additive
      Models (Tr, TrNc, TrNcZw)


      4.2   Wind Influence on Sea Level

      Figure 3a shows the resulting wind influence on sea level, where the large interannual variability stands out. From these
      annual-mean time series, we estimate the wind-driven sea-level trend as is shown in Fig. 3b. For the second period, 1928-2020,
190   the wind-driven trend is 0.12 mm/yr and 0.15 mm/yr for respectively TrNcZw and TrNcPd. Long-term strengthening of the
      zonal wind has increased the sea level along the coast of the Netherlands. This long-term strengthening of the zonal wind
      is consistent with the observed northward shift and increased speed of the jet stream, which could be due to a decreasing
      temperature gradient between the North Pole and the equator at the height of the tropopause (Fig. 7d and 9d from Hallam et al.
      (2022)). A long-term influence of atmospheric drivers (zonal and meridional wind and surface pressure) was found earlier
195   for the period 1953-2003 (Fig. 2c from Dangendorf et al. (2014a)), but our results are in contradiction with the atmospheric-
      driven sea-level drop over the period 1900-2011 found by the same authors. This could be due to an update in the atmospheric
      reanalysis (20CRv3 instead of 20CRv2).
        After removing the trend from the data in Fig. 3a, a spectral analysis is performed (Fig. 3c). The spectra of the wind-impact
      on sea level obtained using both TrNcZw and TrNcPd have a similar shape, but the total variance is larger for TrNcZw compared
200   to TrNcPd which is a result of the larger interannual variability of TrNcZw as shown in Fig. 3a. For both methods, there is more


                                                                       8


## Original PDF page 9

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      energy in the signal for periods larger than two decades than for smaller periods. Therefore, the signals are smoothed using
      a local polynomial regression (LOWESS, Cleveland and Devlin (1988)) with a window of 21 years that effectively removes
      high-frequency variability (dashed lines in Fig. 3c). The resulting detrended and smoothed time series, Fig. 3d, show that
      low-frequency wind variability can raise or drop sea level by over 2 cm over a period of 2 to 5 decades. In App. A, this
205   low-frequency variability lags low-frequency sea-surface temperatures in the North Atlantic that have a similar pattern as the
      Atlantic Multidecadal Variability.

      4.3   Rates of SLR

      The rates of SLR obtained from differentiating the estimated smooth sea-level trend from each of the four models are shown
      in Fig. 4. Reduction of uncertainty is generally the main motivation for removing variability due to known atmospheric drivers
210   from the sea-level trend (Dangendorf et al., 2014a). The rate of change from TrNc has lower uncertainty than the rate from Tr.
      Including the zonal wind (TrNcZw) as a predictive variable further decreases the uncertainty, whereas including the pressure
      difference (TrNcPd) increases the uncertainty again. The standard error in estimating the trend is larger at the time series’ start
      and end because there are fewer constraints than in the middle of the time series.
Across all four specifications, the post (1960–2019) periods show higher rates than the pre (1900–1959) periods. The Tr and TrNcPd models have conditional spread-only bands that cross zero; those for TrNc and TrNcZw lie above zero in the 1960–2019 minus 1900–1959 contrast. For Tr, omitting the 1960s from the later window raises its mean rate from 2.26 to 2.37 mm/yr, increasing the late-minus-pre contrast from 0.44 to 0.55 mm/yr. As a descriptive check only, straight lines fitted to the supplied annual gauge-average observations yield 1.92 mm/yr for the whole period and 1.82 and 2.18 mm/yr for the earlier and later windows. These are observed-series slopes, not GAM estimates. The original tests compared 20-year periods, whereas this amendment uses a fixed 60-year contrast, making the comparisons distinct.

**Table R1. Dutch coastal fitted rates: original 20-year windows beside whole, early and late periods and the paired post-minus-pre contrast (mm/yr).**

| v1 GAM | 1900–19 | 1920–39 | 1940–59 | 2000–19 | 1900–2019 | 1900–1959 | 1960–2019 | Post minus pre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Tr | 2.15 | 1.69 | 1.63 | 2.69 | 2.04 [1.89, 2.22] | 1.82 [1.51, 2.13] | 2.26 [1.87, 2.65] | 0.44 [-0.26, 1.06] |
| TrNc | 2.27 | 1.67 | 1.62 | 2.80 | 2.08 [1.94, 2.23] | 1.85 [1.64, 2.12] | 2.30 [1.98, 2.64] | 0.45 [0.03, 0.89] |
| TrNcZw | 1.82 | 1.68 | 1.47 | 2.97 | 1.94 [1.78, 2.08] | 1.66 [1.43, 1.81] | 2.23 [2.00, 2.47] | 0.57 [0.28, 0.95] |
| TrNcPd | 1.86 | 1.78 | 1.54 | 2.74 | 1.92 [1.70, 2.07] | 1.73 [1.44, 2.01] | 2.11 [1.72, 2.49] | 0.38 [-0.15, 1.00] |

All cells are mm/yr. The four left-hand columns are recomputed means of the v1 fitted annual rates for the original Figure 4 windows (inclusive year labels); they do not carry newly estimated uncertainty. The four right-hand columns reproduce the longer-period comparison and its paired contrast unchanged. Fitted central-derivative point rates and differences, mm/yr. Brackets are conditional spread-only sensitivity bands: for each model and window (or paired contrast), the raw across-draw mean is removed before adding the fitted point; the resulting central 95% range is NOT a calibrated confidence interval. Raw draw centers/quantiles deviate from the fitted points and are recorded alongside them in period-rates.csv. The source describes parametric bootstrap noise and Figure 4 percentile ranges but does not establish that these particular raw column levels form an unbiased distribution around the supplied fit. Their column scale as rates (mm/yr) is assumed for spread; unlike the point rates it cannot be independently verified against matching per-draw level curves. No model refit or onset inference.

**Originally reported TrNcZw rates and uncertainty (v1 Results §4.3, Fig. 4; mm/yr).** In the same chronological order: 1.8 [1.4–2.3], 1.7 [1.3–2.0], 1.5 [1.1–1.8], and 3.0 [2.4–3.5]. These are the authors’ printed, one-decimal point estimates and reported ranges, not new empirical intervals or the spread-only brackets at right. Window labels follow the inclusive 20-year intervals specified by the original Figure 4 caption.


The original wind-adjusted fits (TrNcZw and TrNcPd) put the early-century rates below those in the simpler Tr and TrNc fits and show a later upturn. The original authors reported smaller uncertainty for the zonal-wind fit and a late rate near 3 mm/yr. The new fixed-period results complement, rather than retest, that Fig. 4 interpretation. Original Table 2 compares 2000–2019 with each of the three earlier **20-year** periods under the authors’ equal-rate null. For example, Tr gives 0.23, 0.06 and 0.05; TrNcZw is printed as <0.01 for each. These historical tests are not p-values for the 60-year post-minus-pre contrasts in Table R1.

Across the entire finite central-difference series (year labels 1891–2019), the minimum fitted annual rate occurs in 1954 for Tr, 1941 for TrNc, 1964 for TrNcZw and 1967 for TrNcPd. These are model-specific minima of the smoothed rate, not inferred acceleration onset dates. The decrease before the respective minima could be related to the strong
      Arctic warming from 1900 to 1930, followed by an Arctic cooling from 1930 to 1970 (Fig. 4, Bokuchava and Semenov (2021)).
      This could have influenced sea level through glacier mass loss followed by gain or local steric sea level changes. Since the


                                                                      9


## Original PDF page 10

https://doi.org/10.5194/egusphere-2022-935
Preprint. Discussion started: 4 October 2022
 c Author(s) 2022. CC BY 4.0 License.




                                                                 Annual average                                                                                      Trend
                                            10 (a)                                                                                             2 (b)
         Wind influence on sea level [cm]




                                                                                                           Wind influence on sea level [cm]
                                                                                                                                               1
                                            5
                                                                                                                                               0
                                            0                                                                                                  1
                                                                                                                                               2               Linear trend [mm/yr]:
                                             5                           TrNcZw                                                                                  0.15 0.12
                                                                                                                                               3
                                                                         TrNcPd                                                                                  0.42 0.15
                                                     1850        1900       1950   2000                                                              1850     1900       1950   2000
                                                                        Time                                                                                         Time
                                                            Multitaper spectrum                                                                           Detrended and smoothed
                                                 (c)                                                                                                (d)
                                                                                           Wind influence on sea level [cm]




                                            10                                                                                                1.0
 Power spectrum density




                                            8
                                                                                                                                              0.5
       [cm2. year]




                                            6
                                                                                                                                              0.0
                                            4
                                            2                                                                                                 0.5

                                            0                                                                                                 1.0
                                                 0          20       40       60   80                                                                1850     1900       1950   2000
                                                                   Period [year]                                                                                     Time


Figure 3. Comparison of the wind influence on sea level along the Dutch coast obtained from two different regressors: average zonal wind
of the 6 tide gauge stations (TrNcZw) and the pressure difference between the Northern and Southern boxes (TrNcPd) of Figure 1. (a) Time
series of annual averages. (b) Trend computed using a 3rd-degree polynomial fit with linear trend values over the first half and the second
half of the total period. (c) Spectra obtained using a multitaper method (Lees and Park, 1995). Both the detrended time series (solid lines)
and the detrended and smoothed time series (dashed lines) are shown. Smoothing is obtained from a LOWESS method with a window of 21
years. (d) Smoothed time series.




                                                                                          10


## Original PDF page 11

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




                                             r2000−2019 vs r1900−1919      r2000−2019 vs r1920−1939   r2000−2019 vs r1940−1959
                         Statistical model

                         Tr                                        0.23                        0.06                         0.05
                         TrNc                                      0.14                        0.01                         0.01
                         TrNcZw                                  < 0.01                      < 0.01                       < 0.01
                         TrNcPd                                    0.05                        0.02                         0.01
Table 2. Original v1 short-window tests. Entries are the authors’ reported p-values for a difference at least as large as observed if the rates were equal, comparing 2000–2019 in turn with 1900–1919, 1920–1939 and 1940–1959. The Tr example is 0.23 for the first comparison, as printed in the table. For TrNcZw all three entries are reported as <0.01, not exact zeros. This caption follows the printed entries rather than the inconsistent numerical examples in the v1 caption. No tests in this table were recalculated.



235   local sea-level budget is not closed before 1950 (Frederikse et al., 2020), we can only speculate about the causes of the drop in
      the rate of SLR.


      5    Discussion

      Estimating the trend, nodal cycle and atmospheric processes underlying the wind influence on sea level using the GAM allows
      for avoiding a priori assumptions about the sea-level trend, like having a linear or quadratic shape, while performing the
240   regression analysis. Thereby, the rate of SLR can be computed as a time-evolving variable over the whole observational period
      contrary to being calculated as a constant over an arbitrary period as was done in Calafat and Chambers (2013); Steffelbauer
      et al. (2022). In addition, we propose a careful uncertainty analysis accounting for serially dependent unexplained fluctuations,
      which is used to evaluate the strength of evidence for an acceleration. These two elements help to avoid framing the problem
      of acceleration detection as binary. This is important when advising decision-makers: significance testing based on ad hoc
245   models like a broken line trend may lead to a paradigm shift from a steady rate of SLR in one year to an accelerating rise a few
      years later, as demonstrated by the results in (Calafat and Chambers, 2013; Steffelbauer et al., 2022). To our best knowledge,
      the GAM has not been applied to estimate trends and acceleration in sea-level data before, and we believe it could help solve
      similar acceleration detection problems in regions other than the coast of the Netherlands.
          When removing the wind influence from the sea-level observations, the underlying assumption is that this influence is only
250   due to natural variability and that there is no structural change due to anthropogenic forcing. However, as we find a wind-driven
      trend over the entire period of study 1836-2020 from both the zonal wind and pressure difference model, the trend could also
      continue in the future. We do not know of any study investigating the possible cause of this trend. If it is caused by climate
      change due to anthropogenic forcing, it would be reasonable to expect it to continue in the future. Otherwise, if it is caused
      by natural variability, it might reverse. Most of the CMIP5 and CMIP6 ensembles do not show a systematic trend associated
255   with wind influence on sea level in the North Sea, not over the historical period or in future scenarios. So, they either miss the


                                                                            11


## Original PDF page 12

https://doi.org/10.5194/egusphere-2022-935
Preprint. Discussion started: 4 October 2022
 c Author(s) 2022. CC BY 4.0 License.




                                                          Tr                                                                  TrNc
                                         4.0 (a)                                                             4.0 (b)
                                         3.5                                                                 3.5
                Sea level rate [mm/yr]




                                                                               Sea level rate [mm/yr]
                                         3.0                                                                 3.0
                                         2.5                                                                 2.5
                                         2.0                                                                 2.0
                                         1.5                                                                 1.5
                                         1.0                                                                 1.0
                                         0.5     2.2 1.7 1.6         2.7                                     0.5     2.3 1.7 1.6         2.8
                                              1900 1925 1950 1975 2000 2025                                       1900 1925 1950 1975 2000 2025
                                                        TrNcZw                                                               TrNcPd
                                         4.0 (c)                                                             4.0 (d)
                                         3.5                                                                 3.5
                Sea level rate [mm/yr]




                                                                               Sea level rate [mm/yr]



                                         3.0                                                                 3.0
                                         2.5                                                                 2.5
                                         2.0                                                                 2.0
                                         1.5                                                                 1.5
                                         1.0                                                                 1.0
                                         0.5      1.8 1.7 1.5         3.0                                    0.5     1.9 1.8 1.5         2.7
                                               1900 1925 1950 1975 2000 2025                                      1900 1925 1950 1975 2000 2025

                                  3.00 (e)            Tr                                                     0.7 (f)           Tr
                                                                               Rate standard error [mm/yr]




                                  2.75                TrNc                                                                     TrNc
         Sea level rate [mm/yr]




                                                      TrNcZw                                                 0.6               TrNcZw
                                  2.50                TrNcPd                                                                   TrNcPd
                                  2.25                                                                       0.5
                                  2.00                                                                       0.4
                                  1.75
                                                                                                             0.3
                                  1.50
                                  1.25                                                                       0.2
                                        1900 1925 1950 1975 2000 2025                                              1900 1925 1950 1975 2000 2025
                                                 Time [years]                                                               Time [years]


Figure 4. (a–d) The rates of SLR were obtained for four different statistical models. A window of three years is used, so the rates cannot
be computed for the first and last years of the time series. The period shown here is 1891 to 2019. The dashed lines show the 5th and 95th
percentiles of the uncertainty range computed from a parametric bootstrap method. Numbers in grey under the curves indicate the mean rates
for four different periods ([1900-1919], [1920-1939], [1940-1959], [2000-2019]) (e) Median sea level rates. (f) Standard error of the sea level
rates.
                                                                           12


## Original PDF page 13

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      process driving the trend in the observations, or the trend in the comments has to be attributed to natural variability. In each
      case, the magnitude of around 0.15 mm/yr over the historical period is small enough compared to other sources of uncertainty
      to neglect it when making sea level projections on time scales of more than several decades.
          If the time lag found between North Atlantic SST and wind influence on sea level as described in App. A was found to
260   be physical or if the SST signal could be skillfully forecasted, this relation could provide a source of predictability for the
      deviation between sea level along the Dutch coast and large-scale drivers (e.g. glacier and ice sheet mass loss, global steric...)
      at the decadal time scale.
          From the daily to the interannual time scale, the wind influence on sea level in shallow seas is well understood by the
      barotropic theory of the interplay between the Coriolis force, pressure gradient and surface wind stress (equation 3 from
265   Mangini et al. (2021)). On the multidecadal time scale, as investigated in this study, it is possible that the physical mechanism
      underpinning the relation between wind and sea level also involves steric sea level change (Chen et al., 2014). In particular,
      baroclinic signals in the deep ocean propagating as a volume flux on shallow seas (Bingham and Hughes, 2012; Calafat et al.,
      2012). However, since we use the large interannual variability to define the regression coefficient, we think these coefficients
      mostly reflect the barotropic wind influence.
The original wind-adjusted fitted rate curves in Fig. 4 showed a strong rise from the 1960s toward the 2000s. The standard error of the estimated rate grows after 2000, so persistence of the increase is uncertain. The fixed-window contrasts in Table R1 describe average rates; they are not a test of a specific onset. A potential application to this
      increase would be the extrapolation of the observed rate into the near future. This method was recently used as an additional
      line of evidence for future sea-level rise by Sweet et al. (2022). Based on Fig. 4c, assuming a constant rate of 3 mm/yr from
      2000 onwards, we arrive at a rise of 0.3 m between 2000 and 2100, which is slightly higher than the rise over the 20th century.
275   However, assuming a constant acceleration of 1.5/25= 0.06 mm/yr2 (as inferred from the trend in sea level rate over 1975-2000
      in Fig. 4c), we obtain a rise of 0.6 m, from 2000 to 2100, which is twice the rise without acceleration. Given the complexity of
      changes in the various drivers of global SLR, it would be naive to assume that the acceleration will remain constant during the
      remainder of this century. However, these crude extrapolations illustrate the practical significance of our estimates of the local
      rates of SLR and the importance of obtaining the evolution of these rates over time.


280   6    Conclusions

      In this study, we estimate the sea-level trend and the influence of the nodal cycle and wind on sea level along the coast of the
      Netherlands. We used the average of the observations from six tide gauges and zonal wind and atmospheric pressure at sea
      level from two reanalysis data sets. Using a set of four GAMs, we estimated the trend using B-splines functions and the wind
      influence using linear regression. The four models include either no predictive variables, only the nodal cycle, and, additionally,
285   either zonal wind or pressure gradient as predictive variables. We find that using only one predictive variable for the wind best
      estimates the sea-level trend. The deviance is reduced when more predictive variables are added to the GAM, reducing by 12%
      for adding the nodal cycle and another 37 to 59% for adding the wind.




                                                                      13


## Original PDF page 14

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




        We obtain the wind influence on sea level using the two GAMs that include a wind predictive variable (TrNcZw and TrNcPd).
      Obtaining the wind influence with two different approaches shows the method’s robustness as both methods lead to similar
290   conclusions. We find a long-term sea-level rise due to wind forcing of 0.12 mm/yr or 0.15 mm/yr for 1928-2020, depending on
      the used model. The long-term strengthening of the zonal wind is consistent with an observed northward shift and jet stream
      strengthening (Hallam et al., 2022). Also, we find a low-frequency wind variability which can rise or drop sea level by about
      1 cm over 2 to 5 decades. We find that it is related to multi-decadal sea surface temperature variations in the North Atlantic
      with a similar pattern as the Atlantic Multidecadal Variability. The correlation between SST in the northern part of the North
295   Atlantic and the multidecadal wind-driven sea-level variability can be understood as smaller SST values increase the meridional
      temperature gradient and strengthen the jet stream (Hallam et al., 2022). In summary, we find both a long-term SLR as well as
      a multidecadal sea-level variability due to wind forcing which are both connected to changes in the jet stream through various
      mechanisms (Hallam et al., 2022).
The 1960–2019 period has a higher mean rate than the 1900–1959 period, but this does not imply an onset or causal explanation. The new fixed 60-year contrast differs from the original 20-year comparisons, and the conditional bands do not test statistical significance. The amendment clarifies the distinction between the original and new contrasts. In v1, the wind-adjusted fitted curves suggested an upturn from the 1960s toward the 2000s. That attribution rests on the shape of those original curves and model assumptions; comparing two fixed-period mean rates here neither estimates a breakpoint nor establishes when acceleration began.




      Code and data availability. Currently, all data and code can be found in the GitHub repository: https://github.com/KNMI-sealevel/
      NetherlandsSeaLevelAcceleration. After the review process, when a final version of the code and data is obtained, the code and data will be
      uploaded to Zotero and a DOI will be provided.




                                                                          14


## Original PDF page 15

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




315   Appendix A: Low-frequency wind influence on sea level

      After smoothing the wind influence on sea level, we found a low-frequency wind-driven sea-level signal with an amplitude of
      over 1 cm and a period of 2 to 5 decades (Fig. 3d). Previous authors have not shown this wind-driven low-frequency sea-level
      variability, and it has therefore not been discussed what processes might drive this sea-level variability. The North Atlantic
      Oscillation (NAO) has already been shown to influence the sea level in the North Sea, especially in the winter (Jevrejeva et al.,
320   2005; Dangendorf et al., 2012, 2014a). This is not surprising given how close the correlation pattern in Fig. 1b is to the NAO.
        To go one step further, we look at the relation between low-frequency wind influence on sea level and low-frequency
      sea surface temperature (SST) in the North Atlantic using linear regression. We use monthly SST data from two reanalysis
      products. The COBE-SST2 reanalysis dataset from NOAA has a temporal coverage from 1850 to 2019 (Hirahara et al., 2014).
      The HadISSTv1.1 reanalysis dataset from the Met Office Hadley Centre has a temporal coverage from 1870 to the present, but
325   the data of the incomplete year, 2022, are excluded from our analysis (Rayner et al., 2003). Both data sets have a resolution
      of 1.0°×1.0°. We obtain the low-frequency sea surface temperature by detrending and smoothing the time series. Again, the
      smoothing is obtained using a LOWESS method with a window of 21 years. We perform a linear regression to reconstruct
      the low-frequency wind influence using the low-frequency sea surface temperature as a predictive variable. By performing the
      regression for each grid point in the North Atlantic, we obtain a correlation pattern for this region.
330     This shows that the multidecadal wind-driven sea-level variability can be related to North Atlantic SSTs. Figures A1a and
      c show the correlation pattern for the North Atlantic for TrNcZw and TrNcPd. In this figure, we only show the results for
      COBE-SST2 data since the results obtained using HadISSTv1.1 are similar. In a few regions, the SST is strongly correlated,
      especially in the tropics, north of the equator (box "South") and around Iceland in the Irminger Sea and southern Norwegian
      Sea (box "North"), where the SST explains more than 50% of the variance of wind influence on sea level (not shown). For
335   these boxes and a large region of the North Atlantic, generally used to define the Atlantic Multidecadal Variability (AMV,
      Jüling et al. (2020)), we obtain the area-averaged low-frequency SST. Again, we obtain the relation to low-frequency wind
      influence on sea level using linear regression, including the SST data as a lagged dependent variable for lags from -40 to 40
      years (Fig. A1b, d). The wind influence is negatively correlated with past SST for positive time lags. A few years after the SST
      reaches a minimum in one of these regions, the wind pushes the sea level to a maximum along the Dutch coast. We find that,
340   depending on the case, the correlation coefficient is between -0.3 and -0.7 at lag 0. However, the negative correlation becomes
      stronger with a positive time lag and reaches a minimum for a lag between 3 and 10 years. Here, SST can explain between 35
      and 65% of the variance in wind-driven sea-level variability. We also see that the time lag is smaller for the North and South
      region than for the AMV region. While SST can explain an important part of multidecadal variability for both TrNcZw and
      TrNcPd, the correlation is stronger for TrNcPd.
345     The relation between SST in the "North" box and zonal wind can be understood physically. A minimum temperature in
      this region would tend to increase the meridional temperature gradient and strengthen the jet stream (Hallam et al., 2022).
      Understanding the physical relationship between SST in the other boxes and the sea level in the North Sea, given the potential
      time lag, is not straightforward. Given the noise in the signal, the smoothing could be responsible for this lag, so it is not certain



                                                                       15


## Original PDF page 16

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      that this is a physical feature. We also noticed that the lag increases for increased smoothing (not shown). The uncertainties
350   of the correlations shown in Fig. A1b and d are represented by the standard error. However, both time series are smoothed,
      causing their autocorrelation to increase and the sample size n to alter. Therefore, the uncertainties shown in Fig. A1b and d
      are underestimated.


        (a)                                                            (b)




       (c)                                                             (d)




      Figure A1. (a) and (c) Maps of the correlation coefficients between the wind influence on sea level along the Dutch coast for TrNcZw and
      TrNcPd using COBE-SST2 data. Both variables are detrended and smoothed. (b) and (d) represent the regression coefficients for, respectively,
      TrNcZw and TrNcPd, three regions of the North Atlantic and different time lags. Linear regressions are performed over the longest available
                                                                                                                               √
      period: 1850 - 2019. The shaded areas show 1 standard error of the correlation coefficients (r) is shown, σr = (1 − r2 )/ n − 2, with n the
      length of the time series.




      Author contributions. Iris Keizer, Dewi Le Bars and Cees de Valk developed the model code and performed the simulations. All authors
      contributed to the interpretation of results. Iris Keizer and Dewi Le Bars prepared the manuscript with contribution from all authors.




                                                                             16


## Original PDF page 17

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




355   Competing interests. The authors declare that they have no conflict of interest.




      Acknowledgements. This publication was supported by the project RECEIPT (REmote Climate Effects and their Impact on European sus-
      tainability, Policy and Trade) which received funding from the European Union’s Horizon 2020 Research and Innovation Programme under
      Grant agreement No. 820712 and by PROTECT a European Union’s Horizon 2020 research and innovation program under grant agreement
360   No. 869304.
        Iris Keizer, Dewi Le Bars and Sybren Drijfhout gratefully acknowledge support from the Netherlands Knowledge Programme on Sea-
      level rise that supported them with a special grant. Roderik van de Wal and André Jüling acknowledge support from the Netherlands Polar
      Program to the Dutch Polar Climate and Cryosphere Change Consortium.
        In this study, we used the GAM implementation, Lowess filtering and third-order detrending tool from the statsmodel library (https:
365   //www.statsmodels.org/; Seabold and Perktold (2010)), the multitaper method from the spectrum library (https://pyspectrum.readthedocs.io)
      and the ordinary least squares regression model from the scikit-learn library (https://scikit-learn.org).




                                                                             17


## Original PDF page 18

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      References

      Baart, F., van Gelder, P. H. A. J. M., de Ronde, J., van Koningsveld, M., and Wouters, B.: The Effect of the 18.6-Year Lunar Nodal Cycle
        on Regional Sea-Level Rise Estimates, Journal of Coastal Research, 28, 511–516, https://doi.org/10.2112/JCOASTRES-D-11-00169.1,
370     2011.
      Baart, F., Rongen, G., Hijma, M., Kooi, H., de Winter, R., and Nicolai, R.: Zeespiegelmonitor 2018: De stand van zaken rond de
        zeespiegelstijging langs de Nederlandse kust, Tech. rep., https://deltalife.deltares.nl/deltares/de_nederlandse_delta/zeespiegelstijging/
        160368/Zeespiegelmonitor_2018_final.pdf, 2019.
      Bell, B., Hersbach, H., Simmons, A., Berrisford, P., Dahlgren, P., Horányi, A., Muñoz-Sabater, J., Nicolas, J., Radu, R., Schepers, D., Soci,
375     C., Villaume, S., Bidlot, J.-R., Haimberger, L., Woollen, J., Buontempo, C., and Thépaut, J.-N.: The ERA5 global reanalysis: Preliminary
        extension to 1950, Quarterly Journal of the Royal Meteorological Society, 147, 4186–4227, https://doi.org/10.1002/qj.4174, _eprint:
        https://onlinelibrary.wiley.com/doi/pdf/10.1002/qj.4174, 2021.
      Bingham, R. J. and Hughes, C. W.: Local diagnostics to estimate density-induced sea level variations over topography and along coastlines:
        TOPOGRAPHY AND SEA LEVEL, Journal of Geophysical Research: Oceans, 117, https://doi.org/10.1029/2011JC007276, 2012.
380   Bokuchava, D. D. and Semenov, V. A.: Mechanisms of the Early 20th Century Warming in the Arctic, Earth-Science Reviews, 222, 103 820,
        https://doi.org/10.1016/j.earscirev.2021.103820, 2021.
      Calafat, F. M. and Chambers, D. P.: Quantifying recent acceleration in sea level unrelated to internal climate variability, Geophysical Research
        Letters, 40, 3661–3666, https://doi.org/10.1002/grl.50731, 2013.
      Calafat, F. M., Chambers, D. P., and Tsimplis, M. N.: Mechanisms of decadal sea level variability in the eastern North Atlantic and the
385     Mediterranean Sea, Journal of Geophysical Research: Oceans, 117, https://doi.org/https://doi.org/10.1029/2012JC008285, 2012.
      Casanueva, A., Herrera, S., Fernández, J., Frías, M. D., and Gutiérrez, J. M.: Evaluation and projection of daily temperature
        percentiles from statistical and dynamical downscaling methods, Natural Hazards and Earth System Sciences, 13, 2089–2099,
        https://doi.org/10.5194/nhess-13-2089-2013, publisher: Copernicus GmbH, 2013.
      Chen, X., Dangendorf, S., Narayan, N., O’Driscoll, K., Tsimplis, M. N., Su, J., Mayer, B., and Pohlmann, T.: On sea level change in the North
390     Sea influenced by the North Atlantic Oscillation: Local and remote steric effects, Estuarine, Coastal and Shelf Science, 151, 186–195,
        https://doi.org/10.1016/j.ecss.2014.10.009, 2014.
      Cleveland, W. S. and Devlin, S. J.: Locally Weighted Regression: An Approach to Regression Analysis by Local Fitting, Journal of the
        American Statistical Association, 83, 596–610, https://doi.org/10.1080/01621459.1988.10478639, publisher: Taylor & Francis _eprint:
        https://www.tandfonline.com/doi/pdf/10.1080/01621459.1988.10478639, 1988.
395   Cox, D. R. and Reid, N.: A note on pseudolikelihood constructed from marginal densities, Biometrika, 91, 729–737,
        https://doi.org/https://doi.org/10.1093/biomet/91.3.729, publisher: Oxford University Press, 2004.
      Dangendorf, S., Wahl, T., Hein, H., Jensen, J., Mai, S., and Mudersbach, C.: Mean Sea Level Variability and Influence of the North Atlantic
        Oscillation on Long-Term Trends in the German Bight, Water, 4, 170–195, https://doi.org/10.3390/w4010170, 2012.
      Dangendorf, S., Mudersbach, C., Wahl, T., and Jensen, J.: Characteristics of intra-, inter-annual and decadal sea-level variability and the
400     role of meteorological forcing: the long record of Cuxhaven, Ocean Dynamics, 63, 209–224, https://doi.org/10.1007/s10236-013-0598-0,
        2013.
      Dangendorf, S., Calafat, F. M., Arns, A., Wahl, T., Haigh, I. D., and Jensen, J.: Mean sea level variability in the North Sea: Processes and
        implications, Journal of Geophysical Research: Oceans, 119, https://doi.org/10.1002/2014JC009901, 2014a.



                                                                            18


## Original PDF page 19

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




      Dangendorf, S., Wahl, T., Nilson, E., Klein, B., and Jensen, J.: A new atmospheric proxy for sea level variability in the southeastern North
405     Sea: observations and future ensemble projections, Climate Dynamics, 43, 447–467, https://doi.org/10.1007/s00382-013-1932-4, 2014b.
      Dangendorf, S., Hay, C., Calafat, F. M., Marcos, M., Piecuch, C. G., Berk, K., and Jensen, J.: Persistent acceleration in global sea-level rise
        since the 1960s, Nature Climate Change, 9, 705–710, https://doi.org/10.1038/s41558-019-0531-8, 2019.
      Ezer, T., Haigh, I. D., and Woodworth, P. L.: Nonlinear Sea-Level Trends and Long-Term Variability on Western European Coasts, Jour-
        nal of Coastal Research, 32, 744–755, https://doi.org/10.2112/JCOASTRES-D-15-00165.1, publisher: Coastal Education and Research
410     Foundation, 2016.
      Fox-Kemper, B., Hewitt, H. T., Xiao, C., Aðalgeirsdóttir, G., Drijfhout, S. S., Edwards, T. L., Golledge, N. R., Hemer, M., Kopp, R. E.,
        Krinner, G., Mix, A., Notz, D., Nowicki, S., Nurhati, I. S., Ruiz, L., Sallée, J. B., and Slangen, A. B. A.: Ocean, Cryosphere and Sea Level
        Change. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the
        Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S. L. Connors, C. Péan, S. Berger, N. Caud, Y.
415     Chen, L. Goldfarb, M. I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, T. K. Maycock, T. Waterfield, O. Yelekçi, R. Yu
        and B. Zhou (eds.)], Cambridge University Press, 2021.
      Frederikse, T. and Gerkema, T.: Multi-decadal variability in seasonal mean sea level along the North Sea coast, Ocean Science, 14, 1491–
        1501, https://doi.org/10.5194/os-14-1491-2018, publisher: Copernicus GmbH, 2018.
      Frederikse, T., Riva, R., Kleinherenbrink, M., Wada, Y., van den Broeke, M., and Marzeion, B.: Closing the sea level budget on a re-
420     gional scale: Trends and variability on the Northwestern European continental shelf, Geophysical Research Letters, 43, 10,864–10,872,
        https://doi.org/10.1002/2016GL070750, 2016.
      Frederikse, T., Landerer, F., Caron, L., Adhikari, S., Parkes, D., Humphrey, V. W., Dangendorf, S., Hogarth, P., Zanna, L., Cheng, L., and
        Wu, Y.-H.: The causes of sea-level rise since 1900, Nature, 584, 393–397, https://doi.org/10.1038/s41586-020-2591-3, number: 7821
        Publisher: Nature Publishing Group, 2020.
425   Gill, A. E.: Atmosphere-Ocean Dynamics, Academic Press, google-Books-ID: 1WLNX_lfRp8C, 1982.
      Haasnoot, M., van ’t Klooster, S., and van Alphen, J.: Designing a monitoring system to detect signals to adapt to uncertain climate change,
        Global Environmental Change, 52, 273–285, https://doi.org/10.1016/j.gloenvcha.2018.08.003, 2018.
      Haigh, I. D., Wahl, T., Rohling, E. J., Price, R. M., Pattiaratchi, C. B., Calafat, F. M., and Dangendorf, S.: Timescales for detecting a
        significant acceleration in sea level rise, Nature Communications, 5, 3635, https://doi.org/10.1038/ncomms4635, 2014.
430   Hallam, S., Josey, S. A., McCarthy, G. D., and Hirschi, J. J.-M.: A regional (land–ocean) comparison of the seasonal to decadal variability
        of the Northern Hemisphere jet stream 1871–2011, Climate Dynamics, https://doi.org/10.1007/s00382-022-06185-5, 2022.
      Hastie, T. J. and Tibshirani, R. J.: Generalized Additive Models, Routledge, New York, https://doi.org/10.1201/9780203753781, 2017.
      Hermans, T. H. J., Bars, D. L., Katsman, C. A., Camargo, C. M. L., Gerkema, T., Calafat, F. M., Tinker, J., and Slangen, A. B. A.: Drivers of
        Interannual Sea Level Variability on the Northwestern European Shelf, Journal of Geophysical Research: Oceans, 125, e2020JC016 325,
435     https://doi.org/https://doi.org/10.1029/2020JC016325, _eprint: https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2020JC016325,
        2020.
      Hermans, T. H. J., Katsman, C. A., Camargo, C. M. L., Garner, G. G., Kopp, R. E., and Slangen, A. B. A.: The Effect of Wind Stress on
        Seasonal Sea-Level Change on the Northwestern European Shelf, Journal of Climate, 35, 1745–1759, https://doi.org/10.1175/JCLI-D-21-
        0636.1, publisher: American Meteorological Society Section: Journal of Climate, 2022.
440   Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz-Sabater, J., Nicolas, J., Peubey, C., Radu, R., Schepers, D., Sim-
        mons, A., Soci, C., Abdalla, S., Abellan, X., Balsamo, G., Bechtold, P., Biavati, G., Bidlot, J., Bonavita, M., De Chiara, G., Dahlgren,



                                                                            19


## Original PDF page 20

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




        P., Dee, D., Diamantakis, M., Dragani, R., Flemming, J., Forbes, R., Fuentes, M., Geer, A., Haimberger, L., Healy, S., Hogan, R. J.,
        Hólm, E., Janisková, M., Keeley, S., Laloyaux, P., Lopez, P., Lupu, C., Radnoti, G., de Rosnay, P., Rozum, I., Vamborg, F., Vil-
        laume, S., and Thépaut, J.-N.: The ERA5 global reanalysis, Quarterly Journal of the Royal Meteorological Society, 146, 1999–2049,
445     https://doi.org/10.1002/qj.3803, _eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1002/qj.3803, 2020.
      Hirahara, S., Ishii, M., and Fukuda, Y.: Centennial-Scale Sea Surface Temperature Analysis and Its Uncertainty, Journal of Climate, 27,
        57–75, https://doi.org/10.1175/JCLI-D-12-00837.1, publisher: American Meteorological Society Section: Journal of Climate, 2014.
      Holgate, S. J., Matthews, A., Woodworth, P. L., Rickards, L. J., Tamisiea, M. E., Bradshaw, E., Foden, P. R., Gordon, K. M., Jevrejeva, S.,
        and Pugh, J.: New Data Systems and Products at the Permanent Service for Mean Sea Level, Journal of Coastal Research, 29, 493–504,
450     https://doi.org/10.2112/JCOASTRES-D-12-00175.1, publisher: Coastal Education and Research Foundation, 2013.
      Jevrejeva, S., Moore, J., Woodworth, P., and Grinsted, A.: Influence of large-scale atmospheric circulation on European sea
        level: results based on the wavelet transform method, Tellus A: Dynamic Meteorology and Oceanography, 57, 183–193,
        https://doi.org/10.3402/tellusa.v57i2.14609, publisher: Taylor & Francis _eprint: https://doi.org/10.3402/tellusa.v57i2.14609, 2005.
      Jüling, A., Dijkstra, H. A., Hogg, A. M., and Moon, W.: Multidecadal variability in the climate system: phenomena and mechanisms, The
455     European Physical Journal Plus, 135, 506, https://doi.org/10.1140/epjp/s13360-020-00515-4, 2020.
      Kirch, C. and Politis, D. N.: TFT-bootstrap: Resampling time series in the frequency domain to obtain replicates in the time domain, The
        Annals of Statistics, 39, 1427–1470, https://doi.org/10.1214/10-AOS868, publisher: Institute of Mathematical Statistics, 2011.
      Lees, J. M. and Park, J.: Multiple-taper spectral analysis: A stand-alone C-subroutine, Computers & Geosciences, 21, 199–236,
        https://doi.org/10.1016/0098-3004(94)00067-5, 1995.
460   Lyu, K., Zhang, X., and Church, J. A.: Regional Dynamic Sea Level Simulated in the CMIP5 and CMIP6 Models: Mean Biases, Future
        Projections, and Their Linkages, Journal of Climate, 33, 6377–6398, https://doi.org/10.1175/JCLI-D-19-1029.1, publisher: American
        Meteorological Society, 2020.
      Mangini, F., Chafik, L., Madonna, E., Li, C., Bertino, L., and Nilsen, J. E. : The relationship between the eddy-driven
        jet stream and northern European sea level variability, Tellus A: Dynamic Meteorology and Oceanography, 73, 1–15,
465     https://doi.org/10.1080/16000870.2021.1886419, publisher: Taylor & Francis _eprint: https://doi.org/10.1080/16000870.2021.1886419,
        2021.
      Mastrandrea, M. D., Mach, K. J., Plattner, G.-K., Edenhofer, O., Stocker, T. F., Field, C. B., Ebi, K. L., and Matschoss, P. R.: The IPCC
        AR5 guidance note on consistent treatment of uncertainties: a common approach across the working groups, Climatic Change, 108, 675,
        https://doi.org/10.1007/s10584-011-0178-6, 2011.
470   Rayner, N. A., Parker, D. E., Horton, E. B., Folland, C. K., Alexander, L. V., Rowell, D. P., Kent, E. C., and Kaplan, A.: Global analyses of
        sea surface temperature, sea ice, and night marine air temperature since the late nineteenth century, Journal of Geophysical Research: At-
        mospheres, 108, https://doi.org/10.1029/2002JD002670, _eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1029/2002JD002670, 2003.
      Seabold, S. and Perktold, J.: statsmodels: Econometric and statistical modeling with python, in: 9th Python in Science Conference, 2010.
      Slangen, A. B. A., Katsman, C. A., van de Wal, R. S. W., Vermeersen, L. L. A., and Riva, R. E. M.: Towards regional projections of twenty-first
475     century sea-level change based on IPCC SRES scenarios, Climate Dynamics, 38, 1191–1209, https://doi.org/10.1007/s00382-011-1057-6,
        2012.
      Slivinski, L. C., Compo, G. P., Whitaker, J. S., Sardeshmukh, P. D., Giese, B. S., McColl, C., Allan, R., Yin, X., Vose, R., Titchner, H.,
        Kennedy, J., Spencer, L. J., Ashcroft, L., Brönnimann, S., Brunet, M., Camuffo, D., Cornes, R., Cram, T. A., Crouthamel, R., Domínguez-
        Castro, F., Freeman, J. E., Gergis, J., Hawkins, E., Jones, P. D., Jourdain, S., Kaplan, A., Kubota, H., Blancq, F. L., Lee, T.-C., Lorrey, A.,



                                                                            20


## Original PDF page 21

      https://doi.org/10.5194/egusphere-2022-935
      Preprint. Discussion started: 4 October 2022
       c Author(s) 2022. CC BY 4.0 License.




480     Luterbacher, J., Maugeri, M., Mock, C. J., Moore, G. K., Przybylak, R., Pudmenzky, C., Reason, C., Slonosky, V. C., Smith, C. A., Tinz,
        B., Trewin, B., Valente, M. A., Wang, X. L., Wilkinson, C., Wood, K., and Wyszyński, P.: Towards a more reliable historical reanalysis:
        Improvements for version 3 of the Twentieth Century Reanalysis system, Quarterly Journal of the Royal Meteorological Society, 145,
        2876–2908, https://doi.org/10.1002/qj.3598, _eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1002/qj.3598, 2019.
      Steffelbauer, D. B., Riva, R. E. M., Timmermans, J. S., Kwakkel, J. H., and Bakker, M.: Evidence of regional sea-level rise acceleration for
485     the North Sea, Environmental Research Letters, 17, 074 002, https://doi.org/10.1088/1748-9326/ac753a, publisher: IOP Publishing, 2022.
      Sweet, W., Hamlington, B., Kopp, R., and Weaver, C.: Global and Regional Sea Level Rise Scenarios for the United States: Up- dated
        Mean Projections and Extreme Water Level Probabilities Along U.S. Coastlines., NOAA Technical Report NOS 01, National Oceanic
        and Atmospheric Administration, National Ocean Service, Silver Spring, MD, 111 pp, https://oceanservice.noaa.gov/hazards/sealevelrise/
        noaa-nos-techrpt01-global-regional-SLR-scenarios-US.pdf, 2022.
490   Vries, H. d., Katsman, C., and Drijfhout, S.: Constructing scenarios of regional sea level change using global temperature pathways, Envi-
        ronmental Research Letters, 9, 115 007, https://doi.org/10.1088/1748-9326/9/11/115007, 2014.
      Wahl, T., Haigh, I., Woodworth, P., Albrecht, F., Dillingh, D., Jensen, J., Nicholls, R., Weisse, R., and Wöppelmann, G.: Ob-
        served mean sea level changes around the North Sea coastline from 1800 to present, Earth-Science Reviews, 124, 51–67,
        https://doi.org/10.1016/j.earscirev.2013.05.003, 2013.
495   Walker, J. S., Kopp, R. E., Little, C. M., and Horton, B. P.: Timing of emergence of modern rates of sea-level rise by 1863, Nature Commu-
        nications, 13, 966, https://doi.org/10.1038/s41467-022-28564-6, number: 1 Publisher: Nature Publishing Group, 2022.
      Wood, S. N.: Inference and computation with generalized additive models and their extensions, TEST, 29, 307–339,
        https://doi.org/10.1007/s11749-020-00711-5, 2020.
      Woodworth, P. L.: Differences between mean tide level and mean sea level, Journal of Geodesy, 91, 69–90, https://doi.org/10.1007/s00190-
500     016-0938-1, 2017.




                                                                          21
