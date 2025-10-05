### Visionary Catalysts | NASA Space Apps Challenge 2025

[](https://opensource.org/licenses/MIT)

##  The Challenge

The "From EarthData to Action: Cloud Computing with Earth Observation Data for Predicting Cleaner, Safer Skies" challenge tasked us with creating a scalable tool that provides actionable insights into air quality using NASA data. Our project directly addresses this by building a data pipeline and web application to make complex atmospheric data accessible to the public.

##  Our Solution: A Spatial Air Quality Analysis

Our solution is a scalable web application that processes a large volume of satellite data to generate a comprehensive, high-resolution map of air pollution. The application's core feature is a dashboard that visualizes the average NO₂ concentration over a given time period, allowing anyone to easily identify pollution hotspots.

The app is live and publicly available here:
[Insert Your Live Streamlit App URL Here]

##  Technical Stack & Workflow

We designed a robust data pipeline that leverages cloud-native technologies to overcome common big data challenges.

1.  Data Sourcing: We used "over 80 files" of "Sentinel-5P TROPOMI Level 3" NO₂ data, which is provided in the NetCDF4 format.
2.  Cloud-Native Processing: The data was processed using "Dask", a parallel computing framework, integrated with the "xarray" library. This approach allowed us to combine a 2GB dataset without memory limitations.
3.  Data Standardization: A custom preprocessing function was developed to standardize metadata across all files, handling issues like missing coordinates and inconsistent variable names to ensure data integrity.
4.  Web Application: The final data is visualized using "matplotlib" and served through a "Streamlit" web application, providing a clean and user-friendly interface.

##  How to Run the Project Locally

To replicate our project on your local machine, follow these steps:

1.  Clone the Repository:
    ```bash
    git clone [Insert Your GitHub Repo URL Here]
    cd Visionary-Catalysts-SpaceApps
    ```
2.  Install Dependencies: Ensure you have Anaconda installed. Create a new environment and install the required packages:
    ```bash
    conda create --name spaceapps python=3.10
    conda activate spaceapps
    pip install -r requirements.txt
    ```
3.  Download the Data: Our project requires the Sentinel-5P (TROPOMI) Level 3 NO₂ dataset. Please download the files (as `.nc4` or `.nc` files) and place them in a folder named `NASA TROPOMONI` inside the `nasa-data` directory.
    (Instructions on how to download this data can be found on the [Earthdata Search](https://search.earthdata.nasa.gov/) website.)
4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
    Your application will open in a web browser.

##  Team & Acknowledgements

  *   Team: Visionary Catalysters
  *   Members:
  *     1. Sabarish S S - Sabarish-s-s
  *     2. Karthick S - Karthickspa
  *     3. Prince Dolvin J - princedolvinj-cyber
  *     4. Prajith S - Prajith-hub
  *     5. Midhun Krishna M - midhun1808
  * **Special Thanks:** This project was made possible by the open data and resources provided by NASA and the Streamlit Community.
