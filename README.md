# 🧪 Breast Cancer Dataset Preprocessing Pipeline

This project contains a complete preprocessing pipeline for two clinical datasets related to breast cancer diagnosis and patient health metrics. It performs cleaning, transformation, merging, and normalization operations to prepare the data for further analysis or modeling.

---

## 📁 Input Files

- `bc04.csv`: Contains breast cancer clinical information.
- `pc04.csv`: Contains patient data including physical measurements and demographic information.

---

## ⚙️ Pipeline Steps

### 1. `bc04.csv` Preprocessing

- Drop irrelevant columns: `inv-nodes`, `node-caps`, `irradiat`.
- Remove duplicates based on `pacient` (keep last occurrence).
- Rename `pacient` to `codigo`.
- Replace invalid values (`'?'`, `'erro'`) with `NaN` and drop them.
- Output: `bc_preprocessed.csv`.

### 2. `pc04.csv` Preprocessing

- Remove duplicates based on `codigo`.
- Replace invalid values (`'?'`, `'erro'`) with `NaN` and drop them.
- Remove rows where `sexo` is `'M'` or `'J'`; drop the column.
- Normalize and convert `peso` and `altura` to numeric format.
- Calculate BMI (`IMC`) using:
  IMC = peso / (altura / 100)²
- Categorize BMI into ranges → `IMC_cat`:
  - A: < 18.5
  - N: 18.5 - 25
  - P: 25 - 30
  - 1: 30 - 35
  - 2: 35 - 40
  - 3: ≥ 40
- Map `convenio` values:
  - `particular` → `P`
  - `sus` → `S`
  - `convenio` → `C`
- Output: `pc_preprocessed.csv`

### 3. Data Integration

- Read `bc_preprocessed.csv` and `pc_preprocessed.csv`.
- Ensure `codigo` is string in both datasets.
- Merge on `codigo` using inner join.
- Drop `codigo` after integration.
- Output: `bcc_parcial.csv`.

### 4. Final Transformation

- Remove the numerical `IMC` column.
- Normalize `peso` using **MinMaxScaler** (range [0, 1]).
- Standardize `altura` using **StandardScaler** (mean = 0, std = 1).
- Output: `bcc_final.csv`.

---

## ✅ Output Files

| File Name           | Description                                |
|---------------------|--------------------------------------------|
| `bc_preprocessed.csv` | Cleaned breast cancer clinical data         |
| `pc_preprocessed.csv` | Cleaned patient data with BMI category      |
| `bcc_parcial.csv`     | Integrated dataset (before normalization)   |
| `bcc_final.csv`       | Final dataset (clean, merged, normalized)   |

---

## 🛠 Technologies Used

- Python 3.x
- Pandas
- NumPy
- Scikit-learn

---

## 💡 How to Run

Make sure you have the required libraries installed:

```bash
pip install pandas numpy scikit-learn
python preprocess.py
