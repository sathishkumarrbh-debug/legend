# ML surrogate for NACA 4-digit airfoils (saved for a later paper)

- `study.py`: NACA 4-digit geometry + Hess–Smith panel method (160 panels), validation, 3,000-case dataset, LR / RF / ANN training. Writes `results.json` and figures. Run: `pip install numpy matplotlib scikit-learn && python3 study.py`
- `figs2.py`: airfoil shape and Cp plots.
- Validation: NACA 0012 dCL/dα = 0.120 /deg; NACA 2412 α_L0 = −2.13° (theory −2.08°).
- Test R²: ANN 0.999 (CL), 0.999 (Cp,min); linear regression 0.657 on Cp,min. ANN ≈1,500× faster than the panel solver.
- Limits: inviscid, incompressible. Next for the paper: viscous data (XFOIL/CFD), drag and stall, comparison with Abbott & von Doenhoff experimental data.
- `ICAAN2026_Abstract_SJCET.docx`, `ICAAN2026_PPT_SJCET.pptx`, `deck.js`: first conference draft (not submitted).
