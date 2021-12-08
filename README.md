<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License]https://img.shields.io/github/license/matbmoser/GameOfLife.svg?style=for-the-badge][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/matbmoser/GameOfLife">
    <img src="images/logo.jpg" alt="Logo" width="600" height="300">
  </a>

<h3 align="center">Game Of Life</h3>

  <p align="center">
    We are two students that are learning about HPC, so we programmed this GameOfLife using three diferent methods
    <br />
    <a href="https://github.com/matbmoser/GameOfLife"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/matbmoser/GameOfLife">View Demo</a>
    ·
    <a href="https://github.com/matbmoser/GameOfLife/issues">Report Bug</a>
    ·
    <a href="https://github.com/matbmoser/GameOfLife/issues">Request Feature</a>
  </p>
</div>

## Important

If you want to print the board of the GameOfLife use the ```secuentialGame.py``` file, all the files that contain ```-noprint``` have no grafical interface and give only the time of the execution.


### Built With

* [Python 3.8.5](https://www.python.org/downloads/release/python-385/)
* [Anaconda](https://www.anaconda.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Numba](https://numba.pydata.org/)
* [MPI4PY](https://mpi4py.readthedocs.io/en/stable/)
* [Pygame](https://www.pygame.org/docs/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Open the script you want to execute, and compile it using ```py example.py ```

### Prerequisites

Install OpenMPI from: https://www.open-mpi.org/

* MPI4PY
  ```sh
  python -m pip install mpi4py
  ```

If you have a NVIDIA GPU you shall install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads

* Numba
  ```sh
  python -m pip install numba
  ```  

For mor information check: https://developer.nvidia.com/cuda-python

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/matbmoser/GameOfLife.git
   ```

2. If you want to execute with NUMBA do:
   ```sh
   python parallelGame.py
   ```
    And select the max number of cores

3. If you want to execute with MPI do:
   ```sh
    mpiexec -cores <numofcores> python .\paralellGameMPI.py 
   ```
   You can choose the number of cores to by changing numofcores to 2 for example

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Mathias Moser  - matbmoser@gmail.com

Project Link: [https://github.com/matbmoser/GameOfLife](https://github.com/matbmoser/GameOfLife)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/matbmoser/GameOfLife.svg?style=for-the-badge
[contributors-url]: https://github.com/matbmoser/GameOfLife/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/matbmoser/GameOfLife.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/GameOfLife/network/members
[stars-shield]: https://img.shields.io/github/stars/matbmoser/GameOfLife.svg?style=for-the-badge
[stars-url]: https://github.com/matbmoser/GameOfLife/stargazers
[issues-shield]: https://img.shields.io/github/issues/matbmoser/GameOfLife.svg?style=for-the-badge
[issues-url]: https://github.com/matbmoser/GameOfLife/issues
[license-shield]: https://img.shields.io/github/license/matbmoser/GameOfLife.svg?style=for-the-badge
[license-url]: https://github.com/matbmoser/GameOfLife/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/mathias-brunkow-moser
[product-screenshot]: images/screenshot.png
