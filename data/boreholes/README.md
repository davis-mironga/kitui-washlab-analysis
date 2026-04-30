# Borehole Data

The Kitui borehole master dataset is NOT committed to this repository.
It contains Kitui County Government infrastructure records and GPS coordinates
that should not be publicly accessible without county approval.

**File:** `Kitui_Boreholes_Master_Dataset.xlsx`  
**Location:** Google Drive (shared with project team)  
**Records:** 706 boreholes across 40 wards

## Loading in Colab

```python
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

DRIVE_PATH = '/content/drive/MyDrive/Kitui_WASHLAB/'

# Spatial analysis ready sheet (GPS Verified, 361 records)
df = pd.read_excel(
    DRIVE_PATH + 'Kitui_Boreholes_Master_Dataset.xlsx',
    sheet_name='B_Spatial_Analysis',
    header=2
)
```

## Sheets available
- `A_Master_Dataset` — All 706 boreholes, all columns
- `B_Spatial_Analysis` — 361 GPS-Verified boreholes, spatial-ready
- `C_GPS_Needs_Review` — 146 records needing GPS verification
- `D_Field_GPS_Collection` — 199 boreholes with no GPS (field log template)
- `E_Data_Dictionary` — All column definitions

See `docs/data_dictionary.md` for full column reference.
