# PACO
Programa de Análisis de Cualidades Ópticas

<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">PACO: Optical Qualities Analysis Program</h3>

  <p align="center">
    PACO is a Python toolkit for reading, normalizing, analyzing, and visualizing optical spectra data.<br>
    It provides scripts for reading spectral data, normalizing spectra, searching for saturated lines, plotting with offsets, saving results, and computing statistics.<br>
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#functions">Functions</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

PACO (Programa de Análisis de Cualidades Ópticas) is a Python-based toolkit designed to facilitate the analysis of optical spectra. It provides scripts for reading spectral data, normalizing spectra, searching for saturated lines, plotting with offsets, saving results, and computing statistics. The project is organized for easy extension and automation of common spectroscopy workflows.

### Built With

* Python 3.x
* numpy
* matplotlib

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.x
* pip

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/AwakenChobi/PACO.git
   cd PACO
   ```
2. (Optional) Create a virtual environment
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

## Usage

The main scripts and their purposes are:

- `main.py`: Entry point for batch processing and orchestration.
- `read_xy_file.py`: Reads spectral data from XY files (being X the frecuency/waveleght and Y the intensity).
- `normalize_spectra.py`: Normalizes spectra for comparison.
- `plot_with_offset.py`: Plots multiple datasets (ideally of the same experimental condition) and applies the inputed offset. Some reference wavelenghts are included in the code, but the user can easily add more if they are needed. This function also plots the averaged-normalized spectra. It also have the functionality to detect and mark peaks in the former plot given a minimum intensity for a peak to be considered as one.
- `saturated_lines_searcher.py`: Detects saturated lines in spectra. The saturation limit can be easily modified inside the code.
- `save_normalized_spectra.py`: Saves normalized spectra in a .txt file.
- `save_peaks.py`: Saves detected peaks to a .txt file. The minimum intensity is first asked.
- `compute_stats.py`: Computes statistics on spectral data.
- `rot_temperature.py`: Computes rotational gas temperature from spectral molecular bands (C2, N2+, and OH), either from averaged spectra or dataset-by-dataset. It its important that the spectra has a clean baseline in the interval

Example usage:
```sh
python main.py
```

Optional offset metadata in `.txt` files:

- Add a comment line anywhere in the file (top or bottom recommended):
  `# PACO_X_OFFSET = 0.35`
- Accepted variants are also:
  `# X_OFFSET = 0.35` or `# X_OFFSET: 0.35`
- The value is applied automatically to the X-axis offset for that dataset.
- If no offset line is present, offset defaults to `0.0`.

## Functions

Below is a summary of the main functions defined in the codebase:

### `read_xy_file.py`
- `read_xy_file(filepath)`: Reads an XY data file and returns wavelength and intensity arrays.

### `normalize_spectra.py`
- `normalize_spectrum(wavelengths, intensities)`: Normalizes the intensity array for a given spectrum.

### `plot_with_offset.py`
- `plot_spectra_with_offset(spectra_list, offsets)`: Plots multiple spectra with specified vertical offsets.

### `saturated_lines_searcher.py`
- `find_saturated_lines(wavelengths, intensities, threshold)`: Identifies saturated lines above a given intensity threshold.

### `save_normalized_spectra.py`
- `save_normalized_spectra(filepath, wavelengths, normalized_intensities)`: Saves normalized spectra to a file.

### `save_peaks.py`
- `save_peaks(filepath, peaks)`: Saves detected peaks to a file.

### `compute_stats.py`
- `compute_statistics(intensities)`: Computes statistics (mean, std, etc.) for intensity data.

### `rot_temperature.py`
It is important that the spectra has a clean baseline on the interval between 517.8 and 518.0 nm. Is it is not the case, please consider to rewrite this line of code to fit your spectra adding a baseline that fits your case.
- `rot_temperature_C2(wavelengths, intensities)`: Estimates rotational temperature using C2 molecular features.
- `rot_temperature_N2_plus(wavelengths, intensities)`: Estimates rotational temperature using N2+ molecular features.
- `rot_temperature_OH(wavelengths, intensities)`: Estimates rotational temperature using OH molecular features.

## Roadmap

- [ ] Add GUI for easier interaction
- [ ] Support more file formats
- [ ] Advanced peak detection algorithms

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>

## License

Distributed under the project_license. See `LICENSE.txt` for more information.

## Contact

Antonio Cobos Luque - [@twitter_handle](https://www.researchgate.net/profile/A-Cobos-Luque) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

## Acknowledgments

* [numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/)
* [Laboratorio de Innovación en Plasmas]

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username