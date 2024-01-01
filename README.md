# An Analysis of COVID-19 Vaccine Hesitancy in the U.S.

## Steps to Reproduce

1. Clone this repository
2. Adjust the directory in the `utils.py` file to your local directory
3. Execute `create_all_figures.py` to create figures 2 to 11
   - The resulting figures will be saved/overwritten in the **Figures** folder
4. Use [draw.io](https://app.diagrams.net/) (i.e., free and open-source cross-platform graph drawing software) to open `fig1_proposed_flowchart.drawio` which creates figure 1.
5. To convert PNG to EPS, use the following command (tested on MacOS):

   - Convert all PNG files in the **Figures** folder to EPS
  
   ```bash
   cd Figures
   for file in *.png; do magick convert "$file" -density 300 "${file%.png}.eps"; done
   ```