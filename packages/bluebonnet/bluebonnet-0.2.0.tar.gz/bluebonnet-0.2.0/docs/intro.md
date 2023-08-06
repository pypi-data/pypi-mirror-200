# Introduction to bluebonnet


## Installation

Run the command

```bash
pip install bluebonnet
```

## Usage

`bluebonnet` has a collection of tools for performing reservoir simulation in
tight oil and shale gas reservoirs. The main tools are:

1. `fluids` for modeling PVT and viscosity of oil, water, and gas;
2. `flow` for building physics-based production curves; and
3. `forecast` for fitting and forecasting unconventional production.

Examples can be found in
[the documentation](https://bluebonnet.readthedocs.io/en/latest).

## What makes bluebonnet unique?

The goal for this package is to make it easier to forecast production from
hydrofractured wells. It uses semi-universal recovery factor scaling curves
scaled by drainage volume and time-to-BDF to achieve these feats. These methods
have been used to make forecasts from the individual well level up to the basin
and play level, depending on the availability of fluid property and bottomhole
pressure data.

Compare to the most common unconventional production analysis tool. Emprical
decline curve analysis (DCA) provides very fast answers, but lack physical
meaning. Bluebonnet fits include estimates of the resource within the drainage
volume and of permeability divided by interfracture spacing. A completion
program purporting to increase the size of the fractured area can be tested with
bluebonnet without requiring extensive 3D reservoir simulations.

Also, bluebonnet naturally handles flow transitions, unlike DCA and type curves.
Arps, for instance, has to have multiple segments stitched together to capture
well behavior after the start of boundary dominated flow.

Sometimes, 3-D reservoir simulation is absolutely necessary to understand the
flow patterns around unconventional wells. However, due to the symmetries
inherent in such flow and the independence of production between neighboring
wells, one-dimensional methods like bluebonnet cover many of these use-cases.
